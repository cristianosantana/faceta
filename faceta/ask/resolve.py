from __future__ import annotations

from faceta.ask.understand import ParametrosPergunta
from faceta.query.dims import DIM_TABLE, nomes_por_ids
from faceta.query.errors import ConsultaRejeitada
from faceta.db import SCHEMA


def resolver_nome(pg, dim: str, nome: str) -> str:
    table = DIM_TABLE.get(dim)
    if not table:
        raise ConsultaRejeitada(f"sem dim_* para resolver nome de '{dim}'")
    if not table.replace("_", "").isalnum():
        raise ConsultaRejeitada(f"dim inválida: {table}")

    with pg.cursor() as cur:
        cur.execute(
            f"""
            SELECT id, nome FROM {SCHEMA}.{table}
            WHERE nome ILIKE %s
            ORDER BY length(nome), id
            LIMIT 5
            """,
            (f"%{nome.strip()}%",),
        )
        rows = cur.fetchall()

    if not rows:
        raise ConsultaRejeitada(f"nenhuma entidade '{dim}' com nome parecido com {nome!r}")
    if len(rows) > 1:
        exact = [r for r in rows if str(r[1]).lower() == nome.strip().lower()]
        if len(exact) == 1:
            return str(exact[0][0])
        opts = ", ".join(f"{r[0]}={r[1]}" for r in rows)
        raise ConsultaRejeitada(
            f"nome ambíguo para '{dim}' ({nome!r}); candidatos: {opts}"
        )
    return str(rows[0][0])


def aplicar_resolucao(pg, params: ParametrosPergunta) -> ParametrosPergunta:
    entity_id = params.entity_id
    entity_nome = params.entity_nome
    if entity_id is None and entity_nome:
        entity_id = resolver_nome(pg, params.entity_type, entity_nome)
    elif entity_id and not entity_nome:
        mapa = nomes_por_ids(pg, params.entity_type, [entity_id])
        entity_nome = mapa.get(str(entity_id))

    quebra_valor = params.quebra_valor
    quebra_nome = params.quebra_nome
    if params.quebra and quebra_valor is None and quebra_nome:
        quebra_valor = resolver_nome(pg, params.quebra, quebra_nome)
    elif params.quebra and quebra_valor and not quebra_nome:
        mapa = nomes_por_ids(pg, params.quebra, [quebra_valor])
        quebra_nome = mapa.get(str(quebra_valor))

    return ParametrosPergunta(
        entity_type=params.entity_type,
        granularidade=params.granularidade,
        periodo=params.periodo,
        entity_id=entity_id,
        entity_nome=entity_nome,
        quebra=params.quebra,
        quebra_valor=quebra_valor,
        quebra_nome=quebra_nome,
        comparacao=params.comparacao,
        ranking=params.ranking or (entity_id is None),
    )
