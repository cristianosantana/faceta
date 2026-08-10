# Fase 5 — Insights via Deep Learning

> Spec: `docs/superpowers/specs/2026-08-09-fase-5-insights-design.md`  
> Status: **implementado** (`faceta/insights`)

## Ideia

- Job em **lote** (não no ask): séries → autoencoder TF → se erro > limiar → 1 LLM → tabela `insights`
- Ask só **lê** `insights` e manda ao narrador (ainda ≤2 LLM no ask)

## CLI

```bash
PYTHONPATH=. python -m faceta.insights train --entity-type vendedor --granularidade semanal
PYTHONPATH=. python -m faceta.insights run --entity-type vendedor --granularidade semanal --periodo 2026-W31
PYTHONPATH=. python -m faceta.insights run ... --force-llm   # gera insight mesmo com pouco histórico
PYTHONPATH=. python -m faceta.insights tc
```

## Backend do modelo

Prefere **TensorFlow** quando instalável. No Python 3.14 (sem wheel TF) usa **autoencoder NumPy** equivalente. Modelos em `models/insights/` (gitignored).

## Tabela

`memoria_materializada.insights` — PK (entity_type, entity_id, granularidade, periodo, quebra)
