from dataclasses import dataclass
from typing import Sequence

from projectmaster.entities.core.section import SectionEntity


@dataclass(frozen=True, kw_only=True)
class ProjectEntity:
    """Сущность проекта"""

    sections: Sequence[SectionEntity]
    """Разделы сущностей"""
