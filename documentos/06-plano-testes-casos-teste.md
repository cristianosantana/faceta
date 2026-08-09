# Plano de Testes e Casos de Teste

## 1. Estratégia de Testes
| Nível | Foco |
|---|---|
| Unitário | Motor de consulta genérico isolado (dada uma família de fato conhecida, `entity_type` e parâmetros, a consulta gerada produz o valor esperado) |
| Integração | Cascata completa por família: diário → semanal → mensal → semestral → anual, validando que a soma bate em cada nível, para cada uma das quatro famílias |
| Reconciliação | Soma dos itens de `fato_os_servico` e `fato_os_pagamento` bate com `valor_total` de `fato_os` para a mesma OS |
| Regressão | Reprocessamento de um dia já persistido não altera dias anteriores nem duplica valores |
| Segurança | Nomes de coluna/tabela usados na montagem de SQL nunca vêm de texto livre — só de mapas fixos |
| Modelo | Modelos de deep learning disparam detecção nos casos esperados e não disparam em ruído normal |

## 2. Casos de Teste

| ID | Cenário | Passos | Resultado Esperado |
|---|---|---|---|
| TC01 | OS com múltiplos serviços não perde nem duplica valor | Inserir uma OS com 2 serviços em `fato_os_servico`, valores somando o total da OS | `SUM(valor_atribuido)` = `valor_total` da OS em `fato_os` |
| TC02 | OS com múltiplas formas de pagamento não perde nem duplica valor | Inserir uma OS com 2 formas de pagamento em `fato_os_pagamento` | `SUM(valor_pago)` = `valor_total` da OS em `fato_os` |
| TC03 | Reconciliação sinaliza divergência | Inserir itens de serviço cuja soma não bate com o total da OS | Ingestão sinaliza a divergência, não insere silenciosamente |
| TC04 | Soma semanal bate com soma dos diários, por família | Inserir 7 dias de fato diário (uma família por vez); rodar o cron de cascata semanal | Linha semanal = soma exata das 7 linhas diárias, mesmas dimensões, mesma família |
| TC05 | Motor genérico agrupa por qualquer dimensão, roteando a família certa | Consultar `entity_type = vendedor` (deve rotear para `fato_os`) e depois `entity_type = servico` (deve rotear para `fato_os_servico`) | Cada consulta agrupa pela coluna e família corretas |
| TC06 | Comparação vs. período anterior | Ter fato mensal de dois meses consecutivos; pedir `vs_periodo_anterior` para o segundo mês | Resultado traz o valor do primeiro mês, calculado executando a mesma consulta duas vezes |
| TC07 | Comparação vs. mesmo período do ano anterior | Ter fato mensal de agosto/2025 e agosto/2026 | Resultado traz o valor de agosto/2025 |
| TC08 | Ranking correto | Rodar o motor genérico sem filtro de `entity_id`, para 3 entidades do mesmo `entity_type` no mesmo período | Ranking reflete a ordem decrescente correta, `participacao_pct` somando 100% |
| TC09 | Contrato bloqueia cruzamento servico × forma_pagamento | Pedir quebra por `forma_pagamento` num `entity_type = servico` | Consulta rejeitada — combinação não existe no contrato |
| TC10 | Contrato bloqueia entity_type/quebra não previstos | Pedir uma consulta com `entity_type` ou `quebra` fora do contrato | Consulta rejeitada antes de tocar o banco |
| TC11 | Allowlist impede SQL injection via nome de dimensão | Tentar passar um nome de dimensão que não existe no mapa fixo dimensão→coluna | Consulta rejeitada; nenhuma string arbitrária chega a ser interpolada em SQL |
| TC12 | Idempotência da ingestão | Reexecutar a ingestão do mesmo dia duas vezes, nas quatro famílias | Nenhuma duplicação de linhas |
| TC13 | Nenhuma linha de fato agregado é sobrescrita | Rodar o cron da mesma granularidade/período/família duas vezes | Segunda execução não sobrescreve a linha existente |
| TC14 | Backfill de dia faltante | Simular ausência de um dia; reexecutar o cron diário só para esse dia | Linha do dia inserida corretamente; cron semanal que dependia dela passa a poder rodar |
| TC15 | Comissão ingerida sem recálculo | Comparar valor de comissão em `fato_comissao` com o valor na tabela de origem do MySQL | Valores idênticos, sem transformação de regra aplicada pelo pipeline |
| TC16 | Insight não gerado em ausência de sinal do modelo | Série reconstruída com variação dentro do padrão previsto pelo modelo TensorFlow | Nenhuma chamada a LLM realizada; nenhuma linha nova em `insights` |
| TC17 | Insight gerado quando o modelo sinaliza | Série reconstruída com erro de reconstrução/previsão acima do limiar configurado | Uma chamada a LLM realizada; hipótese cacheada em `insights` |

## 3. Critérios de Aceitação Gerais
- Nenhum caso de teste de agregação, comparação, ranking ou reconciliação depende de LLM
- O custo de LLM só aparece nos casos TC17 e equivalentes (insights) e no caminho de resposta ao usuário (entendimento + narração), nunca nos testes de agregação
