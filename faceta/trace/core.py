from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from faceta.db import ROOT

LOGS_DIR = ROOT / "logs"

_current: ContextVar[TraceRun | None] = ContextVar("faceta_trace_run", default=None)

# attrs que nunca devem ir para o log
_REDACT_KEYS = frozenset(
    {
        "api_key",
        "llm_api_key",
        "openai_api_key",
        "password",
        "mysql_password",
        "postgres_url",
        "authorization",
        "token",
        "secret",
    }
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            lk = str(k).lower()
            if lk in _REDACT_KEYS or any(x in lk for x in ("password", "secret", "api_key", "token")):
                out[k] = "[REDACTED]"
            else:
                out[k] = _sanitize(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [_sanitize(x) for x in obj]
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, uuid.UUID):
        return str(obj)
    return obj


@dataclass
class Span:
    span_id: str
    name: str
    parent_id: str | None
    started_at: datetime
    ended_at: datetime | None = None
    duration_ms: float | None = None
    status: str = "ok"  # ok | error
    attrs: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class TraceRun:
    trace_id: str
    pipeline: str
    started_at: datetime
    path: Path
    attrs: dict[str, Any] = field(default_factory=dict)
    spans: list[Span] = field(default_factory=list)
    _stack: list[str] = field(default_factory=list)
    ended_at: datetime | None = None
    status: str = "ok"
    error: str | None = None

    def _append(self, event: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(_sanitize(event), ensure_ascii=False, default=str)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def emit_run_start(self) -> None:
        self._append(
            {
                "event": "run_start",
                "trace_id": self.trace_id,
                "pipeline": self.pipeline,
                "started_at": _iso(self.started_at),
                "attrs": self.attrs,
            }
        )

    def emit_run_end(self) -> None:
        self.ended_at = _utcnow()
        dur = (self.ended_at - self.started_at).total_seconds() * 1000
        self._append(
            {
                "event": "run_end",
                "trace_id": self.trace_id,
                "pipeline": self.pipeline,
                "status": self.status,
                "error": self.error,
                "ended_at": _iso(self.ended_at),
                "duration_ms": round(dur, 3),
                "span_count": len(self.spans),
            }
        )

    def start_span(self, name: str, **attrs: Any) -> Span:
        parent = self._stack[-1] if self._stack else None
        span = Span(
            span_id=uuid.uuid4().hex[:16],
            name=name,
            parent_id=parent,
            started_at=_utcnow(),
            attrs=dict(attrs),
        )
        self.spans.append(span)
        self._stack.append(span.span_id)
        self._append(
            {
                "event": "span_start",
                "trace_id": self.trace_id,
                "span_id": span.span_id,
                "parent_id": parent,
                "name": name,
                "started_at": _iso(span.started_at),
                "attrs": span.attrs,
            }
        )
        return span

    def end_span(
        self,
        span: Span,
        *,
        status: str = "ok",
        error: str | None = None,
        **attrs: Any,
    ) -> None:
        span.ended_at = _utcnow()
        span.duration_ms = (span.ended_at - span.started_at).total_seconds() * 1000
        span.status = status
        span.error = error
        if attrs:
            span.attrs.update(attrs)
        if self._stack and self._stack[-1] == span.span_id:
            self._stack.pop()
        self._append(
            {
                "event": "span_end",
                "trace_id": self.trace_id,
                "span_id": span.span_id,
                "parent_id": span.parent_id,
                "name": span.name,
                "status": status,
                "error": error,
                "ended_at": _iso(span.ended_at),
                "duration_ms": round(span.duration_ms, 3),
                "attrs": span.attrs,
            }
        )


def current_run() -> TraceRun | None:
    return _current.get()


@contextmanager
def trace_run(pipeline: str, **attrs: Any) -> Iterator[TraceRun]:
    """Abre um run de tracing; grava JSONL em logs/YYYY-MM-DD/<trace_id>.jsonl."""
    trace_id = uuid.uuid4().hex
    day = date.today().isoformat()
    path = LOGS_DIR / day / f"{trace_id}.jsonl"
    run = TraceRun(
        trace_id=trace_id,
        pipeline=pipeline,
        started_at=_utcnow(),
        path=path,
        attrs=dict(attrs),
    )
    token = _current.set(run)
    run.emit_run_start()
    try:
        yield run
    except Exception as e:
        run.status = "error"
        run.error = f"{type(e).__name__}: {e}"
        raise
    finally:
        # fechar spans abertos
        while run._stack:
            sid = run._stack[-1]
            span = next((s for s in run.spans if s.span_id == sid), None)
            if span and span.ended_at is None:
                run.end_span(span, status="error", error=run.error or "span não fechado")
            else:
                run._stack.pop()
        run.emit_run_end()
        _current.reset(token)
        print(f"trace_id={run.trace_id} path={run.path} status={run.status}")


@contextmanager
def span(name: str, **attrs: Any) -> Iterator[Span]:
    """Span aninhado no run atual; no-op se não houver run."""
    run = current_run()
    if run is None:
        # span fantasma sem persistência
        dummy = Span(
            span_id="noop",
            name=name,
            parent_id=None,
            started_at=_utcnow(),
            attrs=dict(attrs),
        )
        try:
            yield dummy
        except Exception as e:
            dummy.status = "error"
            dummy.error = str(e)
            raise
        return

    s = run.start_span(name, **attrs)
    try:
        yield s
    except Exception as e:
        run.end_span(s, status="error", error=f"{type(e).__name__}: {e}")
        raise
    else:
        run.end_span(s)


def load_events(path: Path) -> list[dict[str, Any]]:
    events = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def summarize(path: Path) -> dict[str, Any]:
    events = load_events(path)
    spans_end = [e for e in events if e.get("event") == "span_end"]
    run_end = next((e for e in events if e.get("event") == "run_end"), None)
    run_start = next((e for e in events if e.get("event") == "run_start"), None)
    slowest = sorted(spans_end, key=lambda e: e.get("duration_ms") or 0, reverse=True)
    errors = [e for e in spans_end if e.get("status") == "error"]
    return {
        "path": str(path),
        "trace_id": (run_start or {}).get("trace_id"),
        "pipeline": (run_start or {}).get("pipeline"),
        "status": (run_end or {}).get("status"),
        "duration_ms": (run_end or {}).get("duration_ms"),
        "error": (run_end or {}).get("error"),
        "spans": [
            {
                "name": e.get("name"),
                "status": e.get("status"),
                "duration_ms": e.get("duration_ms"),
                "error": e.get("error"),
                "attrs": e.get("attrs"),
            }
            for e in spans_end
        ],
        "slowest": [
            {"name": e.get("name"), "duration_ms": e.get("duration_ms")}
            for e in slowest[:5]
        ],
        "errors": errors,
    }
