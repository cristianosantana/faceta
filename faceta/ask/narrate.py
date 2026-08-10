from __future__ import annotations

import json
from typing import Any

from faceta.ask.openai_client import chat_text
from faceta.ask.understand import ParametrosPergunta
from faceta.query.engine import ResultadoConsulta


SYSTEM = """Você é o narrador do Faceta. Em português do Brasil, responda de forma clara e objetiva
a pergunta do usuário usando APENAS os números do resultado da consulta e, se houver, os insights
já cacheados (campo insights) — integre-os naturalmente, sem inventar fatos novos.
Não invente valores. Mencione período e granularidade. Se houver ranking, cite os principais.
Se houver comparação, cite variação. Sem markdown excessivo; 1–3 parágrafos curtos.
IMPORTANTE: cite entidades pelo campo entity_nome (e quebra_nome, se houver).
Só use entity_id/quebra_id se o nome estiver ausente ou nulo.
"""


def narrar_resposta(
    pergunta: str,
    params: ParametrosPergunta,
    resultado: ResultadoConsulta,
    insights: list[dict] | None = None,
) -> str:
    payload: dict[str, Any] = {
        "pergunta": pergunta,
        "params": {
            "entity_type": params.entity_type,
            "granularidade": params.granularidade,
            "periodo": params.periodo,
            "entity_id": params.entity_id,
            "entity_nome": params.entity_nome,
            "quebra": params.quebra,
            "comparacao": params.comparacao,
            "ranking": params.ranking,
        },
        "consulta": resultado.to_dict(),
        "insights": insights or [],
    }
    # limitar tamanho para o narrador
    d = payload["consulta"]
    if len(d.get("linhas") or []) > 15:
        d["linhas"] = d["linhas"][:15]
        d["linhas_truncadas"] = True
    return chat_text(SYSTEM, json.dumps(payload, ensure_ascii=False))
