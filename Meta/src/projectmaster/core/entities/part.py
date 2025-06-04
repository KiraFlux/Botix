"""Деталь"""
from dataclasses import dataclass

from projectmaster.core.entities.metadata import Metadata


@dataclass(frozen=True, kw_only=True)
class Part:
    """Деталь"""

    metadata: Metadata
    """Метаданные"""
