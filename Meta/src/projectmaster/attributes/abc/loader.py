import json
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Mapping


@dataclass(frozen=True)
class AttributesLoader[T](ABC):
    """Загрузчик атрибутов"""

    path: Path

    @abstractmethod
    def getSuffix(self) -> str:
        """Суффикс файла атрибутов"""

    @abstractmethod
    def parse(self, data: Mapping[str, Any]) -> T:
        """Преобразовать файл атрибутов"""

    def load(self) -> T:
        """Загрузить атрибуты"""
        with open(self._getFilePath()) as f:
            data = json.load(f)
            return self.parse(data)

    def exists(self) -> bool:
        """Каталог содержит атрибут"""
        return self._getFilePath().exists()

    def _getFilePath(self) -> Path:
        return self.path / f".{self.getSuffix()}"
