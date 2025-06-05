"""
Section
"""
from dataclasses import dataclass
from typing import Sequence

from projectmaster.attributes.core.section import SectionAttributes
from projectmaster.entities.abc.visitable import Visitable
from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.unit import UnitEntity


@dataclass(frozen=True, kw_only=True)
class SectionEntity(Visitable):
    """Раздел"""

    attributes: SectionAttributes
    """Атрибуты раздела"""
    units: Sequence[UnitEntity]
    """Модульные единицы"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitSectionEntity(self)
