from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from faceta.db import SCHEMA, tid
from faceta.ingest.common import clear_day, dims_from_os_row, empresa_subquery
from faceta.ingest import dec


def ingest_fato_os_servico(mysql, pg, dia: date) -> int:
    """Grão: serviço a serviço; familia_servico_id = subgrupos_servicos (via servicos.subgrupo_servico_id)."""
    clear_day(pg, "fato_os_servico_diario", dia)
    sql = f"""
    SELECT
      o.concessionaria_id,
      o.departamento_id,
      o.vendedor_id,
      emp.empresa_id,
      s.produtivo_id,
      s.servico_id,
      COALESCE(sv.subgrupo_servico_id, 0) AS familia_servico_id,
      COALESCE(s.valor_venda_real, 0) AS valor_atribuido
    FROM os_servicos s
    INNER JOIN os o ON o.id = s.os_id AND o.deleted_at IS NULL
    LEFT JOIN servicos sv ON sv.id = s.servico_id
    {empresa_subquery()}
    WHERE s.deleted_at IS NULL
      AND IFNULL(s.cancelado, 0) <> 1
      AND IFNULL(s.fechado, 0) = 1
      AND DATE(COALESCE(s.data_fechamento, s.updated_at)) = %s
    """
    with mysql.cursor() as cur:
        cur.execute(sql, (dia,))
        rows = cur.fetchall()

    agg: dict[tuple, dict] = defaultdict(lambda: {"valor": Decimal("0"), "qtd": 0})
    for r in rows:
        conc, dep, vend, emp = dims_from_os_row(r)
        key = (
            dia,
            conc,
            dep,
            vend,
            tid(r.get("produtivo_id")),
            emp,
            tid(r.get("familia_servico_id")),
            tid(r.get("servico_id")),
        )
        agg[key]["valor"] += dec(r["valor_atribuido"])
        agg[key]["qtd"] += 1

    payload = [
        (k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7], v["valor"], v["qtd"])
        for k, v in agg.items()
    ]
    if payload:
        with pg.cursor() as cur:
            cur.executemany(
                f"""
                INSERT INTO {SCHEMA}.fato_os_servico_diario (
                    data, concessionaria_id, departamento_id, vendedor_id,
                    produtivo_id, empresa_id, familia_servico_id, servico_id,
                    valor_atribuido, quantidade
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                payload,
            )
        pg.commit()
    return len(payload)
