from abc import ABC
from abc import abstractmethod

from projectmaster.abc.entities.visitor import EntityVisitor


class Visitable(ABC):
    """Посещаемый"""

    @abstractmethod
    def accept(self, visitor: EntityVisitor) -> None:
        """Принять посетителя"""
