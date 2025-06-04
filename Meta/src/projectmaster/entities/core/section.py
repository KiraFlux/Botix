"""
Section
"""
from dataclasses import dataclass
from typing import Sequence

from projectmaster.entities.core.unit import Unit


@dataclass(frozen=True, kw_only=True)
class Section:
    """Раздел"""

    units: Sequence[Unit]
    """Модульные единицы"""
