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
"""


def entender_pergunta(pergunta: str, contrato: dict[str, Any] | None = None) -> ParametrosPergunta:
    contrato = contrato or load_contrato()
    tipos = sorted(contrato["entity_types"].keys())
    user = (
        f"entity_types válidos: {tipos}\n"
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
