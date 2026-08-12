"""Helpers de calendário puros (sem I/O) para ops e scripts de mês/ano."""

from __future__ import annotations

from datetime import date, timedelta


def month_bounds(year: int, month: int) -> tuple[date, date]:
    """Retorna [primeiro, próximo_mês)."""
    first = date(year, month, 1)
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    return first, nxt


def days_in_month(year: int, month: int) -> list[date]:
    first, nxt = month_bounds(year, month)
    out: list[date] = []
    d = first
    while d < nxt:
        out.append(d)
        d += timedelta(days=1)
    return out


def days_in_year(ano: int, de_mes: int = 1, ate_mes: int = 12) -> list[date]:
    """Concatena days_in_month() para cada mês do intervalo [de_mes, ate_mes]."""
    if not (1 <= de_mes <= 12 and 1 <= ate_mes <= 12 and de_mes <= ate_mes):
        raise ValueError(f"intervalo de mês inválido: {de_mes}..{ate_mes}")
    out: list[date] = []
    for mes in range(de_mes, ate_mes + 1):
        out.extend(days_in_month(ano, mes))
    return out


def iso_week_label(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def iso_weeks_of_year(ano: int) -> list[tuple[date, str]]:
    """Todas as segundas ISO cujo intervalo toca o ano civil."""
    first, last = date(ano, 1, 1), date(ano, 12, 31)
    monday = first - timedelta(days=first.weekday())
    out: list[tuple[date, str]] = []
    d = monday
    while d <= last:
        out.append((d, iso_week_label(d)))
        d += timedelta(days=7)
    return out


def iso_weeks_touching_month(year: int, month: int) -> list[tuple[date, str]]:
    """Segundas ISO + rótulo YYYY-Www das semanas que intersectam o mês."""
    first, nxt = month_bounds(year, month)
    last = nxt - timedelta(days=1)
    monday = first - timedelta(days=first.weekday())
    weeks: list[tuple[date, str]] = []
    seen: set[str] = set()
    d = monday
    while d <= last:
        week_end = d + timedelta(days=7)
        if week_end > first and d < nxt:
            label = iso_week_label(d)
            if label not in seen:
                seen.add(label)
                weeks.append((d, label))
        d += timedelta(days=7)
    return weeks


def iso_weeks_in_range(ano: int, de_mes: int = 1, ate_mes: int = 12) -> list[tuple[date, str]]:
    """Semanas ISO que tocam o intervalo de meses (união sem duplicar)."""
    if de_mes == 1 and ate_mes == 12:
        return iso_weeks_of_year(ano)
    seen: set[str] = set()
    out: list[tuple[date, str]] = []
    for mes in range(de_mes, ate_mes + 1):
        for monday, label in iso_weeks_touching_month(ano, mes):
            if label not in seen:
                seen.add(label)
                out.append((monday, label))
    out.sort(key=lambda x: x[0])
    return out


def semesters_of_year(ano: int) -> list[tuple[date, str]]:
    return [(date(ano, 1, 1), f"{ano}-H1"), (date(ano, 7, 1), f"{ano}-H2")]


def semesters_in_range(ano: int, de_mes: int = 1, ate_mes: int = 12) -> list[tuple[date, str]]:
    """Semestres que intersectam [de_mes, ate_mes]."""
    out: list[tuple[date, str]] = []
    if max(de_mes, 1) <= min(ate_mes, 6):
        out.append((date(ano, 1, 1), f"{ano}-H1"))
    if max(de_mes, 7) <= min(ate_mes, 12):
        out.append((date(ano, 7, 1), f"{ano}-H2"))
    return out
