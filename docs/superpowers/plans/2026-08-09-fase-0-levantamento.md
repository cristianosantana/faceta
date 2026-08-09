# Fase 0 Levantamento Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rodar introspecção live no MySQL `smart` e produzir `documentos/12-levantamento-fase-0.md`, atualizando os `[PENDENTE]` de schema/frequência nos docs.

**Architecture:** Um script Python (`scripts/fase0_levantamento.py`) conecta via `.env`, lê `INFORMATION_SCHEMA`, executa contagens de estado/comissão e escreve o relatório Markdown. Em seguida os docs de origem são alinhados ao relatório.

**Tech Stack:** Python 3, pymysql, python-dotenv, MySQL `smart`

## Global Constraints

- Credenciais só em `.env` (nunca commitadas); `.env.example` sem senha real
- Não criar DDL Postgres, crons nem ingestão
- Relatório deve fechar os 3 itens da Fase 0 do roadmap
- Spec: `docs/superpowers/specs/2026-08-09-fase-0-levantamento-design.md`

---

### Task 1: Scaffolding de acesso MySQL

**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Create: `.env` (local, gitignored)
- Create: `requirements.txt`

- [x] **Step 1: Criar arquivos de config**

`.gitignore`:
```
.env
.DS_Store
__pycache__/
*.pyc
.venv/
venv/
```

`.env.example`:
```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=smart
MYSQL_USER=root
MYSQL_PASSWORD=
```

`.env` com os valores fornecidos pelo usuário (password `secret`).

`requirements.txt`:
```
pymysql>=1.1.0
python-dotenv>=1.0.0
```

- [x] **Step 2: Instalar deps e testar conexão**

```bash
cd /Users/cristianosoaresdesantana/code/faceta
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -c "from dotenv import load_dotenv; import os, pymysql; load_dotenv(); c=pymysql.connect(host=os.environ['MYSQL_HOST'], port=int(os.environ['MYSQL_PORT']), user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASSWORD'], database=os.environ['MYSQL_DATABASE']); print(c.cursor().execute('SELECT 1')); c.close()"
```

Expected: imprime `1` (ou `None`/linha ok sem erro)

---

### Task 2: Script de levantamento + relatório

**Files:**
- Create: `scripts/fase0_levantamento.py`
- Create: `documentos/12-levantamento-fase-0.md` (gerado)

**Interfaces:**
- Produz: arquivo Markdown em `documentos/12-levantamento-fase-0.md`
- Exit code 0 se tabelas essenciais presentes; ≠0 se faltar tabela essencial ou conexão falhar

- [x] **Step 1: Implementar `scripts/fase0_levantamento.py`**

O script deve:
1. Carregar `.env` da raiz do repo
2. Introspectar tabelas: `departamentos`, `concessionarias`, `grupos_servicos`, `funcionarios`, `funcionario_tipos`, `funcionario_cargos`, `cargos`, `caixa_tipos`, `empresas`, `os`, `os_servicos`, `os_produtos`, `servicos`, `caixas`, `caixas_pendentes`, `comissoes`, `comissao_tipos`, `comissao_periodos`, `comissao_pagamentos`
3. Assertar colunas críticas (`os.vendedor_id`, `os.paga`, `os.fechada`, `os.finalizada`, `os_servicos.produtivo_id`, `caixas.caixa_tipo_id`, `comissoes.comissionado_id`, `cargos.funcionario_tipo_id`, …)
4. Amostrar nomes de dimensões e listar `funcionario_tipos` / `comissao_tipos`
5. Contagens 14 dias: abertas / pagas∩caixa / fechadas / finalizadas; invariante finalizada
6. Contagens: OS fechadas sem comissão; breakdown comissão por tipo de funcionário quando possível
7. Componentes de valor em `comissoes` (null rate) e propor fórmula `valor_comissao = COALESCE(valor_dentro,0)+…`
8. Escrever `documentos/12-levantamento-fase-0.md`

- [x] **Step 2: Rodar o script**

```bash
.venv/bin/python scripts/fase0_levantamento.py
```

Expected: exit 0, arquivo `documentos/12-levantamento-fase-0.md` criado

---

### Task 3: Atualizar docs de origem

**Files:**
- Modify: `documentos/10-dicionario-dados.md`
- Modify: `documentos/05-arquitetura-software-sad.md`
- Modify: `documentos/07-guia-implantacao.md`
- Modify: `docs/superpowers/specs/2026-08-09-fase-0-levantamento-design.md` (status)

- [x] **Step 1: Remover `[PENDENTE]` de schema/frequência** e apontar para `12-levantamento-fase-0.md` com o mapeamento confirmado (incl. `funcionario_tipos`, momento de comissão)
- [x] **Step 2: Verificar** que não restam PENDENTEs de schema de dimensão, comissão ou frequência de leitura nesses trechos

---

## Self-review checklist

- Spec §1–10 cobertos pelas Tasks 1–3
- Sem placeholders TBD no plano de código
- Commit só se o usuário pedir
