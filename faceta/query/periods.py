from __future__ import annotations

import re
from datetime import date

from faceta.cascata.periods import period_bounds
from faceta.query.errors import ConsultaRejeitada
from faceta.query.maps import GRANULARIDADE_SUFIXO


_RE_ISO_DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_RE_WEEK = re.compile(r"^(\d{4})-W(\d{2})$", re.IGNORECASE)
_RE_MONTH = re.compile(r"^(\d{4})-(\d{2})$")
_RE_HALF = re.compile(r"^(\d{4})-H([12])$", re.IGNORECASE)
_RE_YEAR = re.compile(r"^(\d{4})$")


def parse_periodo(texto: str, granularidade: str) -> date:
    """Interpreta o texto do período e devolve a data-chave (início) da granularidade."""
    if granularidade not in GRANULARIDADE_SUFIXO:
        raise ConsultaRejeitada(f"granularidade inválida: {granularidade}")

    t = texto.strip()
    ref: date | None = None

    if m := _RE_ISO_DATE.match(t):
        ref = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    elif m := _RE_WEEK.match(t):
        year, week = int(m.group(1)), int(m.group(2))
        if week < 1 or week > 53:
            raise ConsultaRejeitada(f"semana inválida: {texto}")
        ref = date.fromisocalendar(year, week, 1)
    elif m := _RE_MONTH.match(t):
        year, month = int(m.group(1)), int(m.group(2))
        if month < 1 or month > 12:
            raise ConsultaRejeitada(f"mês inválido: {texto}")
        ref = date(year, month, 1)
    elif m := _RE_HALF.match(t):
        year, h = int(m.group(1)), int(m.group(2))
        ref = date(year, 1 if h == 1 else 7, 1)
    elif m := _RE_YEAR.match(t):
        ref = date(int(m.group(1)), 1, 1)
    else:
        raise ConsultaRejeitada(f"formato de período inválido: {texto}")

    inicio, _ = period_bounds(granularidade, ref)
    return inicio


def periodo_referencia(inicio: date, granularidade: str, comparacao: str) -> date:
    from datetime import timedelta

    if comparacao == "vs_mesmo_periodo_ano_anterior":
        try:
            return inicio.replace(year=inicio.year - 1)
        except ValueError:
            return inicio.replace(year=inicio.year - 1, day=28)

    if comparacao != "vs_periodo_anterior":
        raise ConsultaRejeitada(f"comparação inválida: {comparacao}")

    if granularidade == "diario":
        return inicio - timedelta(days=1)
    if granularidade == "semanal":
        return inicio - timedelta(days=7)
    if granularidade == "mensal":
        y, m = inicio.year, inicio.month - 1
        if m == 0:
            y, m = y - 1, 12
        return date(y, m, 1)
    if granularidade == "semestral":
        if inicio.month == 1:
            return date(inicio.year - 1, 7, 1)
        return date(inicio.year, 1, 1)
    if granularidade == "anual":
        return date(inicio.year - 1, 1, 1)
    raise ConsultaRejeitada(f"granularidade inválida: {granularidade}")
