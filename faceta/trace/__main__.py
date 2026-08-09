from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from faceta.trace.core import load_events, summarize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Faceta — visualizar traces JSONL")
    sub = parser.add_subparsers(dest="cmd", required=True)

    show = sub.add_parser("show", help="Timeline e gargalos de um arquivo .jsonl")
    show.add_argument("arquivo", help="Path logs/YYYY-MM-DD/<trace_id>.jsonl")
    show.add_argument("--raw", action="store_true", help="Imprime eventos brutos")

    args = parser.parse_args(argv)
    if args.cmd == "show":
        path = Path(args.arquivo)
        if not path.is_file():
            print(f"arquivo não encontrado: {path}", file=sys.stderr)
            return 1
        if args.raw:
            for ev in load_events(path):
                print(json.dumps(ev, ensure_ascii=False))
            return 0
        s = summarize(path)
        print(json.dumps(s, ensure_ascii=False, indent=2))
        print()
        print("Timeline:")
        for sp in s["spans"]:
            err = f" ERROR={sp['error']}" if sp.get("error") else ""
            print(f"  {sp['duration_ms']:>10.1f} ms  [{sp['status']}]  {sp['name']}{err}")
        if s.get("slowest"):
            print("\nGargalos:")
            for g in s["slowest"]:
                print(f"  {g['duration_ms']:>10.1f} ms  {g['name']}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
