-- Fase 2: cascata temporal (mesma estrutura do diário; data = início do período)
-- semanal = segunda ISO; mensal = dia 1; semestral = 1/jan ou 1/jul; anual = 1/jan

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_semanal (
    LIKE memoria_materializada.fato_os_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_mensal (
    LIKE memoria_materializada.fato_os_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_semestral (
    LIKE memoria_materializada.fato_os_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_anual (
    LIKE memoria_materializada.fato_os_diario INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_servico_semanal (
    LIKE memoria_materializada.fato_os_servico_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_servico_mensal (
    LIKE memoria_materializada.fato_os_servico_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_servico_semestral (
    LIKE memoria_materializada.fato_os_servico_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_servico_anual (
    LIKE memoria_materializada.fato_os_servico_diario INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_pagamento_semanal (
    LIKE memoria_materializada.fato_os_pagamento_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_pagamento_mensal (
    LIKE memoria_materializada.fato_os_pagamento_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_pagamento_semestral (
    LIKE memoria_materializada.fato_os_pagamento_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_os_pagamento_anual (
    LIKE memoria_materializada.fato_os_pagamento_diario INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS memoria_materializada.fato_comissao_semanal (
    LIKE memoria_materializada.fato_comissao_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_comissao_mensal (
    LIKE memoria_materializada.fato_comissao_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_comissao_semestral (
    LIKE memoria_materializada.fato_comissao_diario INCLUDING ALL
);
CREATE TABLE IF NOT EXISTS memoria_materializada.fato_comissao_anual (
    LIKE memoria_materializada.fato_comissao_diario INCLUDING ALL
);
