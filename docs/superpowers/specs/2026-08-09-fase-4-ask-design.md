# Fase 4 — Entendimento de Pergunta e Narração (Design)

**Data:** 2026-08-09  
**Status:** implementado (`faceta/ask`; critério E2E depende de `LLM_API_KEY`)  
**Dependência:** Fase 3 (contrato + motor)

## 1. Objetivo

US18–US20: pergunta em linguagem natural → ≤2 chamadas LLM → resposta narrada.

**Critério:** uma pergunta real ponta a ponta com `llm_calls ≤ 2`.

## 2. Decisões

| Tema | Decisão |
|---|---|
| Provedor | OpenAI |
| Modelo | `gpt-5-mini` (`LLM_MODEL`) |
| Superfície | `faceta/ask` + CLI `python -m faceta.ask` |
| Resolução de entidade | LLM pode devolver id e/ou nome; nome → ILIKE em `dim_*` (1 hit) |
| Fluxo | LLM₁ JSON → validar → resolver dims → `consultar()` → LLM₂ narração |

## 3. Layout

```
faceta/ask/
  openai_client.py
  understand.py
  resolve.py
  narrate.py
  pipeline.py
  __main__.py
```

## 4. Env

`LLM_API_KEY`, `LLM_MODEL=gpt-5-mini` (opcional `OPENAI_BASE_URL`)

## 5. Fora de escopo

HTTP, insights/TF, retries que gerem >2 chamadas.
