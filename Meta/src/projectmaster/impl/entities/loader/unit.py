"""Строитель сущности модульной единицы"""
from pathlib import Path
from typing import ClassVar

from projectmaster.abc.entities.loader import EntityLoader
from projectmaster.core.entities import MetadataEntity
from projectmaster.core.entities import UnitEntity
from projectmaster.impl.entities.loader.metadata import MetadataEntityLoader
from projectmaster.impl.entities.loader.part import PartEntityLoader
from projectmaster.tools import ExtensionsMatcher


class UnitMetadataEntityLoader(MetadataEntityLoader):

    def name(self) -> str:
        return f"{self._path.parent.name}{MetadataEntity.parse_words_delimiter}{self._path.name}"


class UnitEntityLoader(EntityLoader[UnitEntity]):
    """Строитель модульных единиц"""

    part_extensions: ClassVar = ExtensionsMatcher(("m3d",))

    def load(self) -> UnitEntity:
        return UnitEntity(
            metadata=UnitMetadataEntityLoader(self._path).load(),
            parts=tuple(
                PartEntityLoader(path).load()
                for path in self.part_extensions.find(self.folder(), "*")
            )
        )

    def name(self) -> str:
        return self._path.name

    def folder(self) -> Path:
        return self._path
