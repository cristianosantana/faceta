from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path

import psycopg
import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "memoria_materializada"


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def mysql_connect():
    load_env()
    required = ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise SystemExit(f"Variáveis MySQL ausentes no .env: {', '.join(missing)}")
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        cursorclass=DictCursor,
        charset="utf8mb4",
    )


@contextmanager
def postgres_connect():
    load_env()
    url = os.getenv("POSTGRES_URL")
    if not url:
        raise SystemExit("POSTGRES_URL ausente no .env")
    with psycopg.connect(url) as conn:
        yield conn


def apply_ddl(conn: psycopg.Connection) -> None:
    sql_dir = Path(__file__).parent / "sql"
    ddl = (sql_dir / "ddl_diario.sql").read_text(encoding="utf-8")
    ddl_cascata = (sql_dir / "ddl_cascata.sql").read_text(encoding="utf-8")
    with conn.cursor() as cur:
        # Migrações destrutivas de schema Fase 1 (reprocessar dias afetados)
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

        cur.execute(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = %s AND table_name = 'fato_os_servico_diario'
              AND column_name = 'servico_id'
            """,
            (SCHEMA,),
        )
        if not cur.fetchone():
            # tabela antiga sem servico_id, ou inexistente
            cur.execute(
                """
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = %s AND table_name = 'fato_os_servico_diario'
                """,
                (SCHEMA,),
            )
            if cur.fetchone():
                cur.execute(f"DROP TABLE IF EXISTS {SCHEMA}.fato_os_servico_diario CASCADE")

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

        cur.execute(ddl)
        cur.execute(ddl_cascata)
    conn.commit()


def tid(value) -> str:
    if value is None:
        return ""
    return str(value)
