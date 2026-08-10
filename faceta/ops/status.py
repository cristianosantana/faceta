from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from faceta.db import SCHEMA, postgres_connect


FATO_DIARIO = (
    "fato_os_diario",
    "fato_os_servico_diario",
    "fato_os_pagamento_diario",
    "fato_comissao_diario",
)


def status_cobertura(*, dias: int = 14) -> dict[str, Any]:
    fim = date.today()
    inicio = fim - timedelta(days=dias - 1)
    with postgres_connect() as pg:
        cobertura: dict[str, Any] = {}
        with pg.cursor() as cur:
            for table in FATO_DIARIO:
                cur.execute(
                    f"""
                    SELECT data, COUNT(*) FROM {SCHEMA}.{table}
                    WHERE data >= %s AND data <= %s
                    GROUP BY data ORDER BY data
                    """,
                    (inicio, fim),
                )
                by_day = {r[0].isoformat(): int(r[1]) for r in cur.fetchall()}
                expected = [
                    (inicio + timedelta(days=i)).isoformat() for i in range(dias)
                ]
                gaps = [d for d in expected if d not in by_day]
                cobertura[table] = {
                    "dias_com_dado": len(by_day),
                    "gaps": gaps,
                    "amostra": dict(list(by_day.items())[-5:]),
                }

            cur.execute(
                f"""
                SELECT COUNT(*) FROM {SCHEMA}.fato_os_semanal
                """
            )
            n_sem = int(cur.fetchone()[0])
            cur.execute(f"SELECT COUNT(*) FROM {SCHEMA}.insights")
            n_ins = int(cur.fetchone()[0])
            cur.execute(
                f"""
                SELECT COUNT(*) FROM {SCHEMA}.ingest_reconciliacao
                WHERE data >= %s
                """,
                (inicio,),
            )
            n_rec = int(cur.fetchone()[0])

    return {
        "janela": {"de": inicio.isoformat(), "ate": fim.isoformat()},
        "fatos_diarios": cobertura,
        "fato_os_semanal_linhas": n_sem,
        "insights": n_ins,
        "reconciliacoes_janela": n_rec,
    }
