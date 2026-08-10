#!/usr/bin/env python3
"""Ingestão de todos os dias de um mês (YYYY-MM).

Ex.:
  PYTHONPATH=. .venv/bin/python scripts/mes_ingest.py 2026-07
  PYTHONPATH=. .venv/bin/python scripts/mes_ingest.py 2026-07 --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mes_common import add_ano_mes_arg, days_in_month, run_module  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Faceta — ingestão diária para todos os dias de YYYY-MM"
    )
    add_ano_mes_arg(parser)
    parser.add_argument(
        "--familia",
        default=None,
        help="Repassado a faceta.ingest (os,servico,pagamento,comissao)",
    )
    args = parser.parse_args(argv)
    year, month = args.ano_mes
    dias = days_in_month(year, month)
    print(f"Ingest mês {year:04d}-{month:02d} — {len(dias)} dia(s)")

    failed = 0
    for dia in dias:
        cmd_args = ["--data", dia.isoformat()]
        if args.familia:
            cmd_args.extend(["--familia", args.familia])
        rc = run_module("faceta.ingest", cmd_args, dry_run=args.dry_run)
        if rc != 0:
            print(f"FALHA ingest {dia.isoformat()} exit={rc}", file=sys.stderr)
            failed += 1
            return rc

    print("Concluído." if not failed else f"Falhas: {failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
