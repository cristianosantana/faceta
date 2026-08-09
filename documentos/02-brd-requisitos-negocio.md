# Documento de Requisitos de Negócio (BRD)

## 1. Contexto do Negócio
A rede de concessionárias opera múltiplas entidades analíticas (concessionária, departamento, serviço, vendedor, produtivo, forma de pagamento) sobre as quais usuários fazem perguntas recorrentes: volume por período, comparações com períodos anteriores, participação no total, ranking entre entidades similares, além de comissões já apuradas na origem. O processo atual (`orion_v3`) resolve cada pergunta computando contexto sob demanda através de um pipeline com múltiplas etapas de LLM, o que gera custo e latência proporcionais ao volume de perguntas.

## 2. Necessidade de Negócio
Reduzir o custo por pergunta respondida e a latência de resposta, sem perder a capacidade de responder perguntas analíticas ricas (múltiplas granularidades, comparações, rankings, hipóteses sobre tendências).

## 3. Objetivos de Negócio
- **OB1** — Reduzir o número de chamadas a LLM necessárias para responder uma pergunta analítica típica
- **OB2** — Permitir que uma única consulta a um registro de memória responda a várias perguntas diferentes sobre a mesma entidade
- **OB3** — Manter a qualidade analítica (comparações corretas, rankings corretos, hipóteses plausíveis) equivalente ou superior ao pipeline atual
- **OB4** — Suportar novas dimensões de negócio (novas famílias de serviço, novos departamentos) sem exigir alteração estrutural do sistema

## 4. Requisitos de Negócio de Alto Nível
| ID | Requisito |
|---|---|
| RN01 | O sistema deve responder, para cada entidade analítica relevante (concessionária, departamento, serviço, vendedor, produtivo, forma de pagamento), perguntas em múltiplas granularidades temporais: diária, semanal, mensal, semestral e anual |
| RN02 | O sistema deve calcular comparações automáticas: valor vs. período anterior e valor vs. mesmo período do ano anterior |
| RN03 | O sistema deve calcular a participação de cada entidade no total do seu grupo e o ranking entre entidades comparáveis |
| RN04 | O sistema deve permitir que qualquer dimensão de negócio (departamento, concessionária, família de serviço, vendedor, produtivo, forma de pagamento, empresa) seja tanto o sujeito de uma entidade quanto uma quebra dentro de outra, sem exigir uma estrutura fixa de dimensões |
| RN05 | O sistema deve gerar hipóteses/insights sobre tendências e variações notáveis usando modelos de deep learning treinados sobre o histórico, evitando gerar insights genéricos ou irrelevantes |
| RN06 | O custo de geração de insights (uso de LLM para narração) deve ser incorrido em lote, não por pergunta de usuário |
| RN07 | O sistema deve reaproveitar as tabelas cadastrais já existentes (departamento, concessionária, família de serviço, vendedor, produtivo, forma de pagamento, empresa) como fonte de verdade para IDs e nomes de dimensão |
| RN08 | Como as perguntas dos usuários são imprevisíveis, o sistema deve usar LLM para entender a pergunta e decidir os parâmetros da consulta ao motor genérico — o LLM não recalcula fato, apenas decide o que consultar e narra o resultado |
| RN09 | O sistema deve ingerir as comissões já calculadas nas tabelas de origem do MySQL, sem recalculá-las |
| RN10 | O sistema não precisa responder perguntas que cruzem serviço com forma de pagamento, já que a origem não vincula os dois no nível da OS |

## 5. Fora de Escopo
- Alteração dos sistemas de origem que hoje mantêm os cadastros de departamento, concessionária, família de serviço e empresa
- Qualquer integração, dependência ou fallback com o `orion_v3` — projeto novo e independente
