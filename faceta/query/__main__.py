from __future__ import annotations

import argparse
import json
import sys

from faceta.db import postgres_connect
from faceta.query.engine import consultar
from faceta.query.errors import ConsultaRejeitada
from faceta.query.maps import COMPARACOES, GRANULARIDADE_SUFIXO
from faceta.trace import span, trace_run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Faceta Fase 3 — motor de consulta genérico")
    parser.add_argument("--entity-type", required=True)
    parser.add_argument("--granularidade", required=True, choices=sorted(GRANULARIDADE_SUFIXO))
    parser.add_argument("--periodo", required=True, help="YYYY-MM-DD | YYYY-Www | YYYY-MM | YYYY-H1 | YYYY")
    parser.add_argument("--entity-id", default=None)
    parser.add_argument("--quebra", default=None)
    parser.add_argument("--quebra-valor", default=None)
    parser.add_argument("--comparacao", default=None, choices=sorted(COMPARACOES))
    parser.add_argument("--ranking", action="store_true")
    args = parser.parse_args(argv)

    try:
        with trace_run(
            "query",
            entity_type=args.entity_type,
            granularidade=args.granularidade,
            periodo=args.periodo,
            ranking=args.ranking,
            comparacao=args.comparacao,
        ):
            with postgres_connect() as pg:
                with span(
                    "consultar",
                    entity_type=args.entity_type,
                    granularidade=args.granularidade,
                    periodo=args.periodo,
                    ranking=args.ranking,
                ):
                    result = consultar(
                        pg,
                        entity_type=args.entity_type,
                        granularidade=args.granularidade,
                        periodo=args.periodo,
                        entity_id=args.entity_id,
                        quebra=args.quebra,
                        quebra_valor=args.quebra_valor,
                        comparacao=args.comparacao,
                        ranking=args.ranking,
                    )
    except ConsultaRejeitada as e:
        print(f"REJEITADA: {e}", file=sys.stderr)
        return 2

    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
