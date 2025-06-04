"""Деталь"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Sequence

from projectmaster.entities.core.metadata import Metadata


@dataclass(frozen=True, kw_only=True)
class Part:
    """Деталь"""

    metadata: Metadata
    """Метаданные"""
    prusa_project: Optional[Path]
    """Путь к проекту Prusa этой детали"""
    transitions: Sequence[Path]
    """Пути к файлам переходных форматов"""
