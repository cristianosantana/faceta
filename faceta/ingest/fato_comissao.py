from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from faceta.db import SCHEMA, tid
from faceta.ingest.common import clear_day
from faceta.ingest import dec

FORMULA = (
    "COALESCE(cm.valor_dentro,0) + COALESCE(cm.valor_fora,0) + COALESCE(cm.valor_combo,0) "
    "+ COALESCE(cm.valor_compensado_permuta,0) + COALESCE(cm.comissao_couro,0)"
)


def ingest_fato_comissao(mysql, pg, dia: date) -> int:
    """Componentes pré-calculados na origem; valor_comissao = soma simples (RF04).

    Tipo vem de comissoes.comissao_tipo_id (sempre presente quando há comissionado_id).
    """
    clear_day(pg, "fato_comissao_diario", dia)
    sql = f"""
    SELECT
      cm.comissionado_id,
      cm.comissao_tipo_id,
      ({FORMULA}) AS valor_comissao
    FROM comissoes cm
    WHERE cm.deleted_at IS NULL
      AND cm.comissionado_id IS NOT NULL
      AND cm.comissao_tipo_id IS NOT NULL
      AND DATE(cm.created_at) = %s
    """
    with mysql.cursor() as cur:
        cur.execute(sql, (dia,))
        rows = cur.fetchall()

    agg: dict[tuple, Decimal] = defaultdict(lambda: Decimal("0"))
    skipped = 0
    for r in rows:
        cid = tid(r.get("comissionado_id"))
        tid_ = tid(r.get("comissao_tipo_id"))
        if not cid or not tid_:
            skipped += 1
            continue
        key = (dia, cid, tid_)
        agg[key] += dec(r["valor_comissao"])

    payload = [(k[0], k[1], k[2], v) for k, v in agg.items()]
    if payload:
        with pg.cursor() as cur:
            cur.executemany(
                f"""
                INSERT INTO {SCHEMA}.fato_comissao_diario (
                    data, comissionado_id, comissao_tipo_id, valor_comissao
                ) VALUES (%s, %s, %s, %s)
                """,
                payload,
            )
        pg.commit()
    if skipped:
        print(f"  comissao: {skipped} linhas ignoradas sem comissionado_id/comissao_tipo_id")
    return len(payload)
