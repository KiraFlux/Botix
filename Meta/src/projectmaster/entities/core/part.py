"""Деталь"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Sequence

from projectmaster.entities.abc.visitable import Visitable
from projectmaster.entities.abc.visitor import EntityVisitor
from projectmaster.entities.core.metadata import MetadataEntity


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
