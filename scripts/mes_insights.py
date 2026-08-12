#!/usr/bin/env python3
"""Insights (train + run) por entity_type × semanas ISO do mês.

Cobre todos os entity_types do contrato.yaml (ex.: vendedor, servico, …).

Ex.:
  PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07
  FACETA_ALLOW_FORCE_LLM=1 PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07 --force-llm --limit 5
  PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07 --entity-type vendedor,servico
  PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07 --dry-run
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
    entity_types_from_contrato,
    iso_weeks_touching_month,
    run_module,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Faceta — insights train/run para YYYY-MM (todas as entities)"
    )
    add_ano_mes_arg(parser)
    parser.add_argument(
        "--entity-type",
        default=None,
        help="Lista separada por vírgula (default: todos do contrato.yaml)",
    )
    parser.add_argument(
        "--granularidade",
        default="semanal",
        help="Default: semanal",
    )
    parser.add_argument(
        "--force-llm",
        action="store_true",
        help="DEV ONLY: exige FACETA_ALLOW_FORCE_LLM=1 (não use em cron)",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--skip-train",
        action="store_true",
        help="Não roda train (só run)",
    )
    args = parser.parse_args(argv)
    year, month = args.ano_mes

    if args.force_llm:
        import os

        from dotenv import load_dotenv

        load_dotenv(Path(__file__).resolve().parents[1] / ".env")
        if os.getenv("FACETA_ALLOW_FORCE_LLM", "").strip().lower() not in (
            "1",
            "true",
            "yes",
        ):
            print(
                "ERRO: --force-llm exige FACETA_ALLOW_FORCE_LLM=1 "
                "(não use em cron de produção).",
                file=sys.stderr,
            )
            return 2

    if args.entity_type:
        entities = [x.strip() for x in args.entity_type.split(",") if x.strip()]
    else:
        entities = entity_types_from_contrato()

    weeks = iso_weeks_touching_month(year, month)
    labels = [lab for _, lab in weeks]

    print(
        f"Insights mês {year:04d}-{month:02d} — "
        f"{len(entities)} entity_type(s) × {len(labels)} semana(s) "
        f"granularidade={args.granularidade}"
    )
    print(f"  entities: {', '.join(entities)}")
    print(f"  semanas: {', '.join(labels)}")

    for et in entities:
        if not args.skip_train:
            print(f"— train {et}")
            rc = run_module(
                "faceta.insights",
                [
                    "train",
                    "--entity-type",
                    et,
                    "--granularidade",
                    args.granularidade,
                ],
                dry_run=args.dry_run,
            )
            if rc != 0:
                print(f"FALHA train {et} exit={rc}", file=sys.stderr)
                return rc

        for _, label in weeks:
            cmd = [
                "run",
                "--entity-type",
                et,
                "--granularidade",
                args.granularidade,
                "--periodo",
                label,
            ]
            if args.force_llm:
                cmd.append("--force-llm")
            if args.limit is not None:
                cmd.extend(["--limit", str(args.limit)])
            print(f"— run {et} {label}")
            rc = run_module("faceta.insights", cmd, dry_run=args.dry_run)
            if rc != 0:
                print(f"FALHA run {et} {label} exit={rc}", file=sys.stderr)
                return rc

    print("Concluído.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
