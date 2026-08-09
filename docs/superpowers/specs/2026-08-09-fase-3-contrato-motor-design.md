# Fase 3 — Contrato e Motor de Consulta Genérico (Design)

**Data:** 2026-08-09  
**Status:** implementado (`faceta/query`, `contrato.yaml`; TC01–TC11 via `scripts/fase3_tc.py`)  
**Dependência:** Fases 1–2 (fatos diários + cascata no Postgres)

## 1. Objetivo

Contrato YAML como allowlist/roteador (US09–US11) e motor de consulta genérico com agregação, comparações e ranking (US12–US14).

**Critério de saída:** TC01–TC11 passando contra dado real (TC01–TC04 = saúde ingestão/cascata; TC05–TC11 = motor/contrato).

## 2. Fora de escopo

- HTTP (`GET /consulta` permanece proposta em `08`)
- LLM / insights / TensorFlow
- Airflow

## 3. Decisões

| Tema | Decisão |
|---|---|
| Superfície | Biblioteca Python + CLI `python -m faceta.query` |
| Comissão | `comissionado` e `comissao_tipo` no contrato → `fato_comissao` |
| Período | `YYYY-MM-DD`, `YYYY-Www`, `YYYY-MM`, `YYYY-H1\|H2`, `YYYY` → `data` = início |
| SQL | Só mapas fixos (dimensão→coluna, fato, sufixo); rejeita fora da allowlist antes do banco |

## 4. Layout

```
contrato.yaml
faceta/query/
  maps.py          # allowlists
  errors.py        # ConsultaRejeitada
  contract.py      # load + validar + resolver tabela
  periods.py       # parse período + período de comparação
  engine.py        # consultar()
  __main__.py      # CLI
```

## 5. Contrato (exemplo)

Cada `entity_type`: `fato`, `coluna`, `valor`, `quebras_validas`.  
`servico`/`familia_servico` nunca listam `forma_pagamento` e vice-versa.

## 6. Motor

Entrada: `entity_type`, `entity_id?`, `granularidade`, `periodo`, `quebra?`, `quebra_valor?`, `comparacao?`, `ranking?`.

1. Validar contrato  
2. Resolver tabela e colunas  
3. Agregar `SUM(valor)` (e métricas auxiliares se houver, ex. `quantidade_os`)  
4. Comparação = 2ª execução no período de referência  
5. Ranking = sem filtro de entity (ou `ranking=true`): ordem desc + `RANK()` + `participacao_pct`

## 7. CLI

```bash
PYTHONPATH=. python -m faceta.query \
  --entity-type vendedor \
  --granularidade semanal \
  --periodo 2026-W31 \
  [--entity-id ID] [--quebra departamento] [--quebra-valor X] \
  [--comparacao vs_periodo_anterior] [--ranking]
```

## 8. Verificação TC01–TC11

Script/checklist contra Postgres real: reconciliação/cascata (01–04) + consultas motor (05–11).

## 9. Docs a atualizar

`11-roadmap`, `15-fase3-consulta.md` (novo), SAD §6–8 se preciso, README, requirements (`PyYAML`).
