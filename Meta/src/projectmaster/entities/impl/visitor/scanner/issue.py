from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.metadata import MetadataEntity
from projectmaster.entities.core.part import PartEntity
from projectmaster.entities.core.project import ProjectEntity
from projectmaster.entities.core.section import SectionEntity
from projectmaster.entities.core.unit import UnitEntity


class IssueScannerEntityVisitor(EntityVisitor):
    """Сканирующий посетитель на предмет наличия недостатков"""

    def visitMetadataEntity(self, metadata: MetadataEntity) -> None:
        pass

    def visitPartEntity(self, part: PartEntity) -> None:
        pass

    def visitUnitEntity(self, unit: UnitEntity) -> None:
        pass

    def visitSectionEntity(self, section: SectionEntity) -> None:
        pass

    def visitProjectEntity(self, project: ProjectEntity) -> None:
        pass
