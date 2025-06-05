"""Работа с метаданными сущности"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing import Sequence

from projectmaster.entities.abc.visitable import Visitable
from projectmaster.entities.abc.visitor import EntityVisitor


@dataclass(frozen=True, kw_only=True)
class MetadataEntity(Visitable):
    """Метаданные сущности"""

    parse_words_delimiter: ClassVar = '-'
    """Разделитель слов при чтении"""
    display_words_joiner: ClassVar = ' '
    """Объединитель слов при отображении"""
    version_prefix: ClassVar = 'v'
    """Префикс версии"""

    path: Path
    """Путь"""
    words: Sequence[str]
    """Ключевые слова"""
    version: int
    """Версия"""
    images: Sequence[Path]
    """Изображения"""

    def getDisplayName(self) -> str:
        """Получить отображаемое имя"""
        return self.display_words_joiner.join(self.words)

    def getDisplayVersion(self) -> str:
        """Получить отображаемую версию"""
        return f"{self.version_prefix}{self.version}"

    def getEntityName(self) -> str:
        """Получить имя сущности"""
        w = tuple(self.words) + (self.getDisplayVersion(),)
        return f"{self.parse_words_delimiter.join(w)}"

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitMetadataEntity(self)
