from __future__ import annotations

import argparse
import json
import sys

from faceta.ask.pipeline import perguntar
from faceta.db import postgres_connect
from faceta.query.errors import ConsultaRejeitada


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Faceta Fase 4 — pergunta em linguagem natural")
    parser.add_argument("pergunta", nargs="+", help="Pergunta do usuário")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime JSON completo (params + resultado + narração)",
    )
    parser.add_argument(
        "--sem-narracao",
        action="store_true",
        help="Só entendimento + consulta (1 chamada LLM)",
    )
    args = parser.parse_args(argv)
    texto = " ".join(args.pergunta)

    try:
        with postgres_connect() as pg:
            resp = perguntar(pg, texto, narrar=not args.sem_narracao)
    except ConsultaRejeitada as e:
        print(f"REJEITADA: {e}", file=sys.stderr)
        return 2
    except SystemExit:
        raise
    except Exception as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(resp.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"llm_calls={resp.llm_calls}")
        if resp.trace_id:
            print(f"trace_id={resp.trace_id}")
        print(
            f"params: {resp.params.entity_type} / {resp.params.granularidade} / "
            f"{resp.params.periodo} ranking={resp.params.ranking}"
        )
        print()
        print(resp.narracao or "(sem narração)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
