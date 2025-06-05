"""
Визуализация в текстовом представлении
"""
from dataclasses import dataclass
from typing import TextIO

from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.metadata import MetadataEntity
from projectmaster.entities.core.part import PartEntity
from projectmaster.entities.core.project import ProjectEntity
from projectmaster.entities.core.section import SectionEntity
from projectmaster.entities.core.unit import UnitEntity


@dataclass(frozen=True)
class TextRenderEntityVisitor(EntityVisitor):
    output: TextIO

    def visitMetadataEntity(self, metadata: MetadataEntity) -> None:
        self.output.write(f"{metadata.getDisplayName()} : {metadata.getDisplayVersion()} : [images:{len(metadata.images)}]")

    def visitPartEntity(self, part: PartEntity) -> None:
        pass

    def visitUnitEntity(self, unit: UnitEntity) -> None:
        pass

    def visitSectionEntity(self, section: SectionEntity) -> None:
        pass

    def visitProjectEntity(self, project: ProjectEntity) -> None:
        pass
