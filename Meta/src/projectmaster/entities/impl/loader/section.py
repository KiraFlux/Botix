"""
Загрузчик разделов
"""
from dataclasses import dataclass
from pathlib import Path

from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.section import Section
from projectmaster.entities.impl.loader.unit import UnitLoader
from projectmaster.tools import iterDirs


@dataclass(frozen=True, kw_only=True)
class SectionLoader(EntityLoader[Section]):
    """Загрузчик разделов"""

    _level: int
    """Уровень вложенности раздела"""

    def load(self) -> Section:
        return Section(
            units=tuple(
                UnitLoader(unit_path).load()
                for unit_path in iterDirs(self.folder(), self._level)
            )
        )

    def __post_init__(self) -> None:
        assert 0 <= self._level

    def folder(self) -> Path:
        return self._path
