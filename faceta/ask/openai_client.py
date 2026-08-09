from __future__ import annotations

import os
from typing import Any

from faceta.db import load_env


def get_openai_client():
    load_env()
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("LLM_API_KEY (ou OPENAI_API_KEY) ausente no .env")
    try:
        from openai import OpenAI
    except ImportError as e:
        raise SystemExit("Instale openai: pip install openai") from e
    kwargs: dict[str, Any] = {"api_key": api_key}
    base = os.getenv("OPENAI_BASE_URL")
    if base:
        kwargs["base_url"] = base
    return OpenAI(**kwargs)


def llm_model() -> str:
    load_env()
    return os.getenv("LLM_MODEL") or "gpt-5-mini"


def chat_json(system: str, user: str) -> str:
    client = get_openai_client()
    resp = client.chat.completions.create(
        model=llm_model(),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content
    if not content:
        raise RuntimeError("LLM retornou conteúdo vazio")
    return content


def chat_text(system: str, user: str) -> str:
    client = get_openai_client()
    resp = client.chat.completions.create(
        model=llm_model(),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    content = resp.choices[0].message.content
    if not content:
        raise RuntimeError("LLM retornou conteúdo vazio")
    return content.strip()
