from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FamilySpec:
    nome: str
    origem: str  # tabela diária
    prefixo: str  # sem sufixo de granularidade
    dims: tuple[str, ...]
    metrics: tuple[str, ...]  # colunas a SUM


FAMILIES: dict[str, FamilySpec] = {
    "os": FamilySpec(
        nome="os",
        origem="fato_os_diario",
        prefixo="fato_os",
        dims=(
            "concessionaria_id",
            "departamento_id",
            "vendedor_id",
            "produtivo_id",
            "empresa_id",
        ),
        metrics=("valor_total", "quantidade_os"),
    ),
    "servico": FamilySpec(
        nome="servico",
        origem="fato_os_servico_diario",
        prefixo="fato_os_servico",
        dims=(
            "concessionaria_id",
            "departamento_id",
            "vendedor_id",
            "produtivo_id",
            "empresa_id",
            "familia_servico_id",
            "servico_id",
        ),
        metrics=("valor_atribuido", "quantidade"),
    ),
    "pagamento": FamilySpec(
        nome="pagamento",
        origem="fato_os_pagamento_diario",
        prefixo="fato_os_pagamento",
        dims=(
            "concessionaria_id",
            "departamento_id",
            "vendedor_id",
            "produtivo_id",
            "empresa_id",
            "forma_pagamento_id",
        ),
        metrics=("valor_pago",),
    ),
    "comissao": FamilySpec(
        nome="comissao",
        origem="fato_comissao_diario",
        prefixo="fato_comissao",
        dims=("comissionado_id", "comissao_tipo_id"),
        metrics=("valor_comissao",),
    ),
}


def destino(spec: FamilySpec, granularidade: str) -> str:
    return f"{spec.prefixo}_{granularidade}"
