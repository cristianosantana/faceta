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

## Crons e rotinas de execução

> **Agendador de SO / Airflow ainda `[PENDENTE]`.** Hoje tudo é CLI manual (ou o que você agendar no cron do SO apontando para estes comandos). Prefixo comum: `cd` na raiz do repo + `PYTHONPATH=.` + `.venv/bin/python`.

### Ordem canônica (nunca inverter)

```
0. health / doctor          (opcional, mas recomendado)
1. dims (opcional)          faceta.ingest --only-dims
2. ingest diário            faceta.ingest --data YYYY-MM-DD
3. cascata                  faceta.cascata  (semanal → mensal → semestral → anual)
4. insights                 faceta.insights train|run   (opcional; após cascata)
5. ask / API                faceta.ask  ou  POST /ask
```

Cascata **sempre** soma do `*_diario` (não semana→mês). Se faltar dia no diário, a agregada fica parcial; complete o ingest e rode de novo com `--force` no período.

### Dimensões, famílias e entity_types

| Camada | Valores |
|---|---|
| Famílias de fato (`--familia`) | `os`, `servico`, `pagamento`, `comissao` (default: todas) |
| Granularidades de cascata | `semanal`, `mensal`, `semestral`, `anual` (+ `diario` só na ingestão) |
| Snapshots `dim_*` | departamento, concessionaria, familia_servico, familia_produto, servico, funcionario, forma_pagamento, empresa, comissao_tipo |
| `entity_type` (contrato / ask / insights) | concessionaria, departamento, vendedor, produtivo, empresa, familia_servico, servico, forma_pagamento, comissionado, comissao_tipo |
| Chave de período | `--periodo` = qualquer dia dentro da janela; o job normaliza para o início (segunda ISO / dia 1 / 1-jan\|1-jul / 1-jan) |

### Hipótese A — rotina diária (D−1)

Rodar todo dia (ex. 01:00) para o dia anterior:

```bash
PYTHONPATH=. .venv/bin/python -m faceta.ops health
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-08-10          # ontem; omitir --data = ontem
# opcional: só uma família
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-08-10 --familia comissao
# cascata da semana corrente (parcial ok enquanto a semana não fechou)
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semanal --periodo 2026-08-10
PYTHONPATH=. .venv/bin/python -m faceta.ops doctor
```

Só dimensões (cadastros mudaram, sem reingerir fatos):

```bash
PYTHONPATH=. .venv/bin/python -m faceta.ingest --only-dims
```

### Hipótese B — fechamento de semana (segunda após a semana ISO)

```bash
# ref = qualquer dia da semana (ex. sexta); normaliza para a segunda
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semanal --periodo 2026-07-31 --force
# insights daquela semana (1 entity ou todas via script de mês)
PYTHONPATH=. .venv/bin/python -m faceta.insights train --entity-type vendedor --granularidade semanal
PYTHONPATH=. .venv/bin/python -m faceta.insights run --entity-type vendedor --granularidade semanal --periodo 2026-W31
```

### Hipótese C — fechamento de mês

```bash
# 1) garantir todos os dias do mês no diário
PYTHONPATH=. .venv/bin/python scripts/mes_ingest.py 2026-07
# 2) semanas que tocam o mês + mensal  (script atual: semanal + mensal)
PYTHONPATH=. .venv/bin/python scripts/mes_cascata.py 2026-07
# equivalente manual:
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade mensal --periodo 2026-07-01 --force
# 3) insights (todos entity_types × semanas do mês)
PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07
# ou filtrar:
PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07 --entity-type vendedor,servico,forma_pagamento --limit 10
```

`--dry-run` em qualquer `scripts/mes_*.py` lista os comandos sem executar.

### Hipótese D — fechamento semestral (H1 / H2)

Motor já aceita; **não** está no `mes_cascata.py` — rode na mão após ter diários (e de preferência mensais) do semestre:

```bash
# H1 2026 → ref em jan–jun (normaliza para 2026-01-01)
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semestral --periodo 2026-06-30 --force
# H2 2026 → ref em jul–dez (normaliza para 2026-07-01)
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semestral --periodo 2026-07-01 --force
# uma família só:
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semestral --periodo 2026-07-01 --familia os,comissao --force
```

### Hipótese E — fechamento anual

```bash
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade anual --periodo 2026-12-31 --force
```

### Hipótese F — backfill de intervalo (ops)

```bash
PYTHONPATH=. .venv/bin/python -m faceta.ops backfill --de 2026-07-01 --ate 2026-07-31
PYTHONPATH=. .venv/bin/python -m faceta.ops backfill --de 2026-07-01 --ate 2026-07-31 --cascata   # + semanal --force
```

Depois do backfill, complete mensal / semestral / anual à mão (o flag `--cascata` do ops só força **semanal**).

### Hipótese G — reprocessamento / correção

| Situação | O que rodar |
|---|---|
| Dia errado na origem | `ingest --data D` de novo (DELETE+INSERT do dia) → cascata `--force` nos períodos que contêm D |
| Só comissão | `--familia comissao` no ingest e na cascata |
| Agregada já existe e precisa refazer | cascata com `--force` |
| Agregada existe e pode pular | cascata sem `--force` (insert-only / skip) |
| Insights sem sinal / pouco histórico | Só em **dev**: `FACETA_ALLOW_FORCE_LLM=1 … insights run --force-llm` (bloqueado sem o env — não use em cron) |
| Só treinar modelo | `insights train --entity-type … --granularidade semanal` |

Ordem de `--force` após corrigir um dia `D`:

```bash
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data D
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semanal   --periodo D --force
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade mensal    --periodo D --force
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semestral --periodo D --force
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade anual     --periodo D --force
```

### Hipótese H — pipeline completo de um mês (receita prática)

```bash
PYTHONPATH=. .venv/bin/python -m faceta.ops health
PYTHONPATH=. .venv/bin/python scripts/mes_ingest.py 2026-07
PYTHONPATH=. .venv/bin/python scripts/mes_cascata.py 2026-07
# completar granularidades altas (ainda fora do script de mês):
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semestral --periodo 2026-07-01 --force
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade anual     --periodo 2026-07-01 --force
FACETA_ALLOW_FORCE_LLM=1 PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07 --force-llm --limit 5
PYTHONPATH=. .venv/bin/python -m faceta.ops doctor
PYTHONPATH=. .venv/bin/python -m faceta.ask "Quais vendedores mais venderam na semana 2026-W31?"
```

### Hipótese I — pipeline de um ano (`faceta.ops ano`)

Um processo só (como `backfill`), ordem canônica: dims → diário → semanal → mensal → semestral → anual → insights. Não substitui o cron D−1 nem os CLIs granulares.

```bash
# valida um mês conhecido antes do ano todo
PYTHONPATH=. .venv/bin/python -m faceta.ops ano 2026 --de-mes 7 --ate-mes 7 --skip-insights
# ano corrente: só até ontem (default --ate-hoje)
PYTHONPATH=. .venv/bin/python -m faceta.ops ano 2026
# ano fechado, tolera falhas pontuais
PYTHONPATH=. .venv/bin/python -m faceta.ops ano 2025 --continue-on-error
# só cascata (+ dims), reprocessa agregadas
PYTHONPATH=. .venv/bin/python -m faceta.ops ano 2026 --skip-ingest --skip-insights --force
```

Flags: `--skip-ingest|cascata|semestral|anual|insights|dims`, `--familia`, `--entity-type`, `--force` (cascata), `--force-llm` (exige `FACETA_ALLOW_FORCE_LLM=1`), `--continue-on-error`, `--sem-limite-hoje`.

### Sugestão de crontab (quando for ligar o SO)

Exemplos ilustrativos (ajuste caminho do venv):

```cron
# diário 01:15 — ingest ontem + cascata semanal parcial
15 1 * * *  cd /path/faceta && PYTHONPATH=. .venv/bin/python -m faceta.ingest && PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semanal --periodo $(date -I)
# segunda 02:00 — force da semana anterior + insights vendedor
0 2 * * 1   cd /path/faceta && PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semanal --periodo $(date -I -d 'last friday') --force
# dia 2 do mês 03:00 — mês anterior via scripts
0 3 2 * *   cd /path/faceta && PYTHONPATH=. .venv/bin/python scripts/mes_ingest.py $(date -d 'last month' +%Y-%m) && PYTHONPATH=. .venv/bin/python scripts/mes_cascata.py $(date -d 'last month' +%Y-%m)
# 2/jan e 2/jul 04:00 — semestral
0 4 2 1,7 * cd /path/faceta && PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semestral --periodo $(date -I) --force
# 2/jan 05:00 — anual do ano anterior
0 5 2 1 *   cd /path/faceta && PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade anual --periodo $(date -d 'last year' +%Y-12-31) --force
```

Detalhes: `documentos/09-manual-operacional.md` · `documentos/14-fase2-cascata.md` · `documentos/19-fase6-ops.md`

### Migração de schema (manual, versionada)

`apply_ddl` (chamado no ingest/cascata) só faz **CREATE IF NOT EXISTS**. Drops destrutivos **não** rodam mais automaticamente.

```bash
PYTHONPATH=. .venv/bin/python -m faceta.migrate status
PYTHONPATH=. .venv/bin/python -m faceta.migrate up --dry-run
PYTHONPATH=. .venv/bin/python -m faceta.migrate up    # aplica pendentes + recreate DDL seguro
```

Histórico em `memoria_materializada.schema_migrations`. Após um DROP, reingerir os dias afetados.

## Rodar ingestão

```bash
.venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-07-31
PYTHONPATH=. .venv/bin/python -m faceta.ingest --only-dims
```

Backfill do mês inteiro (`YYYY-MM`):

```bash
PYTHONPATH=. .venv/bin/python scripts/mes_ingest.py 2026-07
PYTHONPATH=. .venv/bin/python scripts/mes_cascata.py 2026-07
PYTHONPATH=. .venv/bin/python scripts/mes_insights.py 2026-07   # todos entity_types × semanas
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
PYTHONPATH=. .venv/bin/python -m faceta.ops ano 2026 --de-mes 7 --ate-mes 7 --skip-insights
```

Doc: `documentos/19-fase6-ops.md`

## API (Fase 7)

```bash
PYTHONPATH=. .venv/bin/uvicorn faceta.api:app --reload --host 127.0.0.1 --port 8000
# POST http://127.0.0.1:8000/ask  {"pergunta":"..."}
# docs: http://127.0.0.1:8000/docs
```

Doc: `documentos/20-fase7-api.md`
