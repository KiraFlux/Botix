"""
Визуализация в текстовом представлении
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import TextIO

from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.metadata import MetadataEntity
from projectmaster.entities.core.part import PartEntity
from projectmaster.entities.core.project import ProjectEntity
from projectmaster.entities.core.section import SectionEntity
from projectmaster.entities.core.unit import UnitEntity


@dataclass
class IntendTextIOAdapter:
    """Адаптер над TextIO для реализации записи с отступами"""

    _intend: ClassVar = 4
    _intend_string: ClassVar = ' ' * _intend

    _source: TextIO
    _intend_level: int = field(init=False, default=0)

    def push(self) -> None:
        """Внести отступ"""
        self._intend_level += 1

    def pop(self) -> None:
        """Вынести отступ"""
        self._intend_level -= 1
        assert self._intend_level >= 0

    def _write(self, s: str) -> None:
        self._source.write(s)

    def write(self, s: str = None) -> None:
        """Записать"""

        if s is not None:
            self._write(self._intend_string * self._intend_level)
            self._write(s)

        self._source.write('\n')


@dataclass(frozen=True)
class TextRenderEntityVisitor(EntityVisitor):
    metadata_name_width: ClassVar = 32

    out: IntendTextIOAdapter

    def visitMetadataEntity(self, metadata: MetadataEntity) -> None:
        s = f"{metadata.getEntityName():{self.metadata_name_width}}"

        if metadata.images:
            s += f": images({len(metadata.images)})"

        self.out.write(s)

    def visitPartEntity(self, part: PartEntity) -> None:
        self.visitMetadataEntity(part.metadata)

        self.out.push()

        s = str()

        if part.prusa_project is not None:
            s += "prusa"

        if s:
            s += '\t'

        if part.transitions:
            s += tuple(p.suffix for p in part.transitions).__str__()

        if s:
            self.out.write(s)

        self.out.pop()

    def visitUnitEntity(self, unit: UnitEntity) -> None:
        self.visitMetadataEntity(unit.metadata)

        for part in unit.parts:
            self.out.push()
            self.visitPartEntity(part)
            self.out.pop()

    def visitSectionEntity(self, section: SectionEntity) -> None:
        self.out.write(f"{section.attributes.name} ({len(section.units)})")

        self.out.push()
        self.out.write(f"{section.attributes.desc}")
        self.out.pop()

        self.out.write()

        for unit in section.units:
            self.out.push()

            self.visitUnitEntity(unit)
            self.out.write()

            self.out.pop()

    def visitProjectEntity(self, project: ProjectEntity) -> None:
        self.out.write(f"РАЗДЕЛЫ: ({len(project.sections)})")
        self.out.write()

        for section in project.sections:
            self.visitSectionEntity(section)
            self.out.write()
