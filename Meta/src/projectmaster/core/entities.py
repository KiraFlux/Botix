from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing import Optional
from typing import Sequence

from projectmaster.abc.visitor import EntityVisitor
from projectmaster.abc.visitor import Visitable
from projectmaster.core.attributes import SectionAttributes


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


@dataclass(frozen=True, kw_only=True)
class PartEntity(Visitable):
    """Деталь"""

    metadata: MetadataEntity
    """Метаданные"""
    prusa_project: Optional[Path]
    """Путь к проекту Prusa этой детали"""
    transitions: Sequence[Path]
    """Пути к файлам переходных форматов"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitPartEntity(self)


@dataclass(frozen=True, kw_only=True)
class ProjectEntity(Visitable):
    """Сущность проекта"""

    sections: Sequence[SectionEntity]
    """Разделы сущностей"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitProjectEntity(self)


@dataclass(frozen=True, kw_only=True)
class SectionEntity(Visitable):
    """Раздел"""

    attributes: SectionAttributes
    """Атрибуты раздела"""
    units: Sequence[UnitEntity]
    """Модульные единицы"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitSectionEntity(self)


@dataclass(frozen=True, kw_only=True)
class UnitEntity(Visitable):
    """Модульная единица"""

    metadata: MetadataEntity
    """Метаданные модуля"""
    parts: Sequence[PartEntity]
    """Детали"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitUnitEntity(self)
