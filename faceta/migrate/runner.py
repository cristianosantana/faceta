from __future__ import annotations

from collections.abc import Callable

import psycopg

from faceta.db import SCHEMA
from faceta.migrate.versions import v001_drop_legado_fase1

MigrationFn = Callable[[psycopg.Connection], list[str]]

# Ordem fixa. IDs estáveis — nunca renomear após aplicar em algum ambiente.
MIGRATIONS: list[tuple[str, str, MigrationFn]] = [
    (
        "001_drop_legado_fase1",
        "DROP condicional de tabelas/dims com schema pré-Fase1 (beneficiario_id, "
        "fato_os_servico sem servico_id, dim_familia sem grupo_servico_id).",
        v001_drop_legado_fase1.up,
    ),
]


def _ensure_table(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA}.schema_migrations (
                id TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                note TEXT
            )
            """
        )
    conn.commit()


def applied_ids(conn: psycopg.Connection) -> set[str]:
    _ensure_table(conn)
    with conn.cursor() as cur:
        cur.execute(f"SELECT id FROM {SCHEMA}.schema_migrations")
        return {r[0] for r in cur.fetchall()}


def pending(conn: psycopg.Connection) -> list[tuple[str, str, MigrationFn]]:
    done = applied_ids(conn)
    return [m for m in MIGRATIONS if m[0] not in done]


def status(conn: psycopg.Connection) -> list[dict]:
    done = applied_ids(conn)
    out = []
    for mid, desc, _ in MIGRATIONS:
        out.append({"id": mid, "applied": mid in done, "description": desc})
    return out


def run_up(
    conn: psycopg.Connection, *, dry_run: bool = False
) -> list[dict]:
    """Aplica migrações pendentes na ordem. Retorna log por migração."""
    results: list[dict] = []
    for mid, desc, fn in pending(conn):
        if dry_run:
            results.append({"id": mid, "dry_run": True, "actions": ["(seria aplicada)"]})
            continue
        actions = fn(conn)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO {SCHEMA}.schema_migrations (id, note)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (mid, desc),
            )
        conn.commit()
        results.append({"id": mid, "dry_run": False, "actions": actions})
    return results
