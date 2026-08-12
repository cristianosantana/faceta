from __future__ import annotations

import argparse
import json
import sys

from faceta.ingest import parse_data
from faceta.ops.ano import ano_pipeline
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

    ano_p = sub.add_parser(
        "ano",
        help=(
            "Pipeline completo do ano (in-process): "
            "dims → diário → semanal → mensal → semestral → anual → insights"
        ),
    )
    ano_p.add_argument("ano", type=int, help="Ano civil (ex.: 2026)")
    ano_p.add_argument("--de-mes", type=int, default=1)
    ano_p.add_argument("--ate-mes", type=int, default=12)
    ano_p.add_argument(
        "--familia",
        default=None,
        help="Famílias separadas por vírgula (default: todas)",
    )
    ano_p.add_argument(
        "--entity-type",
        default=None,
        help="entity_types separados por vírgula (default: todos do contrato)",
    )
    ano_p.add_argument("--skip-ingest", action="store_true")
    ano_p.add_argument("--skip-cascata", action="store_true")
    ano_p.add_argument("--skip-semestral", action="store_true")
    ano_p.add_argument("--skip-anual", action="store_true")
    ano_p.add_argument("--skip-insights", action="store_true")
    ano_p.add_argument("--skip-dims", action="store_true")
    ano_p.add_argument(
        "--force",
        action="store_true",
        help="--force na cascata (reprocessa períodos existentes)",
    )
    ano_p.add_argument(
        "--force-llm",
        action="store_true",
        help="requer FACETA_ALLOW_FORCE_LLM=1 (mesma trava do insights)",
    )
    ano_p.add_argument(
        "--continue-on-error",
        action="store_true",
        help="não aborta o ano inteiro por 1 dia/período com falha",
    )
    ano_p.add_argument(
        "--sem-limite-hoje",
        dest="ate_hoje",
        action="store_false",
        default=True,
        help="também processa dias >= hoje (default: só até ontem no ano corrente)",
    )

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

    if args.cmd == "ano":
        familias = None
        if args.familia:
            familias = [x.strip() for x in args.familia.split(",") if x.strip()]
        entity_types = None
        if args.entity_type:
            entity_types = [
                x.strip() for x in args.entity_type.split(",") if x.strip()
            ]
        try:
            r = ano_pipeline(
                args.ano,
                de_mes=args.de_mes,
                ate_mes=args.ate_mes,
                familias=familias,
                entity_types=entity_types,
                skip_ingest=args.skip_ingest,
                skip_cascata=args.skip_cascata,
                skip_semestral=args.skip_semestral,
                skip_anual=args.skip_anual,
                skip_insights=args.skip_insights,
                skip_dims=args.skip_dims,
                force_cascata=args.force,
                force_llm=args.force_llm,
                ate_hoje=args.ate_hoje,
                continue_on_error=args.continue_on_error,
            )
        except Exception as e:
            print(f"FALHA ops ano: {type(e).__name__}: {e}", file=sys.stderr)
            return 1
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("ok") else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
