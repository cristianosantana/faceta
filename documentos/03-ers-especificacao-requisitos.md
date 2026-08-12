# Especificação de Requisitos de Software (ERS / SRS)

## 1. Visão Geral do Sistema
Sistema composto por seis camadas: (1) ingestão diária a partir do MySQL, separada em três famílias de fato por grão — `fato_os` (cabeçalho, dimensões únicas por OS: concessionária, departamento, vendedor, empresa; `produtivo_id` sentinela), `fato_os_servico` (item de serviço + produtivo, multivalorado por OS) e `fato_os_pagamento` (item de pagamento, multivalorado por OS) — mais ingestão de `fato_comissao` (componentes pré-calculados na origem + soma simples na ingestão); (2) cascata de agregação por tempo em que cada granularidade (`semanal`…`anual`) soma o fato **diário** no intervalo do calendário (completude parcial), insert-only com reprocessamento explícito (`--force`), aplicada a cada família independentemente; (3) contrato declarativo, allowlist de dimensões/quebras/comparações válidas por `entity_type`, incluindo o roteamento para a família de fato correta; (4) motor de consulta genérico que roda `GROUP BY` em tempo de leitura sobre a tabela agregada certa, incluindo comparações e ranking; (5) entendimento de pergunta via LLM, traduzindo a pergunta nos parâmetros dessa consulta; (6) detecção de insights via modelos de deep learning (TensorFlow), rodando em lote sobre séries reconstruídas pelo motor genérico, com narração por LLM condicional e cache enxuto. O caminho de resposta ao usuário usa no máximo duas chamadas a LLM.

## 2. Requisitos Funcionais

| ID | Descrição |
|---|---|
| RF01 | O sistema deve ingerir diariamente, do MySQL, um registro de fato por OS em `fato_os`, contendo `data`, `valor_total`, `quantidade_os` e as chaves de dimensão únicas por OS (`concessionaria_id`, `departamento_id`, `vendedor_id`, `empresa_id`; `produtivo_id` sentinela `''`) |
| RF02 | O sistema deve ingerir diariamente, do MySQL, um registro por combinação (dims + serviço unitário + produtivo) em `fato_os_servico`, com `servico_id`, `familia_servico_id` (= `subgrupos_servicos`), `produtivo_id` (de `os_servicos`) e `valor_atribuido` |
| RF03 | O sistema deve ingerir diariamente, do MySQL, um registro por combinação (OS, forma de pagamento) em `fato_os_pagamento`, com `valor_pago` por cada forma dentro da OS |
| RF04 | O sistema deve ingerir diariamente comissões a partir de `comissoes` no MySQL em `fato_comissao` (`comissionado_id`, `comissao_tipo_id`). Os **componentes** (`valor_dentro`, `valor_fora`, `valor_combo`, `valor_compensado_permuta`, `comissao_couro`) já vêm pré-calculados pela origem; a ingestão aplica apenas a **soma simples** desses campos em `valor_comissao` — sem percentual, faixa ou outra regra de negócio |
| RF05 | O sistema deve validar, na ingestão, que `SUM(valor_atribuido)` em `fato_os_servico` e `SUM(valor_pago)` em `fato_os_pagamento` batem com `valor_total` da respectiva OS em `fato_os`, sinalizando divergência |
| RF06 | O sistema deve calcular fatos agregados semanais, mensais, semestrais e anuais em cascata, para cada uma das quatro famílias independentemente — cada granularidade somando o fato **diário** no intervalo do calendário (não encadeando semana→mês), preservando todas as colunas de dimensão da sua família; completude parcial permitida |
| RF07 | O sistema deve, na hora da pergunta, calcular a comparação com o período imediatamente anterior e com o mesmo período do ano anterior, executando a mesma consulta agregada duas vezes sobre a tabela de fato da granularidade e família corretas |
| RF08 | O sistema deve calcular ranking de entidades dentro do mesmo `entity_type` e período na hora da pergunta, via `RANK()` sobre o resultado agrupado, incluindo posição e participação percentual |
| RF09 | O sistema deve permitir quebra dos valores por dimensões válidas para o `entity_type` consultado, conforme declarado no contrato — sem permitir quebra entre `familia_servico` e `forma_pagamento`, já que a origem não vincula os dois no nível da OS |
| RF10 | O sistema deve ler, para cada `entity_type`, um contrato declarativo definindo a família de fato (`fato_os`, `fato_os_servico`, `fato_os_pagamento` ou `fato_comissao`), a coluna que representa o `entity_id`, e quais quebras e comparações são válidas |
| RF11 | O sistema deve montar as consultas de agregação (motor genérico) parametrizando apenas colunas presentes num mapa fixo dimensão→coluna, nunca interpolando texto livre do contrato ou da pergunta diretamente em SQL |
| RF12 | O sistema deve, em lote, reconstruir séries históricas por `entity_type` (a partir da família de fato correspondente) usando o motor de consulta genérico e aplicar modelos de deep learning (autoencoder, previsão por rede recorrente/atenção, ou clusterização de séries) para identificar variações notáveis |
| RF13 | O sistema deve invocar um LLM para narrar um insight em linguagem natural **somente** quando o modelo de detecção sinalizar uma variação notável, e deve cachear o resultado numa tabela `insights` enxuta (chave `entity_type + entity_id + granularidade + periodo + quebra`) |
| RF14 | O sistema deve rejeitar consultas cujo `entity_type` ou `quebra` não estejam previstos no contrato, antes de executar qualquer SQL |
| RF15 | O sistema deve interpretar a pergunta do usuário via LLM e traduzi-la nos parâmetros do motor de consulta genérico: `entity_type`, `entity_id` (se a pergunta nomeia uma entidade específica), `granularidade`, `periodo`, `quebra` e `comparacao` — sem que o LLM precise saber a qual família de fato o `entity_type` pertence |
| RF16 | O sistema deve responder ao usuário final com no máximo duas chamadas a LLM por pergunta: uma para entendimento da pergunta (RF15) e uma para narração da resposta a partir do resultado da consulta |

## 3. Requisitos Não Funcionais

| ID | Categoria | Descrição |
|---|---|---|
| RNF01 | Desempenho | A consulta que responde a uma pergunta deve rodar sobre a tabela de fato já agregada pela granularidade e família corretas (nunca sobre o fato diário bruto para períodos longos) |
| RNF02 | Custo | Chamadas a LLM no caminho de resposta ao usuário devem se limitar a entendimento da pergunta (RF15) e narração da resposta final (RF16). Chamadas a LLM para narração de insight ocorrem em lote, fora do caminho de resposta |
| RNF03 | Escalabilidade | Adicionar uma nova dimensão de negócio não deve exigir alteração de schema das tabelas de fato existentes, apenas uma nova coluna dimensional (na família de fato correta) e uma entrada no mapa dimensão→coluna e no contrato |
| RNF04 | Consistência | Cada fato diário é a única fonte de verdade da sua família; granularidades superiores derivam exclusivamente do diário da mesma família no intervalo; default insert-only (reprocessamento só com `--force`) |
| RNF05 | Auditabilidade | Toda comparação e ranking apresentados numa resposta devem ser reproduzíveis executando a mesma consulta do motor genérico contra as tabelas de fato, sem lógica oculta |
| RNF06 | Integridade referencial | IDs de dimensão nos fatos devem referenciar as tabelas cadastrais existentes no MySQL; nomes de dimensão não devem ser armazenados como texto solto sem normalização |
| RNF07 | Segurança | Nomes de coluna e de tabela usados para montar SQL dinamicamente devem vir exclusivamente de mapas fixos (allowlist), nunca de texto livre do usuário, da pergunta interpretada pelo LLM, ou do contrato sem validação |
| RNF08 | Integridade de dado | Divergências entre `valor_total` de `fato_os` e a soma dos itens em `fato_os_servico`/`fato_os_pagamento` devem ser sinalizadas na ingestão, não silenciadas |

## 4. Restrições Técnicas
- O fato bruto (OS, itens de serviço, itens de pagamento), as comissões já calculadas e as tabelas cadastrais residem em **MySQL**, externo ao Postgres de destino
- Persistência dos fatos agregados em Postgres, quatro famílias (`fato_os`, `fato_os_servico`, `fato_os_pagamento`, `fato_comissao`) × cinco granularidades cada
- Serviço e forma de pagamento não podem ser cruzados como quebra um do outro — limitação confirmada da origem, não uma pendência técnica
