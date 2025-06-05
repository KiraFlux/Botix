"""
Сущность представляющая собой сборочную единицу (модуль)
"""
from dataclasses import dataclass
from typing import Sequence

from projectmaster.entities.abc.visitable import Visitable
from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.metadata import MetadataEntity
from projectmaster.entities.core.part import PartEntity


@dataclass(frozen=True, kw_only=True)
class UnitEntity(Visitable):
    """Модульная единица"""

    metadata: MetadataEntity
    """Метаданные модуля"""
    parts: Sequence[PartEntity]
    """Детали"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitUnitEntity(self)
