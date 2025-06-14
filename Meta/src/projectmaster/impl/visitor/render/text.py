"""
Визуализация в текстовом представлении
"""

from dataclasses import dataclass
from typing import ClassVar

from engines.text import FormatTextIOAdapter
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

        self.out.write(f"{metadata.getEntityName():{self.metadata_name_width}}")

        if metadata.images:
            with self.out.markedList():
                self.out.write(f"Изображения: ({len(metadata.images)})")

                with self.out.numericList():
                    for i in metadata.images:
                        self.out.write(i.name)

    def visitPartEntity(self, part: PartEntity) -> None:
        self.visitMetadataEntity(part.metadata)

        if part.prusa_project or part.transitions:
            with self.out.markedList():
                self.out.write("Обменные форматы")

                with self.out.markedList():
                    if part.prusa_project is not None:
                        self.out.write("prusa")

                    for p in part.transitions:
                        self.out.write(p.suffix)

    def visitUnitEntity(self, unit: UnitEntity) -> None:
        self.visitMetadataEntity(unit.metadata)

        with self.out.numericList():
            for part in unit.parts:
                self.visitPartEntity(part)

    def visitSectionEntity(self, section: SectionEntity) -> None:
        self.out.write(f"{section.attributes.name} ({len(section.units)})")

        with self.out.markedList():
            self.out.write(f"{section.attributes.desc}")
            self.out.write(f"Уровень: {section.attributes.level}")

        self.out.write()

        with self.out.numericList():
            for unit in section.units:
                self.visitUnitEntity(unit)
                self.out.write()

    def visitProjectEntity(self, project: ProjectEntity) -> None:
        self.out.write(f"РАЗДЕЛЫ: ({len(project.sections)})")
        self.out.write()

        for section in project.sections:
            self.visitSectionEntity(section)
            self.out.write()
