# Fase 0 — Levantamento MySQL (Design)

**Data:** 2026-08-09  
**Status:** implementado (relatório em `documentos/12-levantamento-fase-0.md`)  
**Abordagem:** script de introspecção live + relatório

## 1. Objetivo

Fechar os três pré-requisitos da Fase 0 (`documentos/11-roadmap.md`) antes de qualquer ingestão:

1. Validar o schema real das tabelas cadastrais no MySQL
2. Mapear o schema exato das tabelas de comissão na origem
3. Confirmar frequência / critério de disponibilidade dos dados (quando e sob quais flags a OS entra em cada recorte analítico)

**Critério de saída:** relatório gerado com schema validado, regras de estado documentadas, e `[PENDENTE]` de schema/frequência removidos dos docs de origem — Fase 1 desbloqueada.

## 2. Fora de escopo

- DDL Postgres, crons, ingestão, cascata, contrato YAML, LLM, TensorFlow
- Versionar senha ou `.env` real no repositório
- Escolher agendador de cron ou infra de produção

## 3. Fonte e acesso

- Database: `smart` em MySQL (`127.0.0.1:3306`)
- Credenciais via `.env` (não commitado); template em `.env.example`
- Inventário de colunas de referência: `documentos/tabelas_mysql.sql` (lista de `SELECT` por tabela; o live é a fonte de verdade de tipos/nulls)

## 4. Mapeamento origem → Faceta

| Conceito Faceta | Tabela MySQL | Colunas-chave | Observação |
|---|---|---|---|
| `departamento` | `departamentos` | `id`, `nome` | plural no MySQL |
| `concessionaria` | `concessionarias` | `id`, `nome` | campos extras (CNPJ etc.) não entram no fato |
| `familia_servico` | `subgrupos_servicos` | `id`, `nome`, `grupo_servico_id` | via `servicos.subgrupo_servico_id` — **não** `grupos_servicos` |
| `familia_produto` | `subgrupos_produtos` | `id`, `nome`, `grupo_produto_id` | espelho produtos |
| `vendedor` | `funcionarios` | `id`, `nome` | `os.vendedor_id` → funcionário; papel via `funcionario_tipos` (cadeia `funcionario_cargos` → `cargos.funcionario_tipo_id`) |
| `produtivo` | `funcionarios` | `id`, `nome` | `os_servicos.produtivo_id` → funcionário; mesmo cadastro, papel distinto em `funcionario_tipos` |
| `servico` | `servicos` | `id`, `nome`, `subgrupo_servico_id` | entra no fato como `servico_id` |
| `funcionario_tipos` | `funcionario_tipos` | `id`, `nome` | discrimina vendedor vs produtivo (e demais tipos); incluir no levantamento |
| `forma_pagamento` | `caixa_tipos` | `id`, `nome` | via `caixas.caixa_tipo_id` |
| `empresa` | `empresas` | `id`, `nome` | nível de faturamento / empresa |
| cabeçalho OS | `os` | `id`, valores, FKs, flags de estado, datas | grão de `fato_os` |
| itens serviço | `os_servicos` | `os_id`, `servico_id`, `produtivo_id`, valores, `fechado` | grão de `fato_os_servico` (serviço a serviço) |
| itens pagamento | `caixas` | `os_id`, `caixa_tipo_id`, `valor` | grão de `fato_os_pagamento`; `caixas_pendentes` = cobrança pendente, **não** prova de paga |
| comissão | `comissoes` | `comissionado_id`, `comissao_tipo_id`, componentes de valor, `os_servico_id` / `os_produto_id` | satélites: `comissao_tipos`, `comissao_periodos`, `comissao_pagamentos` |

**Papel vendedor/produtivo:** ambos são linhas em `funcionarios`. O tipo vem de `funcionario_tipos`, ligado por `funcionario_cargos` → `cargos.funcionario_tipo_id`. O script lista os nomes em `funcionario_tipos` e valida essa cadeia no live. Tabelas de suporte da cadeia (`funcionario_cargos`, `cargos`) entram na introspecção junto com as do mapeamento.

## 5. Regras de estado da OS

Definidas pelo negócio; o script valida com contagens. **Não** usar `os.finalizada` como proxy de paga∩fechada.

| Estado | Critério | Data sugerida para o dia |
|---|---|---|
| Abertas | OS criadas | `os.created_at` |
| Pagas | `os.paga = 1` **e** existe ≥1 linha em `caixas` | `os.data_pagamento` |
| Fechadas | Itens ativos (`cancelado <> 1`) todos com `fechado = 1` em `os_servicos` **ou** (exclusivo) `os_produtos` | `os.data_fechamento` (confrontar flag `os.fechada`) |
| Canceladas | `os.cancelada = 1` | `os.data_cancelamento` |
| Paga sem caixa (inconsistência) | `os.paga = 1` **e** zero linhas em `caixas` | **Não** é cancelada; maioria costuma estar fechada — sinalizar qualidade de origem |

Premissas:
- Uma OS vincula-se a **apenas uma** família de itens: `os_servicos` **ou** `os_produtos` (não ambas com itens ativos).
- `caixas_pendentes` **não** conta como prova de pagamento.
- Flag `os.finalizada` permanece no schema de origem, mas **não** entra na definição analítica do Faceta.

Checagens no live: divergência `os.fechada` vs fechada derivada; contagem de `paga=1` sem `caixas` (e quantas dessas estão fechadas); OS com itens ativos nas duas tabelas (viola exclusividade).

## 6. Comissão — momento de geração e mapeamento para `fato_comissao`

### 6.1 Momento de geração (regra de negócio)

- **Regra geral:** comissões são geradas **no pagamento** da OS. Por isso é esperado existir OS **fechada sem comissão** (ainda não paga).
- **Exceção — produtivo:** comissão do produtivo é gerada **ao fechar serviços** (`os_servicos.fechado` / fechamento do serviço), não no pagamento.
- Consequência para a Fase 1: o cron de `fato_comissao` **não** deve assumir 1:1 com `os.fechada`; deve ler `comissoes` já materializadas e aceitar OS fechada sem linha de comissão (exceto o caso produtivo, onde a comissão pode existir antes do pagamento).

O script deve reportar, nos últimos 14 dias: contagem de OS fechadas sem nenhuma `comissoes` ligada (via `os_servicos`/`os_produtos`); e amostra de comissões de produtivo vs demais tipos.

### 6.2 Mapeamento para `fato_comissao`

- `comissionado_id` ← `comissoes.comissionado_id`
- `comissao_tipo_id` ← `comissoes.comissao_tipo_id` (sempre presente com comissionado; **não** usar `funcionario_tipos`)
- `valor_comissao` ← fórmula dos componentes (`valor_dentro`, `valor_fora`, `valor_combo`, `valor_compensado_permuta`, `comissao_couro`)

Comissão é cópia/agregação de valores já calculados — sem reimplementar regra de negócio.

## 7. Artefatos

| Artefato | Papel |
|---|---|
| `scripts/fase0_levantamento.py` | introspecção + geração do relatório |
| `.env.example` | `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD` |
| `.gitignore` | ignora `.env` |
| `requirements.txt` | `pymysql`, `python-dotenv` |
| `documentos/12-levantamento-fase-0.md` | saída gerada (schema, mapeamento, contagens, fórmula de comissão, frequência) |
| updates em `10-dicionario-dados.md`, `05-arquitetura-software-sad.md` (§5), `07-guia-implantacao.md` (§4.6) | remover `[PENDENTE]` de schema/frequência com o conteúdo confirmado |

## 8. Comportamento do script

1. Carregar `.env`
2. Conectar ao MySQL `smart`
3. Para cada tabela do mapeamento (§4): ler `INFORMATION_SCHEMA.COLUMNS` (e keys quando disponível)
4. Assertar presença das colunas/FKs críticas; falhar com mensagem clara se faltar algo essencial
5. Amostras: nomes de dimensões; valores de `funcionario_tipos`; distribuição de `comissao_tipos`; amostra de `comissoes` com componentes de valor
6. Contagens dos últimos 14 dias: abertas / pagas (`paga`+`caixas`) / fechadas derivadas / canceladas (`os.cancelada`); inconsistência `paga=1` sem `caixas`; divergência vs `os.fechada`; exclusividade serviços×produtos
7. Contagens de alinhamento comissão × estado: OS fechadas (derivadas) sem comissão; breakdown por tipo de funcionário
8. Escrever `documentos/12-levantamento-fase-0.md` e imprimir resumo no stdout

## 9. Tratamento de erro

- Sem `.env` ou conexão recusada → exit ≠ 0 com mensagem acionável
- Tabela esperada ausente → registrar no relatório como bloqueio e exit ≠ 0
- Divergências de flag vs estado derivado (qualquer contagem > 0) → registrar no relatório (não bloqueia escrita; marca risco para Fase 1)

## 10. Teste / verificação

- Rodar o script contra o MySQL local e confirmar geração do relatório
- Conferir que o relatório cobre os 3 itens do roadmap Fase 0
- Conferir que docs atualizados não deixam `[PENDENTE]` de schema de dimensão, schema de comissão ou frequência de leitura
