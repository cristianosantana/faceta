# Faceta

Também conhecido como **Facetado**.

Faceta leva o nome do padrão de **busca facetada**: filtrar e agrupar o mesmo conjunto de dados por múltiplas dimensões independentes. Cada dimensão — uma *faceta* — pode ser combinada com as demais sem dependência de ordem ou hierarquia fixa.

## Status

- **Fase 0** — levantamento MySQL: feito  
- **Fase 1** — ingestão diária + `dim_*` + `servico_id` no fato de serviço: feito  
- **Fase 2** — cascata temporal (diário → semanal/mensal/…): feito  
- **Fase 3** — contrato + motor de consulta: feito  

## Rodar ingestão

```bash
.venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/python -m faceta.ingest --data 2026-07-31
PYTHONPATH=. .venv/bin/python -m faceta.ingest --only-dims
```

## Cascata (Fase 2)

Soma sempre a partir do diário; completude parcial; `--force` para reprocessar:

```bash
PYTHONPATH=. .venv/bin/python -m faceta.cascata --granularidade semanal --periodo 2026-07-31
```

## Consulta (Fase 3)

```bash
PYTHONPATH=. .venv/bin/python -m faceta.query --entity-type vendedor --granularidade semanal --periodo 2026-W31 --ranking
PYTHONPATH=. .venv/bin/python scripts/fase3_tc.py
```

Docs: `documentos/15-fase3-consulta.md` · `documentos/14-fase2-cascata.md` · `documentos/13-fase1-ingestao.md` · `documentos/11-roadmap.md`
