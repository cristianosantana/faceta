# Histórias de Usuário e Backlog

## Personas
- **Narrator (consumidor automatizado):** camada de LLM que usa o motor de consulta genérico para responder perguntas de usuário final
- **Engenheiro de dados / operador:** responsável por manter os crons de ingestão, os crons de cascata e o contrato
- **Analista de negócio:** define quais dimensões, quebras e comparações são válidas via contrato

## Épico 1 — Ingestão das Três Famílias de Fato + Comissão
- **US01** Como engenheiro de dados, quero ingerir diariamente o cabeçalho de cada OS em `fato_os` (concessionária, departamento, vendedor, produtivo, empresa, valor total), para ter a base das dimensões que são sempre únicas por OS.
- **US02** Como engenheiro de dados, quero ingerir diariamente os itens de serviço de cada OS em `fato_os_servico` **por `servico_id`** (com `familia_servico_id` = subgrupo), para responder perguntas por serviço unitário e por família sem perder valor.
- **US04** Como engenheiro de dados, quero ingerir as comissões já calculadas (`comissionado_id`, `comissao_tipo_id`) das tabelas de origem do MySQL, para não precisar reimplementar as regras de comissão.
- **US05** Como sistema, quero validar que a soma dos itens de serviço e de pagamento bate com o valor total da OS na ingestão, para sinalizar divergência de dado cedo.
- **US06** Como engenheiro de dados, quero que toda ingestão seja idempotente, para poder reprocessar com segurança em caso de falha.

## Épico 2 — Cascata por Tempo (cada família, independente)
- **US07** Como sistema, quero somar cada granularidade (`semanal`…`anual`) a partir do fato **diário** já persistido (intervalo de calendário), para cada uma das quatro famílias, sem recomputar do MySQL e sem encadear semana→mês.
- **US08** Como sistema, quero que cada linha de fato agregado seja escrita uma única vez por padrão (insert-only) e só seja substituída com reprocessamento explícito (`--force`), para evitar merge entre execuções concorrentes.

## Épico 3 — Contrato como Allowlist e Roteador
- **US09** Como analista de negócio, quero declarar em um contrato quais dimensões podem ser sujeito (`entity_type`), a qual família de fato cada uma pertence, e quais quebras/comparações são válidas, para controlar o que pode ser consultado sem alterar código.
- **US10** Como sistema, quero rejeitar uma consulta cujo `entity_type` ou quebra não estejam no contrato antes de montar qualquer SQL, para evitar consultas inválidas ou inseguras.
- **US11** Como analista de negócio, quero que o contrato jamais permita cruzar serviço com forma de pagamento como quebra, porque a origem não vincula os dois no nível da OS.

## Épico 4 — Motor de Consulta Genérico
- **US12** Como sistema, quero montar a consulta de agregação parametrizando a coluna de agrupamento e a tabela/família de fato a partir de mapas fixos, para que qualquer dimensão possa ser sujeito sem precisar de uma query nova por entidade.
- **US13** Como sistema, quero calcular comparações (vs. período anterior, vs. mesmo período do ano anterior) executando a mesma consulta para o período de referência.
- **US14** Como sistema, quero calcular ranking e participação percentual na hora da pergunta, via `RANK()` sobre o resultado agrupado.

## Épico 5 — Insights e Hipóteses (Deep Learning)
- **US15** Como sistema, quero reconstruir séries históricas por `entity_type` (incluindo comissão) usando o motor de consulta genérico, em lote, para alimentar os modelos de detecção sem duplicar dado.
- **US16** Como sistema, quero detectar variações notáveis usando modelos de deep learning treinados sobre essas séries, para decidir quando vale a pena gerar um insight textual.
- **US17** Como sistema, quero acionar um LLM apenas quando o modelo de detecção sinalizar uma variação notável, para narrar o insight e cachear o resultado numa tabela enxuta.

## Épico 6 — Entendimento de Pergunta
- **US18** Como usuário, quero fazer perguntas em linguagem livre e imprevisível sobre qualquer dimensão (incluindo comissão), sem precisar saber a qual família de fato ela pertence.
- **US19** Como sistema, quero traduzir a pergunta nos parâmetros do motor de consulta genérico via uma única chamada a LLM, validando contra o contrato antes de executar qualquer SQL.
- **US20** Como sistema, quero narrar a resposta final a partir do resultado da consulta, usando uma segunda chamada a LLM, para que o total de chamadas por pergunta seja no máximo duas.

## Backlog priorizado (sugestão inicial)
1. US01, US02, US03, US04, US05, US06 — ingestão das quatro famílias de fato
2. US07, US08 — cascata por tempo
3. US09, US10, US11 — contrato como allowlist e roteador
4. US12, US13, US14 — motor de consulta genérico
5. US15, US16, US17 — insights via deep learning
6. US18, US19, US20 — entendimento de pergunta + narração da resposta
