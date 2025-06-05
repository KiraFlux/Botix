"""
Визуализация в текстовом представлении
"""

from dataclasses import dataclass
from typing import ClassVar
from typing import TextIO

from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.metadata import MetadataEntity
from projectmaster.entities.core.part import PartEntity
from projectmaster.entities.core.project import ProjectEntity
from projectmaster.entities.core.section import SectionEntity
from projectmaster.entities.core.unit import UnitEntity


@dataclass(frozen=True)
class TextRenderEntityVisitor(EntityVisitor):
    metadata_name_width: ClassVar = 24
    section_name_width: ClassVar = 32

    output: TextIO

    def writeLine(self) -> None:
        """Перенос строки"""
        self.output.write('\n')

    def writeTab(self) -> None:
        """Отступ"""
        self.output.write('\t')

    def visitMetadataEntity(self, metadata: MetadataEntity) -> None:
        self.output.write(f"{metadata.getEntityName():{self.metadata_name_width}}")

        if metadata.images:
            self.output.write(f": images({len(metadata.images)})")

    def visitPartEntity(self, part: PartEntity) -> None:
        self.visitMetadataEntity(part.metadata)

        if part.prusa_project is not None:
            self.writeTab()
            self.output.write("prusa")

        if part.transitions:
            self.writeTab()
            self.output.write('(' + ','.join(p.suffix for p in part.transitions) + ')')

    def visitUnitEntity(self, unit: UnitEntity) -> None:
        self.visitMetadataEntity(unit.metadata)
        self.writeLine()

        for part in unit.parts:
            self.writeTab()
            self.visitPartEntity(part)
            self.writeLine()

    def visitSectionEntity(self, section: SectionEntity) -> None:
        self.output.write(f"{section.attributes.name:.<{self.section_name_width}} ({len(section.units)})")
        self.writeLine()

        self.writeTab()
        self.output.write(f"{section.attributes.desc}")
        self.writeLine()

        self.writeLine()

        for unit in section.units:
            self.visitUnitEntity(unit)
            self.writeLine()

    def visitProjectEntity(self, project: ProjectEntity) -> None:
        self.output.write(f"РАЗДЕЛЫ: ({len(project.sections)})")
        self.writeLine()

        self.writeLine()

        for section in project.sections:
            self.visitSectionEntity(section)
            self.writeLine()
