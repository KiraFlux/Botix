from projectmaster.abc.visitor import EntityVisitor
from projectmaster.core.entities import MetadataEntity
from projectmaster.core.entities import PartEntity
from projectmaster.core.entities import ProjectEntity
from projectmaster.core.entities import SectionEntity
from projectmaster.core.entities import UnitEntity


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
