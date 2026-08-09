# Manual de Instalação e Implantação (Deployment Guide)

> Vários itens abaixo dependem de decisões de infraestrutura ainda não fechadas na conversa — estão marcados como `[PENDENTE]`.

## 1. Pré-requisitos
- Postgres (para as quatro famílias de fato — `fato_os`, `fato_os_servico`, `fato_os_pagamento`, `fato_comissao` — cada uma em cinco granularidades, mais a tabela `insights`)
- Acesso de leitura ao **MySQL** de origem: OS, itens de serviço, itens de pagamento, comissões já calculadas, e tabelas cadastrais (departamento, concessionária, família de serviço, vendedor, produtivo, forma de pagamento, empresa)
- Agendador: nesta fase, **execução manual por hora** (CLI); Airflow/cron do SO ficam `[PENDENTE]` para produção — ver `11-roadmap.md`
- Ambiente Python com **TensorFlow** para treino e inferência dos modelos de detecção de anomalia/previsão
- Acesso a um provedor de LLM para entendimento de pergunta, narração da resposta e narração de insights (lote)

## 2. Estrutura de Banco de Dados
1. Criar schema dedicado (sugestão: `memoria_materializada`)
2. Criar `fato_os_diario`, `fato_os_servico_diario`, `fato_os_pagamento_diario`, `fato_comissao_diario` (scripts em `05-arquitetura-software-sad.md`, seções 3 e 5)
3. Criar as tabelas de cascata (`_semanal`, `_mensal`, `_semestral`, `_anual`) para cada uma das quatro famílias, mesma estrutura de colunas
4. Criar tabela `insights` (DER em `05-arquitetura-software-sad.md`, seção 2)
5. Implementar o motor de consulta genérico (mapas dimensão→coluna e entity_type→família/tabela, seção 7) como camada de acesso compartilhada — todo código que lê fato deve passar por ele

## 3. Configuração do Contrato
1. Definir `contrato.yaml` com os `entity_types` válidos, a família de fato de cada um, suas quebras e comparações permitidas (exemplo em `05-arquitetura-software-sad.md`, seção 6)
2. Confirmar que `servico` e `forma_pagamento` nunca aparecem como quebra um do outro
3. Versionar esse arquivo junto ao código — mudanças no contrato afetam o que pode ser consultado e devem passar por revisão

## 4. Rotina de Ingestão Diária (quatro fontes)
1. Cron que lê OS do MySQL e insere o cabeçalho em `fato_os_diario`
2. Cron que lê itens de serviço por OS e insere em `fato_os_servico_diario`
3. Cron que lê itens de pagamento por OS e insere em `fato_os_pagamento_diario`
4. Cron que lê as comissões já calculadas nas tabelas de origem e insere em `fato_comissao_diario`, sem transformação de regra
5. Cada cron valida idempotência (chave primária composta evita duplicação em reprocessamento) e, para serviço/pagamento, reconcilia a soma dos itens contra `valor_total` da OS correspondente, sinalizando divergência
6. Frequência e schema de origem confirmados no levantamento (`12-levantamento-fase-0.md`): job diário processando o dia D−1 por recorte. **Paga** = `os.paga` + linha em `caixas`; **fechada** = itens ativos todos `fechado` em `os_servicos` XOR `os_produtos`; **cancelada** = `os.cancelada`; `paga=1` sem `caixas` = inconsistência (não cancelada). Comissão geral no pagamento; comissão do produtivo no fechamento de itens. `os.finalizada` não é critério analítico.

## 5. Crons de Cascata (por família e granularidade, insert-only)
Uma rotina por família × granularidade (semanal, mensal, semestral, anual), cada uma somando o nível imediatamente inferior já persistido da mesma família:
1. Agendar cada cron com a frequência compatível: semanal só roda após os 7 dias estarem completos; mensal após as semanas do mês; e assim por diante
2. Se um dia faltar em qualquer família, a recuperação é reexecutar o cron diário daquela família para o dia específico — os crons de nível superior daquela família aguardam completude antes de rodar

## 6. Job de Insights (lote, periódico, separado dos crons de cascata)
1. Para cada `entity_type` do contrato, reconstrói a série histórica usando o motor de consulta genérico (roteando para a família de fato correta, incluindo `fato_comissao`)
2. Aplica o modelo TensorFlow de detecção sobre a série
3. Se disparado, chama o LLM para narrar o insight e grava apenas o resultado (não os números) na tabela `insights`
4. `[PENDENTE]` Definir cadência desse job e cadência de retreino dos modelos

## 7. Variáveis de Ambiente (sugestão inicial)
```
POSTGRES_URL=postgresql://postgres:secret@localhost:5432/postgres
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=smart
MYSQL_USER=root
MYSQL_PASSWORD=
CONTRATO_PATH=./contrato.yaml
LLM_API_KEY=
LLM_MODEL=
TF_MODEL_PATH=
INSIGHT_DETECTION_THRESHOLD=
```

> Credenciais reais ficam só no `.env` (gitignored). Agendamento das rotinas: execução **manual por hora** nesta fase (ver `11-roadmap.md`).

## 8. Validação Pós-Implantação
- Rodar TC01–TC17 (ver `06-plano-testes-casos-teste.md`) contra o ambiente implantado
- Conferir que uma pergunta de teste, do entendimento à narração, realiza no máximo duas chamadas a LLM
- Conferir que nenhuma consulta do motor genérico interpola nome de coluna ou tabela fora dos mapas fixos
- Conferir que uma tentativa de cruzar serviço com forma de pagamento é rejeitada pelo contrato
