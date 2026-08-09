from __future__ import annotations

DIMENSAO_TO_COLUNA: dict[str, str] = {
    "concessionaria": "concessionaria_id",
    "departamento": "departamento_id",
    "vendedor": "vendedor_id",
    "produtivo": "produtivo_id",
    "empresa": "empresa_id",
    "familia_servico": "familia_servico_id",
    "servico": "servico_id",
    "forma_pagamento": "forma_pagamento_id",
    "comissionado": "comissionado_id",
    "comissao_tipo": "comissao_tipo_id",
}

GRANULARIDADE_SUFIXO: dict[str, str] = {
    "diario": "_diario",
    "semanal": "_semanal",
    "mensal": "_mensal",
    "semestral": "_semestral",
    "anual": "_anual",
}

FATO_BASES: frozenset[str] = frozenset(
    {"fato_os", "fato_os_servico", "fato_os_pagamento", "fato_comissao"}
)

VALOR_COLUNAS: frozenset[str] = frozenset(
    {"valor_total", "valor_atribuido", "valor_pago", "valor_comissao"}
)

COMPARACOES: frozenset[str] = frozenset(
    {"vs_periodo_anterior", "vs_mesmo_periodo_ano_anterior"}
)
