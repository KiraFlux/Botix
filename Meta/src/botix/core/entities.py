from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing import Optional
from typing import Sequence

from botix.abc.visitor import EntityVisitor
from botix.abc.visitor import Visitable
from botix.core.attributes import PartsSectionAttributes
from botix.core.attributes import UnitAttributes
from botix.core.attributes import UnitsSectionAttributes


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
    """Метаданные данной детали"""
    transitions: Sequence[Path]
    """Пути к файлам переходных форматов данной детали"""
    prusa_project: Optional[Path]
    """Путь к проекту Prusa Slicer данной детали"""
    orca_project: Optional[Path]
    """Путь к проекту Orca Slicer данной детали"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitPartEntity(self)


@dataclass(frozen=True, kw_only=True)
class UnitEntity(Visitable):
    """Сборочная единица"""

    metadata: MetadataEntity
    """Метаданные сборочной единицы"""
    transition_assembly: Optional[Path]
    """Путь к файлу сборки в переходном формате"""
    parts: Sequence[PartEntity]
    """Входящие в состав детали"""
    attributes: Optional[UnitAttributes]
    """Атрибуты сборочной единицы"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitUnitEntity(self)


@dataclass(frozen=True, kw_only=True)
class UnitsSectionEntity(Visitable):
    """Раздел сборочных единиц"""

    attributes: UnitsSectionAttributes
    """Атрибуты данного раздела сборочных единиц"""
    units: Sequence[UnitEntity]
    """Сборочные единицы данного раздела"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitUnitsSectionEntity(self)


@dataclass(frozen=True, kw_only=True)
class PartsSectionEntity(Visitable):
    """Раздел общих деталей"""

    attributes: PartsSectionAttributes
    """Атрибуты данного раздела общих деталей"""
    parts: Sequence[PartEntity]
    """Детали данного раздела"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitPartsEntity(self)


@dataclass(frozen=True, kw_only=True)
class ProjectEntity(Visitable):
    """Сущность проекта"""

    units_sections: Sequence[UnitsSectionEntity]
    """Входящие в данный проект разделы сборочных единиц"""
    parts_sections: Sequence[PartsSectionEntity]
    """Входящие в данный проект разделы общих деталей"""

    def accept(self, visitor: EntityVisitor) -> None:
        visitor.visitProjectEntity(self)
