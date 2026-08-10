#!/usr/bin/env python3
"""Cascata semanal (semanas que tocam o mês) + mensal para YYYY-MM.

Ex.:
  PYTHONPATH=. .venv/bin/python scripts/mes_cascata.py 2026-07
  PYTHONPATH=. .venv/bin/python scripts/mes_cascata.py 2026-07 --force
  PYTHONPATH=. .venv/bin/python scripts/mes_cascata.py 2026-07 --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mes_common import (  # noqa: E402
    add_ano_mes_arg,
    iso_weeks_touching_month,
    month_bounds,
    run_module,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Faceta — cascata semanal + mensal para YYYY-MM"
    )
    add_ano_mes_arg(parser)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Repassado a faceta.cascata (DELETE do período + INSERT)",
    )
    parser.add_argument(
        "--familia",
        default=None,
        help="Repassado a faceta.cascata",
    )
    args = parser.parse_args(argv)
    year, month = args.ano_mes
    first, _ = month_bounds(year, month)
    weeks = iso_weeks_touching_month(year, month)

    print(
        f"Cascata mês {year:04d}-{month:02d} — "
        f"{len(weeks)} semana(s) + mensal force={args.force}"
    )

    def _extra() -> list[str]:
        out: list[str] = []
        if args.force:
            out.append("--force")
        if args.familia:
            out.extend(["--familia", args.familia])
        return out

    for monday, label in weeks:
        cmd_args = [
            "--granularidade",
            "semanal",
            "--periodo",
            monday.isoformat(),
            *_extra(),
        ]
        print(f"— semanal {label} (ref {monday.isoformat()})")
        rc = run_module("faceta.cascata", cmd_args, dry_run=args.dry_run)
        if rc != 0:
            print(f"FALHA cascata semanal {label} exit={rc}", file=sys.stderr)
            return rc

    cmd_mensal = [
        "--granularidade",
        "mensal",
        "--periodo",
        first.isoformat(),
        *_extra(),
    ]
    print(f"— mensal (ref {first.isoformat()})")
    rc = run_module("faceta.cascata", cmd_mensal, dry_run=args.dry_run)
    if rc != 0:
        print(f"FALHA cascata mensal exit={rc}", file=sys.stderr)
        return rc

    print("Concluído.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
