"""
Section
"""
from dataclasses import dataclass
from typing import Sequence

from projectmaster.attributes.core.section import SectionAttributes
from projectmaster.entities.core.unit import UnitEntity


@dataclass(frozen=True, kw_only=True)
class SectionEntity:
    """Раздел"""

    attributes: SectionAttributes
    """Атрибуты раздела"""
    units: Sequence[UnitEntity]
    """Модульные единицы"""
