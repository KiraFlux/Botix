"""
Сущность представляющая собой сборочную единицу (модуль)
"""
from dataclasses import dataclass
from typing import Sequence

from projectmaster.entities.core.metadata import MetadataEntity
from projectmaster.entities.core.part import PartEntity


@dataclass(frozen=True, kw_only=True)
class UnitEntity:
    """Модульная единица"""

    metadata: MetadataEntity
    """Метаданные модуля"""
    parts: Sequence[PartEntity]
    """Детали"""
