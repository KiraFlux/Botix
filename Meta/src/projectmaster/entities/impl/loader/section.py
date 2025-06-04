"""
Загрузчик разделов
"""
from pathlib import Path

from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.section import Section
from projectmaster.entities.impl.loader.unit import UnitLoader
from projectmaster.tools import iterDirs


class SectionLoader(EntityLoader[Section]):
    """Загрузчик разделов"""

    def load(self) -> Section:
        return Section(
            units=tuple(
                UnitLoader(unit_version).load()
                for unit_type in iterDirs(self.folder())
                for unit_kind in iterDirs(unit_type)
                for unit_version in iterDirs(unit_kind)
            )
        )

    def folder(self) -> Path:
        return self._path
