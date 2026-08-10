from __future__ import annotations

import json
from typing import Any

from faceta.db import SCHEMA


def upsert_insight(
    pg,
    *,
    entity_type: str,
    entity_id: str,
    granularidade: str,
    periodo: str,
    quebra: str = "",
    hipotese: dict[str, Any],
    erro_reconstrucao: float | None = None,
) -> None:
    with pg.cursor() as cur:
        cur.execute(
            f"""
            INSERT INTO {SCHEMA}.insights
                (entity_type, entity_id, granularidade, periodo, quebra, hipotese, erro_reconstrucao)
            VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s)
            ON CONFLICT (entity_type, entity_id, granularidade, periodo, quebra)
            DO UPDATE SET
                hipotese = EXCLUDED.hipotese,
                erro_reconstrucao = EXCLUDED.erro_reconstrucao,
                created_at = NOW()
            """,
            (
                entity_type,
                entity_id,
                granularidade,
                periodo,
                quebra or "",
                json.dumps(hipotese, ensure_ascii=False),
                erro_reconstrucao,
            ),
        )
    pg.commit()


def fetch_insights(
    pg,
    *,
    entity_type: str,
    granularidade: str,
    periodo: str,
    entity_ids: list[str],
    quebra: str = "",
) -> list[dict[str, Any]]:
    if not entity_ids:
        return []
    with pg.cursor() as cur:
        cur.execute(
            f"""
            SELECT entity_id, hipotese, erro_reconstrucao, created_at
            FROM {SCHEMA}.insights
            WHERE entity_type = %s
              AND granularidade = %s
              AND periodo = %s
              AND quebra = %s
              AND entity_id = ANY(%s)
            """,
            (entity_type, granularidade, periodo, quebra or "", entity_ids),
        )
        rows = cur.fetchall()
    out = []
    for eid, hipotese, erro, created_at in rows:
        if isinstance(hipotese, str):
            hipotese = json.loads(hipotese)
        out.append(
            {
                "entity_id": str(eid),
                "hipotese": hipotese,
                "erro_reconstrucao": float(erro) if erro is not None else None,
                "created_at": created_at.isoformat() if created_at else None,
            }
        )
    return out


def count_insights(pg) -> int:
    with pg.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {SCHEMA}.insights")
        return int(cur.fetchone()[0])
