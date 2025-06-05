from __future__ import annotations

from typing import ClassVar

from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.metadata import MetadataEntity
from projectmaster.tools import ExtensionsMatcher


class MetadataEntityLoader(EntityLoader[MetadataEntity]):
    """Строитель метаданных"""

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
