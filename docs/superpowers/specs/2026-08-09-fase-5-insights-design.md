# Fase 5 — Insights via Deep Learning (Design)

**Data:** 2026-08-09  
**Status:** implementado (`faceta/insights`; TC16–TC17 OK; fallback NumPy se sem TF)  

## Decisões
- Modelo: autoencoder TensorFlow (erro de reconstrução vs limiar)
- Escopo: CLI configurável (`--entity-type`, `--granularidade`); default vendedor/semanal
- Tabela `insights` separada dos fatos; job em lote (não no ask)
- Ask: após consultar, lê `insights` relevantes e passa ao narrador (sem LLM extra de geração)

## Critério
TC16–TC17 + ao menos um insight real gerado
