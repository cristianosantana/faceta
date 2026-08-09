# Fase 1 Ingestão Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ingerir as quatro famílias `fato_*_diario` no Postgres a partir do MySQL, com CLI manual, idempotência e reconciliação.

**Architecture:** Pacote `faceta/` com DDL Postgres, conexões via `.env`, um módulo de ingestão por família (data do evento), CLI `python -m faceta.ingest --data D`.

**Tech Stack:** Python 3, pymysql, psycopg3, python-dotenv, MySQL `smart`, Postgres local

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-09-fase-1-ingestao-design.md`
- Dimensões só no MySQL; fatos só no Postgres
- Insert-only: delete+insert por `data=D` por família; sem UPDATE
- Disparo manual (sem Airflow)

---

### Task 1: DDL + conexões + scaffold

**Files:** Create `faceta/`, `faceta/sql/ddl_diario.sql`, `faceta/db.py`, update `requirements.txt`

- [x] DDL schema `memoria_materializada` + 4 fatos + `ingest_reconciliacao`
- [x] `db.py` mysql/postgres helpers
- [x] deps: `psycopg[binary]`

### Task 2: Ingestão das 4 famílias + CLI

**Files:** `faceta/ingest/*.py`

- [x] `fato_os`, `fato_os_servico`, `fato_os_pagamento`, `fato_comissao`
- [x] reconcile
- [x] CLI `--data` / `--familia`

### Task 3: Rodar contra dia real + docs

- [x] `python -m faceta.ingest --data <dia>`
- [x] Atualizar roadmap Fase 1 + `documentos/13-fase1-ingestao.md`
- [x] Marcar spec como implementada
