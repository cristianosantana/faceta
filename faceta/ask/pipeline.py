from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from faceta.ask.narrate import narrar_resposta
from faceta.ask.resolve import aplicar_resolucao
from faceta.ask.understand import ParametrosPergunta, entender_pergunta
from faceta.query.contract import load_contrato, validar_consulta
from faceta.query.engine import ResultadoConsulta, consultar
from faceta.query.errors import ConsultaRejeitada
from faceta.trace import span, trace_run


@dataclass
class RespostaAsk:
    pergunta: str
    params: ParametrosPergunta
    resultado: ResultadoConsulta
    narracao: str
    llm_calls: int
    trace_id: str | None = None
    trace_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "pergunta": self.pergunta,
            "params": asdict(self.params),
            "resultado": self.resultado.to_dict(),
            "narracao": self.narracao,
            "llm_calls": self.llm_calls,
            "trace_id": self.trace_id,
            "trace_path": self.trace_path,
        }


def perguntar(pg, pergunta: str, *, narrar: bool = True) -> RespostaAsk:
    """Pipeline Fase 4: entender (1 LLM) → motor → narrar (1 LLM). Máx. 2 chamadas."""
    if not pergunta.strip():
        raise ConsultaRejeitada("pergunta vazia")

    with trace_run("ask", pergunta=pergunta[:500], narrar=narrar) as run:
        with span("load_contrato"):
            contrato = load_contrato()

        with span("entender_pergunta", regra="LLM1_json_params"):
            params = entender_pergunta(pergunta, contrato)
        llm_calls = 1

        with span(
            "resolver_dims",
            regra="nome_ILIKE_dim",
            entity_type=params.entity_type,
            entity_nome=params.entity_nome,
        ):
            params = aplicar_resolucao(pg, params)

        with span(
            "validar_contrato",
            entity_type=params.entity_type,
            granularidade=params.granularidade,
            quebra=params.quebra,
            comparacao=params.comparacao,
        ):
            validar_consulta(
                contrato,
                entity_type=params.entity_type,
                granularidade=params.granularidade,
                quebra=params.quebra,
                comparacao=params.comparacao,
            )

        with span(
            "consultar",
            entity_type=params.entity_type,
            granularidade=params.granularidade,
            periodo=params.periodo,
            ranking=params.ranking,
            comparacao=params.comparacao,
        ):
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
            with span("narrar_resposta", regra="LLM2_narracao", n_linhas=len(resultado.linhas)):
                narracao = narrar_resposta(pergunta, params, resultado)
            llm_calls += 1

        if llm_calls > 2:
            raise RuntimeError(f"llm_calls={llm_calls} excede o máximo de 2")

        with span("resultado", llm_calls=llm_calls, n_linhas=len(resultado.linhas)):
            pass

        return RespostaAsk(
            pergunta=pergunta,
            params=params,
            resultado=resultado,
            narracao=narracao,
            llm_calls=llm_calls,
            trace_id=run.trace_id,
            trace_path=str(run.path),
        )
