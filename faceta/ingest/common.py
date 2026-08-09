from __future__ import annotations

from datetime import date

from faceta.db import SCHEMA, tid


def clear_day(pg, table: str, dia: date) -> None:
    with pg.cursor() as cur:
        cur.execute(f"DELETE FROM {SCHEMA}.{table} WHERE data = %s", (dia,))
    pg.commit()


def clear_reconcile(pg, dia: date, familia: str | None = None) -> None:
    with pg.cursor() as cur:
        if familia:
            cur.execute(
                f"DELETE FROM {SCHEMA}.ingest_reconciliacao WHERE data = %s AND familia = %s",
                (dia, familia),
            )
        else:
            cur.execute(f"DELETE FROM {SCHEMA}.ingest_reconciliacao WHERE data = %s", (dia,))
    pg.commit()


def insert_reconcile(pg, rows: list[tuple]) -> None:
    if not rows:
        return
    with pg.cursor() as cur:
        cur.executemany(
            f"""
            INSERT INTO {SCHEMA}.ingest_reconciliacao
                (data, familia, os_id, esperado, obtido, diff, detalhe)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )
    pg.commit()


def empresa_subquery() -> str:
    """Primeira empresa_faturamento_id não nula por OS via caixas."""
    return """
    LEFT JOIN (
        SELECT c.os_id, MIN(c.empresa_faturamento_id) AS empresa_id
        FROM caixas c
        WHERE c.deleted_at IS NULL
          AND IFNULL(c.cancelado, 0) <> 1
          AND c.empresa_faturamento_id IS NOT NULL
        GROUP BY c.os_id
    ) emp ON emp.os_id = o.id
    """


def dims_from_os_row(r: dict) -> tuple[str, str, str, str]:
    return (
        tid(r.get("concessionaria_id")),
        tid(r.get("departamento_id")),
        tid(r.get("vendedor_id")),
        tid(r.get("empresa_id")),
    )
