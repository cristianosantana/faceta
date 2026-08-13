from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from faceta.db import ROOT
from faceta.query.errors import ConsultaRejeitada
from faceta.query.maps import (
    COMPARACOES,
    DIMENSAO_TO_COLUNA,
    FATO_BASES,
    FILTRO_FIXO_COLUNAS,
    GRANULARIDADE_SUFIXO,
    RESOLVE_DIM_TABLES,
    VALOR_COLUNAS,
)

DEFAULT_CONTRATO = ROOT / "contrato.yaml"


def load_contrato(path: Path | None = None) -> dict[str, Any]:
    p = path or DEFAULT_CONTRATO
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "entity_types" not in data:
        raise ConsultaRejeitada("contrato inválido: falta entity_types")
    _validar_estrutura(data)
    return data


def _validar_estrutura(contrato: dict[str, Any]) -> None:
    for nome, cfg in contrato["entity_types"].items():
        if nome not in DIMENSAO_TO_COLUNA:
            raise ConsultaRejeitada(f"entity_type '{nome}' fora do mapa dimensão→coluna")
        fato = cfg.get("fato")
        coluna = cfg.get("coluna")
        valor = cfg.get("valor")
        if fato not in FATO_BASES:
            raise ConsultaRejeitada(f"fato inválido para {nome}: {fato}")
        if coluna != DIMENSAO_TO_COLUNA[nome]:
            raise ConsultaRejeitada(
                f"coluna de {nome} deve ser {DIMENSAO_TO_COLUNA[nome]!r}, got {coluna!r}"
            )
        if valor not in VALOR_COLUNAS:
            raise ConsultaRejeitada(f"valor inválido para {nome}: {valor}")
        for q in cfg.get("quebras_validas") or []:
            if q not in DIMENSAO_TO_COLUNA:
                raise ConsultaRejeitada(f"quebra '{q}' de {nome} fora do mapa dimensão→coluna")
            if q == nome:
                raise ConsultaRejeitada(f"quebra '{q}' não pode ser o próprio entity_type")
            # US11: servico × forma_pagamento
            if {nome, q} == {"servico", "forma_pagamento"}:
                raise ConsultaRejeitada("contrato inválido: servico × forma_pagamento")
            if {nome, q} == {"familia_servico", "forma_pagamento"}:
                raise ConsultaRejeitada("contrato inválido: familia_servico × forma_pagamento")

        ff = cfg.get("filtro_fixo")
        if ff is not None:
            if not isinstance(ff, dict) or not ff:
                raise ConsultaRejeitada(f"filtro_fixo inválido para {nome}")
            for col, vals in ff.items():
                if col not in FILTRO_FIXO_COLUNAS:
                    raise ConsultaRejeitada(
                        f"filtro_fixo coluna '{col}' de {nome} fora da allowlist"
                    )
                if not isinstance(vals, list) or not vals:
                    raise ConsultaRejeitada(
                        f"filtro_fixo.{col} de {nome} deve ser lista não vazia de valores"
                    )
                for v in vals:
                    if v is None or str(v).strip() == "":
                        raise ConsultaRejeitada(f"filtro_fixo.{col} de {nome} tem valor vazio")

        rd = cfg.get("resolve_dim")
        if rd is not None:
            if rd not in RESOLVE_DIM_TABLES:
                raise ConsultaRejeitada(f"resolve_dim inválido para {nome}: {rd}")


def resolver_entity(contrato: dict[str, Any], entity_type: str) -> dict[str, Any]:
    types = contrato.get("entity_types") or {}
    if entity_type not in types:
        raise ConsultaRejeitada(f"entity_type não previsto no contrato: {entity_type}")
    if entity_type not in DIMENSAO_TO_COLUNA:
        raise ConsultaRejeitada(f"entity_type fora do mapa dimensão→coluna: {entity_type}")
    return types[entity_type]


def validar_consulta(
    contrato: dict[str, Any],
    *,
    entity_type: str,
    granularidade: str,
    quebra: str | None = None,
    comparacao: str | None = None,
) -> dict[str, Any]:
    cfg = resolver_entity(contrato, entity_type)

    allowed_g = set(contrato.get("granularidades_validas") or GRANULARIDADE_SUFIXO)
    if granularidade not in allowed_g or granularidade not in GRANULARIDADE_SUFIXO:
        raise ConsultaRejeitada(f"granularidade inválida: {granularidade}")

    if quebra is not None:
        if quebra not in DIMENSAO_TO_COLUNA:
            raise ConsultaRejeitada(f"quebra fora do mapa dimensão→coluna: {quebra}")
        validas = set(cfg.get("quebras_validas") or [])
        if quebra not in validas:
            raise ConsultaRejeitada(
                f"quebra '{quebra}' não permitida para entity_type '{entity_type}'"
            )
        if {entity_type, quebra} == {"servico", "forma_pagamento"}:
            raise ConsultaRejeitada("cruzamento servico × forma_pagamento bloqueado")

    if comparacao is not None:
        allowed_c = set(contrato.get("comparacoes_validas") or COMPARACOES)
        if comparacao not in allowed_c or comparacao not in COMPARACOES:
            raise ConsultaRejeitada(f"comparação inválida: {comparacao}")

    return cfg


def tabela_fato(entity_cfg: dict[str, Any], granularidade: str) -> str:
    fato = entity_cfg["fato"]
    if fato not in FATO_BASES:
        raise ConsultaRejeitada(f"fato fora da allowlist: {fato}")
    sufixo = GRANULARIDADE_SUFIXO[granularidade]
    return f"{fato}{sufixo}"


def coluna_dimensao(nome: str) -> str:
    if nome not in DIMENSAO_TO_COLUNA:
        raise ConsultaRejeitada(f"dimensão fora do mapa: {nome}")
    return DIMENSAO_TO_COLUNA[nome]


def filtro_fixo_params(entity_cfg: dict[str, Any]) -> list[tuple[str, list[str]]]:
    """Retorna [(coluna, [valores])] do filtro_fixo, já normalizado em strings."""
    ff = entity_cfg.get("filtro_fixo") or {}
    out: list[tuple[str, list[str]]] = []
    for col, vals in ff.items():
        if col not in FILTRO_FIXO_COLUNAS:
            raise ConsultaRejeitada(f"filtro_fixo coluna fora da allowlist: {col}")
        out.append((col, [str(v) for v in vals]))
    return out
