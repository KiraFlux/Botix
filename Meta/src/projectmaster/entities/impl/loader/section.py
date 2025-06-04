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
        t = list()

        for module_type in iterDirs(self.folder()):
            for module_class in iterDirs(module_type):
                for module_version in iterDirs(module_class):
                    t.append(UnitLoader(module_version).load())

        pass

        return Section(
            units=tuple(
                t
            )
        )

    def folder(self) -> Path:
        return self._path
