from abc import ABC
from abc import abstractmethod

from projectmaster.entities.abc.visitor import EntityVisitor


class Visitable(ABC):
    """Посещаемый"""

    @abstractmethod
    def accept(self, visitor: EntityVisitor) -> None:
        """Принять посетителя"""
