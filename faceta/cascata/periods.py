from __future__ import annotations

from datetime import date, timedelta


GRANULARIDADES = ("semanal", "mensal", "semestral", "anual")


def period_bounds(granularidade: str, ref: date) -> tuple[date, date]:
    """Retorna [início, fim) do período que contém `ref`."""
    if granularidade == "semanal":
        inicio = ref - timedelta(days=ref.weekday())  # segunda ISO
        return inicio, inicio + timedelta(days=7)
    if granularidade == "mensal":
        inicio = ref.replace(day=1)
        if inicio.month == 12:
            fim = date(inicio.year + 1, 1, 1)
        else:
            fim = date(inicio.year, inicio.month + 1, 1)
        return inicio, fim
    if granularidade == "semestral":
        if ref.month <= 6:
            return date(ref.year, 1, 1), date(ref.year, 7, 1)
        return date(ref.year, 7, 1), date(ref.year + 1, 1, 1)
    if granularidade == "anual":
        return date(ref.year, 1, 1), date(ref.year + 1, 1, 1)
    raise ValueError(f"granularidade inválida: {granularidade}")
