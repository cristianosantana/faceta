from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from faceta.cascata.engine import cascade_family
from faceta.cascata.families import FAMILIES
from faceta.db import apply_ddl, mysql_connect, postgres_connect
from faceta.ingest.dimensoes import sync_dimensoes
from faceta.ingest.fato_comissao import ingest_fato_comissao
from faceta.ingest.fato_os import ingest_fato_os
from faceta.ingest.fato_os_pagamento import ingest_fato_os_pagamento
from faceta.ingest.fato_os_servico import ingest_fato_os_servico
from faceta.ingest.reconcile import reconcile_day
from faceta.trace import span, trace_run


FAMILIAS = {
    "os": ingest_fato_os,
    "servico": ingest_fato_os_servico,
    "pagamento": ingest_fato_os_pagamento,
    "comissao": ingest_fato_comissao,
}


def backfill(
    de: date,
    ate: date,
    *,
    cascata: bool = False,
    familias: list[str] | None = None,
) -> dict[str, Any]:
    if ate < de:
        raise ValueError("ate < de")
    nomes = familias or list(FAMILIAS.keys())
    dias: list[date] = []
    d = de
    while d <= ate:
        dias.append(d)
        d += timedelta(days=1)

    resultados: list[dict[str, Any]] = []
    with trace_run("ops_backfill", de=de.isoformat(), ate=ate.isoformat(), cascata=cascata):
        mysql = mysql_connect()
        try:
            with postgres_connect() as pg:
                with span("apply_ddl"):
                    apply_ddl(pg)
                with span("sync_dimensoes"):
                    sync_dimensoes(mysql, pg)
                for dia in dias:
                    with span("ingest_dia", data=dia.isoformat()):
                        counts = {}
                        for nome in nomes:
                            counts[nome] = FAMILIAS[nome](mysql, pg, dia)
                        diverg = reconcile_day(mysql, pg, dia)
                        resultados.append(
                            {"data": dia.isoformat(), "counts": counts, "reconcile": diverg}
                        )
                if cascata:
                    # cascata semanal para cada segunda no intervalo
                    vistos: set[date] = set()
                    for dia in dias:
                        from faceta.cascata.periods import period_bounds

                        ini, _ = period_bounds("semanal", dia)
                        if ini in vistos:
                            continue
                        vistos.add(ini)
                        with span("cascata_semanal", data=ini.isoformat()):
                            for fam in FAMILIES:
                                cascade_family(pg, fam, "semanal", ini, force=True)
        finally:
            mysql.close()
    return {"dias": len(dias), "resultados": resultados, "cascata": cascata}
