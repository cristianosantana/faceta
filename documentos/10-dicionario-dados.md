# Dicionário de Dados — Dimensões e Fatos

## 1. Tabelas de Dimensão (MySQL, externas — este projeto não as cria)
Validado no live (`documentos/12-levantamento-fase-0.md`). Nomes reais no MySQL são no plural; vendedor e produtivo compartilham `funcionarios` e se discriminam por `funcionario_tipos`.

| Conceito Faceta | Tabela MySQL | Colunas usadas | Observação |
|---|---|---|---|
| `departamento` | `departamentos` | `id`, `nome` | — |
| `concessionaria` | `concessionarias` | `id`, `nome` | CNPJ/razão social etc. não entram no fato |
| `familia_servico` | `grupos_servicos` | `id`, `nome` | via `servicos.grupo_servico_id` |
| `vendedor` | `funcionarios` | `id`, `nome` | `os.vendedor_id`; tipo via `funcionario_tipos` |
| `produtivo` | `funcionarios` | `id`, `nome` | `os_servicos.produtivo_id`; tipo via `funcionario_tipos` |
| `forma_pagamento` | `caixa_tipos` | `id`, `nome` | via `caixas.caixa_tipo_id` |
| `empresa` | `empresas` | `id`, `nome` | — |

Cadeia de papel: `funcionarios` → `funcionario_cargos` → `cargos.funcionario_tipo_id` → `funcionario_tipos`.

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
| `fato_os_servico` | 1 linha por combinação (dimensões + serviço)/dia | + `familia_servico_id` | `valor_atribuido`, `quantidade` | Sim (uma OS pode ter mais de um serviço) |
| `fato_os_pagamento` | 1 linha por combinação (dimensões + forma)/dia | + `forma_pagamento_id` | `valor_pago` | Sim (uma OS pode ter mais de uma forma de pagamento) |
| `fato_comissao` | 1 linha por beneficiário/tipo/dia | `beneficiario_tipo`, `beneficiario_id`, `tipo_comissao` | `valor_comissao` | Ingerido pronto, sem cálculo |

Cada família tem 5 tabelas (uma por granularidade: `_diario`, `_semanal`, `_mensal`, `_semestral`, `_anual`), mesma estrutura de colunas em cascata.

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
