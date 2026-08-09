# Tracing (JSONL em `logs/`)

> Spec: `docs/superpowers/specs/2026-08-09-tracing-design.md`  
> Persistência: **somente** arquivos em `logs/` (já no `.gitignore`).

## Objetivos

1. **Visibilidade** — spans + attrs (regras/params) por etapa  
2. **Diagnóstico** — `status=error` + mensagem no span  
3. **Auditoria** — arquivo histórico por `trace_id`  
4. **Performance** — `duration_ms` por span  

## Formato

`logs/YYYY-MM-DD/<trace_id>.jsonl` — uma linha JSON por evento (`run_start`, `span_start`, `span_end`, `run_end`).

Pipelines instrumentados: `ask`, `ingest`, `cascata`, `query`.

## CLI

```bash
PYTHONPATH=. python -m faceta.query --entity-type vendedor --granularidade semanal --periodo 2026-W31 --ranking
# imprime: trace_id=... path=logs/...

PYTHONPATH=. python -m faceta.trace show logs/2026-08-09/<trace_id>.jsonl
```

Segredos (`password`, `api_key`, etc.) são redigidos.
