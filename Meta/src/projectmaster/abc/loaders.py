import json
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Mapping
from typing import final


@dataclass(frozen=True)
class Loader[T](ABC):
    """Общий загрузчик"""

    _path: Path
    """Рабочий путь"""

    @abstractmethod
    def load(self) -> T:
        """Загрузить"""


class AttributesLoader[T](Loader[T], ABC):

    @abstractmethod
    def getSuffix(self) -> str:
        """Суффикс файла атрибутов"""

    @abstractmethod
    def parse(self, data: Mapping[str, Any]) -> T:
        """Преобразовать файл атрибутов"""

    @final
    def load(self) -> T:
        with open(self._getFilePath()) as f:
            data = json.load(f)
            return self.parse(data)

    @final
    def exists(self) -> bool:
        """Каталог содержит атрибут"""
        return self._getFilePath().exists()

    def _getFilePath(self) -> Path:
        return self._path / f".{self.getSuffix()}"


class EntityLoader[T](Loader[T], ABC):

    def name(self) -> str:
        """Имя сущности"""
        return self._path.stem

    def folder(self) -> Path:
        """Каталог с материалами для сущности"""
        return self._path.parent
