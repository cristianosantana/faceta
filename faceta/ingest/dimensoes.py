from __future__ import annotations

from faceta.db import SCHEMA, tid

# MySQL origem → Postgres dim_*
# familia_servico / familia_produto = SUBGRUPOS (não grupos_*)
DIM_SPECS = [
    {
        "pg": "dim_departamento",
        "sql": "SELECT id, nome, ativo FROM departamentos",
        "cols": ("id", "nome", "ativo"),
    },
    {
        "pg": "dim_concessionaria",
        "sql": "SELECT id, nome, ativo FROM concessionarias",
        "cols": ("id", "nome", "ativo"),
    },
    {
        "pg": "dim_familia_servico",
        "sql": "SELECT id, nome, grupo_servico_id, ativo FROM subgrupos_servicos",
        "cols": ("id", "nome", "grupo_servico_id", "ativo"),
    },
    {
        "pg": "dim_familia_produto",
        "sql": "SELECT id, nome, grupo_produto_id, ativo FROM subgrupos_produtos",
        "cols": ("id", "nome", "grupo_produto_id", "ativo"),
    },
    {
        "pg": "dim_funcionario",
        "sql": "SELECT id, nome FROM funcionarios",
        "cols": ("id", "nome"),
    },
    {
        "pg": "dim_forma_pagamento",
        "sql": "SELECT id, nome, ativo FROM caixa_tipos",
        "cols": ("id", "nome", "ativo"),
    },
    {
        "pg": "dim_empresa",
        "sql": "SELECT id, nome, ativo FROM empresas",
        "cols": ("id", "nome", "ativo"),
    },
    {
        "pg": "dim_comissao_tipo",
        "sql": "SELECT id, nome, ativo FROM comissao_tipos",
        "cols": ("id", "nome", "ativo"),
    },
    {
        "pg": "dim_servico",
        "sql": (
            "SELECT id, nome, subgrupo_servico_id AS familia_servico_id, ativo FROM servicos"
        ),
        "cols": ("id", "nome", "familia_servico_id", "ativo"),
    },
]


def _row_values(row: dict, cols: tuple[str, ...]) -> tuple:
    out = []
    for c in cols:
        v = row.get(c)
        if c in ("id", "familia_servico_id", "grupo_servico_id", "grupo_produto_id"):
            out.append(tid(v) if v is not None else (None if c != "id" else ""))
        elif c == "nome":
            out.append(v or "")
        elif c == "ativo":
            out.append(bool(v) if v is not None else None)
        else:
            out.append(v)
    return tuple(out)


def sync_dimensoes(mysql, pg) -> dict[str, int]:
    """Cópia enxuta MySQL → Postgres para resolver nomes sem join na origem."""
    counts: dict[str, int] = {}
    with mysql.cursor() as mcur, pg.cursor() as pcur:
        for spec in DIM_SPECS:
            mcur.execute(spec["sql"])
            rows = mcur.fetchall()
            table = f"{SCHEMA}.{spec['pg']}"
            cols = spec["cols"]
            pcur.execute(f"TRUNCATE {table}")
            if not rows:
                counts[spec["pg"]] = 0
                continue
            payload = [_row_values(r, cols) for r in rows]
            col_list = ", ".join(cols)
            placeholders = ", ".join(["%s"] * len(cols))
            pcur.executemany(
                f"""
                INSERT INTO {table} ({col_list}, synced_at)
                VALUES ({placeholders}, NOW())
                """,
                payload,
            )
            counts[spec["pg"]] = len(payload)
    pg.commit()
    return counts
