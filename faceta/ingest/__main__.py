from __future__ import annotations

import argparse
import sys
from datetime import date

from faceta.db import apply_ddl, mysql_connect, postgres_connect
from faceta.ingest import parse_data, yesterday
from faceta.ingest.dimensoes import sync_dimensoes
from faceta.ingest.fato_comissao import ingest_fato_comissao
from faceta.ingest.fato_os import ingest_fato_os
from faceta.ingest.fato_os_pagamento import ingest_fato_os_pagamento
from faceta.ingest.fato_os_servico import ingest_fato_os_servico
from faceta.ingest.reconcile import reconcile_day

FAMILIAS = {
    "os": ingest_fato_os,
    "servico": ingest_fato_os_servico,
    "pagamento": ingest_fato_os_pagamento,
    "comissao": ingest_fato_comissao,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Faceta Fase 1 — ingestão diária MySQL → Postgres")
    parser.add_argument(
        "--data",
        help="Dia a ingerir (YYYY-MM-DD). Default: ontem.",
        default=None,
    )
    parser.add_argument(
        "--familia",
        help="Famílias separadas por vírgula: os,servico,pagamento,comissao (default: todas)",
        default="os,servico,pagamento,comissao",
    )
    parser.add_argument(
        "--skip-ddl",
        action="store_true",
        help="Não aplicar DDL",
    )
    parser.add_argument(
        "--skip-reconcile",
        action="store_true",
        help="Não rodar reconciliação",
    )
    parser.add_argument(
        "--skip-dims",
        action="store_true",
        help="Não sincronizar dimensões (dim_*)",
    )
    parser.add_argument(
        "--only-dims",
        action="store_true",
        help="Só sincronizar dimensões (ignora fatos)",
    )
    args = parser.parse_args(argv)
    dia = parse_data(args.data) if args.data else yesterday()

    print(f"Ingestão Faceta — data={dia.isoformat()}")
    mysql = mysql_connect()
    try:
        with postgres_connect() as pg:
            if not args.skip_ddl:
                apply_ddl(pg)
                print("DDL ok")
            if not args.skip_dims or args.only_dims:
                dim_counts = sync_dimensoes(mysql, pg)
                for name, n in dim_counts.items():
                    print(f"  {name}: {n} linhas")
            if args.only_dims:
                print("Concluído (somente dimensões).")
                return 0

            nomes = [x.strip() for x in args.familia.split(",") if x.strip()]
            for n in nomes:
                if n not in FAMILIAS:
                    print(f"Família inválida: {n}. Use: {', '.join(FAMILIAS)}", file=sys.stderr)
                    return 1
            for nome in nomes:
                n = FAMILIAS[nome](mysql, pg, dia)
                print(f"  {nome}: {n} linhas agregadas")
            if not args.skip_reconcile:
                divergencias = reconcile_day(mysql, pg, dia)
                print(f"  reconciliacao: {divergencias} achados")
    finally:
        mysql.close()
    print("Concluído.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
