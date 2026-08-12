from __future__ import annotations

import json
from typing import Any

from faceta.ask.openai_client import chat_text


SYSTEM = """Você narra um insight analítico curto em português do Brasil.
Recebe série e sinal de anomalia (erro de reconstrução do autoencoder).
Responda APENAS JSON: {"assunto": "...", "descricao": "...", "confianca": 0.0 a 1.0}
Não invente números além dos fornecidos. Sem markdown.
Se modelo_bootstrap=true, o modelo foi treinado com dados sintéticos: use confianca baixa (≤0.35)
e mencione incerteza por histórico insuficiente.
"""


def narrar_insight(
    *,
    entity_type: str,
    entity_id: str,
    entity_nome: str | None,
    granularidade: str,
    periodo: str,
    valores: list[float],
    erro: float,
    threshold: float,
    modelo_bootstrap: bool = False,
) -> dict[str, Any]:
    payload = {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "entity_nome": entity_nome,
        "granularidade": granularidade,
        "periodo": periodo,
        "serie_valores": valores[-12:],
        "erro_reconstrucao": erro,
        "limiar": threshold,
        "modelo_bootstrap": modelo_bootstrap,
    }
    raw = chat_text(SYSTEM, json.dumps(payload, ensure_ascii=False))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # tenta extrair bloco JSON
        start, end = raw.find("{"), raw.rfind("}")
        if start >= 0 and end > start:
            data = json.loads(raw[start : end + 1])
        else:
            data = {
                "assunto": "Variação notável detectada",
                "descricao": raw.strip()[:500],
                "confianca": 0.5,
            }
    conf = float(data.get("confianca") or 0.5)
    if modelo_bootstrap:
        conf = min(conf, 0.35)
    return {
        "assunto": str(data.get("assunto") or "Insight"),
        "descricao": str(data.get("descricao") or ""),
        "confianca": conf,
        "modelo_bootstrap": modelo_bootstrap,
    }
