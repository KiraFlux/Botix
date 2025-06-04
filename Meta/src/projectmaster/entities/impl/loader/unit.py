"""Строитель сущности модульной единицы"""
from pathlib import Path
from typing import ClassVar

from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.metadata import Metadata
from projectmaster.entities.core.unit import Unit
from projectmaster.entities.impl.loader.metadata import MetadataLoader
from projectmaster.entities.impl.loader.part import PartLoader
from projectmaster.tools import ExtensionsMatcher


class UnitMetadataLoader(MetadataLoader):

    def name(self) -> str:
        return f"{self._path.parent.name}{Metadata.parse_words_delimiter}{self._path.name}"


class UnitLoader(EntityLoader[Unit]):
    """Строитель модульных единиц"""

    part_extensions: ClassVar = ExtensionsMatcher(("m3d",))

    def load(self) -> Unit:
        return Unit(
            metadata=UnitMetadataLoader(self._path).load(),
            parts=tuple(
                PartLoader(path).load()
                for path in self.part_extensions.find(self.folder(), "*")
            )
        )

    def name(self) -> str:
        return self._path.name

    def folder(self) -> Path:
        return self._path
