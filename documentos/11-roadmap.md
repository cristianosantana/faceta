# Roadmap

> Datas não estão definidas (`[PENDENTE]` orçamento e prazo macro — ver `01-termo-abertura-projeto.md`). O que segue é a sequência de dependências entre fases, mapeada ao backlog de `04-historias-usuario-backlog.md` — a ordem é a parte confiável deste documento, as durações são só um ponto de partida a ajustar quando prazo/recursos forem definidos.

## Fase 0 — Levantamento (pré-requisito de tudo)
- Validar o schema real das tabelas cadastrais no MySQL — **feito** (`12-levantamento-fase-0.md`, `10-dicionario-dados.md`)
- Mapear o schema exato das tabelas de comissão na origem — **feito** (`comissoes` + satélites; fórmula e momento documentados)
- Confirmar frequência de disponibilidade dos dados no MySQL — **feito** (ingestão D−1 por recorte; ver §7 do levantamento)
- Estados analíticos (paga / fechada derivada / cancelada por `os.cancelada`; paga sem caixa = inconsistência) — **feitos** (`10-dicionario-dados.md`, `12-levantamento-fase-0.md` §5); `os.finalizada` fora do critério
- **Bloqueia:** todas as fases seguintes
- **Como regenerar:** `python scripts/fase0_levantamento.py` (requer `.env` com acesso ao MySQL `smart`)

## Fase 1 — Ingestão das Quatro Famílias de Fato
- US01–US06 (Épico 1): `fato_os`, `fato_os_servico`, `fato_os_pagamento`, `fato_comissao`, idempotência, reconciliação
- Destino: Postgres local (`POSTGRES_URL` no `.env`)
- Agendamento: **manual / horário** (operador dispara; sem Airflow nesta etapa)
- **Critério de saída:** um dia real ingerido nas quatro famílias, com reconciliação batendo

## Fase 2 — Cascata por Tempo
- US07–US08 (Épico 2): crons de cascata semanal/mensal/semestral/anual, para as quatro famílias
- **Critério de saída:** um período fechado completo (ex.: uma semana) materializado corretamente em todas as famílias, sem merge, sem sobrescrita

## Fase 3 — Contrato e Motor de Consulta Genérico
- US09–US14 (Épicos 3 e 4): contrato como allowlist, roteamento por família, agregação, comparações, ranking
- **Critério de saída:** TC01–TC11 (`06-plano-testes-casos-teste.md`) passando contra dado real

## Fase 4 — Entendimento de Pergunta e Narração
- US18–US20 (Épico 6): LLM traduz pergunta em parâmetros, motor genérico responde, LLM narra
- **Critério de saída:** uma pergunta real, ponta a ponta, em no máximo 2 chamadas de LLM

## Fase 5 — Insights via Deep Learning
- US15–US17 (Épico 5): reconstrução de série, modelo TensorFlow, narração condicional
- **Depende de:** histórico acumulado suficiente nas Fases 1–2 (modelo precisa de série histórica pra treinar)
- **Critério de saída:** TC16–TC17 passando; ao menos um insight real gerado e validado manualmente

## Fase 6 — Operação
- Monitoramento (`09-manual-operacional.md`, seção 5), diagnóstico de problemas comuns, backfill
- **Critério de saída:** sistema rodando em produção com as métricas de sucesso do `01-termo-abertura-projeto.md` (seção 7) mensuradas

## Dependências entre fases
```
Fase 0 → Fase 1 → Fase 2 → Fase 3 → Fase 4 → Fase 6
                              ↘ Fase 5 (paralela à 4, depende da 1-2) ↗
```
A Fase 5 (insights) pode começar em paralelo à Fase 4 assim que houver histórico suficiente — não precisa esperar a camada de pergunta estar pronta, já que consome os fatos diretamente via motor genérico.

## Decisões de infra / gestão (atualizado)

| Item | Status | Decisão / nota |
|---|---|---|
| Orçamento e prazo macro | `[PENDENTE]` | Ver `01-termo-abertura-projeto.md` |
| Agendador de cron (SO vs Airflow) | **Decidido (fase atual)** | Execução **manual**, sob demanda / **por hora** — sem Airflow nem cron do SO por enquanto; jobs da Fase 1+ devem ser invocáveis via CLI |
| Servidor / infraestrutura específica | `[PENDENTE]` | Ambiente local de desenvolvimento; produção a definir |
| Postgres (destino dos fatos) | **Disponível (local)** | URL em `.env` como `POSTGRES_URL` (ex.: `postgresql://postgres:secret@localhost:5432/postgres`) — não versionar senha |

## Itens ainda pendentes (não bloqueiam Fase 1 local)
- Orçamento e prazo macro
- Servidor/infraestrutura de produção
