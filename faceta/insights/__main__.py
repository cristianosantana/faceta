from __future__ import annotations

import argparse
import json
import sys

from faceta.db import postgres_connect
from faceta.insights.job import run_job, train_job
from faceta.insights.tc import run_tc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Faceta Fase 5 — insights (autoencoder TF)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    tr = sub.add_parser("train", help="Treina autoencoder nas séries")
    tr.add_argument("--entity-type", default="vendedor")
    tr.add_argument("--granularidade", default="semanal")
    tr.add_argument("--window", type=int, default=8)
    tr.add_argument("--epochs", type=int, default=40)

    run = sub.add_parser("run", help="Detecta e grava insights se sinal")
    run.add_argument("--entity-type", default="vendedor")
    run.add_argument("--granularidade", default="semanal")
    run.add_argument("--periodo", required=True, help="YYYY-MM-DD | YYYY-Www | …")
    run.add_argument("--sem-narracao", action="store_true")
    run.add_argument(
        "--force-llm",
        action="store_true",
        help="Força sinal+LLM (útil p/ gerar 1 insight real com pouco histórico)",
    )
    run.add_argument("--limit", type=int, default=None, help="Limita N entidades (após ordenar por valor)")

    sub.add_parser("tc", help="TC16–TC17")

    args = parser.parse_args(argv)

    if args.cmd == "tc":
        return run_tc()

    with postgres_connect() as pg:
        if args.cmd == "train":
            info = train_job(
                pg,
                entity_type=args.entity_type,
                granularidade=args.granularidade,
                window=args.window,
                epochs=args.epochs,
            )
            print(json.dumps(info, ensure_ascii=False, indent=2))
            return 0
        if args.cmd == "run":
            results = run_job(
                pg,
                entity_type=args.entity_type,
                granularidade=args.granularidade,
                periodo=args.periodo,
                narrar=not args.sem_narracao,
                force_llm=args.force_llm,
                limit=args.limit,
            )
            sinais = [r for r in results if r.sinal]
            gravados = [r for r in results if r.insight_gravado]
            print(f"series={len(results)} sinais={len(sinais)} insights_gravados={len(gravados)}")
            for r in gravados[:10]:
                print(f"  {r.entity_id} erro={r.erro} hipotese={r.hipotese}")
            return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
