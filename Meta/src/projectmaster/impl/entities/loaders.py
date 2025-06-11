from __future__ import annotations

from pathlib import Path
from typing import ClassVar
from typing import Optional

from projectmaster.abc.loaders import EntityLoader
from projectmaster.core.entities import MetadataEntity
from projectmaster.core.entities import PartEntity
from projectmaster.core.entities import ProjectEntity
from projectmaster.core.entities import SectionEntity
from projectmaster.core.entities import UnitEntity
from projectmaster.impl.attributes.loader.section import SectionAttributesLoader
from projectmaster.tools import ExtensionsMatcher
from projectmaster.tools import iterDirs


class MetadataEntityLoader(EntityLoader[MetadataEntity]):
    """Загрузчик метаданных"""

    default_version: ClassVar = 1
    """Версия, если префикс отсутствует"""
    image_extensions: ClassVar = ExtensionsMatcher(("png", "jpg", "jpeg"))
    """Расширение файла изображения"""

    def load(self) -> MetadataEntity:
        words = self.name().split(MetadataEntity.parse_words_delimiter)

        if words[-1].lower().startswith(MetadataEntity.version_prefix):
            *words, version_string = words
            pure_version_string = version_string[slice(len(MetadataEntity.version_prefix), None)]
            v = int(pure_version_string)
        else:
            v = self.default_version

        return MetadataEntity(
            path=self._path,
            words=words,
            version=v,
            images=tuple(self.image_extensions.find(self.folder(), f"{self.name()}{MetadataEntity.parse_words_delimiter}*"))
        )


class PartEntityLoader(EntityLoader[PartEntity]):
    """Строитель сущности представления детали"""

    prusa_project_extension: ClassVar = "3mf"
    """Расширение проекта Prusa"""
    transition_extensions: ClassVar = ExtensionsMatcher(("stp", "step", "stl", "obj"))
    """Переходные форматы деталей"""

    def load(self) -> PartEntity:
        """Создать представление детали"""
        return PartEntity(
            metadata=MetadataEntityLoader(self._path).load(),
            prusa_project=self._loadPrusaProjectFile(),
            transitions=tuple(self.transition_extensions.find(self.folder(), self.name()))
        )

    def _loadPrusaProjectFile(self) -> Optional[Path]:
        prusa_path = self.folder() / f"{self.name()}.{self.prusa_project_extension}"
        return prusa_path if prusa_path.exists() else None


class ProjectEntityLoader(EntityLoader[ProjectEntity]):
    def load(self) -> ProjectEntity:
        return ProjectEntity(
            sections=tuple(
                SectionEntityLoader(p).load()
                for p in iterDirs(self.folder())
                if SectionAttributesLoader(self.folder() / p).exists()
            )
        )

    def folder(self) -> Path:
        return self._path


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
