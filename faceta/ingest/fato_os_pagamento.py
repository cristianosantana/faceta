from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from faceta.db import SCHEMA, tid
from faceta.ingest.common import clear_day, dims_from_os_row
from faceta.ingest import dec


def ingest_fato_os_pagamento(mysql, pg, dia: date) -> int:
    clear_day(pg, "fato_os_pagamento_diario", dia)
    sql = """
    SELECT
      o.concessionaria_id,
      o.departamento_id,
      o.vendedor_id,
      c.empresa_faturamento_id AS empresa_id,
      c.caixa_tipo_id AS forma_pagamento_id,
      c.valor AS valor_pago
    FROM caixas c
    INNER JOIN os o ON o.id = c.os_id AND o.deleted_at IS NULL
    WHERE c.deleted_at IS NULL
      AND IFNULL(c.cancelado, 0) <> 1
      AND o.paga = 1
      AND DATE(COALESCE(c.data_pagamento, o.data_pagamento)) = %s
    """
    with mysql.cursor() as cur:
        cur.execute(sql, (dia,))
        rows = cur.fetchall()

    agg: dict[tuple, Decimal] = defaultdict(lambda: Decimal("0"))
    for r in rows:
        conc, dep, vend, emp = dims_from_os_row(r)
        key = (dia, conc, dep, vend, "", emp, tid(r.get("forma_pagamento_id")))
        agg[key] += dec(r["valor_pago"])

    payload = [
        (k[0], k[1], k[2], k[3], k[4], k[5], k[6], valor)
        for k, valor in agg.items()
    ]
    if payload:
        with pg.cursor() as cur:
            cur.executemany(
                f"""
                INSERT INTO {SCHEMA}.fato_os_pagamento_diario (
                    data, concessionaria_id, departamento_id, vendedor_id,
                    produtivo_id, empresa_id, forma_pagamento_id, valor_pago
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                payload,
            )
        pg.commit()
    return len(payload)
