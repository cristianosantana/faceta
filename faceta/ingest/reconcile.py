from __future__ import annotations

from datetime import date
from decimal import Decimal

from faceta.ingest.common import clear_reconcile, insert_reconcile
from faceta.ingest import dec


def reconcile_day(mysql, pg, dia: date) -> int:
    """Sinaliza divergências pagamento vs soma de itens para OS pagas em D."""
    clear_reconcile(pg, dia)
    sql = """
    SELECT
      o.id AS os_id,
      COALESCE((
        SELECT SUM(COALESCE(s.valor_venda_real, 0))
        FROM os_servicos s
        WHERE s.os_id = o.id AND s.deleted_at IS NULL AND IFNULL(s.cancelado, 0) <> 1
      ), 0) AS soma_servicos,
      COALESCE((
        SELECT SUM(COALESCE(p.valor_venda_real, p.valor_venda, 0))
        FROM os_produtos p
        WHERE p.os_id = o.id AND p.deleted_at IS NULL AND IFNULL(p.cancelado, 0) <> 1
      ), 0) AS soma_produtos,
      (
        SELECT COUNT(*) FROM os_servicos s
        WHERE s.os_id = o.id AND s.deleted_at IS NULL AND IFNULL(s.cancelado, 0) <> 1
      ) AS n_servicos,
      COALESCE((
        SELECT SUM(c.valor)
        FROM caixas c
        WHERE c.os_id = o.id AND c.deleted_at IS NULL AND IFNULL(c.cancelado, 0) <> 1
      ), 0) AS soma_caixas
    FROM os o
    WHERE o.deleted_at IS NULL
      AND o.paga = 1
      AND DATE(o.data_pagamento) = %s
    """
    with mysql.cursor() as cur:
        cur.execute(sql, (dia,))
        rows = cur.fetchall()

    findings = []
    for r in rows:
        itens = dec(r["soma_servicos"]) if int(r["n_servicos"] or 0) > 0 else dec(r["soma_produtos"])
        pago = dec(r["soma_caixas"])
        diff = pago - itens
        if abs(diff) > Decimal("0.01"):
            findings.append(
                (
                    dia,
                    "pagamento_vs_itens",
                    int(r["os_id"]),
                    itens,
                    pago,
                    diff,
                    "SUM(caixas) vs soma itens ativos",
                )
            )
        if pago == 0:
            findings.append(
                (
                    dia,
                    "paga_sem_caixa",
                    int(r["os_id"]),
                    itens,
                    pago,
                    diff,
                    "os.paga=1 sem valor em caixas",
                )
            )

    # serviços fechados em D vs cabeçalho (soma itens da OS)
    sql_s = """
    SELECT
      o.id AS os_id,
      COALESCE(SUM(COALESCE(s.valor_venda_real, 0)), 0) AS soma_fechados_dia,
      COALESCE((
        SELECT SUM(COALESCE(sx.valor_venda_real, 0))
        FROM os_servicos sx
        WHERE sx.os_id = o.id AND sx.deleted_at IS NULL AND IFNULL(sx.cancelado, 0) <> 1
      ), 0) AS soma_todos_servicos
    FROM os_servicos s
    INNER JOIN os o ON o.id = s.os_id AND o.deleted_at IS NULL
    WHERE s.deleted_at IS NULL
      AND IFNULL(s.cancelado, 0) <> 1
      AND IFNULL(s.fechado, 0) = 1
      AND DATE(COALESCE(s.data_fechamento, s.updated_at)) = %s
    GROUP BY o.id
    """
    with mysql.cursor() as cur:
        cur.execute(sql_s, (dia,))
        serv_rows = cur.fetchall()
    for r in serv_rows:
        # informativo: parcial do dia vs total OS (não é erro se parcial)
        fechados = dec(r["soma_fechados_dia"])
        todos = dec(r["soma_todos_servicos"])
        if todos > 0 and fechados > todos + Decimal("0.01"):
            findings.append(
                (
                    dia,
                    "servico_fechado_gt_total",
                    int(r["os_id"]),
                    todos,
                    fechados,
                    fechados - todos,
                    "soma fechados no dia > soma serviços da OS",
                )
            )

    insert_reconcile(pg, findings)
    return len(findings)
