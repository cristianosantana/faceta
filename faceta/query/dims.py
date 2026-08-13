from __future__ import annotations

from faceta.db import SCHEMA
from faceta.query.contract import load_contrato
from faceta.query.engine import ResultadoConsulta
from faceta.query.errors import ConsultaRejeitada

# Fallback quando o contrato não define resolve_dim
DIM_TABLE: dict[str, str] = {
    "concessionaria": "dim_concessionaria",
    "departamento": "dim_departamento",
    "vendedor": "dim_funcionario",
    "produtivo": "dim_funcionario",
    "empresa": "dim_empresa",
    "familia_servico": "dim_familia_servico",
    "servico": "dim_servico",
    "forma_pagamento": "dim_forma_pagamento",
    "comissao_vendedor": "dim_funcionario",
    "comissao_produtivo": "dim_funcionario",
    "comissao_concessionaria": "dim_concessionaria",
    "comissao_indicador": "dim_indicador",
    "comissao_tipo": "dim_comissao_tipo",
}


def _assert_ident(name: str) -> None:
    if not name.replace("_", "").isalnum():
        raise ConsultaRejeitada(f"identificador inválido: {name!r}")


def dim_table_for(dim: str, contrato: dict | None = None) -> str | None:
    """Tabela dim_* para entity_type/quebra: resolve_dim do contrato ou DIM_TABLE."""
    contrato = contrato or load_contrato()
    cfg = (contrato.get("entity_types") or {}).get(dim) or {}
    rd = cfg.get("resolve_dim")
    if rd:
        return str(rd)
    return DIM_TABLE.get(dim)


def nomes_por_ids(pg, dim: str, ids: list[str]) -> dict[str, str]:
    """Resolve id → nome em dim_* para qualquer dimensão do contrato."""
    if not ids:
        return {}
    table = dim_table_for(dim)
    if not table:
        return {}
    _assert_ident(table)
    uniq = list({str(i) for i in ids if i is not None and str(i) != ""})
    if not uniq:
        return {}
    with pg.cursor() as cur:
        cur.execute(
            f"SELECT id, nome FROM {SCHEMA}.{table} WHERE id = ANY(%s)",
            (uniq,),
        )
        return {str(r[0]): (r[1] or "") for r in cur.fetchall()}


def enriquecer_resultado(pg, resultado: ResultadoConsulta) -> ResultadoConsulta:
    """Preenche entity_nome / quebra_nome em todas as linhas."""
    entity_ids = [L.entity_id for L in resultado.linhas]
    mapa_e = nomes_por_ids(pg, resultado.entity_type, entity_ids)

    mapa_q: dict[str, str] = {}
    quebra = getattr(resultado, "quebra", None)
    if quebra:
        qids = [L.quebra_id for L in resultado.linhas if L.quebra_id is not None]
        mapa_q = nomes_por_ids(pg, quebra, qids)

    for L in resultado.linhas:
        L.entity_nome = mapa_e.get(str(L.entity_id)) or L.entity_nome
        if L.quebra_id is not None and mapa_q:
            L.quebra_nome = mapa_q.get(str(L.quebra_id)) or L.quebra_nome
    return resultado
