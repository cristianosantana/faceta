# Dicionário de Dados — Dimensões e Fatos

## 1. Tabelas de Dimensão

### 1.1 Origem (MySQL `smart` — fonte de verdade)
Validado no live (`documentos/12-levantamento-fase-0.md`). Nomes reais no MySQL são no plural; vendedor e produtivo compartilham `funcionarios` e se discriminam por `funcionario_tipos`.

| Conceito Faceta | Tabela MySQL | Colunas usadas | Observação |
|---|---|---|---|
| `departamento` | `departamentos` | `id`, `nome` | — |
| `concessionaria` | `concessionarias` | `id`, `nome` | CNPJ/razão social etc. não entram no fato |
| `familia_servico` | `subgrupos_servicos` | `id`, `nome`, `grupo_servico_id` | **não** é `grupos_servicos`; via `servicos.subgrupo_servico_id` |
| `familia_produto` | `subgrupos_produtos` | `id`, `nome`, `grupo_produto_id` | espelho para produtos |
| `vendedor` / `produtivo` / `comissionado` | `funcionarios` | `id`, `nome` | IDs nos fatos apontam para cá |
| `forma_pagamento` | `caixa_tipos` | `id`, `nome` | via `caixas.caixa_tipo_id` |
| `empresa` | `empresas` | `id`, `nome` | — |
| `comissao_tipo` | `comissao_tipos` | `id`, `nome` | via `comissoes.comissao_tipo_id` |
| `servico` | `servicos` | `id`, `nome`, `subgrupo_servico_id` | serviço unitário; família = subgrupo |

### 1.2 Snapshot no Postgres (ajuste Fase 1)
Para ler fatos **sem** depender do MySQL em toda consulta, o ingest sincroniza cópias enxutas em `memoria_materializada`:

| Postgres | Origem MySQL |
|---|---|
| `dim_departamento` | `departamentos` |
| `dim_concessionaria` | `concessionarias` |
| `dim_familia_servico` | `subgrupos_servicos` |
| `dim_familia_produto` | `subgrupos_produtos` |
| `dim_servico` | `servicos` (`familia_servico_id` ← `subgrupo_servico_id`) |
| `dim_funcionario` | `funcionarios` |
| `dim_forma_pagamento` | `caixa_tipos` |
| `dim_empresa` | `empresas` |
| `dim_comissao_tipo` | `comissao_tipos` |

Sync: `TRUNCATE` + `INSERT` a cada ingest (ou `python -m faceta.ingest --only-dims`). A origem MySQL continua canônica; o snapshot pode atrasar até o próximo sync.

Cadeia de papel (só na origem): `funcionarios` → `funcionario_cargos` → `cargos.funcionario_tipo_id` → `funcionario_tipos`.

### Estados da OS (critérios analíticos Faceta)
Validado em `12-levantamento-fase-0.md` §5. **Não** usar `os.finalizada` como proxy.

| Estado | Critério | Fonte |
|---|---|---|
| Paga | `os.paga = 1` **e** ≥1 linha em `caixas` | `caixas_pendentes` não prova pagamento |
| Fechada | Itens ativos (`cancelado <> 1`) todos com `fechado = 1` em `os_servicos` **ou** (exclusivo) `os_produtos` | Uma OS só vincula a uma das duas tabelas |
| Cancelada | `os.cancelada = 1` | Flag da origem |
| Paga sem caixa | `os.paga = 1` **e** zero `caixas` | Inconsistência — **não** é cancelada (muitas estão fechadas) |

Detalhe de comissão (origem `comissoes`, momento pagamento vs fechamento de item do produtivo, fórmula de valor): ver `12-levantamento-fase-0.md` §6.

## 2. Tabelas de Fato (Postgres, criadas por este projeto)
Resumo — DDL completo em `05-arquitetura-software-sad.md`, seções 3, 4 e 5.

| Família | Grão | Dimensões | Métrica | Multivalorada por OS? |
|---|---|---|---|---|
| `fato_os` | 1 linha por combinação única de dimensões/dia | concessionaria, departamento, vendedor, produtivo, empresa | `valor_total`, `quantidade_os` | Não |
| `fato_os_servico` | 1 linha por combinação (dims + família + **serviço**)/dia | + `familia_servico_id` (`subgrupos_servicos`), + `servico_id` | `valor_atribuido`, `quantidade` | Sim; grão serviço a serviço |

| `fato_os_pagamento` | 1 linha por combinação (dimensões + forma)/dia | + `forma_pagamento_id` | `valor_pago` | Sim (uma OS pode ter mais de uma forma de pagamento) |
| `fato_comissao` | 1 linha por comissionado/tipo/dia | `comissionado_id`, `comissao_tipo_id` | `valor_comissao` | Ingerido pronto; nomes iguais ao MySQL |

Cada família tem 5 tabelas (uma por granularidade: `_diario`, `_semanal`, `_mensal`, `_semestral`, `_anual`), mesma estrutura de colunas. Cascata: cada agregada soma o `_diario` no intervalo (não semana→mês); completude parcial; ver `14-fase2-cascata.md`.

Nomes de dimensão resolvem via `dim_*` no Postgres (`faceta/query/dims.py`): o motor e o ask preenchem `entity_nome` / `quebra_nome` a partir dos IDs.

## 3. Tabela de Cache de Insights (Postgres, criada por este projeto)
| Coluna | Descrição |
|---|---|
| `entity_type` (PK) | Dimensão que é o sujeito do insight |
| `entity_id` (PK) | Valor da dimensão |
| `granularidade` (PK) | Nível de tempo do insight |
| `periodo` (PK) | Período coberto |
| `quebra` (PK) | Dimensão de quebra, se houver (nulo = agregado total) |
| `hipotese` (JSONB) | `assunto`, `descricao`, `confianca` — narrado pelo LLM |

## 4. Mapas Fixos (código, não tabela — usados pelo Motor de Consulta Genérico)
- `DIMENSAO_TO_COLUNA`: nome lógico de dimensão → coluna real (allowlist de segurança)
- `entity_type → família de fato`: vem do `contrato.yaml` (ver `05-arquitetura-software-sad.md`, seção 6)
