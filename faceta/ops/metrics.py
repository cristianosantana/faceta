from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from faceta.trace.core import LOGS_DIR, load_events


def metrics_from_traces(*, days: int | None = None) -> dict[str, Any]:
    if not LOGS_DIR.is_dir():
        return {"ok": False, "error": f"{LOGS_DIR} inexistente", "runs": 0}

    files: list[Path] = sorted(LOGS_DIR.rglob("*.jsonl"))
    if days is not None:
        # filtra por pasta YYYY-MM-DD
        from datetime import date, timedelta

        keep = {
            (date.today() - timedelta(days=i)).isoformat() for i in range(days)
        }
        files = [f for f in files if f.parent.name in keep]

    by_pipeline: dict[str, list[float]] = defaultdict(list)
    llm_calls: list[int] = []
    errors = 0
    runs = 0
    ask_over_2 = 0

    for path in files:
        try:
            events = load_events(path)
        except Exception:
            continue
        run_end = next((e for e in events if e.get("event") == "run_end"), None)
        run_start = next((e for e in events if e.get("event") == "run_start"), None)
        if not run_end:
            continue
        runs += 1
        pipe = (run_start or {}).get("pipeline") or "unknown"
        dur = float(run_end.get("duration_ms") or 0)
        by_pipeline[pipe].append(dur)
        if run_end.get("status") == "error":
            errors += 1

        # llm_calls em span resultado (ask)
        for e in events:
            if e.get("event") == "span_end" and e.get("name") == "resultado":
                attrs = e.get("attrs") or {}
                if "llm_calls" in attrs:
                    n = int(attrs["llm_calls"])
                    llm_calls.append(n)
                    if n > 2:
                        ask_over_2 += 1

    def _agg(vals: list[float]) -> dict[str, float]:
        if not vals:
            return {}
        return {
            "n": len(vals),
            "avg_ms": round(sum(vals) / len(vals), 2),
            "max_ms": round(max(vals), 2),
            "min_ms": round(min(vals), 2),
        }

    return {
        "ok": True,
        "runs": runs,
        "errors": errors,
        "pipelines": {k: _agg(v) for k, v in sorted(by_pipeline.items())},
        "llm_calls_ask": {
            "amostras": len(llm_calls),
            "max": max(llm_calls) if llm_calls else None,
            "avg": round(sum(llm_calls) / len(llm_calls), 2) if llm_calls else None,
            "acima_de_2": ask_over_2,
            "meta_ok": ask_over_2 == 0,
        },
        "arquivos": len(files),
    }
