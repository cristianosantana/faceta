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
        "pg": "dim_indicador",
        "sql": "SELECT id, nome, ativo FROM indicadores",
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

# funcionario → tipos (via cargos). Usado p/ resolver vendedor vs produtivo sem ambiguidade.
PAPEIS_SQL = """
SELECT DISTINCT
  f.id AS funcionario_id,
  ft.id AS tipo_id,
  ft.nome AS tipo_nome
FROM funcionarios f
INNER JOIN funcionario_cargos fc
  ON fc.funcionario_id = f.id AND fc.deleted_at IS NULL
INNER JOIN cargos c
  ON c.id = fc.cargo_id AND c.deleted_at IS NULL
INNER JOIN funcionario_tipos ft
  ON ft.id = c.funcionario_tipo_id
WHERE f.deleted_at IS NULL
  AND ft.id IS NOT NULL
"""


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


def _sync_papeis(mysql_cur, pg_cur) -> int:
    mysql_cur.execute(PAPEIS_SQL)
    rows = mysql_cur.fetchall()
    table = f"{SCHEMA}.dim_funcionario_papel"
    pg_cur.execute(f"TRUNCATE {table}")
    if not rows:
        return 0
    payload = [
        (tid(r["funcionario_id"]), tid(r["tipo_id"]), (r.get("tipo_nome") or "").strip())
        for r in rows
        if r.get("funcionario_id") is not None and r.get("tipo_id") is not None
    ]
    if not payload:
        return 0
    pg_cur.executemany(
        f"""
        INSERT INTO {table} (funcionario_id, tipo_id, tipo_nome, synced_at)
        VALUES (%s, %s, %s, NOW())
        """,
        payload,
    )
    return len(payload)


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
        counts["dim_funcionario_papel"] = _sync_papeis(mcur, pcur)
    pg.commit()
    return counts
