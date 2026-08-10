"""Helpers compartilhados dos scripts de mês (YYYY-MM)."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_ano_mes(s: str) -> tuple[int, int]:
    parts = s.strip().split("-")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("use YYYY-MM (ex.: 2026-07)")
    try:
        year, month = int(parts[0]), int(parts[1])
    except ValueError as e:
        raise argparse.ArgumentTypeError("use YYYY-MM (ex.: 2026-07)") from e
    if year < 2000 or year > 2100 or not (1 <= month <= 12):
        raise argparse.ArgumentTypeError("ano/mês fora do intervalo esperado")
    return year, month


def month_bounds(year: int, month: int) -> tuple[date, date]:
    """Retorna [primeiro, próximo_mês)."""
    first = date(year, month, 1)
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    return first, nxt


def days_in_month(year: int, month: int) -> list[date]:
    first, nxt = month_bounds(year, month)
    out: list[date] = []
    d = first
    while d < nxt:
        out.append(d)
        d += timedelta(days=1)
    return out


def iso_week_label(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def iso_weeks_touching_month(year: int, month: int) -> list[tuple[date, str]]:
    """Segundas ISO + rótulo YYYY-Www das semanas que intersectam o mês."""
    first, nxt = month_bounds(year, month)
    last = nxt - timedelta(days=1)
    monday = first - timedelta(days=first.weekday())
    weeks: list[tuple[date, str]] = []
    seen: set[str] = set()
    d = monday
    while d <= last:
        week_end = d + timedelta(days=7)
        if week_end > first and d < nxt:
            label = iso_week_label(d)
            if label not in seen:
                seen.add(label)
                weeks.append((d, label))
        d += timedelta(days=7)
    return weeks


def entity_types_from_contrato() -> list[str]:
    import yaml

    path = REPO_ROOT / "contrato.yaml"
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return list((data.get("entity_types") or {}).keys())


def run_module(module: str, args: list[str], *, dry_run: bool = False) -> int:
    cmd = [sys.executable, "-m", module, *args]
    print("+", shlex_join(cmd))
    if dry_run:
        return 0
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(REPO_ROOT) if not existing else f"{REPO_ROOT}{os.pathsep}{existing}"
    )
    r = subprocess.run(cmd, cwd=str(REPO_ROOT), env=env)
    return r.returncode


def shlex_join(parts: list[str]) -> str:
    out: list[str] = []
    for p in parts:
        if any(c.isspace() for c in p):
            out.append(repr(p))
        else:
            out.append(p)
    return " ".join(out)


def add_ano_mes_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "ano_mes",
        type=parse_ano_mes,
        help="Mês a processar (YYYY-MM), ex.: 2026-07",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Só imprime os comandos, não executa",
    )
