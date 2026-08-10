# Fase 6 — Operação

> Spec: `docs/superpowers/specs/2026-08-09-fase-6-ops-design.md`  
> Status: **implementado** (toolkit local; deploy produção `[PENDENTE]`)

## CLI

```bash
PYTHONPATH=. python -m faceta.ops health
PYTHONPATH=. python -m faceta.ops status --dias 14
PYTHONPATH=. python -m faceta.ops backfill --de 2026-07-30 --ate 2026-07-31 --cascata
PYTHONPATH=. python -m faceta.ops metrics --dias 30
PYTHONPATH=. python -m faceta.ops doctor
```

| Comando | Uso |
|---|---|
| `health` | MySQL, Postgres/schema, contrato |
| `status` | Gaps de fatos diários, cascata, insights, reconciliação |
| `backfill` | Reingere intervalo; `--cascata` força semanal |
| `metrics` | Latência por pipeline + `llm_calls` dos traces ask (meta ≤2) |
| `doctor` | Checklist do manual §4 + health/metrics |

## Rotina sugerida (local)

1. `ops health`  
2. `ingest` do dia (ou `ops backfill`)  
3. `cascata` da semana/mês fechado  
4. `insights run` (opcional)  
5. `ops doctor` + `ops metrics`  

## Critério de sucesso (local)

- `health` e `doctor` ok  
- `metrics.llm_calls_ask.meta_ok` (≤2) quando houver traces de ask  
- Produção/servidor: ainda `[PENDENTE]` no termo de abertura
