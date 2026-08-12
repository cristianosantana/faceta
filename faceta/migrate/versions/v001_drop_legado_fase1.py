"""Migração 001 — drops destrutivos da evolução Fase 1 (antes embutidos em apply_ddl).

Só remove tabelas se detectar schema legado. Após DROP, `apply_ddl` (CREATE IF NOT EXISTS)
recria a estrutura atual; é preciso reingerir os dias afetados.
"""

from __future__ import annotations

import psycopg

from faceta.db import SCHEMA


def up(conn: psycopg.Connection) -> list[str]:
    actions: list[str] = []
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = %s AND table_name = 'fato_comissao_diario'
              AND column_name = 'beneficiario_id'
            """,
            (SCHEMA,),
        )
        if cur.fetchone():
            cur.execute(f"DROP TABLE IF EXISTS {SCHEMA}.fato_comissao_diario CASCADE")
            actions.append("DROP fato_comissao_diario (coluna beneficiario_id legada)")

        cur.execute(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = %s AND table_name = 'fato_os_servico_diario'
              AND column_name = 'servico_id'
            """,
            (SCHEMA,),
        )
        has_servico_id = cur.fetchone()
        cur.execute(
            """
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = %s AND table_name = 'fato_os_servico_diario'
            """,
            (SCHEMA,),
        )
        if cur.fetchone() and not has_servico_id:
            cur.execute(f"DROP TABLE IF EXISTS {SCHEMA}.fato_os_servico_diario CASCADE")
            actions.append("DROP fato_os_servico_diario (sem coluna servico_id)")

        cur.execute(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = %s AND table_name = 'dim_familia_servico'
              AND column_name = 'grupo_servico_id'
            """,
            (SCHEMA,),
        )
        has_grupo = cur.fetchone()
        cur.execute(
            """
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = %s AND table_name = 'dim_familia_servico'
            """,
            (SCHEMA,),
        )
        if cur.fetchone() and not has_grupo:
            cur.execute(f"DROP TABLE IF EXISTS {SCHEMA}.dim_familia_servico CASCADE")
            actions.append("DROP dim_familia_servico (sem grupo_servico_id)")

    conn.commit()
    if not actions:
        actions.append("noop (schema já atual ou tabelas ausentes)")
    return actions
