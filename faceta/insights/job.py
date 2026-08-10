from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from faceta.db import apply_ddl
from faceta.insights.model import (
    DEFAULT_WINDOW,
    detect_signal,
    load_bundle,
    reconstruction_error,
    train_autoencoder,
)
from faceta.insights.narrate_insight import narrar_insight
from faceta.insights.series import carregar_series
from faceta.insights.store import upsert_insight
from faceta.query.dims import nomes_por_ids
from faceta.query.periods import parse_periodo
from faceta.trace import span, trace_run


@dataclass
class DetectResult:
    entity_id: str
    erro: float | None
    sinal: bool
    insight_gravado: bool
    hipotese: dict[str, Any] | None = None


def train_job(
    pg,
    *,
    entity_type: str = "vendedor",
    granularidade: str = "semanal",
    window: int = DEFAULT_WINDOW,
    epochs: int = 40,
) -> dict[str, Any]:
    with trace_run("insights_train", entity_type=entity_type, granularidade=granularidade):
        apply_ddl(pg)
        with span("carregar_series"):
            series = carregar_series(pg, entity_type=entity_type, granularidade=granularidade)
        with span("train_autoencoder", n_series=len(series), window=window):
            bundle = train_autoencoder(
                [s.valores() for s in series],
                window=window,
                epochs=epochs,
                entity_type=entity_type,
                granularidade=granularidade,
            )
        return {
            "n_series": len(series),
            "path": str(bundle.path),
            "threshold": bundle.threshold,
            "window": bundle.window,
        }


def run_job(
    pg,
    *,
    entity_type: str = "vendedor",
    granularidade: str = "semanal",
    periodo: str,
    narrar: bool = True,
    force_llm: bool = False,
    limit: int | None = None,
) -> list[DetectResult]:
    """Detecta anomalias; LLM só se sinal (US17)."""
    with trace_run(
        "insights_run",
        entity_type=entity_type,
        granularidade=granularidade,
        periodo=periodo,
    ):
        apply_ddl(pg)
        periodo_key = parse_periodo(periodo, granularidade).isoformat()
        with span("load_model"):
            model, bundle = load_bundle(entity_type, granularidade)
        with span("carregar_series"):
            series = carregar_series(pg, entity_type=entity_type, granularidade=granularidade)
        # prioriza maiores valores no período alvo
        series = sorted(
            series,
            key=lambda s: s.pontos[-1].valor if s.pontos else 0,
            reverse=True,
        )
        if limit is not None:
            series = series[:limit]
        nomes = nomes_por_ids(pg, entity_type, [s.entity_id for s in series])

        results: list[DetectResult] = []
        for s in series:
            with span("detect", entity_id=s.entity_id):
                erro = reconstruction_error(model, s.valores(), window=bundle.window)
                sinal = detect_signal(erro, bundle.threshold)
                if force_llm:
                    sinal = True
                    erro = erro if erro is not None else bundle.threshold * 2

                hipotese = None
                gravado = False
                if sinal and erro is not None:
                    if narrar:
                        with span("narrar_insight", regra="LLM_condicional"):
                            hipotese = narrar_insight(
                                entity_type=entity_type,
                                entity_id=s.entity_id,
                                entity_nome=nomes.get(s.entity_id),
                                granularidade=granularidade,
                                periodo=periodo_key,
                                valores=s.valores(),
                                erro=erro,
                                threshold=bundle.threshold,
                            )
                    else:
                        hipotese = {
                            "assunto": "Sinal de anomalia (sem narração)",
                            "descricao": f"erro={erro:.6f} limiar={bundle.threshold:.6f}",
                            "confianca": 0.7,
                        }
                    with span("upsert_insight"):
                        upsert_insight(
                            pg,
                            entity_type=entity_type,
                            entity_id=s.entity_id,
                            granularidade=granularidade,
                            periodo=periodo_key,
                            hipotese=hipotese,
                            erro_reconstrucao=erro,
                        )
                    gravado = True

                results.append(
                    DetectResult(
                        entity_id=s.entity_id,
                        erro=erro,
                        sinal=sinal,
                        insight_gravado=gravado,
                        hipotese=hipotese,
                    )
                )
        return results
