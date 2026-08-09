from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Iterable


def parse_data(value: str | date | None) -> date:
    if value is None:
        return date.today().fromordinal(date.today().toordinal() - 1)
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    return date.fromisoformat(str(value))


def yesterday() -> date:
    today = date.today()
    return date.fromordinal(today.toordinal() - 1)


def dec(value) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def chunked(rows: list, size: int = 500) -> Iterable[list]:
    for i in range(0, len(rows), size):
        yield rows[i : i + size]
