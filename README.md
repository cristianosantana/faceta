# Faceta

Também conhecido como **Facetado**.

Faceta leva o nome do padrão de **busca facetada**: filtrar e agrupar o mesmo conjunto de dados por múltiplas dimensões independentes. Cada dimensão — uma *faceta* — pode ser combinada com as demais sem dependência de ordem ou hierarquia fixa.

## Status

- **Fase 0** — levantamento MySQL: feito  
- **Fase 1** — ingestão diária + `dim_*` + `servico_id` no fato de serviço: feito  

## Rodar ingestão

```bash
.venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-07-31
PYTHONPATH=. .venv/bin/python -m faceta.ingest --only-dims
```

Docs: `documentos/13-fase1-ingestao.md` · `documentos/10-dicionario-dados.md` · `documentos/11-roadmap.md`
