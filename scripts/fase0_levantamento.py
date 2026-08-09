#!/usr/bin/env python3
"""Fase 0 — introspecção live do MySQL smart + relatório Markdown."""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pymysql
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "documentos" / "12-levantamento-fase-0.md"

TABLES = [
    "departamentos",
    "concessionarias",
    "grupos_servicos",
    "funcionarios",
    "funcionario_tipos",
    "funcionario_cargos",
    "cargos",
    "caixa_tipos",
    "empresas",
    "os",
    "os_servicos",
    "os_produtos",
    "servicos",
    "caixas",
    "caixas_pendentes",
    "comissoes",
    "comissao_tipos",
    "comissao_periodos",
    "comissao_pagamentos",
]

REQUIRED_COLUMNS = {
    "departamentos": ["id", "nome"],
    "concessionarias": ["id", "nome"],
    "grupos_servicos": ["id", "nome"],
    "funcionarios": ["id", "nome"],
    "funcionario_tipos": ["id", "nome"],
    "funcionario_cargos": ["funcionario_id", "cargo_id"],
    "cargos": ["id", "funcionario_tipo_id"],
    "caixa_tipos": ["id", "nome"],
    "empresas": ["id", "nome"],
    "os": [
        "id",
        "created_at",
        "vendedor_id",
        "concessionaria_id",
        "departamento_id",
        "paga",
        "data_pagamento",
        "fechada",
        "data_fechamento",
        "finalizada",
        "data_finalizacao",
        "valor_bruto",
        "valor_liquido",
    ],
    "os_servicos": [
        "id",
        "os_id",
        "servico_id",
        "produtivo_id",
        "valor_venda_real",
        "fechado",
        "data_fechamento",
    ],
    "os_produtos": ["id", "os_id", "produto_id"],
    "servicos": ["id", "nome", "grupo_servico_id"],
    "caixas": ["id", "os_id", "caixa_tipo_id", "valor"],
    "caixas_pendentes": ["id", "os_id", "valor"],
    "comissoes": [
        "id",
        "comissionado_id",
        "comissao_tipo_id",
        "os_servico_id",
        "os_produto_id",
        "valor_dentro",
        "valor_fora",
        "valor_combo",
        "valor_compensado_permuta",
        "comissao_couro",
        "created_at",
    ],
    "comissao_tipos": ["id", "nome"],
    "comissao_periodos": ["id", "nome"],
    "comissao_pagamentos": ["id", "funcionario_id", "comissao_tipo_id"],
}

COMISSAO_VALOR_COLS = [
    "valor_dentro",
    "valor_fora",
    "valor_combo",
    "valor_compensado_permuta",
    "comissao_couro",
]

LOOKBACK_DAYS = 14
FORMULA = (
    "COALESCE(valor_dentro,0) + COALESCE(valor_fora,0) + COALESCE(valor_combo,0) "
    "+ COALESCE(valor_compensado_permuta,0) + COALESCE(comissao_couro,0)"
)

# OS fechada derivada: itens ativos todos fechados em os_servicos XOR os_produtos
SQL_FECHADA_DERIVADA = """
(
  (
    EXISTS (
      SELECT 1 FROM os_servicos s
      WHERE s.os_id = o.id
        AND IFNULL(s.cancelado, 0) <> 1
        AND s.deleted_at IS NULL
    )
    AND NOT EXISTS (
      SELECT 1 FROM os_servicos s
      WHERE s.os_id = o.id
        AND IFNULL(s.cancelado, 0) <> 1
        AND s.deleted_at IS NULL
        AND IFNULL(s.fechado, 0) <> 1
    )
    AND NOT EXISTS (
      SELECT 1 FROM os_produtos p
      WHERE p.os_id = o.id
        AND IFNULL(p.cancelado, 0) <> 1
        AND p.deleted_at IS NULL
    )
  )
  OR
  (
    EXISTS (
      SELECT 1 FROM os_produtos p
      WHERE p.os_id = o.id
        AND IFNULL(p.cancelado, 0) <> 1
        AND p.deleted_at IS NULL
    )
    AND NOT EXISTS (
      SELECT 1 FROM os_produtos p
      WHERE p.os_id = o.id
        AND IFNULL(p.cancelado, 0) <> 1
        AND p.deleted_at IS NULL
        AND IFNULL(p.fechado, 0) <> 1
    )
    AND NOT EXISTS (
      SELECT 1 FROM os_servicos s
      WHERE s.os_id = o.id
        AND IFNULL(s.cancelado, 0) <> 1
        AND s.deleted_at IS NULL
    )
  )
)
"""


def log(msg: str) -> None:
    print(msg, flush=True)


def connect():
    load_dotenv(ROOT / ".env")
    required = ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise SystemExit(f"Variáveis ausentes no .env: {', '.join(missing)}")
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        read_timeout=120,
        write_timeout=120,
    )


def fetch_all(cur, sql, params=None):
    cur.execute(sql, params or ())
    return cur.fetchall()


def fetch_one(cur, sql, params=None):
    cur.execute(sql, params or ())
    return cur.fetchone()


def introspect_columns(cur, database: str) -> dict[str, list[dict]]:
    rows = fetch_all(
        cur,
        """
        SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME IN ({placeholders})
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """.format(placeholders=",".join(["%s"] * len(TABLES))),
        [database, *TABLES],
    )
    by_table: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_table[r["TABLE_NAME"]].append(r)
    return by_table


def check_required(by_table: dict[str, list[dict]]) -> list[str]:
    errors = []
    for table, cols in REQUIRED_COLUMNS.items():
        if table not in by_table or not by_table[table]:
            errors.append(f"Tabela essencial ausente: {table}")
            continue
        present = {c["COLUMN_NAME"] for c in by_table[table]}
        for col in cols:
            if col not in present:
                errors.append(f"Coluna essencial ausente: {table}.{col}")
    return errors


def sample_dim_safe(cur, table: str, limit: int = 10) -> list[dict]:
    cols = {r["COLUMN_NAME"] for r in fetch_all(
        cur,
        """
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
        """,
        (table,),
    )}
    where = "WHERE deleted_at IS NULL" if "deleted_at" in cols else ""
    return fetch_all(cur, f"SELECT id, nome FROM `{table}` {where} ORDER BY id LIMIT %s", (limit,))


def fmt_val(v):
    if isinstance(v, Decimal):
        return f"{v:.4f}".rstrip("0").rstrip(".")
    if isinstance(v, datetime):
        return v.isoformat(sep=" ", timespec="seconds")
    if isinstance(v, date):
        return v.isoformat()
    return str(v)


def md_table(headers: list[str], rows: list[list]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt_val(c) if c is not None else "" for c in row) + " |")
    return "\n".join(lines)


def columns_md(cols: list[dict]) -> str:
    rows = [
        [c["COLUMN_NAME"], c["COLUMN_TYPE"], c["IS_NULLABLE"], c["COLUMN_KEY"] or ""]
        for c in cols
    ]
    return md_table(["coluna", "tipo", "nullable", "key"], rows)


def has_column(by_table: dict[str, list[dict]], table: str, col: str) -> bool:
    return any(c["COLUMN_NAME"] == col for c in by_table.get(table, []))


def main() -> int:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    since = (date.today() - timedelta(days=LOOKBACK_DAYS)).isoformat()
    blocking_errors: list[str] = []
    findings: list[str] = []

    try:
        conn = connect()
    except Exception as e:
        print(f"Falha de conexão MySQL: {e}", file=sys.stderr)
        return 1

    database = os.environ["MYSQL_DATABASE"]
    sections: list[str] = []

    with conn:
        with conn.cursor() as cur:
            log("1/7 INFORMATION_SCHEMA…")
            by_table = introspect_columns(cur, database)
            blocking_errors.extend(check_required(by_table))

            sections.append("# Levantamento Fase 0 — MySQL `smart`\n")
            sections.append(f"> Gerado em `{generated_at}` por `scripts/fase0_levantamento.py`.\n")
            sections.append("## 1. Conclusões (Fase 0)\n")
            conclusions_idx = len(sections)
            sections.append("")

            sections.append("## 2. Schema introspectado\n")
            for table in TABLES:
                cols = by_table.get(table, [])
                if not cols:
                    sections.append(f"### `{table}`\n\n**AUSENTE**\n")
                    continue
                sections.append(f"### `{table}`\n\n{columns_md(cols)}\n")

            sections.append("## 3. Mapeamento origem → Faceta (confirmado no live)\n")
            map_rows = [
                ["departamento", "departamentos", "id, nome", "—"],
                ["concessionaria", "concessionarias", "id, nome", "extras ignorados na ingestão"],
                ["familia_servico", "grupos_servicos", "id, nome", "via servicos.grupo_servico_id"],
                ["vendedor", "funcionarios", "id, nome", "os.vendedor_id; tipo via funcionario_tipos"],
                ["produtivo", "funcionarios", "id, nome", "os_servicos.produtivo_id; tipo via funcionario_tipos"],
                ["funcionario_tipos", "funcionario_tipos", "id, nome", "cadeia funcionario_cargos → cargos.funcionario_tipo_id"],
                ["forma_pagamento", "caixa_tipos", "id, nome", "via caixas.caixa_tipo_id"],
                ["empresa", "empresas", "id, nome", "—"],
                ["fato_os", "os", "flags + FKs + valores", "grão cabeçalho"],
                ["fato_os_servico", "os_servicos", "os_id, servico_id, produtivo_id, valores", "—"],
                ["fato_os_pagamento", "caixas", "os_id, valor, caixa_tipo_id", "caixas_pendentes ≠ prova de paga"],
                ["fato_comissao", "comissoes", "comissionado_id, comissao_tipo_id, valores", "satélites comissao_*"],
            ]
            sections.append(
                md_table(["conceito Faceta", "tabela MySQL", "colunas-chave", "obs"], map_rows) + "\n"
            )

            log("2/7 amostras de dimensões…")
            sections.append("## 4. Amostras de dimensões e tipos\n")
            for table in [
                "departamentos",
                "concessionarias",
                "grupos_servicos",
                "caixa_tipos",
                "empresas",
                "funcionario_tipos",
                "comissao_tipos",
            ]:
                try:
                    rows = sample_dim_safe(cur, table, 10)
                    sections.append(
                        f"### `{table}`\n\n"
                        + md_table(["id", "nome"], [[r["id"], r["nome"]] for r in rows])
                        + "\n"
                    )
                except Exception as e:
                    findings.append(f"Amostra `{table}` falhou: {e}")
                    sections.append(f"### `{table}`\n\nErro: `{e}`\n")

            tipo_rows = fetch_all(
                cur,
                """
                SELECT ft.id, ft.nome, COUNT(DISTINCT fc.funcionario_id) AS funcionarios
                FROM funcionario_tipos ft
                LEFT JOIN cargos c ON c.funcionario_tipo_id = ft.id
                LEFT JOIN funcionario_cargos fc ON fc.cargo_id = c.id
                GROUP BY ft.id, ft.nome
                ORDER BY ft.id
                """,
            )
            sections.append(
                "### Cadeia funcionario_tipos → cargos → funcionario_cargos\n\n"
                + md_table(
                    ["funcionario_tipo_id", "nome", "funcionarios_distintos"],
                    [[r["id"], r["nome"], r["funcionarios"]] for r in tipo_rows],
                )
                + "\n"
            )

            log("3/7 contagens de estado da OS…")
            sections.append(f"## 5. Estados da OS (últimos {LOOKBACK_DAYS} dias)\n")
            sections.append(
                "Critérios de negócio (Faceta — **não** usar `os.finalizada` como paga∩fechada):\n"
                "- **Abertas:** `DATE(created_at)`\n"
                "- **Pagas:** `os.paga = 1` **e** ≥1 linha em `caixas` (`caixas_pendentes` não conta)\n"
                "- **Fechadas (derivadas):** itens ativos (`cancelado <> 1`) todos com `fechado = 1` "
                "em `os_servicos` **ou** (exclusivo) `os_produtos`\n"
                "- **Canceladas:** `os.cancelada = 1`\n"
                "- **Paga sem caixa (inconsistência, não cancelada):** `os.paga = 1` **e** zero `caixas`\n"
            )

            cx_del = "AND c.deleted_at IS NULL" if has_column(by_table, "caixas", "deleted_at") else ""
            sql_tem_caixa = f"""
EXISTS (
  SELECT 1 FROM caixas c
  WHERE c.os_id = o.id {cx_del}
  LIMIT 1
)
"""

            abertas = fetch_all(
                cur,
                """
                SELECT DATE(created_at) AS dia, COUNT(*) AS n
                FROM os
                WHERE deleted_at IS NULL AND created_at >= %s
                GROUP BY DATE(created_at)
                ORDER BY dia
                """,
                (since,),
            )
            pagas = fetch_all(
                cur,
                f"""
                SELECT DATE(o.data_pagamento) AS dia, COUNT(*) AS n
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND o.paga = 1
                  AND o.data_pagamento >= %s
                  AND {sql_tem_caixa}
                GROUP BY DATE(o.data_pagamento)
                ORDER BY dia
                """,
                (since,),
            )
            fechadas = fetch_all(
                cur,
                f"""
                SELECT DATE(COALESCE(o.data_fechamento, o.updated_at)) AS dia, COUNT(*) AS n
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND COALESCE(o.data_fechamento, o.updated_at) >= %s
                  AND {SQL_FECHADA_DERIVADA}
                GROUP BY DATE(COALESCE(o.data_fechamento, o.updated_at))
                ORDER BY dia
                """,
                (since,),
            )
            canceladas = fetch_all(
                cur,
                """
                SELECT DATE(COALESCE(o.data_cancelamento, o.updated_at)) AS dia, COUNT(*) AS n
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND o.cancelada = 1
                  AND COALESCE(o.data_cancelamento, o.updated_at) >= %s
                GROUP BY DATE(COALESCE(o.data_cancelamento, o.updated_at))
                ORDER BY dia
                """,
                (since,),
            )
            paga_sem_caixa = fetch_all(
                cur,
                f"""
                SELECT DATE(COALESCE(o.data_pagamento, o.updated_at)) AS dia, COUNT(*) AS n
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND o.paga = 1
                  AND COALESCE(o.data_pagamento, o.updated_at) >= %s
                  AND NOT ({sql_tem_caixa})
                GROUP BY DATE(COALESCE(o.data_pagamento, o.updated_at))
                ORDER BY dia
                """,
                (since,),
            )

            by_day: dict[str, dict[str, int]] = defaultdict(lambda: {
                "abertas": 0, "pagas": 0, "fechadas": 0, "canceladas": 0, "paga_sem_caixa": 0
            })
            for label, rows in [
                ("abertas", abertas),
                ("pagas", pagas),
                ("fechadas", fechadas),
                ("canceladas", canceladas),
                ("paga_sem_caixa", paga_sem_caixa),
            ]:
                for r in rows:
                    if r["dia"] is None:
                        continue
                    by_day[str(r["dia"])][label] = int(r["n"])

            if by_day:
                sections.append(
                    md_table(
                        ["dia", "abertas", "pagas", "fechadas_deriv", "canceladas", "paga_sem_caixa"],
                        [
                            [
                                d,
                                v["abertas"],
                                v["pagas"],
                                v["fechadas"],
                                v["canceladas"],
                                v["paga_sem_caixa"],
                            ]
                            for d, v in sorted(by_day.items())
                        ],
                    )
                    + "\n"
                )
            else:
                sections.append("_Sem linhas no período._\n")

            log("4/7 divergências / inconsistências…")
            div_fechada = fetch_one(
                cur,
                f"""
                SELECT COUNT(*) AS n
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND COALESCE(o.data_fechamento, o.updated_at) >= %s
                  AND (
                    (IFNULL(o.fechada, 0) = 1 AND NOT ({SQL_FECHADA_DERIVADA}))
                    OR (IFNULL(o.fechada, 0) <> 1 AND ({SQL_FECHADA_DERIVADA}))
                  )
                """,
                (since,),
            )
            div_fechada_n = int(div_fechada["n"]) if div_fechada else 0

            paga_sem = fetch_one(
                cur,
                f"""
                SELECT
                  COUNT(*) AS n,
                  SUM(CASE WHEN IFNULL(o.fechada, 0) = 1 THEN 1 ELSE 0 END) AS com_fechada,
                  SUM(CASE WHEN IFNULL(o.cancelada, 0) = 1 THEN 1 ELSE 0 END) AS com_cancelada
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND COALESCE(o.data_pagamento, o.updated_at) >= %s
                  AND o.paga = 1
                  AND NOT ({sql_tem_caixa})
                """,
                (since,),
            )
            paga_sem_n = int(paga_sem["n"]) if paga_sem else 0
            paga_sem_fechada_n = int(paga_sem["com_fechada"] or 0) if paga_sem else 0
            paga_sem_cancelada_n = int(paga_sem["com_cancelada"] or 0) if paga_sem else 0

            exclusividade = fetch_one(
                cur,
                """
                SELECT COUNT(*) AS n
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND o.created_at >= %s
                  AND EXISTS (
                    SELECT 1 FROM os_servicos s
                    WHERE s.os_id = o.id AND IFNULL(s.cancelado, 0) <> 1 AND s.deleted_at IS NULL
                  )
                  AND EXISTS (
                    SELECT 1 FROM os_produtos p
                    WHERE p.os_id = o.id AND IFNULL(p.cancelado, 0) <> 1 AND p.deleted_at IS NULL
                  )
                """,
                (since,),
            )
            exclusividade_n = int(exclusividade["n"]) if exclusividade else 0

            if div_fechada_n:
                findings.append(
                    f"Divergência `os.fechada` vs fechada derivada: {div_fechada_n} OS "
                    f"(últimos {LOOKBACK_DAYS} dias)."
                )
            if paga_sem_n:
                findings.append(
                    f"Inconsistência `paga=1` sem `caixas`: {paga_sem_n} OS "
                    f"({paga_sem_fechada_n} com `os.fechada=1`, {paga_sem_cancelada_n} com "
                    f"`os.cancelada=1`) — não tratar como cancelada."
                )
            if exclusividade_n:
                findings.append(
                    f"Exclusividade violada (itens ativos em `os_servicos` e `os_produtos`): "
                    f"{exclusividade_n} OS criadas no período."
                )

            sections.append(
                "### Checagens vs flags / inconsistências\n\n"
                + md_table(
                    ["checagem", "contagem"],
                    [
                        ["divergência os.fechada ↔ fechada derivada", div_fechada_n],
                        ["paga=1 sem caixas (inconsistência)", paga_sem_n],
                        ["… dessas com os.fechada=1", paga_sem_fechada_n],
                        ["… dessas com os.cancelada=1", paga_sem_cancelada_n],
                        ["itens ativos em os_servicos E os_produtos", exclusividade_n],
                    ],
                )
                + "\n"
            )

            log("5/7 alinhamento comissão × fechamento…")
            sections.append("## 6. Comissão — schema, momento e fórmula\n")
            sections.append(
                "### Regras de negócio\n\n"
                "- Comissão **geral** gerada no **pagamento** → OS fechada sem comissão é esperado.\n"
                "- **Exceção produtivo:** comissão gerada ao **fechar serviços/itens**.\n"
                "- Ingestão de `fato_comissao` lê `comissoes` materializadas; não assume 1:1 com fechada derivada.\n"
            )

            fechadas_sem = fetch_one(
                cur,
                f"""
                SELECT COUNT(*) AS n
                FROM os o
                WHERE o.deleted_at IS NULL
                  AND COALESCE(o.data_fechamento, o.updated_at) >= %s
                  AND {SQL_FECHADA_DERIVADA}
                  AND NOT EXISTS (
                    SELECT 1
                    FROM os_servicos oss
                    INNER JOIN comissoes cm
                      ON cm.os_servico_id = oss.id AND cm.deleted_at IS NULL
                    WHERE oss.os_id = o.id
                    LIMIT 1
                  )
                  AND NOT EXISTS (
                    SELECT 1
                    FROM os_produtos osp
                    INNER JOIN comissoes cm
                      ON cm.os_produto_id = osp.id AND cm.deleted_at IS NULL
                    WHERE osp.os_id = o.id
                    LIMIT 1
                  )
                """,
                (since,),
            )
            fechadas_sem_n = int(fechadas_sem["n"]) if fechadas_sem else 0
            sections.append(
                f"**OS fechadas (derivadas) sem comissão ligada (últimos {LOOKBACK_DAYS} dias):** "
                f"`{fechadas_sem_n}` (esperado pela regra de pagamento).\n"
            )

            log("6/7 breakdown de comissões…")
            comissao_por_tipo = fetch_all(
                cur,
                f"""
                SELECT
                  COALESCE(ft.nome, '(sem tipo / cargo)') AS beneficiario_tipo,
                  ct.nome AS tipo_comissao,
                  COUNT(*) AS qtd,
                  SUM({FORMULA}) AS valor_total
                FROM comissoes cm
                LEFT JOIN comissao_tipos ct ON ct.id = cm.comissao_tipo_id
                LEFT JOIN (
                  SELECT fc.funcionario_id, MIN(cg.funcionario_tipo_id) AS funcionario_tipo_id
                  FROM funcionario_cargos fc
                  INNER JOIN cargos cg ON cg.id = fc.cargo_id
                  WHERE IFNULL(fc.ativo, 1) = 1
                    AND fc.deleted_at IS NULL
                  GROUP BY fc.funcionario_id
                ) fmap ON fmap.funcionario_id = cm.comissionado_id
                LEFT JOIN funcionario_tipos ft ON ft.id = fmap.funcionario_tipo_id
                WHERE cm.deleted_at IS NULL
                  AND cm.created_at >= %s
                GROUP BY COALESCE(ft.nome, '(sem tipo / cargo)'), ct.nome
                ORDER BY qtd DESC
                LIMIT 40
                """,
                (since,),
            )
            sections.append(
                "### Comissões recentes por tipo de funcionário × tipo de comissão\n\n"
                + (
                    md_table(
                        ["beneficiario_tipo", "tipo_comissao", "qtd", "valor_total"],
                        [
                            [
                                r["beneficiario_tipo"],
                                r["tipo_comissao"],
                                r["qtd"],
                                r["valor_total"],
                            ]
                            for r in comissao_por_tipo
                        ],
                    )
                    if comissao_por_tipo
                    else "_Sem comissões no período._"
                )
                + "\n"
            )

            log("7/7 componentes de valor + fórmula…")
            total_cm = fetch_one(
                cur,
                "SELECT COUNT(*) AS n FROM comissoes WHERE deleted_at IS NULL AND created_at >= %s",
                (since,),
            )
            total_n = int(total_cm["n"]) if total_cm else 0
            null_rows = []
            for col in COMISSAO_VALOR_COLS:
                r = fetch_one(
                    cur,
                    f"""
                    SELECT
                      SUM(CASE WHEN `{col}` IS NULL THEN 1 ELSE 0 END) AS nulos,
                      SUM(CASE WHEN `{col}` IS NOT NULL AND `{col}` <> 0 THEN 1 ELSE 0 END) AS nao_zero
                    FROM comissoes
                    WHERE deleted_at IS NULL AND created_at >= %s
                    """,
                    (since,),
                )
                null_rows.append([col, r["nulos"] or 0, r["nao_zero"] or 0, total_n])
            sections.append(
                "### Componentes de valor em `comissoes`\n\n"
                + md_table(["coluna", "nulos", "não-zero", "total_periodo"], null_rows)
                + "\n"
            )

            formula_display = f"valor_comissao = {FORMULA}"
            sections.append(
                "### Fórmula fixada para `fato_comissao.valor_comissao`\n\n"
                f"`{formula_display}`\n\n"
                "- `beneficiario_id` ← `comissoes.comissionado_id`\n"
                "- `beneficiario_tipo` ← `funcionario_tipos.nome` via cargo ativo do comissionado\n"
                "- `tipo_comissao` ← preferir `comissao_tipos.id` estável na ingestão; nome via dimensão/join\n"
                "- Data sugerida do fato: `DATE(comissoes.created_at)` "
                "(geração no pagamento ou no fechamento do serviço do produtivo)\n"
            )

            sections.append("## 7. Frequência de leitura (recomendação)\n")
            sections.append(
                "Não há um único “dia fechado” global. A ingestão diária deve filtrar por **recorte**:\n\n"
                "| Recorte / família | Quando ler o dia D | Filtro |\n"
                "|---|---|---|\n"
                "| Abertas / `fato_os` (criação) | D+1 | `DATE(os.created_at) = D` |\n"
                "| Pagas / pagamentos | D+1 | `os.paga = 1` + existe `caixas`, `DATE(data_pagamento) = D` |\n"
                "| Fechadas / itens | D+1 | fechada derivada (itens ativos todos `fechado`); preferir não confiar só em `os.fechada` |\n"
                "| Canceladas | D+1 | `os.cancelada = 1`, `DATE(data_cancelamento) = D` |\n"
                "| Paga sem caixa | D+1 | inconsistência de origem (`paga=1` sem `caixas`); não ingerir como cancelada |\n"
                "| Comissão (geral) | D+1 após pagamentos | `comissoes` do dia; aceitar OS fechada sem comissão |\n"
                "| Comissão (produtivo) | D+1 após fechamento de itens | pode existir antes do pagamento |\n\n"
                "Cadência sugerida: **um job diário após 00:30** processando o dia D−1 "
                "para todos os recortes, sem bloquear comissão na ausência de pagamento.\n"
            )

            if findings:
                sections.append("## 8. Achados / riscos\n")
                for f in findings:
                    sections.append(f"- {f}\n")

            ok_schema = not blocking_errors
            conclusions = [
                f"- **Schema cadastral:** {'validado no live' if ok_schema else 'BLOQUEADO — ver erros abaixo'}.",
                "- **Comissão:** origem `comissoes` (+ `comissao_tipos`, `comissao_periodos`, `comissao_pagamentos`); "
                f"fórmula `{formula_display}`.",
                "- **Vendedor/produtivo:** `funcionarios` discriminados por `funcionario_tipos` "
                "(via `funcionario_cargos` → `cargos`).",
                "- **Estados:** paga = `paga`+`caixas`; fechada = itens ativos todos fechados "
                "(`os_servicos` XOR `os_produtos`); cancelada = `os.cancelada`; "
                "`paga=1` sem `caixas` = inconsistência (não cancelada); "
                "`os.finalizada` não é critério analítico.",
                f"- **Frequência:** ingestão diária do dia D−1 por recorte; "
                f"OS fechadas (derivadas) sem comissão no período: `{fechadas_sem_n}`.",
                f"- **Divergências/inconsistências:** fechada flag↔derivada `{div_fechada_n}`; "
                f"paga sem caixa `{paga_sem_n}` (fechada `{paga_sem_fechada_n}`); "
                f"exclusividade `{exclusividade_n}`.",
            ]
            if blocking_errors:
                conclusions.append("- **Erros bloqueantes:**")
                conclusions.extend(f"  - {e}" for e in blocking_errors)
            sections[conclusions_idx] = "\n".join(conclusions) + "\n"

    REPORT_PATH.write_text("\n".join(sections), encoding="utf-8")
    log(f"Relatório escrito em {REPORT_PATH}")
    if blocking_errors:
        print("Erros bloqueantes:", file=sys.stderr)
        for e in blocking_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    if findings:
        log("Achados (não bloqueantes):")
        for f in findings:
            log(f"  - {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
