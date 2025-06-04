"""Работа с метаданными сущности"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing import Iterable
from typing import Sequence


@dataclass(frozen=True, kw_only=True)
class Metadata:
    """Метаданные сущности"""

    parse_words_delimiter: ClassVar = '-'
    """Разделитель слов при чтении"""
    display_words_joiner: ClassVar = ' '
    """Объединитель слов при отображении"""
    version_prefix: ClassVar = 'v'
    """Префикс версии"""
    default_version: ClassVar = 1
    """Версия, если префикс отсутствует"""
    image_extensions: ClassVar = ("png", "jpg", "jpeg")
    """Расширение файла изображения"""

    path: Path
    """Путь"""
    words: Sequence[str]
    """Ключевые слова"""
    version: int
    """Версия"""
    images: Sequence[Path]
    """Изображения"""

    @classmethod
    def extractVersion(cls, vs: str) -> int:
        """Извлечь версию из строки"""
        pure_version_string = vs[slice(len(cls.version_prefix), None)]
        return int(pure_version_string)

    def getDisplayName(self) -> str:
        """Получить отображаемое имя"""
        return self.display_words_joiner.join(self.words)

    def getDisplayVersion(self) -> str:
        """Получить отображаемую версию"""
        return f"{self.version_prefix}{self.version}"

    @classmethod
    def getImageFilePatterns(cls, filename: str) -> Iterable[str]:
        """Получить шаблон пути изображения"""
        return (
            f"{filename}{cls.parse_words_delimiter}*.{e}"
            for e in cls.image_extensions
        )
