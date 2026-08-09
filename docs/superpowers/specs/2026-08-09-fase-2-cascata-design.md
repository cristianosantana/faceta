# Fase 2 — Cascata por Tempo (Design)

**Data:** 2026-08-09  
**Status:** implementado (`faceta/cascata`; verificado semana ISO `2026-07-27`)  
**Dependência:** Fase 1 (fatos `*_diario` no Postgres)

## 1. Objetivo

Materializar tabelas `*_semanal`, `*_mensal`, `*_semestral`, `*_anual` para as quatro famílias (`fato_os`, `fato_os_servico`, `fato_os_pagamento`, `fato_comissao`), somando o nível **diário** já persistido (US07–US08).

**Critério de saída:** um período fechado (ex.: uma semana ISO) materializado corretamente nas quatro famílias; reexecução sem `--force` não sobrescreve; com `--force` reinsere o período.

## 2. Fora de escopo

- Contrato YAML / motor de consulta (Fase 3)
- LLM / TensorFlow
- Airflow / cron do SO (disparo manual via CLI, igual Fase 1)
- Recálculo a partir de MySQL (só lê Postgres)

## 3. Decisões fechadas

| Tema | Decisão |
|---|---|
| Fonte de cada nível | Sempre `*_diario` no intervalo do calendário (**não** semana→mês) |
| Motivo | Pagamentos/eventos no fim do mês não devem distorcer cascata via semana |
| Completude | **Parcial**: soma os dias que existirem (5 ou 6 dias numa semana é válido; intervalo vazio → 0 linhas / skip) |
| Idempotência | Default **insert-only**: se o período já tem linhas, pula |
| Reprocessamento | `--force`: `DELETE WHERE data = início_do_período` + `INSERT` |
| Abordagem | Pacote `faceta/cascata` + CLI `python -m faceta.cascata` (espelha ingest) |

## 4. Chaves de período

Coluna `data` nas tabelas agregadas = **início inclusivo** do período; fim = exclusivo.

| Granularidade | `data` (início) | Intervalo `[início, fim)` |
|---|---|---|
| `semanal` | segunda ISO da semana | +7 dias |
| `mensal` | dia 1 do mês | 1º do mês seguinte |
| `semestral` | 1/jan ou 1/jul | +6 meses |
| `anual` | 1/jan | +1 ano |

CLI aceita `--periodo YYYY-MM-DD` (qualquer dia dentro do período); o job normaliza para o início.

## 5. Agregação

Para cada família × granularidade × período:

1. Resolver `[início, fim)` e tabela destino / origem (`*_diario`).
2. Se já existem linhas com `data = início` e **não** `--force` → skip (log).
3. Se `--force` → `DELETE FROM destino WHERE data = início`.
4. `INSERT … SELECT` agrupando por todas as colunas de dimensão (PK sem `data`), somando métricas numéricas:
   - `fato_os`: `SUM(valor_total)`, `SUM(quantidade_os)`
   - `fato_os_servico`: `SUM(valor_atribuido)`, `SUM(quantidade)`
   - `fato_os_pagamento`: `SUM(valor_pago)`
   - `fato_comissao`: `SUM(valor_comissao)`
5. Filtro: `origem.data >= início AND origem.data < fim`.
6. `data` gravada = início do período.

Sem exigência de N dias presentes. Sem linhas no diário no intervalo → nada a inserir (ok).

## 6. DDL

Reutilizar / aplicar `faceta/sql/ddl_cascata.sql` (`CREATE TABLE … LIKE …_diario INCLUDING ALL`). Integrar em `apply_ddl` (ou aplicar no CLI de cascata) para criar as 16 tabelas.

## 7. CLI

```bash
PYTHONPATH=. python -m faceta.cascata \
  --granularidade semanal \
  --periodo 2026-07-28 \
  [--familia os,servico,pagamento,comissao] \
  [--force] \
  [--skip-ddl]
```

- `--granularidade`: `semanal|mensal|semestral|anual` (obrigatório)
- `--periodo`: data de referência (obrigatório)
- `--familia`: default todas
- `--force`: apaga e reinsere o período
- Opcional útil: `--todas-granularidades` para o mesmo `--periodo` (roda as 4 em ordem) — nice-to-have, não bloqueia critério de saída

## 8. Layout de código

```
faceta/cascata/
  __init__.py
  __main__.py      # CLI
  periods.py       # início/fim por granularidade
  engine.py        # delete (force) + insert select genérico
  families.py      # mapa família → tabelas, dims, métricas
faceta/sql/ddl_cascata.sql
```

`apply_ddl` passa a aplicar também `ddl_cascata.sql` após `ddl_diario.sql`.

## 9. Verificação

1. Garantir diários no intervalo (ex. semana ISO que contenha `2026-07-31` ou dias já ingeridos).
2. Rodar cascata semanal nas 4 famílias.
3. Conferir: `SUM(métrica)` no diário no intervalo = `SUM(métrica)` na linha(s) semanal(is) para as mesmas dims.
4. Reexecutar sem `--force` → 0 inserts novos / skip.
5. `--force` → mesmos totais, sem duplicar.

## 10. Documentação (atualizada com as decisões)

Já alinhados às decisões desta spec (antes/durante implementação):

- `documentos/14-fase2-cascata.md` — resumo operacional
- `documentos/11-roadmap.md` — Fase 2 (decisões + critério)
- `documentos/07-guia-implantacao.md` — § cascata
- `documentos/05-arquitetura-software-sad.md` — Camada 2
- `documentos/04-historias-usuario-backlog.md` — US07/US08
- `documentos/03-ers-especificacao-requisitos.md` — RF06 / RNF04 / visão geral
- `documentos/06-plano-testes-casos-teste.md` — TC04 parcial
- `documentos/09-manual-operacional.md` — rotina e diagnóstico
- `documentos/10-dicionario-dados.md` — nota de cascata
- `README.md` — status + comando alvo

Após critério de saída (código + verificação): marcar Fase 2 como **feito** no roadmap/README e status desta spec como `implementado`.
