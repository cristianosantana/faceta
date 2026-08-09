# Tracing JSONL em `logs/` (Design)

**Data:** 2026-08-09  
**Status:** aprovado  
**Decisão:** apenas arquivos JSONL em `logs/` (gitignored); sem Postgres/OTel.

## Objetivos cobertos
1. Visibilidade ponta a ponta (spans + attrs de regras/params)
2. Diagnóstico (span com `status=error` + `error`)
3. Auditoria (arquivo histórico por `trace_id`)
4. Performance (`duration_ms` por span)

## Formato
- Path: `logs/YYYY-MM-DD/<trace_id>.jsonl`
- Uma linha JSON por evento: `run_start` | `span_start` | `span_end` | `run_end`
- CLI: `python -m faceta.trace show <arquivo>`
