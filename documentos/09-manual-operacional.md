# Manual Operacional

> Este sistema não tem interface de usuário final própria nesta fase — quem opera é a equipe técnica e, indiretamente, o narrator/chat público que consulta via o motor genérico. Este manual substitui o "Manual do Usuário Final" tradicional por um guia operacional.

## 1. Rotina Diária Esperada
1. `python -m faceta.ops health` — conferir MySQL/Postgres/contrato
2. Ingestão do dia: `python -m faceta.ingest --data YYYY-MM-DD` (ou `faceta.ops backfill`)
3. Cascata no fechamento da janela: `python -m faceta.cascata --granularidade semanal --periodo …`
4. Insights (opcional): `python -m faceta.insights run --periodo …`
5. `python -m faceta.ops doctor` e `python -m faceta.ops metrics` — gaps, reconciliação, llm_calls≤2
6. Perguntas via `python -m faceta.ask "…"` (motor + lookup de insights)

### Backfill por mês (`YYYY-MM`)
```bash
PYTHONPATH=. python scripts/mes_ingest.py 2026-07
PYTHONPATH=. python scripts/mes_cascata.py 2026-07          # semanal (semanas do mês) + mensal
PYTHONPATH=. python scripts/mes_insights.py 2026-07         # train+run × todos entity_types × semanas
# --dry-run em qualquer um; cascata --force; insights --force-llm --limit 5 --entity-type vendedor,servico
```


## 2. Como Adicionar um Novo Tipo de Entidade (entity_type)
1. Confirmar a qual família de fato a dimensão pertence (`fato_os` se for única por OS; se for multivalorada como serviço/pagamento, precisa de uma família própria nova — ver seção 3)
2. Adicionar a entrada correspondente em `contrato.yaml`, com a família, coluna de agrupamento, quebras e comparações válidas
3. Validar com uma consulta de teste ao motor genérico (TC05 do plano de testes) antes de liberar para perguntas reais

## 3. Como Adicionar uma Nova Dimensão
**Se a dimensão é sempre única por OS** (como concessionária, departamento, vendedor, empresa): adicionar a coluna em `fato_os` e em todas as tabelas de cascata dessa família.
**Se a dimensão pode ser múltipla por OS** (como serviço, **produtivo**, pagamento): criar/usar família de fato no grão certo (`fato_os_servico` / `fato_os_pagamento`), com as dimensões únicas replicadas mais a dimensão multivalorada — e sua própria cascata por tempo.
Em ambos os casos:
1. Confirmar que a dimensão já existe como tabela cadastral no MySQL com ID estável
2. Adicionar a dimensão ao mapa fixo `DIMENSAO_TO_COLUNA` do motor genérico — sem essa entrada, a dimensão nunca pode ser usada em consulta, por segurança
3. Garantir que a ingestão diária passa a preencher a nova coluna/família
4. Adicionar a dimensão como quebra válida no contrato dos `entity_types` relevantes, avaliando se cruzamentos fazem sentido dado como a origem estrutura o dado (ver o caso servico × forma_pagamento como referência de quando **não** permitir)

## 4. Diagnóstico de Problemas Comuns
| Sintoma | Causa provável | Ação |
|---|---|---|
| Consulta rejeitada com `entity_type`/quebra aparentemente válidos | Contrato desatualizado ou allowlist (`DIMENSAO_TO_COLUNA`) sem a dimensão nova | Verificar `contrato.yaml` e o mapa fixo do motor genérico |
| Divergência entre `fato_os` e soma de `fato_os_servico`/`fato_os_pagamento` | Item de serviço/pagamento faltando ou duplicado na origem | Verificar a extração da OS específica no MySQL antes de reprocessar |
| Valores duplicados/incorretos em qualquer fato diário | Ingestão não idempotente ou reprocessamento indevido | Verificar chave primária composta e lógica de reexecução |
| `insights` sempre vazio para um `entity_type` | Job de insights não está reconstruindo série pra esse tipo, ou limiar de detecção alto demais | Revisar `INSIGHT_DETECTION_THRESHOLD` e se o `entity_type` está incluído no job |
| Semana/mês com dado incompleto | Ingestão diária não rodou para algum dia | Cascata aceita parcial (soma o que houver); para completar, reingerir o dia faltante e rodar cascata com `--force` no período |
| Comissão divergente da origem | Job de ingestão aplicando alguma transformação indevida | Comissão deve ser cópia direta — nenhuma regra de cálculo deve existir neste pipeline (RF04) |
| Custo de LLM acima do esperado | Modelo de detecção disparando com frequência maior que o previsto, ou perguntas gerando mais de 2 chamadas | Revisar limiar do modelo de detecção; auditar entendimento de pergunta e narração |

## 5. Monitoramento Recomendado
- Latência das consultas do motor genérico por família e granularidade — `faceta.ops metrics`
- Número de chamadas a LLM por pergunta respondida (deve ser sempre ≤ 2) — traces ask em `metrics.llm_calls_ask`
- Número de chamadas a LLM no job de insights por execução
- **Traces JSONL** em `logs/` (`17-tracing.md`): `python -m faceta.trace show <arquivo>`
- Divergências de reconciliação — `faceta.ops doctor` / tabela `ingest_reconciliacao`
- Consultas rejeitadas pela allowlist do contrato
- Playbook completo: `19-fase6-ops.md`
