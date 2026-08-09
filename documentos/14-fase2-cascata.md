# Fase 2 — Cascata por Tempo

> Spec: `docs/superpowers/specs/2026-08-09-fase-2-cascata-design.md`  
> Status: **implementado** (`faceta/cascata`); verificado semana ISO `2026-07-27` (ref. `2026-07-31`).

## Decisões

| Tema | Decisão |
|---|---|
| Fonte | Cada granularidade (`semanal` … `anual`) soma **somente** `*_diario` no intervalo do calendário |
| Por quê não semana→mês | Eventos no fim do mês (ex. OS paga tarde) deixariam a semana e o mês inconsistentes se a cascata fosse em cadeia |
| Completude | **Parcial**: 5 ou 6 dias numa semana bastam; soma o que existir; intervalo sem diário → 0 linhas |
| Idempotência | Default **insert-only**: se o período já tem linhas, pula |
| Reprocessamento | `--force`: `DELETE` do período (`data` = início) + `INSERT` |

## Como rodar

```bash
PYTHONPATH=. python -m faceta.cascata --granularidade semanal --periodo 2026-07-31
PYTHONPATH=. python -m faceta.cascata --granularidade mensal --periodo 2026-07-31 --force
```

`--periodo` = qualquer dia dentro do intervalo; o job normaliza para o início (segunda ISO / dia 1 / etc.).

## Chaves de período (`data` = início)

| Granularidade | Início | Intervalo |
|---|---|---|
| semanal | segunda ISO | +7 dias |
| mensal | dia 1 | até 1º do mês seguinte |
| semestral | 1/jan ou 1/jul | +6 meses |
| anual | 1/jan | +1 ano |

## Famílias e métricas

- `fato_os_*`: `valor_total`, `quantidade_os`
- `fato_os_servico_*`: `valor_atribuido`, `quantidade`
- `fato_os_pagamento_*`: `valor_pago`
- `fato_comissao_*`: `valor_comissao`

DDL: `faceta/sql/ddl_cascata.sql`.

## Verificação (critério de saída)

Semana `2026-07-27`..`2026-08-03`: `SUM` diário = `SUM` semanal nas quatro famílias; segunda execução sem `--force` → skip.
