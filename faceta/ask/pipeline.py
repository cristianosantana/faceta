from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from faceta.ask.narrate import narrar_resposta
from faceta.ask.resolve import aplicar_resolucao
from faceta.ask.understand import ParametrosPergunta, entender_pergunta
from faceta.query.contract import load_contrato, validar_consulta
from faceta.query.engine import ResultadoConsulta, consultar
from faceta.query.errors import ConsultaRejeitada


@dataclass
class RespostaAsk:
    pergunta: str
    params: ParametrosPergunta
    resultado: ResultadoConsulta
    narracao: str
    llm_calls: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "pergunta": self.pergunta,
            "params": asdict(self.params),
            "resultado": self.resultado.to_dict(),
            "narracao": self.narracao,
            "llm_calls": self.llm_calls,
        }


def perguntar(pg, pergunta: str, *, narrar: bool = True) -> RespostaAsk:
    """Pipeline Fase 4: entender (1 LLM) → motor → narrar (1 LLM). Máx. 2 chamadas."""
    if not pergunta.strip():
        raise ConsultaRejeitada("pergunta vazia")

    contrato = load_contrato()
    params = entender_pergunta(pergunta, contrato)
    llm_calls = 1

    params = aplicar_resolucao(pg, params)

    validar_consulta(
        contrato,
        entity_type=params.entity_type,
        granularidade=params.granularidade,
        quebra=params.quebra,
        comparacao=params.comparacao,
    )

    resultado = consultar(
        pg,
        entity_type=params.entity_type,
        granularidade=params.granularidade,
        periodo=params.periodo,
        entity_id=params.entity_id,
        quebra=params.quebra,
        quebra_valor=params.quebra_valor,
        comparacao=params.comparacao,
        ranking=params.ranking,
        contrato=contrato,
    )

    narracao = ""
    if narrar:
        narracao = narrar_resposta(pergunta, params, resultado)
        llm_calls += 1

    if llm_calls > 2:
        raise RuntimeError(f"llm_calls={llm_calls} excede o máximo de 2")

    return RespostaAsk(
        pergunta=pergunta,
        params=params,
        resultado=resultado,
        narracao=narracao,
        llm_calls=llm_calls,
    )
