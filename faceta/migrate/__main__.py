from __future__ import annotations

import argparse
import json
import sys

from faceta.db import apply_ddl, postgres_connect
from faceta.migrate.runner import run_up, status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Migrações destrutivas/versionadas do schema Faceta. "
            "Rodar manualmente — não faz parte do ingest/cascata."
        )
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Lista migrações e se já foram aplicadas")
    up = sub.add_parser("up", help="Aplica migrações pendentes")
    up.add_argument(
        "--dry-run",
        action="store_true",
        help="Só lista o que seria aplicado",
    )
    up.add_argument(
        "--no-ddl",
        action="store_true",
        help="Não roda apply_ddl (CREATE IF NOT EXISTS) após as migrações",
    )

    args = parser.parse_args(argv)

    with postgres_connect() as pg:
        if args.cmd == "status":
            rows = status(pg)
            print(json.dumps(rows, ensure_ascii=False, indent=2))
            pending_n = sum(1 for r in rows if not r["applied"])
            print(f"pendentes={pending_n}")
            return 0

        if args.cmd == "up":
            results = run_up(pg, dry_run=args.dry_run)
            if not results:
                print("Nenhuma migração pendente.")
            else:
                for r in results:
                    print(f"{r['id']}: {r['actions']}")
            if args.dry_run:
                return 0
            if not args.no_ddl:
                apply_ddl(pg)
                print("apply_ddl ok (CREATE IF NOT EXISTS)")
            print(
                "Atenção: se houve DROP, reingerir dias afetados "
                "(scripts/mes_ingest.py / faceta.ops backfill)."
            )
            return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
