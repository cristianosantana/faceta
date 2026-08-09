# Fase 3 — Contrato e Motor de Consulta Genérico

> Spec: `docs/superpowers/specs/2026-08-09-fase-3-contrato-motor-design.md`  
> Status: **implementado**; TC01–TC11 OK (`scripts/fase3_tc.py`).

## Superfície

- Contrato: `contrato.yaml` (raiz do repo)
- API Python: `from faceta.query import consultar`
- CLI: `python -m faceta.query`

```bash
PYTHONPATH=. python -m faceta.query \
  --entity-type vendedor \
  --granularidade semanal \
  --periodo 2026-W31 \
  --ranking

PYTHONPATH=. python -m faceta.query \
  --entity-type vendedor \
  --granularidade mensal \
  --periodo 2026-07 \
  --comparacao vs_periodo_anterior \
  --ranking
```

## Período

`YYYY-MM-DD` · `YYYY-Www` · `YYYY-MM` · `YYYY-H1|H2` · `YYYY` → normalizado para `data` início da granularidade.

## Entity types

Inclui dims de OS/serviço/pagamento e **`comissionado` / `comissao_tipo`** → `fato_comissao`.  
Bloqueio: `servico` × `forma_pagamento` (e família × forma).

## Verificação

```bash
PYTHONPATH=. python scripts/fase3_tc.py
```
