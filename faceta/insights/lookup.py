from __future__ import annotations

from typing import Any

from faceta.ask.understand import ParametrosPergunta
from faceta.insights.store import fetch_insights
from faceta.query.engine import ResultadoConsulta
from faceta.query.periods import parse_periodo


def insights_para_ask(
    pg,
    params: ParametrosPergunta,
    resultado: ResultadoConsulta,
    *,
    top_n: int = 5,
) -> list[dict[str, Any]]:
    """Lookup em insights (sem gerar). Match por chave; ranking → top N entity_ids."""
    periodo_key = parse_periodo(params.periodo, params.granularidade).isoformat()
    quebra = params.quebra or ""

    if params.entity_id:
        ids = [params.entity_id]
    else:
        ids = [L.entity_id for L in resultado.linhas[:top_n]]

    rows = fetch_insights(
        pg,
        entity_type=params.entity_type,
        granularidade=params.granularidade,
        periodo=periodo_key,
        entity_ids=ids,
        quebra=quebra,
    )
    # enriquecer com nome do resultado se houver
    nomes = {L.entity_id: L.entity_nome for L in resultado.linhas}
    for r in rows:
        r["entity_nome"] = nomes.get(r["entity_id"])
    return rows
