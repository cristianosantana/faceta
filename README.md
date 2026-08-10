# Faceta

Também conhecido como **Facetado**.

Faceta leva o nome do padrão de **busca facetada**: filtrar e agrupar o mesmo conjunto de dados por múltiplas dimensões independentes. Cada dimensão — uma *faceta* — pode ser combinada com as demais sem dependência de ordem ou hierarquia fixa.

## Status

- **Fase 0** — levantamento MySQL: feito  
- **Fase 1** — ingestão diária + `dim_*` + `servico_id` no fato de serviço: feito  
- **Fase 2** — cascata temporal (diário → semanal/mensal/…): feito  
- **Fase 3** — contrato + motor de consulta: feito  
- **Fase 4** — pergunta + narração (OpenAI): feito (requer `LLM_API_KEY`)  
- **Fase 5** — insights (autoencoder + tabela `insights`): feito  
- **Fase 6** — operação (`faceta.ops`): feito (local; prod `[PENDENTE]`)  
- **Fase 7** — API FastAPI (`POST /ask`): feito (sem auth)  

## Rodar ingestão

```bash
.venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-07-31
PYTHONPATH=. .venv/bin/python -m faceta.ingest --only-dims
```

## Cascata (Fase 2)

Soma sempre a partir do diário; completude parcial; `--force` para reprocessar:

```bash
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semanal --periodo 2026-07-31
```

## Consulta (Fase 3)

```bash
PYTHONPATH=. .venv/bin/python -m faceta.query --entity-type vendedor --granularidade semanal --periodo 2026-W31 --ranking
PYTHONPATH=. .venv/bin/python scripts/fase3_tc.py
```

## Pergunta (Fase 4)

```bash
# .env: LLM_API_KEY=...  LLM_MODEL=gpt-5-mini
PYTHONPATH=. .venv/bin/python -m faceta.ask "Quais vendedores mais venderam na semana 2026-W31?"
```

Docs: `documentos/17-tracing.md` · `documentos/16-fase4-ask.md` · `documentos/15-fase3-consulta.md` · `documentos/11-roadmap.md`

## Tracing

JSONL em `logs/` (gitignored):

```bash
PYTHONPATH=. .venv/bin/python -m faceta.trace show logs/2026-08-09/<trace_id>.jsonl
```

## Insights (Fase 5)

```bash
PYTHONPATH=. .venv/bin/python -m faceta.insights train --entity-type vendedor --granularidade semanal
PYTHONPATH=. .venv/bin/python -m faceta.insights run --periodo 2026-W31 --limit 1
PYTHONPATH=. .venv/bin/python -m faceta.insights tc
```

Ask consulta `insights` e envia ao narrador. Doc: `documentos/18-fase5-insights.md`

## Operação (Fase 6)

```bash
PYTHONPATH=. .venv/bin/python -m faceta.ops health
PYTHONPATH=. .venv/bin/python -m faceta.ops doctor
PYTHONPATH=. .venv/bin/python -m faceta.ops metrics
```

Doc: `documentos/19-fase6-ops.md`

## API (Fase 7)

```bash
PYTHONPATH=. .venv/bin/uvicorn faceta.api:app --reload --host 127.0.0.1 --port 8000
# POST http://127.0.0.1:8000/ask  {"pergunta":"..."}
# docs: http://127.0.0.1:8000/docs
```

Doc: `documentos/20-fase7-api.md`
