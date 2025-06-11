"""Загрузчик сущностей"""
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EntityLoader[T](ABC):
    """Загрузчик сущностей"""

    _path: Path
    """Путь к сущности"""

    @abstractmethod
    def load(self) -> T:
        """загрузить сущность"""

    def name(self) -> str:
        """Имя сущности"""
        return self._path.stem

    def folder(self) -> Path:
        """Каталог с материалами для сущности"""
        return self._path.parent
