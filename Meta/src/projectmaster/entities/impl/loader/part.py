from __future__ import annotations

from pathlib import Path
from typing import ClassVar
from typing import Optional

from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.part import Part
from projectmaster.entities.impl.loader.metadata import MetadataLoader
from projectmaster.tools import ExtensionsMatcher


class PartLoader(EntityLoader[Part]):
    """Строитель сущности представления детали"""

    prusa_project_extension: ClassVar = "3mf"
    """Расширение проекта Prusa"""
    transition_extensions: ClassVar = ExtensionsMatcher(("stp", "step", "stl", "obj"))
    """Переходные форматы деталей"""

    def load(self) -> Part:
        """Создать представление детали"""
        return Part(
            metadata=MetadataLoader(self._path).load(),
            prusa_project=self._loadPrusaProjectFile(),
            transitions=tuple(self.transition_extensions.find(self.folder(), self.name()))
        )

    def _loadPrusaProjectFile(self) -> Optional[Path]:
        prusa_path = self.folder() / f"{self.name()}.{self.prusa_project_extension}"
        return prusa_path if prusa_path.exists() else None
