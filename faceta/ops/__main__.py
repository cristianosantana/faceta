from __future__ import annotations

import argparse
import json
import sys

from faceta.ingest import parse_data
from faceta.ops.backfill import backfill
from faceta.ops.doctor import doctor
from faceta.ops.health import healthcheck
from faceta.ops.metrics import metrics_from_traces
from faceta.ops.status import status_cobertura


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Faceta Fase 6 — operação")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("health", help="MySQL + Postgres + contrato")
    st = sub.add_parser("status", help="Cobertura de fatos / gaps / insights")
    st.add_argument("--dias", type=int, default=14)

    bf = sub.add_parser("backfill", help="Reingere intervalo de dias")
    bf.add_argument("--de", required=True, help="YYYY-MM-DD")
    bf.add_argument("--ate", required=True, help="YYYY-MM-DD")
    bf.add_argument("--cascata", action="store_true", help="Após ingest, cascata semanal --force")

    met = sub.add_parser("metrics", help="Agrega traces em logs/")
    met.add_argument("--dias", type=int, default=30)

    sub.add_parser("doctor", help="Checklist de diagnóstico operacional")

    args = parser.parse_args(argv)

    if args.cmd == "health":
        r = healthcheck()
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("ok") else 1

    if args.cmd == "status":
        r = status_cobertura(dias=args.dias)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "backfill":
        de = parse_data(args.de)
        ate = parse_data(args.ate)
        r = backfill(de, ate, cascata=args.cascata)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "metrics":
        r = metrics_from_traces(days=args.dias)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("ok") else 1

    if args.cmd == "doctor":
        r = doctor()
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("ok") else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
