from __future__ import annotations

import argparse
import sys

from faceta.cascata.engine import cascade_family
from faceta.cascata.families import FAMILIES
from faceta.cascata.periods import GRANULARIDADES
from faceta.db import apply_ddl, postgres_connect
from faceta.ingest import parse_data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Faceta Fase 2 — cascata temporal (diário → semanal/mensal/…)"
    )
    parser.add_argument(
        "--granularidade",
        required=True,
        choices=GRANULARIDADES,
        help="Nível a materializar",
    )
    parser.add_argument(
        "--periodo",
        required=True,
        help="Qualquer dia dentro do período (YYYY-MM-DD); normalizado para o início",
    )
    parser.add_argument(
        "--familia",
        default="os,servico,pagamento,comissao",
        help="Famílias separadas por vírgula (default: todas)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="DELETE do período + INSERT (reprocessamento)",
    )
    parser.add_argument(
        "--skip-ddl",
        action="store_true",
        help="Não aplicar DDL",
    )
    args = parser.parse_args(argv)
    ref = parse_data(args.periodo)

    nomes = [x.strip() for x in args.familia.split(",") if x.strip()]
    for n in nomes:
        if n not in FAMILIES:
            print(f"Família inválida: {n}. Use: {', '.join(FAMILIES)}", file=sys.stderr)
            return 1

    print(
        f"Cascata Faceta — granularidade={args.granularidade} "
        f"periodo_ref={ref.isoformat()} force={args.force}"
    )
    with postgres_connect() as pg:
        if not args.skip_ddl:
            apply_ddl(pg)
            print("DDL ok")
        for nome in nomes:
            r = cascade_family(
                pg, nome, args.granularidade, ref, force=args.force
            )
            if r.skipped:
                print(
                    f"  {nome}: skip (já existe data={r.inicio.isoformat()} "
                    f"[{r.inicio}..{r.fim}))"
                )
            else:
                print(
                    f"  {nome}: {r.rows} linhas "
                    f"[{r.inicio.isoformat()}..{r.fim.isoformat()})"
                )
    print("Concluído.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
