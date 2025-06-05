"""Деталь"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Sequence

from projectmaster.entities.core.metadata import MetadataEntity


@dataclass(frozen=True, kw_only=True)
class PartEntity:
    """Деталь"""

    metadata: MetadataEntity
    """Метаданные"""
    prusa_project: Optional[Path]
    """Путь к проекту Prusa этой детали"""
    transitions: Sequence[Path]
    """Пути к файлам переходных форматов"""
