from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from faceta.db import SCHEMA, tid
from faceta.ingest.common import clear_day, dims_from_os_row, empresa_subquery
from faceta.ingest import dec


def ingest_fato_os(mysql, pg, dia: date) -> int:
    clear_day(pg, "fato_os_diario", dia)
    sql = f"""
    SELECT
      o.id AS os_id,
      o.concessionaria_id,
      o.departamento_id,
      o.vendedor_id,
      emp.empresa_id,
      COALESCE((
        SELECT SUM(COALESCE(s.valor_venda_real, 0))
        FROM os_servicos s
        WHERE s.os_id = o.id
          AND s.deleted_at IS NULL
          AND IFNULL(s.cancelado, 0) <> 1
      ), 0) AS soma_servicos,
      COALESCE((
        SELECT SUM(COALESCE(p.valor_venda_real, p.valor_venda, 0))
        FROM os_produtos p
        WHERE p.os_id = o.id
          AND p.deleted_at IS NULL
          AND IFNULL(p.cancelado, 0) <> 1
      ), 0) AS soma_produtos,
      (
        SELECT COUNT(*) FROM os_servicos s
        WHERE s.os_id = o.id AND s.deleted_at IS NULL AND IFNULL(s.cancelado, 0) <> 1
      ) AS n_servicos,
      (
        SELECT COUNT(*) FROM os_produtos p
        WHERE p.os_id = o.id AND p.deleted_at IS NULL AND IFNULL(p.cancelado, 0) <> 1
      ) AS n_produtos
    FROM os o
    {empresa_subquery()}
    WHERE o.deleted_at IS NULL
      AND DATE(o.created_at) = %s
    """
    with mysql.cursor() as cur:
        cur.execute(sql, (dia,))
        rows = cur.fetchall()

    agg: dict[tuple, dict] = defaultdict(lambda: {"valor": Decimal("0"), "qtd": 0})
    for r in rows:
        conc, dep, vend, emp = dims_from_os_row(r)
        key = (dia, conc, dep, vend, "", emp)
        if int(r["n_servicos"] or 0) > 0:
            valor = dec(r["soma_servicos"])
        else:
            valor = dec(r["soma_produtos"])
        agg[key]["valor"] += valor
        agg[key]["qtd"] += 1

    payload = [
        (k[0], k[1], k[2], k[3], k[4], k[5], v["valor"], v["qtd"])
        for k, v in agg.items()
    ]
    if payload:
        with pg.cursor() as cur:
            cur.executemany(
                f"""
                INSERT INTO {SCHEMA}.fato_os_diario (
                    data, concessionaria_id, departamento_id, vendedor_id,
                    produtivo_id, empresa_id, valor_total, quantidade_os
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                payload,
            )
        pg.commit()
    return len(payload)
