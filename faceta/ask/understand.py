from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from faceta.ask.openai_client import chat_json
from faceta.query.contract import load_contrato
from faceta.query.errors import ConsultaRejeitada
from faceta.query.maps import COMPARACOES, GRANULARIDADE_SUFIXO


@dataclass
class ParametrosPergunta:
    entity_type: str
    granularidade: str
    periodo: str
    entity_id: str | None = None
    entity_nome: str | None = None
    quebra: str | None = None
    quebra_valor: str | None = None
    quebra_nome: str | None = None
    comparacao: str | None = None
    ranking: bool = False


SYSTEM = """Você traduz perguntas analíticas de negócio em parâmetros JSON para um motor de consulta.
Responda APENAS um objeto JSON válido com as chaves:
entity_type, granularidade, periodo, entity_id, entity_nome, quebra, quebra_valor, quebra_nome, comparacao, ranking.

Regras:
- entity_type deve ser um dos tipos listados no contrato (mensagem do usuário).
- granularidade: diario | semanal | mensal | semestral | anual
- periodo: YYYY-MM-DD | YYYY-Www | YYYY-MM | YYYY-H1 | YYYY-H2 | YYYY (ano)
- Se a pergunta pedir ranking / "quais" / "top" / "mais", ranking=true e entity_id/entity_nome null
- Se nomear uma entidade específica, preencha entity_nome (e entity_id só se tiver certeza do id)
- comparacao: vs_periodo_anterior | vs_mesmo_periodo_ano_anterior | null
- quebra: dimensão de breakdown se pedida; senão null
- Use null para campos ausentes; ranking boolean
- Não invente famílias de fato; ignore SQL

Semântica temporal (CRÍTICO — as famílias NÃO compartilham o mesmo "dia"):
O campo `data` de cada família marca um evento distinto no ciclo de vida da OS.
Escolha o entity_type cuja família casa com a intenção temporal da pergunta:

1) fato_os (abertura / OS criada) — data = DATE(os.created_at)
   entity_types: concessionaria, departamento, vendedor, empresa
   Use para: "faturamento aberto", "OS criadas", "vendas abertas", volume de abertura no período.
   NÃO use para "quanto entrou de caixa" nem "produção fechada".

2) fato_os_servico (fechamento do item de serviço) — data = DATE(data_fechamento do item), só itens fechado=1
   entity_types: servico, familia_servico, produtivo
   Use para: "produção", "serviços fechados", "quanto o produtivo X fez", valor atribuído no fechamento.
   NÃO use para caixa/pagamento nem para mera abertura de OS.

3) fato_os_pagamento (pagamento / caixa) — data = DATE(data_pagamento)
   entity_types: forma_pagamento
   Use para: "quanto entrou", "receita recebida", "caixa do dia", formas de pagamento no período.
   NÃO use para abertura de OS nem produção fechada.

4) fato_comissao (geração da comissão) — data = DATE(comissoes.created_at)
   comissionado_id é polimórfico: NÃO use um "comissionado" genérico.
   entity_types:
   - comissao_vendedor — comissão de vendedor (tipo VENDEDOR)
   - comissao_produtivo — comissão de produtivo (tipo PRODUTIVO)
   - comissao_concessionaria — comissão da concessionária
   - comissao_indicador — comissão de indicador externo (INDICADOR1/2)
   - comissao_tipo — total por categoria de tipo (sem filtrar o quem)
   Use para: "comissão do vendedor X", "ranking de indicadores por comissão", "quanto de comissão de concessionária".

Heurísticas de linguagem:
- "entrou" / "recebido" / "pago" / "caixa" / "PIX" / "cartão" → forma_pagamento (pagamento)
- "fechou" / "produção" / "produtivo" / "serviço executado" → servico | familia_servico | produtivo
  (se a pergunta for sobre *comissão* do produtivo → comissao_produtivo)
- "abriu" / "criou" / "OS do dia" / "faturamento aberto" / ranking de vendedor por abertura → vendedor | concessionaria | departamento | empresa
- "comissão" + vendedor → comissao_vendedor
- "comissão" + produtivo → comissao_produtivo
- "comissão" + concessionária → comissao_concessionaria
- "comissão" + indicador → comissao_indicador
- "comissão" só por tipo/categoria (sem quem) → comissao_tipo
"""


def entender_pergunta(pergunta: str, contrato: dict[str, Any] | None = None) -> ParametrosPergunta:
    contrato = contrato or load_contrato()
    tipos = sorted(contrato["entity_types"].keys())
    roteamento = []
    for et in tipos:
        cfg = contrato["entity_types"][et]
        roteamento.append(f"{et}→{cfg.get('fato')}({cfg.get('valor')})")
    user = (
        f"entity_types válidos: {tipos}\n"
        f"roteamento entity_type→fato(métrica): {', '.join(roteamento)}\n"
        f"granularidades: {sorted(GRANULARIDADE_SUFIXO)}\n"
        f"comparacoes: {sorted(COMPARACOES)}\n\n"
        f"Pergunta: {pergunta}"
    )
    raw = chat_json(SYSTEM, user)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ConsultaRejeitada(f"LLM não retornou JSON válido: {e}") from e

    entity_type = data.get("entity_type")
    granularidade = data.get("granularidade")
    periodo = data.get("periodo")
    if not entity_type or not granularidade or not periodo:
        raise ConsultaRejeitada(
            f"JSON incompleto do LLM (faltam entity_type/granularidade/periodo): {data}"
        )

    ranking = bool(data.get("ranking") or False)
    comparacao = data.get("comparacao") or None
    if comparacao in ("", "null", "None"):
        comparacao = None

    return ParametrosPergunta(
        entity_type=str(entity_type),
        granularidade=str(granularidade),
        periodo=str(periodo),
        entity_id=_opt_str(data.get("entity_id")),
        entity_nome=_opt_str(data.get("entity_nome")),
        quebra=_opt_str(data.get("quebra")),
        quebra_valor=_opt_str(data.get("quebra_valor")),
        quebra_nome=_opt_str(data.get("quebra_nome")),
        comparacao=comparacao,
        ranking=ranking,
    )


def _opt_str(v: Any) -> str | None:
    if v is None or v == "" or v == "null":
        return None
    return str(v)
