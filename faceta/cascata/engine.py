from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from faceta.cascata.families import FAMILIES, destino
from faceta.cascata.periods import period_bounds
from faceta.db import SCHEMA


@dataclass
class CascadeResult:
    familia: str
    granularidade: str
    inicio: date
    fim: date
    skipped: bool
    rows: int


def _period_exists(pg, table: str, inicio: date) -> bool:
    with pg.cursor() as cur:
        cur.execute(
            f"SELECT 1 FROM {SCHEMA}.{table} WHERE data = %s LIMIT 1",
            (inicio,),
        )
        return cur.fetchone() is not None


def cascade_family(
    pg,
    familia: str,
    granularidade: str,
    ref: date,
    *,
    force: bool = False,
) -> CascadeResult:
    if familia not in FAMILIES:
        raise ValueError(f"família inválida: {familia}")
    spec = FAMILIES[familia]
    inicio, fim = period_bounds(granularidade, ref)
    table_dest = destino(spec, granularidade)
    # allowlist: só nomes do mapa
    _assert_ident(spec.origem)
    _assert_ident(table_dest)
    for col in (*spec.dims, *spec.metrics):
        _assert_ident(col)

    if _period_exists(pg, table_dest, inicio) and not force:
        return CascadeResult(
            familia=familia,
            granularidade=granularidade,
            inicio=inicio,
            fim=fim,
            skipped=True,
            rows=0,
        )

    if force:
        with pg.cursor() as cur:
            cur.execute(
                f"DELETE FROM {SCHEMA}.{table_dest} WHERE data = %s",
                (inicio,),
            )
        pg.commit()

    dims_sql = ", ".join(spec.dims)
    metrics_sql = ", ".join(f"SUM({m}) AS {m}" for m in spec.metrics)
    insert_cols = ", ".join(("data", *spec.dims, *spec.metrics))
    select_dims = ", ".join(spec.dims)

    sql = f"""
    INSERT INTO {SCHEMA}.{table_dest} ({insert_cols})
    SELECT %s::date, {select_dims}, {metrics_sql}
    FROM {SCHEMA}.{spec.origem}
    WHERE data >= %s AND data < %s
    GROUP BY {dims_sql}
    """
    with pg.cursor() as cur:
        cur.execute(sql, (inicio, inicio, fim))
        rows = cur.rowcount if cur.rowcount is not None and cur.rowcount >= 0 else 0
    pg.commit()

    return CascadeResult(
        familia=familia,
        granularidade=granularidade,
        inicio=inicio,
        fim=fim,
        skipped=False,
        rows=rows,
    )


def _assert_ident(name: str) -> None:
    if not name.replace("_", "").isalnum():
        raise ValueError(f"identificador inválido: {name!r}")
