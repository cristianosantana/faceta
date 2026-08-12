"""Helpers compartilhados dos scripts de mês (YYYY-MM).

Funções de calendário vivem em ``faceta.ops.calendario`` (também usadas por ``ops ano``).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from faceta.ops.calendario import (  # noqa: F401
    days_in_month,
    days_in_year,
    iso_week_label,
    iso_weeks_in_range,
    iso_weeks_of_year,
    iso_weeks_touching_month,
    month_bounds,
    semesters_in_range,
    semesters_of_year,
)

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
