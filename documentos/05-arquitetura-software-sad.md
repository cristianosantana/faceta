# Documento de Arquitetura de Software (SAD)

## 0. Stack Tecnológico
| Camada | Tecnologia | Papel |
|---|---|---|
| Origem dos dados | **MySQL** | OS, itens, comissões, cadastros (fonte de verdade das dimensões) |
| Destino dos fatos | **Postgres** | `fato_*` + snapshots `dim_*` (id/nome) + `insights` |
| Ingestão e cascata | **CLI / execução manual** (por hora nesta fase; Airflow/SO `[PENDENTE]` para produção) | Lê MySQL → grava fatos e sync `dim_*` no Postgres |
| Motor de consulta genérico | **Python + SQL parametrizado** | Monta e executa as consultas de agregação, comparação e ranking em tempo de leitura, usando mapas fixos como allowlist |
| Detecção de insights | **TensorFlow** | Autoencoder / rede recorrente-atenção / clusterização sobre séries reconstruídas pelo motor genérico |
| Entendimento de pergunta e narração | **LLM** (provedor a definir) | Traduz pergunta em parâmetros de consulta; narra o resultado e os insights em linguagem natural |
| Contrato | **YAML versionado** | Allowlist de `entity_types`, famílias de fato, quebras e comparações válidas |

## 1. Visão Geral
Uma OS tem dimensões de dois tipos: **únicas** (concessionária, departamento, vendedor, produtivo, empresa — sempre uma por OS) e **multivaloradas** (serviço e forma de pagamento — uma OS pode ter mais de um serviço e mais de uma forma de pagamento). Forçar tudo numa linha só, como no desenho anterior, soma valor errado sempre que uma OS tem mais de um serviço ou mais de uma forma de pagamento. A correção é separar em **três famílias de fato**, cada uma com sua própria cascata por tempo:

```mermaid
flowchart LR
    A[MySQL\nOS + itens + dimensões + comissões] -->|cron de ingestão| B[fato_os\ncabeçalho, dimensões únicas]
    A -->|cron de ingestão| C[fato_os_servico\n1 linha por OS x serviço]
    A -->|cron de ingestão| D[fato_os_pagamento\n1 linha por OS x forma pagto]
    A -->|cron de ingestão| E2[fato_comissao\nlido pronto do MySQL]
    B -->|cascata| B2[... semanal/mensal/semestral/anual]
    C -->|cascata| C2[... semanal/mensal/semestral/anual]
    D -->|cascata| D2[... semanal/mensal/semestral/anual]
    E2 -->|cascata| E3[... semanal/mensal/semestral/anual]
    U[Pergunta do usuário] --> Q[LLM: Entendimento da Pergunta]
    Q -->|entity_type, granularidade, quebra, comparação| M[Motor de Consulta Genérico\nroteia p/ o fato certo]
    M --> B2
    M --> C2
    M --> D2
    M --> E3
    M --> N[LLM: Narrador da Resposta]
    N --> R[Resposta ao usuário]
    B --> J[Job de Insights\nvia Motor Genérico]
    C --> J
    D --> J
    E2 --> J
    J --> TF[Modelo TensorFlow]
    TF -->|variação notável| GI[LLM Narrador de Insight]
    GI --> IT[(insights)]
```

## 2. Modelo de Dados (DER)

```mermaid
erDiagram
    FATO_OS {
        date data
        string concessionaria_id FK
        string departamento_id FK
        string vendedor_id FK
        string produtivo_id FK
        string empresa_id FK
        numeric valor_total
        integer quantidade_os
    }
    FATO_OS_SERVICO {
        date data
        string concessionaria_id FK
        string departamento_id FK
        string vendedor_id FK
        string produtivo_id FK
        string empresa_id FK
        string familia_servico_id FK
        string servico_id FK
        numeric valor_atribuido
        integer quantidade
    }
    FATO_OS_PAGAMENTO {
        date data
        string concessionaria_id FK
        string departamento_id FK
        string vendedor_id FK
        string produtivo_id FK
        string empresa_id FK
        string forma_pagamento_id FK
        numeric valor_pago
    }
    FATO_COMISSAO {
        date data
        string comissionado_id
        string comissao_tipo_id
        numeric valor_comissao
    }
    INSIGHTS {
        string entity_type PK
        string entity_id PK
        string granularidade PK
        string periodo PK
        string quebra PK
        jsonb hipotese
    }

    FATO_OS ||--o{ FATO_OS_SERVICO : "itemização (mesma OS)"
    FATO_OS ||--o{ FATO_OS_PAGAMENTO : "split de pagamento (mesma OS)"
    FATO_OS ||--o{ FATO_COMISSAO : "gera cálculo de comissão"
```

> As três famílias de fato (`FATO_OS`, `FATO_OS_SERVICO`, `FATO_OS_PAGAMENTO`) carregam as mesmas dimensões únicas (concessionária, departamento, vendedor, produtivo, empresa) de forma redundante — cada uma é autossuficiente para seu próprio `GROUP BY`, sem precisar de join entre elas. Em `FATO_OS_SERVICO`, `familia_servico_id` aponta para **`subgrupos_servicos`** (não `grupos_servicos`) e `servico_id` para o serviço unitário — grão serviço a serviço. `forma_pagamento_id` só existe em `FATO_OS_PAGAMENTO`. **Cruzar serviço com forma de pagamento** (ex.: "quanto de Filme Solar foi pago no PIX") não é suportado: confirmado que a origem no MySQL guarda serviços e formas de pagamento como duas listas independentes por OS, sem vínculo direto entre um serviço específico e uma forma específica — cruzar as duas exigiria alocar valor arbitrariamente, então essa combinação fica permanentemente fora do escopo, não é uma pendência a resolver.

## 3. Camada 1 — Fatos Diários (três famílias, dimensões únicas redundantes)
```sql
CREATE TABLE fato_os_diario (
    data DATE NOT NULL,
    concessionaria_id TEXT, departamento_id TEXT, vendedor_id TEXT, produtivo_id TEXT, empresa_id TEXT,
    valor_total NUMERIC NOT NULL,
    quantidade_os INTEGER,
    PRIMARY KEY (data, concessionaria_id, departamento_id, vendedor_id, produtivo_id, empresa_id)
);

CREATE TABLE fato_os_servico_diario (
    data DATE NOT NULL,
    concessionaria_id TEXT, departamento_id TEXT, vendedor_id TEXT, produtivo_id TEXT, empresa_id TEXT,
    familia_servico_id TEXT NOT NULL,  -- subgrupos_servicos.id
    servico_id TEXT NOT NULL,           -- servicos.id (grão serviço a serviço)
    valor_atribuido NUMERIC NOT NULL,
    quantidade INTEGER,
    PRIMARY KEY (data, concessionaria_id, departamento_id, vendedor_id, produtivo_id, empresa_id, familia_servico_id, servico_id)
);

CREATE TABLE fato_os_pagamento_diario (
    data DATE NOT NULL,
    concessionaria_id TEXT, departamento_id TEXT, vendedor_id TEXT, produtivo_id TEXT, empresa_id TEXT,
    forma_pagamento_id TEXT NOT NULL,
    valor_pago NUMERIC NOT NULL,
    PRIMARY KEY (data, concessionaria_id, departamento_id, vendedor_id, produtivo_id, empresa_id, forma_pagamento_id)
);
```
`SUM(valor_atribuido)` em `fato_os_servico_diario`, agrupado por OS, deve bater com `valor_total` de `fato_os_diario` para a mesma OS — essa reconciliação é uma checagem de qualidade de dado na ingestão, não uma regra do banco. O mesmo vale para `fato_os_pagamento_diario`.

## 4. Camada 2 — Cascata por Tempo (cada família, independente)
Mesmo padrão de antes, aplicado três vezes:
```
fato_os_semanal   ← soma de fato_os_diario da semana
fato_os_servico_semanal ← soma de fato_os_servico_diario da semana
fato_os_pagamento_semanal ← soma de fato_os_pagamento_diario da semana
... mensal, semestral, anual, mesmo padrão para as três famílias
```
Insert-only, sem merge, mesma lógica de backfill pontual em caso de dia faltante.

## 5. Camada 3 — Fato de Comissão (ingerido, não calculado)
Diferente do que parecia inicialmente, comissão **não precisa ser calculada por este projeto** — já existem tabelas de comissão prontas no MySQL de origem. `fato_comissao` é só mais um alvo de ingestão, igual a `fato_os`:
```sql
CREATE TABLE fato_comissao_diario (
    data DATE NOT NULL,
    comissionado_id TEXT NOT NULL,   -- comissoes.comissionado_id
    comissao_tipo_id TEXT NOT NULL,  -- comissoes.comissao_tipo_id → comissao_tipos
    valor_comissao NUMERIC NOT NULL,
    PRIMARY KEY (data, comissionado_id, comissao_tipo_id)
);
```
O cron de ingestão lê `comissoes` no MySQL (satélites: `comissao_tipos`, `comissao_periodos`, `comissao_pagamentos`) e insere aqui, mesmo padrão de idempotência de `fato_os`. Cascata por tempo se aplica do mesmo jeito.

Mapeamento confirmado no levantamento (`12-levantamento-fase-0.md`):
- `comissionado_id` ← `comissoes.comissionado_id` (mesmo nome da origem)
- `comissao_tipo_id` ← `comissoes.comissao_tipo_id` (sempre preenchido quando há comissionado; **não** derivar de `funcionario_tipos`/cargo — concessionária/indicador não têm cargo)
- `valor_comissao` ← `COALESCE(valor_dentro,0)+COALESCE(valor_fora,0)+COALESCE(valor_combo,0)+COALESCE(valor_compensado_permuta,0)+COALESCE(comissao_couro,0)`
- Momento: comissão geral no **pagamento**; comissão do **produtivo** ao **fechar itens** — OS fechada sem comissão é esperado; não assumir 1:1 com fechada derivada
- Estados da OS para ingestão: ver `10-dicionario-dados.md` (paga / fechada derivada / cancelada por flag; `paga=1` sem `caixas` é inconsistência); não usar `os.finalizada` como paga∩fechada

## 6. Camada 4 — Contrato (agora também roteia para a família de fato certa)
```yaml
entity_types:
  concessionaria: { fato: fato_os, coluna: concessionaria_id, quebras_validas: [departamento, vendedor, produtivo] }
  departamento:   { fato: fato_os, coluna: departamento_id,   quebras_validas: [concessionaria, vendedor] }
  vendedor:       { fato: fato_os, coluna: vendedor_id,       quebras_validas: [concessionaria, departamento] }
  produtivo:      { fato: fato_os, coluna: produtivo_id,      quebras_validas: [concessionaria, departamento] }
  familia_servico: { fato: fato_os_servico, coluna: familia_servico_id, quebras_validas: [concessionaria, departamento, servico] }
  servico:        { fato: fato_os_servico, coluna: servico_id, quebras_validas: [concessionaria, departamento, familia_servico] }
  forma_pagamento: { fato: fato_os_pagamento, coluna: forma_pagamento_id, quebras_validas: [concessionaria, departamento] }
```
Note que `servico` e `forma_pagamento` **não aparecem como quebra válida um do outro** — reflete a limitação da seção 2 (sem itemização cruzada na origem, essa combinação não existe).

## 7. Motor de Consulta Genérico
```python
DIMENSAO_TO_COLUNA = {
    "concessionaria": "concessionaria_id", "departamento": "departamento_id",
    "vendedor": "vendedor_id", "produtivo": "produtivo_id",
    "familia_servico": "familia_servico_id", "servico": "servico_id", "forma_pagamento": "forma_pagamento_id",
}
GRANULARIDADE_SUFIXO = {"diario": "_diario", "semanal": "_semanal", "mensal": "_mensal",
                        "semestral": "_semestral", "anual": "_anual"}

def tabela(entity_type, granularidade, contrato):
    fato_base = contrato["entity_types"][entity_type]["fato"]   # ex.: 'fato_os_servico'
    return fato_base + GRANULARIDADE_SUFIXO[granularidade]        # ex.: 'fato_os_servico_mensal'
```
```sql
SELECT {coluna_entity_id} AS entity_id, SUM({coluna_valor}) AS valor
FROM {tabela_resolvida}
WHERE data/periodo = :periodo [AND {coluna_quebra} = :quebra_valor]
GROUP BY {coluna_entity_id} [, {coluna_quebra}];
```
`{coluna_valor}` também vem do contrato (`valor_total`, `valor_atribuido` ou `valor_pago`, conforme a família). O roteamento pra tabela certa acontece automaticamente a partir do `entity_type` — o LLM de entendimento de pergunta nunca precisa saber que existem três famílias de fato, só devolve `entity_type`.

## 8. Comparações e Ranking (tempo de leitura, mesma lógica de antes)
Sem mudança de princípio — a mesma consulta roda duas vezes (período pedido + período de referência) para comparações, e sem filtro de `entity_id` com `RANK()` para ranking. A única diferença é que agora a consulta pode mirar em qualquer uma das três famílias, resolvida pelo contrato.

## 9. Entendimento de Pergunta
Sem mudança de princípio: LLM traduz a pergunta em `entity_type`, `entity_id` (opcional), `granularidade`, `periodo`, `quebra`, `comparacao`. A resolução de qual família de fato consultar é interna do motor genérico (seção 7), nunca exposta à camada de entendimento.

## 10. Insights (deep learning, roda em lote)
Mesmo desenho de antes — reconstrói série via motor genérico, aplica TensorFlow, narra condicionalmente, cacheia em `insights`. Agora o job de insights também pode olhar `fato_comissao` como uma quarta fonte de série (ex.: detectar comissão fora do padrão).

## 11. Projeto Independente
Este sistema não reutiliza nem depende do `orion_v3` — é um projeto novo, com base de dados, contrato e pipeline próprios. Não há fallback nem convivência operacional entre os dois.
