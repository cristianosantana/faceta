"""Pipeline anual in-process: dims → diário → cascata → insights.

Um processo, uma conexão MySQL + Postgres — mesmo padrão de ``faceta.ops.backfill``.
Não substitui os CLIs granulares nem o cron D−1; serve para histórico / ano fechado.
"""

from __future__ import annotations

from datetime import date
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
from faceta.insights.job import run_job, train_job
from faceta.ops.calendario import (
    days_in_year,
    iso_weeks_in_range,
    month_bounds,
    semesters_in_range,
)
from faceta.query.contract import load_contrato
from faceta.trace import span, trace_run

FAMILIAS_INGEST = {
    "os": ingest_fato_os,
    "servico": ingest_fato_os_servico,
    "pagamento": ingest_fato_os_pagamento,
    "comissao": ingest_fato_comissao,
}


def entity_types_from_contrato() -> list[str]:
    return list(load_contrato()["entity_types"].keys())


def _cascata_todas_familias(
    pg,
    granularidade: str,
    ref: date,
    familias: list[str] | None,
    force: bool,
    falhas: dict[str, list],
    *,
    continue_on_error: bool,
) -> None:
    nomes = familias or list(FAMILIES.keys())
    for nome in nomes:
        if nome not in FAMILIES:
            raise ValueError(f"família inválida: {nome}")
        try:
            r = cascade_family(pg, nome, granularidade, ref, force=force)
            tag = "skip" if r.skipped else f"{r.rows} linhas"
            print(
                f"  cascata {granularidade}/{nome} "
                f"ref={ref.isoformat()} → {tag}"
            )
        except Exception as e:
            falhas["cascata"].append(
                {
                    "granularidade": granularidade,
                    "familia": nome,
                    "ref": ref.isoformat(),
                    "erro": str(e),
                }
            )
            if not continue_on_error:
                raise


def ano_pipeline(
    ano: int,
    *,
    de_mes: int = 1,
    ate_mes: int = 12,
    familias: list[str] | None = None,
    entity_types: list[str] | None = None,
    skip_ingest: bool = False,
    skip_cascata: bool = False,
    skip_semestral: bool = False,
    skip_anual: bool = False,
    skip_insights: bool = False,
    skip_dims: bool = False,
    force_cascata: bool = False,
    force_llm: bool = False,
    ate_hoje: bool = True,
    continue_on_error: bool = False,
) -> dict[str, Any]:
    if not (2000 <= ano <= 2100):
        raise ValueError(f"ano fora do intervalo esperado: {ano}")
    if not (1 <= de_mes <= 12 and 1 <= ate_mes <= 12 and de_mes <= ate_mes):
        raise ValueError(f"meses inválidos: {de_mes}..{ate_mes}")

    falhas: dict[str, list] = {"ingest": [], "cascata": [], "insights": []}
    dias = days_in_year(ano, de_mes, ate_mes)
    if ate_hoje and ano == date.today().year:
        hoje = date.today()
        dias = [d for d in dias if d < hoje]

    familias_ingest = familias or list(FAMILIAS_INGEST.keys())
    for n in familias_ingest:
        if n not in FAMILIAS_INGEST:
            raise ValueError(f"família de ingest inválida: {n}")

    with trace_run(
        "ops_ano",
        ano=ano,
        de_mes=de_mes,
        ate_mes=ate_mes,
        force_cascata=force_cascata,
        force_llm=force_llm,
    ):
        mysql = mysql_connect()
        try:
            with postgres_connect() as pg:
                with span("apply_ddl"):
                    apply_ddl(pg)
                    print("DDL ok")

                if not skip_dims:
                    with span("sync_dimensoes"):
                        counts = sync_dimensoes(mysql, pg)
                        print(f"dims sync: {counts}")

                # 1) diário
                if not skip_ingest:
                    print(f"Ingest: {len(dias)} dia(s)")
                    for dia in dias:
                        with span("ingest_dia", data=dia.isoformat()):
                            try:
                                for nome in familias_ingest:
                                    n = FAMILIAS_INGEST[nome](mysql, pg, dia)
                                    print(f"  ingest {dia.isoformat()} {nome}={n}")
                                reconcile_day(mysql, pg, dia)
                            except Exception as e:
                                falhas["ingest"].append(
                                    {"data": dia.isoformat(), "erro": str(e)}
                                )
                                print(
                                    f"  FALHA ingest {dia.isoformat()}: {e}",
                                    flush=True,
                                )
                                if not continue_on_error:
                                    raise

                # 2–5) cascata: semanal → mensal → semestral → anual
                if not skip_cascata:
                    weeks = iso_weeks_in_range(ano, de_mes, ate_mes)
                    print(f"Cascata semanal: {len(weeks)} semana(s)")
                    for monday, label in weeks:
                        with span("cascata_semanal", periodo=label):
                            try:
                                _cascata_todas_familias(
                                    pg,
                                    "semanal",
                                    monday,
                                    familias,
                                    force_cascata,
                                    falhas,
                                    continue_on_error=continue_on_error,
                                )
                            except Exception:
                                if not continue_on_error:
                                    raise

                    print(f"Cascata mensal: {de_mes:02d}..{ate_mes:02d}")
                    for mes in range(de_mes, ate_mes + 1):
                        primeiro, _ = month_bounds(ano, mes)
                        with span("cascata_mensal", periodo=f"{ano}-{mes:02d}"):
                            try:
                                _cascata_todas_familias(
                                    pg,
                                    "mensal",
                                    primeiro,
                                    familias,
                                    force_cascata,
                                    falhas,
                                    continue_on_error=continue_on_error,
                                )
                            except Exception:
                                if not continue_on_error:
                                    raise

                    if not skip_semestral:
                        semis = semesters_in_range(ano, de_mes, ate_mes)
                        print(f"Cascata semestral: {[s[1] for s in semis]}")
                        for inicio, label in semis:
                            with span("cascata_semestral", periodo=label):
                                try:
                                    _cascata_todas_familias(
                                        pg,
                                        "semestral",
                                        inicio,
                                        familias,
                                        force_cascata,
                                        falhas,
                                        continue_on_error=continue_on_error,
                                    )
                                except Exception:
                                    if not continue_on_error:
                                        raise

                    if not skip_anual and de_mes == 1 and ate_mes == 12:
                        print(f"Cascata anual: {ano}")
                        with span("cascata_anual", periodo=str(ano)):
                            try:
                                _cascata_todas_familias(
                                    pg,
                                    "anual",
                                    date(ano, 1, 1),
                                    familias,
                                    force_cascata,
                                    falhas,
                                    continue_on_error=continue_on_error,
                                )
                            except Exception:
                                if not continue_on_error:
                                    raise
                    elif not skip_anual:
                        print(
                            f"Cascata anual: pulada "
                            f"(só com --de-mes 1 --ate-mes 12; atual={de_mes}..{ate_mes})"
                        )

                # 6) insights
                if not skip_insights:
                    entidades = entity_types or entity_types_from_contrato()
                    weeks = iso_weeks_in_range(ano, de_mes, ate_mes)
                    print(
                        f"Insights: {len(entidades)} entity_type(s) × "
                        f"{len(weeks)} semana(s)"
                    )
                    for et in entidades:
                        with span("insights_train", entity_type=et):
                            try:
                                info = train_job(
                                    pg, entity_type=et, granularidade="semanal"
                                )
                                print(f"  train {et}: {info}")
                            except Exception as e:
                                falhas["insights"].append(
                                    {"entity_type": et, "fase": "train", "erro": str(e)}
                                )
                                print(f"  FALHA train {et}: {e}", flush=True)
                                if not continue_on_error:
                                    raise
                                continue
                        for _, label in weeks:
                            with span(
                                "insights_run", entity_type=et, periodo=label
                            ):
                                try:
                                    results = run_job(
                                        pg,
                                        entity_type=et,
                                        granularidade="semanal",
                                        periodo=label,
                                        force_llm=force_llm,
                                    )
                                    grav = sum(1 for r in results if r.insight_gravado)
                                    print(
                                        f"  run {et} {label}: "
                                        f"series={len(results)} gravados={grav}"
                                    )
                                except Exception as e:
                                    falhas["insights"].append(
                                        {
                                            "entity_type": et,
                                            "periodo": label,
                                            "erro": str(e),
                                        }
                                    )
                                    print(
                                        f"  FALHA run {et} {label}: {e}",
                                        flush=True,
                                    )
                                    if not continue_on_error:
                                        raise
        finally:
            mysql.close()

    n_falhas = sum(len(v) for v in falhas.values())
    return {
        "ano": ano,
        "de_mes": de_mes,
        "ate_mes": ate_mes,
        "dias_processados": len(dias) if not skip_ingest else 0,
        "dias_candidatos": len(dias),
        "falhas": falhas,
        "n_falhas": n_falhas,
        "ok": n_falhas == 0,
    }
