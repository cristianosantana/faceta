# Fase 4 — Entendimento de Pergunta e Narração

> Spec: `docs/superpowers/specs/2026-08-09-fase-4-ask-design.md`  
> Status: **implementado** (`faceta/ask`)

## Fluxo

1. LLM₁ → JSON (`entity_type`, período, ranking, nome/id…)  
2. Validar contrato + resolver nome em `dim_*`  
3. Motor `consultar()` (enriquece `entity_nome` / `quebra_nome` via `dim_*` para **todas** as dimensões)  
4. LLM₂ → narração em PT-BR (cita nomes, não IDs)  

Máximo **2** chamadas LLM.

## Env

```
LLM_API_KEY=sk-...
LLM_MODEL=gpt-5-mini
# opcional: OPENAI_BASE_URL=
```

## CLI

```bash
PYTHONPATH=. python -m faceta.ask "Quais vendedores mais venderam na semana 2026-W31?"
PYTHONPATH=. python -m faceta.ask --json "Quanto vendeu o vendedor X em julho de 2026?"
PYTHONPATH=. python -m faceta.ask --sem-narracao "ranking de serviços em 2026-07"
```
