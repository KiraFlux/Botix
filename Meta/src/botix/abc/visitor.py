from abc import ABC
from abc import abstractmethod


class EntityVisitor(ABC):
    """Базовый посетитель сущностей"""

    @abstractmethod
    def visitMetadataEntity(self, metadata) -> None:
        """Посетить сущность метаданных"""

    @abstractmethod
    def visitPartEntity(self, part) -> None:
        """Посетить сущность детали"""

    @abstractmethod
    def visitPartsEntity(self, parts_section) -> None:
        """Посетить раздел деталей"""

    @abstractmethod
    def visitUnitEntity(self, unit) -> None:
        """Посетить сущность модульной единицы"""

    @abstractmethod
    def visitUnitsSectionEntity(self, units_section) -> None:
        """Посетить сущность раздела сборочных единиц"""

    @abstractmethod
    def visitProjectEntity(self, project) -> None:
        """Посетить сущность проекта"""


class Visitable(ABC):
    """Посещаемый"""

    @abstractmethod
    def accept(self, visitor: EntityVisitor) -> None:
        """Принять посетителя"""
