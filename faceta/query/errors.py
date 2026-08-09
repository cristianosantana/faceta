from __future__ import annotations


class ConsultaRejeitada(Exception):
    """Consulta inválida segundo contrato/allowlist (antes de tocar o banco)."""
