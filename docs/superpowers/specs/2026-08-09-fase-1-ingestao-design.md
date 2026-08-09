# Fase 1 — Ingestão das Quatro Famílias de Fato (Design)

**Data:** 2026-08-09  
**Status:** implementado + ajustes (`dim_*`, `comissionado_id`/`comissao_tipo_id`, família=`subgrupos_*`, `servico_id` no fato)
**Dependência:** Fase 0 concluída (`documentos/12-levantamento-fase-0.md`)

## 1. Objetivo

Materializar no **Postgres** as tabelas diárias `fato_os_diario`, `fato_os_servico_diario`, `fato_os_pagamento_diario`, `fato_comissao_diario`, com ingestão **idempotente** e **reconciliação** sinalizada (US01–US06). **Ajuste:** snapshots `dim_*` no Postgres para resolver nomes sem join MySQL em toda leitura.

**Critério de saída:** um dia real ingerido nas quatro famílias; reexecução do mesmo dia não duplica; divergências de reconciliação registradas (não silenciosas).

## 2. Fora de escopo

- Cascata semanal/mensal/… (Fase 2)
- Contrato YAML / motor genérico / LLM / TensorFlow
- Airflow / cron do SO (disparo **manual** / por hora via CLI)

## 3. Onde vivem os dados

| Camada | Banco |
|---|---|
| Dimensões (fonte de verdade) | MySQL `smart` |
| Snapshots `dim_*` (id, nome) | Postgres (`POSTGRES_URL`) |
| Fatos diários | Postgres (`POSTGRES_URL`) |

## 4. Data do evento por família (insert-only)

**Sem `UPDATE` de fatos já gravados.** Pagamento posterior à criação gera **novas** linhas na data do pagamento.

| Família | Filtro do job para o dia D | Coluna `data` |
|---|---|---|
| `fato_os` | `DATE(os.created_at) = D`, `deleted_at IS NULL` | D (criação) |
| `fato_os_servico` | itens `os_servicos` com fechamento em D (`DATE(data_fechamento)=D` ou, se nulo, `DATE(updated_at)` quando `fechado=1`), ativos | D (fechamento do item) |
| `fato_os_pagamento` | `caixas` com OS paga (`os.paga=1`) e evento em D (`DATE(os.data_pagamento)=D` ou data do caixa), `caixas.deleted_at IS NULL` | D (pagamento) |
| `fato_comissao` | `DATE(comissoes.created_at) = D`, `deleted_at IS NULL` | D (geração da comissão) |

Reexecução do dia D: `DELETE FROM fato_*_diario WHERE data = D` + `INSERT` (idempotência por reprocessamento).

## 5. Mapeamento de campos

### 5.1 `fato_os_diario`
- Dims: `concessionaria_id`, `departamento_id`, `vendedor_id` ← `os.*`
- `produtivo_id` ← sentinela `''` (produtivo só no fato de serviço)
- `empresa_id` ← `caixas.empresa_faturamento_id` (primeira caixa da OS, se houver; senão `''`)
- `valor_total` ← soma dos itens ativos da OS: `os_servicos.valor_venda_real` **ou** (XOR) valor dos `os_produtos` ativos — **não** usar `os.valor_bruto`/`valor_liquido` como fonte canônica
- `quantidade_os` ← contagem de OS agregadas na chave dimensional do dia
- PK: `(data, concessionaria_id, departamento_id, vendedor_id, produtivo_id, empresa_id)`

### 5.2 `fato_os_servico_diario`
- Só `os_servicos` (OS só-produto **não** entram aqui)
- `servico_id` ← `os_servicos.servico_id` (**grão serviço a serviço**)
- `familia_servico_id` ← `servicos.subgrupo_servico_id` → `subgrupos_servicos` (**não** `grupos_servicos`)
- `produtivo_id` ← `os_servicos.produtivo_id` (ou `''`)
- Demais dims do cabeçalho `os` + `empresa_id` como em 5.1
- `valor_atribuido` ← `valor_venda_real`; `quantidade` ← count na chave
- PK inclui `familia_servico_id` **e** `servico_id`

### 5.3 `fato_os_pagamento_diario`
- Fonte: `caixas` (não `caixas_pendentes` como prova de paga)
- `forma_pagamento_id` ← `caixa_tipo_id`
- `valor_pago` ← `caixas.valor`
- Dims do `os` + empresa do caixa
- PK inclui `forma_pagamento_id`

### 5.4 `fato_comissao_diario`
- `comissionado_id` ← `comissoes.comissionado_id`
- `comissao_tipo_id` ← `comissoes.comissao_tipo_id` (origem; **não** usar `funcionario_tipos` — quem não tem cargo, ex. concessionária/indicador, ainda tem tipo de comissão)
- `valor_comissao` ← fórmula Fase 0
- PK: `(data, comissionado_id, comissao_tipo_id)`

## 6. Reconciliação (US05)

Tabela Postgres `ingest_reconciliacao` (ou log estruturado + tabela):

| Campo | Uso |
|---|---|
| `data`, `familia`, `os_id` (quando aplicável), `esperado`, `obtido`, `diff`, `created_at` | divergência |

Regras:
- **Serviço vs cabeçalho:** para OS cujo evento de criação é D **e** que têm serviços, comparar soma de serviços (todos os itens da OS, não só os fechados em D) com `valor_total` materializado — ou reconciliar no job de serviço quando o último item fecha (preferência de implementação: reconciliar no job `fato_os` as OS criadas em D que já têm todos os serviços fechados; demais = `pendente`)
- **Pagamento vs cabeçalho:** no job de pagamento do dia D, para cada OS paga em D, `SUM(caixas.valor)` vs soma de itens da OS; divergência → registro
- Divergência **não** impede insert dos fatos; só sinaliza (RNF08)

`paga=1` sem `caixas` = inconsistência de origem (Fase 0); não gerar pagamento; pode registrar achado.

## 7. Artefatos

```
faceta/
  __init__.py
  db.py                 # conexões MySQL + Postgres via .env
  ddl.py / sql/ddl_diario.sql
  ingest/
    __main__.py         # CLI
    fato_os.py
    fato_os_servico.py
    fato_os_pagamento.py
    fato_comissao.py
    reconcile.py
requirements.txt        # + psycopg[binary]
documentos/13-fase1-ingestao.md   # como rodar + decisões
```

CLI:
```bash
python -m faceta.ingest --data 2026-08-08
python -m faceta.ingest --data 2026-08-08 --familia os,comissao
```

## 8. Idempotência e erros

- Sem `.env` / Postgres / MySQL → exit ≠ 0
- Falha no meio de uma família → não marcar sucesso; reexecução do dia é segura (delete+insert da família)
- Ordem sugerida no “all”: `os` → `servico` → `pagamento` → `comissao` → reconcile

## 9. Verificação

1. Aplicar DDL no Postgres local
2. Rodar ingest para um dia com volume real
3. Conferir counts > 0 nas quatro tabelas (ou explicar zero legítimo, ex. dia sem comissão)
4. Reexecutar o mesmo dia → mesmas counts, sem duplicar
5. Ver linhas em `ingest_reconciliacao` se houver divergência conhecida
