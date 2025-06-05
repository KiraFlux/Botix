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
    def visitProjectEntity(self, project) -> None:
        """Посетить сущность проекта"""

    @abstractmethod
    def visitSectionEntity(self, section) -> None:
        """Посетить сущность раздела"""

    @abstractmethod
    def visitUnitEntity(self, unit) -> None:
        """Посетить сущность модульной единицы"""
