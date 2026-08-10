# Fase 6 — Operação (Design)

**Data:** 2026-08-09  
**Status:** implementado (`faceta/ops`; produção `[PENDENTE]`)  
**Escopo:** toolkit ops local + playbook (não deploy de produção).

## CLI `python -m faceta.ops`
- `health` — MySQL, Postgres, schema, contrato
- `status` — cobertura fatos/gaps, insights
- `backfill --de --ate [--cascata]`
- `metrics` — agrega traces JSONL
- `doctor` — checklist diagnóstico

## Critério local
Comandos rodando; métrica ≤2 LLM/ask via traces. Produção `[PENDENTE]`.
