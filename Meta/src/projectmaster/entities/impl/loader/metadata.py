from __future__ import annotations

from typing import ClassVar

from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.metadata import Metadata
from projectmaster.tools import ExtensionsMatcher


class MetadataLoader(EntityLoader[Metadata]):
    """Строитель метаданных"""

    default_version: ClassVar = 1
    """Версия, если префикс отсутствует"""
    image_extensions: ClassVar = ExtensionsMatcher(("png", "jpg", "jpeg"))
    """Расширение файла изображения"""

    def load(self) -> Metadata:
        words = self.name().split(Metadata.parse_words_delimiter)

        if words[-1].lower().startswith(Metadata.version_prefix):
            *words, version_string = words
            pure_version_string = version_string[slice(len(Metadata.version_prefix), None)]
            v = int(pure_version_string)
        else:
            v = self.default_version

        return Metadata(
            path=self._path,
            words=words,
            version=v,
            images=tuple(self.image_extensions.find(self.folder(), f"{self.name()}{Metadata.parse_words_delimiter}*"))
        )
