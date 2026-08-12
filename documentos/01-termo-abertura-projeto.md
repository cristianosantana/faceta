# Termo de Abertura do Projeto (Project Charter)

**Projeto (nome provisório):** Memória Materializada
**Status:** Rascunho para validação
**Data:** 09/08/2026

> Nome definitivo, patrocinador, orçamento e prazos macro estão marcados como `[PENDENTE]` — este documento reflete o que foi definido em conversa até aqui; os campos de gestão de projeto (orçamento, prazo, patrocinador) precisam ser preenchidos por quem os detém.

## 1. Objetivo do Projeto
Criar um sistema de memória analítica — projeto novo e independente, sem reaproveitamento do Orion (`orion_v3`) — capaz de responder perguntas imprevisíveis sobre vendas, serviços, comissões e formas de pagamento em múltiplas granularidades temporais e dimensões de negócio, substituindo a resolução de contexto multi-etapas por consultas agregadas rápidas sobre dados pré-agregados por tempo.

## 2. Justificativa
O pipeline atual do Orion (`intent.interpret → fact.plan → fact.resolve → fact.extract → workspace.build → narrator`) resolve contexto em tempo real, com múltiplas chamadas a modelos de linguagem por pergunta do usuário, incluindo etapas caras de planejamento e extração de fatos. Isso foi identificado como **custoso e ineficiente**. A hipótese de negócio é que, pré-agregando os dados por tempo (não por entidade) e mantendo um motor de consulta genérico, o LLM deixa de precisar planejar e extrair fatos — ele continua necessário em dois pontos, mas ambos mais baratos que o pipeline atual: (1) **entender a pergunta** (imprevisível por natureza) e traduzi-la nos parâmetros de uma consulta (qual dimensão é o sujeito, granularidade, quebra, comparação), e (2) **narrar a resposta final** em linguagem natural a partir do resultado. O que sai do caminho crítico é o cálculo do fato bruto e a extração de contexto — isso passa a ser 100% pré-agregado via SQL em cascata, com modelos de deep learning rodando em lote só para detecção de insights.

## 3. Escopo Macro

### Dentro do escopo
- Ingestão diária de fatos totalmente dimensionais a partir do MySQL, separados em três famílias por grão (OS, itens de serviço da OS, itens de pagamento da OS) mais ingestão de comissões já calculadas na origem
- Cascata de agregação por tempo (diário → semanal → mensal → semestral → anual), insert-only, para cada família de fato
- Motor de consulta genérico que roteia qualquer dimensão de negócio como sujeito da pergunta, calculando comparações e ranking em tempo de leitura
- Contrato declarativo funcionando como allowlist de dimensões, quebras e comparações válidas
- Geração de insights/hipóteses via modelos de deep learning, com narração por LLM aplicada apenas quando o modelo sinaliza uma variação notável

### Fora do escopo (nesta fase)
- Qualquer dependência ou integração com o `orion_v3` — este é um projeto novo e independente, não uma evolução ou substituição dele
- Ingestão em tempo real (o "diário" mais recente pode exigir um caminho quente separado, a definir)
- Interface de usuário final além do consumo pelo narrator/LLM
- Cálculo de regras de comissão (já vem pronto do MySQL de origem)
- Cruzamento entre serviço e forma de pagamento (a origem não vincula um serviço específico a uma forma de pagamento específica dentro da mesma OS)

## 4. Partes Interessadas (Stakeholders)
| Papel | Responsabilidade |
|---|---|
| Cristiano | Arquitetura, especificação, implementação |
| Narrator / camada de chat público | Consumidor principal do motor de consulta genérico |
| MySQL de origem | Fonte das OS, itens de serviço, itens de pagamento, comissões e tabelas cadastrais (departamento, concessionária, família de serviço, vendedor, produtivo, forma de pagamento, empresa) |

## 5. Premissas
- As dimensões cadastrais já existem no MySQL de origem com IDs estáveis
- Vendedor é único por OS; **produtivo** é por item de serviço (`os_servicos`); serviço e forma de pagamento são multivalorados por OS
- A origem tem itemização de serviços e de formas de pagamento por OS, mas como duas listas independentes, sem vínculo direto entre um serviço e uma forma de pagamento específicos
- Comissões: componentes pré-calculados no MySQL; este projeto só aplica a **soma simples** em `valor_comissao` (não recalcula percentual/faixa)
- O destino dos fatos agregados é Postgres, em tabelas separadas por família de fato e granularidade

## 6. Restrições
- `[PENDENTE]` Orçamento
- `[PENDENTE]` Prazo macro
- Infraestrutura de hospedagem: solução única (não dividida entre múltiplos servidores/ambientes), viabilizada pelo fato de o fluxo ser mais determinístico que o do `orion_v3` — `[PENDENTE]` apenas o provedor/servidor específico

## 7. Critérios de Sucesso
- Redução mensurável de chamadas a LLM por pergunta respondida, comparado ao pipeline `orion_v3` (meta: no máximo 2 chamadas por pergunta)
- Um mesmo conjunto de fatos agregados por tempo capaz de responder qualquer combinação válida de sujeito/quebra/comparação através do motor de consulta genérico, sem pré-computar cada combinação
- Latência de resposta muito menor que o pipeline atual, por não depender de resolução de contexto multi-etapas em tempo real
