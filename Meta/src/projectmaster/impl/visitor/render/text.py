"""
Визуализация в текстовом представлении
"""

from dataclasses import dataclass
from typing import ClassVar

from engines.text import FormatTextIOAdapter
from engines.text import MockWritingMethod
from projectmaster.abc.visitor import EntityVisitor
from projectmaster.core.entities import MetadataEntity
from projectmaster.core.entities import PartEntity
from projectmaster.core.entities import ProjectEntity
from projectmaster.core.entities import SectionEntity
from projectmaster.core.entities import UnitEntity


@dataclass(frozen=True)
class TextRenderEntityVisitor(EntityVisitor):
    metadata_name_width: ClassVar = 32

    out: FormatTextIOAdapter

    def visitMetadataEntity(self, metadata: MetadataEntity) -> None:
        s = f"{metadata.getEntityName():{self.metadata_name_width}}"

        if metadata.images:
            s += f": images({len(metadata.images)})"

        self.out.write(s)

    def visitPartEntity(self, part: PartEntity) -> None:
        self.visitMetadataEntity(part.metadata)

        with self.out.use(MockWritingMethod()):
            s = str()

            if part.prusa_project is not None:
                s += "prusa"

            if s:
                s += '\t'

            if part.transitions:
                s += tuple(p.suffix for p in part.transitions).__str__()

            if s:
                self.out.write(s)

    def visitUnitEntity(self, unit: UnitEntity) -> None:
        self.visitMetadataEntity(unit.metadata)

        for part in unit.parts:
            with self.out.use(MockWritingMethod()):
                self.visitPartEntity(part)

    def visitSectionEntity(self, section: SectionEntity) -> None:
        self.out.write(f"{section.attributes.name} ({len(section.units)})")

        with self.out.use(MockWritingMethod()):
            self.out.write(f"{section.attributes.desc}")

        self.out.write()

        for unit in section.units:
            with self.out.use(MockWritingMethod()):
                self.visitUnitEntity(unit)
                self.out.write()

    def visitProjectEntity(self, project: ProjectEntity) -> None:
        self.out.write(f"РАЗДЕЛЫ: ({len(project.sections)})")
        self.out.write()

        for section in project.sections:
            self.visitSectionEntity(section)
            self.out.write()
