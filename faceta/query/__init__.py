"""Contrato e motor de consulta genérico (Fase 3)."""

from faceta.query.engine import ResultadoConsulta, consultar
from faceta.query.errors import ConsultaRejeitada
from faceta.query.contract import load_contrato, validar_consulta

__all__ = [
    "ConsultaRejeitada",
    "ResultadoConsulta",
    "consultar",
    "load_contrato",
    "validar_consulta",
]
