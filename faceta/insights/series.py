from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from faceta.db import SCHEMA
from faceta.query.contract import coluna_dimensao, load_contrato, tabela_fato
from faceta.query.errors import ConsultaRejeitada
from faceta.query.maps import GRANULARIDADE_SUFIXO


@dataclass
class PontoSerie:
    data: date
    valor: float


@dataclass
class SerieEntity:
    entity_id: str
    pontos: list[PontoSerie]

    def valores(self) -> list[float]:
        return [p.valor for p in self.pontos]


def carregar_series(
    pg,
    *,
    entity_type: str,
    granularidade: str,
    contrato=None,
) -> list[SerieEntity]:
    """US15: reconstrói séries por entity_id a partir da tabela de fato da granularidade."""
    if granularidade not in GRANULARIDADE_SUFIXO:
        raise ConsultaRejeitada(f"granularidade inválida: {granularidade}")
    contrato = contrato or load_contrato()
    if entity_type not in contrato["entity_types"]:
        raise ConsultaRejeitada(f"entity_type não previsto: {entity_type}")
    cfg = contrato["entity_types"][entity_type]
    table = tabela_fato(cfg, granularidade)
    col = coluna_dimensao(entity_type)
    valor = cfg["valor"]
    for ident in (table, col, valor):
        if not ident.replace("_", "").isalnum():
            raise ConsultaRejeitada(f"ident inválido: {ident}")

    sql = f"""
    SELECT data, {col} AS entity_id, SUM({valor}) AS valor
    FROM {SCHEMA}.{table}
    GROUP BY data, {col}
    ORDER BY {col}, data
    """
    with pg.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    by_id: dict[str, list[PontoSerie]] = {}
    for data, eid, valor_v in rows:
        by_id.setdefault(str(eid), []).append(
            PontoSerie(data=data, valor=float(Decimal(valor_v)))
        )
    return [SerieEntity(entity_id=k, pontos=v) for k, v in by_id.items()]
