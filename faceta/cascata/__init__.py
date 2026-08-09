"""Cascata temporal: agrega fatos diários em granularidades superiores."""

from faceta.cascata.engine import CascadeResult, cascade_family
from faceta.cascata.families import FAMILIES
from faceta.cascata.periods import GRANULARIDADES, period_bounds

__all__ = [
    "CascadeResult",
    "FAMILIES",
    "GRANULARIDADES",
    "cascade_family",
    "period_bounds",
]
