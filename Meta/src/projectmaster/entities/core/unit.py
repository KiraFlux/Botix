"""
Сущность представляющая собой сборочную единицу (модуль)
"""
from dataclasses import dataclass
from typing import Sequence

from projectmaster.entities.core.metadata import Metadata
from projectmaster.entities.core.part import Part


@dataclass(frozen=True, kw_only=True)
class Unit:
    """Модульная единица"""

    metadata: Metadata
    """Метаданные модуля"""
    parts: Sequence[Part]
    """Детали"""
