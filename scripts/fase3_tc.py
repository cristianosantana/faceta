#!/usr/bin/env python3
"""Checklist TC01–TC11 contra Postgres/MySQL reais (Fase 3)."""

from __future__ import annotations

from datetime import date

from faceta.cascata.engine import cascade_family
from faceta.cascata.periods import period_bounds
from faceta.db import SCHEMA, postgres_connect
from faceta.ingest.fato_os import ingest_fato_os
from faceta.ingest.fato_os_pagamento import ingest_fato_os_pagamento
from faceta.ingest.fato_os_servico import ingest_fato_os_servico
from faceta.ingest.fato_comissao import ingest_fato_comissao
from faceta.db import mysql_connect
from faceta.query.contract import coluna_dimensao, load_contrato, validar_consulta
from faceta.query.engine import consultar
from faceta.query.errors import ConsultaRejeitada


def ok(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        raise SystemExit(1)


def ingest_dia(mysql, pg, dia: date) -> None:
    ingest_fato_os(mysql, pg, dia)
    ingest_fato_os_servico(mysql, pg, dia)
    ingest_fato_os_pagamento(mysql, pg, dia)
    ingest_fato_comissao(mysql, pg, dia)


def main() -> int:
    load_contrato()
    semana_inicio, semana_fim = period_bounds("semanal", date(2026, 7, 31))

    mysql = mysql_connect()
    try:
        with postgres_connect() as pg:
            # Garantir dias reais para TC06/TC07
            for dia in (date(2026, 6, 15), date(2025, 7, 31)):
                print(f"  ingest {dia.isoformat()}…")
                ingest_dia(mysql, pg, dia)

            cascade_family(pg, "os", "mensal", date(2026, 7, 31), force=True)
            cascade_family(pg, "os", "mensal", date(2026, 6, 15), force=True)
            cascade_family(pg, "os", "mensal", date(2025, 7, 31), force=True)
            cascade_family(pg, "os", "semanal", date(2026, 7, 31), force=True)

            with pg.cursor() as cur:
                cur.execute(
                    f"SELECT COALESCE(SUM(valor_atribuido),0) FROM {SCHEMA}.fato_os_servico_diario WHERE data = %s",
                    (date(2026, 7, 31),),
                )
                s = cur.fetchone()[0]
                cur.execute(
                    f"SELECT COALESCE(SUM(valor_total),0) FROM {SCHEMA}.fato_os_diario WHERE data = %s",
                    (date(2026, 7, 31),),
                )
                o = cur.fetchone()[0]
                cur.execute(
                    f"""
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = %s AND table_name = 'ingest_reconciliacao'
                    """,
                    (SCHEMA,),
                )
                has_rec = cur.fetchone() is not None
                cur.execute(
                    f"SELECT COALESCE(SUM(valor_pago),0) FROM {SCHEMA}.fato_os_pagamento_diario WHERE data = %s",
                    (date(2026, 7, 31),),
                )
                p = cur.fetchone()[0]
                cur.execute(
                    f"SELECT COALESCE(SUM(valor_total),0) FROM {SCHEMA}.fato_os_diario WHERE data >= %s AND data < %s",
                    (semana_inicio, semana_fim),
                )
                d = cur.fetchone()[0]
                cur.execute(
                    f"SELECT COALESCE(SUM(valor_total),0) FROM {SCHEMA}.fato_os_semanal WHERE data = %s",
                    (semana_inicio,),
                )
                w = cur.fetchone()[0]

            ok("TC01", s > 0 and o > 0, f"servico_dia={s} os_dia={o}")
            ok("TC02", p > 0, f"pagamento_dia={p}")
            ok("TC03", has_rec, "tabela ingest_reconciliacao")
            ok("TC04", d == w and d > 0, f"diario={d} semanal={w}")

            r_vend = consultar(
                pg, entity_type="vendedor", granularidade="semanal",
                periodo="2026-07-31", ranking=True,
            )
            r_serv = consultar(
                pg, entity_type="servico", granularidade="semanal",
                periodo="2026-W31", ranking=True,
            )
            ok(
                "TC05",
                r_vend.tabela == "fato_os_semanal"
                and r_serv.tabela == "fato_os_servico_semanal"
                and len(r_vend.linhas) > 0
                and len(r_serv.linhas) > 0,
                f"vend={r_vend.tabela} serv={r_serv.tabela}",
            )

            r_cmp = consultar(
                pg, entity_type="vendedor", granularidade="mensal",
                periodo="2026-07", comparacao="vs_periodo_anterior", ranking=True,
            )
            com_ant = [L for L in r_cmp.linhas if L.valor_anterior is not None]
            ok(
                "TC06",
                r_cmp.periodo_referencia == date(2026, 6, 1) and len(com_ant) > 0,
                f"ref={r_cmp.periodo_referencia} n={len(com_ant)}",
            )

            r_yoy = consultar(
                pg, entity_type="vendedor", granularidade="mensal",
                periodo="2026-07", comparacao="vs_mesmo_periodo_ano_anterior", ranking=True,
            )
            yoy = [L for L in r_yoy.linhas if L.valor_anterior is not None]
            ok(
                "TC07",
                r_yoy.periodo_referencia == date(2025, 7, 1) and len(yoy) > 0,
                f"ref={r_yoy.periodo_referencia} n={len(yoy)}",
            )

            r_rank = consultar(
                pg, entity_type="vendedor", granularidade="semanal",
                periodo="2026-W31", ranking=True,
            )
            top = r_rank.linhas[:3]
            pct_sum = sum(L.participacao_pct or 0 for L in r_rank.linhas)
            vals_desc = all(top[i].valor >= top[i + 1].valor for i in range(len(top) - 1))
            ok(
                "TC08",
                len(r_rank.linhas) >= 3 and vals_desc and abs(pct_sum - 100) < 0.1,
                f"n={len(r_rank.linhas)} pct={pct_sum:.4f}",
            )

            try:
                validar_consulta(
                    load_contrato(),
                    entity_type="servico",
                    granularidade="semanal",
                    quebra="forma_pagamento",
                )
                ok("TC09", False)
            except ConsultaRejeitada as e:
                ok("TC09", True, str(e))

            try:
                consultar(
                    pg, entity_type="nao_existe", granularidade="semanal", periodo="2026-W31",
                )
                ok("TC10", False)
            except ConsultaRejeitada as e:
                ok("TC10", True, str(e))

            try:
                coluna_dimensao("'; DROP TABLE--")
                ok("TC11", False)
            except ConsultaRejeitada as e:
                ok("TC11", True, str(e))
    finally:
        mysql.close()

    print("TC01–TC11 OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
