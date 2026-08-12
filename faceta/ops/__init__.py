"""Fase 6 — operação (health, status, backfill, ano, metrics, doctor)."""

from faceta.ops.ano import ano_pipeline
from faceta.ops.doctor import doctor
from faceta.ops.health import healthcheck

__all__ = ["ano_pipeline", "doctor", "healthcheck"]
