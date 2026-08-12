"""Migrações explícitas e versionadas do schema Postgres.

Uso (manual, uma vez por ambiente — NÃO roda no ingest/cascata):

    PYTHONPATH=. python -m faceta.migrate status
    PYTHONPATH=. python -m faceta.migrate up
    PYTHONPATH=. python -m faceta.migrate up --dry-run
"""

from __future__ import annotations

from faceta.migrate.runner import pending, run_up, status

__all__ = ["pending", "run_up", "status"]
