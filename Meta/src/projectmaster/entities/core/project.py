from dataclasses import dataclass
from typing import Sequence

from projectmaster.entities.abc.visitable import Visitable
from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.section import SectionEntity


@dataclass(frozen=True, kw_only=True)
class ProjectEntity(Visitable):
    """Сущность проекта"""

    sections: Sequence[SectionEntity]
    """Разделы сущностей"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitProjectEntity(self)
