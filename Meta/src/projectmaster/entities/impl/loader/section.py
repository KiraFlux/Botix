"""
Загрузчик разделов
"""
from dataclasses import dataclass
from pathlib import Path

from projectmaster.attributes.impl.loader.section import SectionAttributesLoader
from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.section import SectionEntity
from projectmaster.entities.impl.loader.unit import UnitEntityLoader
from projectmaster.tools import iterDirs


@dataclass(frozen=True, kw_only=True)
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
