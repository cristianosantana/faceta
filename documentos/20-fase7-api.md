# Fase 7 — API FastAPI

> Spec implícita: `11-roadmap.md` Fase 7 · `08-documentacao-api.md`  
> Status: **implementado** (`faceta/api.py`) — **sem autenticação** (local/dev)

## Subir

```bash
.venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/uvicorn faceta.api:app --reload --host 127.0.0.1 --port 8000
```

Swagger: http://127.0.0.1:8000/docs

## Rotas

| Método | Path | Descrição |
|---|---|---|
| `GET` | `/health` | Postgres ok? |
| `POST` | `/ask` | Pergunta NL → ask pipeline |

### `POST /ask`

```bash
curl -s http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"pergunta":"Quais vendedores mais venderam na semana 2026-W31?"}'
```

Body: `{ "pergunta": "...", "sem_narracao": false }`  
Resposta: `RespostaAsk` (`narracao`, `params`, `resultado`, `insights`, `llm_calls`, `trace_id`, …)

Auth: **não** nesta fase.
