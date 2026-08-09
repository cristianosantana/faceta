from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

from faceta.db import SCHEMA
from faceta.query.contract import (
    coluna_dimensao,
    load_contrato,
    tabela_fato,
    validar_consulta,
)
from faceta.query.errors import ConsultaRejeitada
from faceta.query.periods import parse_periodo, periodo_referencia


def _assert_ident(name: str) -> None:
    if not name.replace("_", "").isalnum():
        raise ConsultaRejeitada(f"identificador inválido: {name!r}")


@dataclass
class LinhaResultado:
    entity_id: str
    valor: Decimal
    ranking: int | None = None
    participacao_pct: float | None = None
    quebra_id: str | None = None
    valor_anterior: Decimal | None = None
    variacao_pct: float | None = None


@dataclass
class ResultadoConsulta:
    entity_type: str
    granularidade: str
    periodo: Any
    tabela: str
    fato: str
    linhas: list[LinhaResultado]
    comparacao: str | None = None
    periodo_referencia: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "granularidade": self.granularidade,
            "periodo": self.periodo.isoformat(),
            "tabela": self.tabela,
            "fato": self.fato,
            "comparacao": self.comparacao,
            "periodo_referencia": (
                self.periodo_referencia.isoformat() if self.periodo_referencia else None
            ),
            "linhas": [
                {
                    **{k: (str(v) if isinstance(v, Decimal) else v) for k, v in asdict(L).items()}
                }
                for L in self.linhas
            ],
        }


def consultar(
    pg,
    *,
    entity_type: str,
    granularidade: str,
    periodo: str,
    entity_id: str | None = None,
    quebra: str | None = None,
    quebra_valor: str | None = None,
    comparacao: str | None = None,
    ranking: bool = False,
    contrato: dict[str, Any] | None = None,
) -> ResultadoConsulta:
    contrato = contrato or load_contrato()
    cfg = validar_consulta(
        contrato,
        entity_type=entity_type,
        granularidade=granularidade,
        quebra=quebra,
        comparacao=comparacao,
    )
    if quebra_valor is not None and quebra is None:
        raise ConsultaRejeitada("quebra_valor sem quebra")

    inicio = parse_periodo(periodo, granularidade)
    table = tabela_fato(cfg, granularidade)
    col_entity = coluna_dimensao(entity_type)
    col_valor = cfg["valor"]
    for ident in (table, col_entity, col_valor):
        _assert_ident(ident)

    col_quebra = None
    if quebra:
        col_quebra = coluna_dimensao(quebra)
        _assert_ident(col_quebra)

    want_rank = ranking or entity_id is None
    linhas = _agregar(
        pg,
        table=table,
        col_entity=col_entity,
        col_valor=col_valor,
        data=inicio,
        entity_id=entity_id,
        col_quebra=col_quebra,
        quebra_valor=quebra_valor,
        with_rank=want_rank,
    )

    ref_inicio = None
    if comparacao:
        ref_inicio = periodo_referencia(inicio, granularidade, comparacao)
        antigas = _agregar(
            pg,
            table=table,
            col_entity=col_entity,
            col_valor=col_valor,
            data=ref_inicio,
            entity_id=entity_id,
            col_quebra=col_quebra,
            quebra_valor=quebra_valor,
            with_rank=False,
        )
        mapa = {(r.entity_id, r.quebra_id): r.valor for r in antigas}
        for r in linhas:
            prev = mapa.get((r.entity_id, r.quebra_id))
            r.valor_anterior = prev
            if prev is not None and prev != 0:
                r.variacao_pct = float((r.valor - prev) / prev * 100)

    return ResultadoConsulta(
        entity_type=entity_type,
        granularidade=granularidade,
        periodo=inicio,
        tabela=table,
        fato=cfg["fato"],
        linhas=linhas,
        comparacao=comparacao,
        periodo_referencia=ref_inicio,
    )


def _agregar(
    pg,
    *,
    table: str,
    col_entity: str,
    col_valor: str,
    data,
    entity_id: str | None,
    col_quebra: str | None,
    quebra_valor: str | None,
    with_rank: bool,
) -> list[LinhaResultado]:
    where = ["data = %s"]
    params: list[Any] = [data]
    if entity_id is not None:
        where.append(f"{col_entity} = %s")
        params.append(entity_id)
    if col_quebra is not None and quebra_valor is not None:
        where.append(f"{col_quebra} = %s")
        params.append(quebra_valor)

    group = [col_entity]
    has_quebra_col = col_quebra is not None and quebra_valor is None
    # se quebra_valor fixo, ainda podemos projetar a coluna no SELECT via GROUP
    if col_quebra is not None:
        group.append(col_quebra)
        has_quebra_col = True

    where_sql = " AND ".join(where)
    group_sql = ", ".join(group)
    quebra_select = f", {col_quebra} AS quebra_id" if has_quebra_col else ""

    if with_rank:
        sql = f"""
        WITH base AS (
            SELECT {col_entity} AS entity_id{quebra_select},
                   SUM({col_valor}) AS valor
            FROM {SCHEMA}.{table}
            WHERE {where_sql}
            GROUP BY {group_sql}
        ),
        tot AS (SELECT COALESCE(SUM(valor), 0) AS total FROM base)
        SELECT
            b.entity_id,
            b.valor,
            {"b.quebra_id," if has_quebra_col else ""}
            RANK() OVER (ORDER BY b.valor DESC) AS ranking,
            CASE WHEN t.total = 0 THEN 0
                 ELSE ROUND((b.valor * 100.0 / t.total)::numeric, 4)
            END AS participacao_pct
        FROM base b
        CROSS JOIN tot t
        ORDER BY b.valor DESC, b.entity_id
        """
    else:
        sql = f"""
        SELECT {col_entity} AS entity_id{quebra_select},
               SUM({col_valor}) AS valor
        FROM {SCHEMA}.{table}
        WHERE {where_sql}
        GROUP BY {group_sql}
        ORDER BY valor DESC, entity_id
        """

    with pg.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    out: list[LinhaResultado] = []
    for row in rows:
        if with_rank:
            if has_quebra_col:
                eid, valor, qid, rank, pct = row[0], row[1], row[2], row[3], row[4]
            else:
                eid, valor, rank, pct = row[0], row[1], row[2], row[3]
                qid = None
            out.append(
                LinhaResultado(
                    entity_id=str(eid),
                    valor=Decimal(valor),
                    ranking=int(rank),
                    participacao_pct=float(pct),
                    quebra_id=str(qid) if qid is not None else None,
                )
            )
        else:
            if has_quebra_col:
                eid, qid, valor = row[0], row[1], row[2]
            else:
                eid, valor = row[0], row[1]
                qid = None
            out.append(
                LinhaResultado(
                    entity_id=str(eid),
                    valor=Decimal(valor),
                    quebra_id=str(qid) if qid is not None else None,
                )
            )
    return out
