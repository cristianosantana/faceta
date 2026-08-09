# Manual Operacional

> Este sistema não tem interface de usuário final própria nesta fase — quem opera é a equipe técnica e, indiretamente, o narrator/chat público que consulta via o motor genérico. Este manual substitui o "Manual do Usuário Final" tradicional por um guia operacional.

## 1. Rotina Diária Esperada
1. Quatro crons de ingestão leem o MySQL: OS (`fato_os`), itens de serviço (`fato_os_servico`), itens de pagamento (`fato_os_pagamento`) e comissões já calculadas (`fato_comissao`)
2. A ingestão de serviço/pagamento reconcilia a soma dos itens contra o valor total da OS, sinalizando divergência
3. Nos fechamentos de cada janela de tempo, os crons de cascata correspondentes (por família) somam o nível inferior já persistido e inserem a linha nova — nenhuma linha existente é alterada
4. O job de insights roda periodicamente, reconstruindo séries via o motor genérico (para as quatro famílias) e narrando apenas o que os modelos sinalizarem
5. Perguntas de usuário são respondidas em tempo real pelo motor de consulta genérico — nenhuma ação manual necessária em operação normal

## 2. Como Adicionar um Novo Tipo de Entidade (entity_type)
1. Confirmar a qual família de fato a dimensão pertence (`fato_os` se for única por OS; se for multivalorada como serviço/pagamento, precisa de uma família própria nova — ver seção 3)
2. Adicionar a entrada correspondente em `contrato.yaml`, com a família, coluna de agrupamento, quebras e comparações válidas
3. Validar com uma consulta de teste ao motor genérico (TC05 do plano de testes) antes de liberar para perguntas reais

## 3. Como Adicionar uma Nova Dimensão
**Se a dimensão é sempre única por OS** (como concessionária, departamento, vendedor, produtivo): adicionar a coluna em `fato_os` e em todas as tabelas de cascata dessa família.
**Se a dimensão pode ser múltipla por OS** (como serviço, pagamento): criar uma nova família de fato (`fato_os_<dimensao>`), com as dimensões únicas replicadas mais a nova dimensão, e sua própria cascata por tempo — mesma estrutura de `fato_os_servico`.
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
| Semana/mês com dado incompleto | Cron diário não rodou para algum dia, em alguma família (falha, atraso na origem) | Reexecutar o cron diário daquela família para o dia específico que faltou; os crons de nível superior devem aguardar completude antes de rodar |
| Comissão divergente da origem | Job de ingestão aplicando alguma transformação indevida | Comissão deve ser cópia direta — nenhuma regra de cálculo deve existir neste pipeline (RF04) |
| Custo de LLM acima do esperado | Modelo de detecção disparando com frequência maior que o previsto, ou perguntas gerando mais de 2 chamadas | Revisar limiar do modelo de detecção; auditar entendimento de pergunta e narração |

## 5. Monitoramento Recomendado
- Latência das consultas do motor genérico por família e granularidade
- Número de chamadas a LLM por pergunta respondida (deve ser sempre ≤ 2)
- Número de chamadas a LLM no job de insights por execução
- Divergências de reconciliação (serviço/pagamento vs. total da OS) por execução de ingestão
- Consultas rejeitadas pela allowlist do contrato, como sinal de dado novo não mapeado ou tentativa inválida (ex.: cruzamento servico × forma_pagamento)
