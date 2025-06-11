"""
Загрузчик разделов
"""
from pathlib import Path

from projectmaster.impl.attributes.loader.section import SectionAttributesLoader
from projectmaster.abc.loaders import EntityLoader
from projectmaster.core.entities import SectionEntity
from projectmaster.impl.entities.loader.unit import UnitEntityLoader
from projectmaster.tools import iterDirs


class SectionEntityLoader(EntityLoader[SectionEntity]):
    """Загрузчик разделов"""

    def load(self) -> SectionEntity:
        attributes = SectionAttributesLoader(self.folder()).load()

        return SectionEntity(
            attributes=attributes,
            units=tuple(
                UnitEntityLoader(unit_path).load()
                for unit_path in iterDirs(self.folder(), attributes.level)
            )
        )

    def folder(self) -> Path:
        return self._path
