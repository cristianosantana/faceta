# Fase 2 Cascata — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** CLI `python -m faceta.cascata` agregando `*_diario` → semanal/mensal/semestral/anual (spec `2026-08-09-fase-2-cascata-design.md`).

**Architecture:** `periods.py` (limites), `families.py` (mapa allowlist), `engine.py` (skip/force + INSERT…SELECT), `__main__.py` (CLI). `apply_ddl` aplica também `ddl_cascata.sql`.

**Tech Stack:** Python 3, psycopg, Postgres schema `memoria_materializada`.

### Task 1: periods + families + engine + CLI
- Criar `faceta/cascata/{periods,families,engine,__init__,__main__}.py`
- Integrar `ddl_cascata.sql` em `faceta/db.py:apply_ddl`
- Verificar: cascata semanal do período que contém `2026-07-31`; skip sem force; force reinsere; SUM diário = SUM semanal

### Task 2: Docs pós-critério
- Roadmap/README/`14-fase2-cascata.md`/spec → status implementado
