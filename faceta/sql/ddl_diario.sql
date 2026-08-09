-- Fase 1: fatos diários no Postgres
CREATE SCHEMA IF NOT EXISTS memoria_materializada;

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_diario (
    data DATE NOT NULL,
    concessionaria_id TEXT NOT NULL DEFAULT '',
    departamento_id TEXT NOT NULL DEFAULT '',
    vendedor_id TEXT NOT NULL DEFAULT '',
    produtivo_id TEXT NOT NULL DEFAULT '',
    empresa_id TEXT NOT NULL DEFAULT '',
    valor_total NUMERIC NOT NULL,
    quantidade_os INTEGER NOT NULL,
    PRIMARY KEY (data, concessionaria_id, departamento_id, vendedor_id, produtivo_id, empresa_id)
);

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_servico_diario (
    data DATE NOT NULL,
    concessionaria_id TEXT NOT NULL DEFAULT '',
    departamento_id TEXT NOT NULL DEFAULT '',
    vendedor_id TEXT NOT NULL DEFAULT '',
    produtivo_id TEXT NOT NULL DEFAULT '',
    empresa_id TEXT NOT NULL DEFAULT '',
    familia_servico_id TEXT NOT NULL DEFAULT '',
    servico_id TEXT NOT NULL DEFAULT '',
    valor_atribuido NUMERIC NOT NULL,
    quantidade INTEGER NOT NULL,
    PRIMARY KEY (data, concessionaria_id, departamento_id, vendedor_id, produtivo_id, empresa_id, familia_servico_id, servico_id)
);

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_pagamento_diario (
    data DATE NOT NULL,
    concessionaria_id TEXT NOT NULL DEFAULT '',
    departamento_id TEXT NOT NULL DEFAULT '',
    vendedor_id TEXT NOT NULL DEFAULT '',
    produtivo_id TEXT NOT NULL DEFAULT '',
    empresa_id TEXT NOT NULL DEFAULT '',
    forma_pagamento_id TEXT NOT NULL DEFAULT '',
    valor_pago NUMERIC NOT NULL,
    PRIMARY KEY (data, concessionaria_id, departamento_id, vendedor_id, produtivo_id, empresa_id, forma_pagamento_id)
);

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_comissao_diario (
    data DATE NOT NULL,
    comissionado_id TEXT NOT NULL,
    comissao_tipo_id TEXT NOT NULL,
    valor_comissao NUMERIC NOT NULL,
    PRIMARY KEY (data, comissionado_id, comissao_tipo_id)
);

CREATE TABLE IF NOT EXISTS memoria_materializada.ingest_reconciliacao (
    id BIGSERIAL PRIMARY KEY,
    data DATE NOT NULL,
    familia TEXT NOT NULL,
    os_id BIGINT,
    esperado NUMERIC,
    obtido NUMERIC,
    diff NUMERIC,
    detalhe TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ingest_reconciliacao_data_idx
    ON memoria_materializada.ingest_reconciliacao (data, familia);

-- Snapshots de dimensão no Postgres (ajuste Fase 1): fatos guardam IDs; nomes resolvem aqui.
-- Fonte de verdade continua no MySQL; sync = cópia enxuta (id, nome [, ativo]).

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_departamento (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_concessionaria (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_familia_servico (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    grupo_servico_id TEXT,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_familia_produto (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    grupo_produto_id TEXT,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_funcionario (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_forma_pagamento (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_empresa (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_comissao_tipo (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memoria_materializada.dim_servico (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    familia_servico_id TEXT,
    ativo BOOLEAN,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
