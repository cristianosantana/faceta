# Fase 1 — Ingestão diária

## Como rodar

```bash
cd /Users/cristianosoaresdesantana/code/faceta
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# .env com MYSQL_* e POSTGRES_URL

PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-07-31
PYTHONPATH=. .venv/bin/python -m faceta.ingest              # ontem
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-07-31 --familia comissao
PYTHONPATH=. .venv/bin/python -m faceta.ingest --only-dims  # só dimensões
```

## Decisões vigentes

| Tema | Decisão |
|---|---|
| Bancos | Dimensões: origem MySQL + snapshot Postgres `dim_*`. Fatos: só Postgres `memoria_materializada` |
| Data do fato | **Evento por família** (não o mesmo “dia”): `fato_os` = abertura `DATE(created_at)`; `fato_os_servico` = fechamento do item; `fato_os_pagamento` = pagamento; `fato_comissao` = `DATE(comissoes.created_at)`. Ver `10-dicionario-dados.md` §2.1 |
| Idempotência | `DELETE` do dia D + `INSERT` por família |
| `fato_os.valor_total` | Soma itens (`os_servicos` XOR `os_produtos`); `produtivo_id` sentinela `''` (produtivo real só em `fato_os_servico`); `empresa_id` via caixa |
| `fato_os_servico` | Grão **serviço a serviço**: `servico_id` + `familia_servico_id` (= `subgrupos_servicos`, via `servicos.subgrupo_servico_id`) |
| `fato_comissao` | `comissionado_id` + `comissao_tipo_id` (nomes MySQL); tipo **não** vem de cargo |
| Reconciliação | `ingest_reconciliacao` (não bloqueia insert) |

### Snapshots `dim_*`

| Postgres | MySQL |
|---|---|
| `dim_departamento` | `departamentos` |
| `dim_concessionaria` | `concessionarias` |
| `dim_familia_servico` | `subgrupos_servicos` |
| `dim_familia_produto` | `subgrupos_produtos` |
| `dim_servico` | `servicos` |
| `dim_funcionario` | `funcionarios` |
| `dim_forma_pagamento` | `caixa_tipos` |
| `dim_empresa` | `empresas` |
| `dim_comissao_tipo` | `comissao_tipos` |

## Exemplos de leitura

```sql
-- OS por concessionária
SELECT f.data, d.nome AS concessionaria, f.valor_total
FROM memoria_materializada.fato_os_diario f
JOIN memoria_materializada.dim_concessionaria d ON d.id = f.concessionaria_id
WHERE f.data = '2026-07-31';

-- Serviço a serviço (com família = subgrupo)
SELECT s.nome AS servico, fam.nome AS familia, SUM(x.valor_atribuido) AS valor
FROM memoria_materializada.fato_os_servico_diario x
JOIN memoria_materializada.dim_servico s ON s.id = x.servico_id
LEFT JOIN memoria_materializada.dim_familia_servico fam ON fam.id = x.familia_servico_id
WHERE x.data = '2026-07-31'
GROUP BY 1, 2
ORDER BY valor DESC;
```

## Histórico de ajustes (ainda Fase 1)

1. Snapshots `dim_*` no Postgres (evitar join MySQL em toda leitura)
2. Comissão: `comissionado_id` / `comissao_tipo_id` (fim de `beneficiario_*` / `desconhecido` via cargo)
3. Família = `subgrupos_servicos` / `subgrupos_produtos` (não `grupos_*`)
4. `servico_id` em `fato_os_servico` (grão serviço a serviço) + `dim_servico`

## Verificado

Dia `2026-07-31` (após ajustes): fato_os ~66, fato_os_servico **236** (com `servico_id`), pagamento ~56, comissao ~165; dims syncadas; reexecução idempotente.
