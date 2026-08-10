from __future__ import annotations

from typing import Any

from faceta.db import SCHEMA, postgres_connect
from faceta.ops.health import healthcheck
from faceta.ops.metrics import metrics_from_traces
from faceta.ops.status import status_cobertura
from faceta.trace.core import LOGS_DIR, load_events


def doctor() -> dict[str, Any]:
    """Checklist operacional (manual §4 + métricas)."""
    findings: list[dict[str, Any]] = []
    h = healthcheck()
    if not h["ok"]:
        findings.append(
            {
                "id": "health",
                "severity": "error",
                "msg": "healthcheck falhou",
                "detail": h["checks"],
            }
        )
    else:
        findings.append({"id": "health", "severity": "ok", "msg": "MySQL/Postgres/contrato ok"})

    st = status_cobertura(dias=14)
    gaps_total = sum(len(v.get("gaps") or []) for v in st["fatos_diarios"].values())
    if gaps_total > 10:
        findings.append(
            {
                "id": "gaps",
                "severity": "warn",
                "msg": f"{gaps_total} dias sem fato na janela de 14d (parcial é esperado)",
                "detail": {k: v["gaps"][:5] for k, v in st["fatos_diarios"].items()},
            }
        )
    else:
        findings.append(
            {"id": "gaps", "severity": "ok", "msg": f"gaps na janela: {gaps_total}"}
        )

    with postgres_connect() as pg:
        with pg.cursor() as cur:
            cur.execute(
                f"""
                SELECT familia, COUNT(*) FROM {SCHEMA}.ingest_reconciliacao
                GROUP BY familia ORDER BY 2 DESC
                """
            )
            rec = {r[0]: int(r[1]) for r in cur.fetchall()}
    if rec:
        findings.append(
            {
                "id": "reconcile",
                "severity": "info",
                "msg": "há registros de reconciliação (divergências sinalizadas)",
                "detail": rec,
            }
        )
    else:
        findings.append(
            {"id": "reconcile", "severity": "ok", "msg": "sem linhas em ingest_reconciliacao"}
        )

    m = metrics_from_traces(days=30)
    llm = m.get("llm_calls_ask") or {}
    if llm.get("amostras"):
        if llm.get("meta_ok"):
            findings.append(
                {
                    "id": "llm_meta",
                    "severity": "ok",
                    "msg": f"llm_calls ask ≤2 (amostras={llm['amostras']}, max={llm['max']})",
                }
            )
        else:
            findings.append(
                {
                    "id": "llm_meta",
                    "severity": "error",
                    "msg": f"ask com llm_calls >2: {llm.get('acima_de_2')}",
                }
            )
    else:
        findings.append(
            {
                "id": "llm_meta",
                "severity": "warn",
                "msg": "sem traces de ask com llm_calls ainda",
            }
        )

    # traces com error
    err_files = []
    if LOGS_DIR.is_dir():
        for path in sorted(LOGS_DIR.rglob("*.jsonl"))[-50:]:
            try:
                events = load_events(path)
            except Exception:
                continue
            run_end = next((e for e in events if e.get("event") == "run_end"), None)
            if run_end and run_end.get("status") == "error":
                err_files.append(str(path))
    if err_files:
        findings.append(
            {
                "id": "trace_errors",
                "severity": "warn",
                "msg": f"{len(err_files)} traces recentes com status=error",
                "detail": err_files[:5],
            }
        )
    else:
        findings.append({"id": "trace_errors", "severity": "ok", "msg": "sem errors recentes em traces"})

    ok = not any(f["severity"] == "error" for f in findings)
    return {"ok": ok, "findings": findings, "status": st, "metrics": m}
