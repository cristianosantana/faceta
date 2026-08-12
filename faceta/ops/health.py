from __future__ import annotations

import json
from typing import Any

from faceta.db import SCHEMA, mysql_connect, postgres_connect
from faceta.query.contract import load_contrato
from faceta.trace.core import LOGS_DIR


def healthcheck() -> dict[str, Any]:
    out: dict[str, Any] = {"ok": True, "checks": {}}

    # Contrato
    try:
        c = load_contrato()
        out["checks"]["contrato"] = {
            "ok": True,
            "entity_types": len(c.get("entity_types") or {}),
        }
    except Exception as e:
        out["ok"] = False
        out["checks"]["contrato"] = {"ok": False, "error": str(e)}

    # MySQL
    try:
        mysql = mysql_connect()
        with mysql.cursor() as cur:
            cur.execute("SELECT 1 AS n")
            cur.fetchone()
        mysql.close()
        out["checks"]["mysql"] = {"ok": True}
    except Exception as e:
        out["ok"] = False
        out["checks"]["mysql"] = {"ok": False, "error": str(e)}

    # Postgres + schema
    try:
        with postgres_connect() as pg:
            with pg.cursor() as cur:
                cur.execute("SELECT 1")
                cur.execute(
                    """
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = %s
                    ORDER BY table_name
                    """,
                    (SCHEMA,),
                )
                tables = [r[0] for r in cur.fetchall()]
            required = [
                "fato_os_diario",
                "fato_os_servico_diario",
                "fato_os_pagamento_diario",
                "fato_comissao_diario",
                "dim_funcionario",
                "dim_funcionario_papel",
                "insights",
                "ingest_reconciliacao",
            ]
            missing = [t for t in required if t not in tables]
            out["checks"]["postgres"] = {
                "ok": len(missing) == 0,
                "schema": SCHEMA,
                "n_tables": len(tables),
                "missing": missing,
            }
            if missing:
                out["ok"] = False
    except Exception as e:
        out["ok"] = False
        out["checks"]["postgres"] = {"ok": False, "error": str(e)}

    out["checks"]["logs_dir"] = {
        "ok": True,
        "path": str(LOGS_DIR),
        "exists": LOGS_DIR.is_dir(),
    }
    return out
