-- Fase 5: cache de insights (hipótese textual; separado dos fatos)
CREATE TABLE IF NOT EXISTS memoria_materializada.insights (
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    granularidade TEXT NOT NULL,
    periodo TEXT NOT NULL,
    quebra TEXT NOT NULL DEFAULT '',
    hipotese JSONB NOT NULL,
    erro_reconstrucao NUMERIC,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (entity_type, entity_id, granularidade, periodo, quebra)
);

CREATE INDEX IF NOT EXISTS insights_periodo_idx
    ON memoria_materializada.insights (entity_type, granularidade, periodo);
