"""Деталь"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing import Optional
from typing import Sequence

from projectmaster.core.entities.metadata import Metadata
from projectmaster.core.tools import make_glob


@dataclass(frozen=True, kw_only=True)
class Part:
    """Деталь"""

    metadata: Metadata
    """Метаданные"""
    prusa_project: Optional[Path]
    """Путь к проекту Prusa этой детали"""
    transitions: Sequence[Path]
    """Пути к файлам переходных форматов"""


@dataclass
class PartBuilder:
    """Строитель сущности представления детали"""

    prusa_project_extension: ClassVar = "3mf"
    """Расширение проекта Prusa"""
    transition_extensions: ClassVar = ("stp", "step", "stl", "obj")
    """Переходные форматы деталей"""

    _path: Path
    """Путь к исходной детали"""

    def build(self) -> Part:
        """Создать представление детали"""
        return Part(
            metadata=self._loadMetadata(),
            prusa_project=self._loadPrusaProjectFile(),
            transitions=self._loadTranslationFiles()
        )

    @property
    def _filename(self) -> str:
        return self._path.stem

    @property
    def _folder(self) -> Path:
        return self._path.parent

    def _loadMetadata(self) -> Metadata:
        words = self._filename.split(Metadata.parse_words_delimiter)

        if words[-1].lower().startswith(Metadata.version_prefix):
            *words, version_string = words
            v = Metadata.extractVersion(version_string)
        else:
            v = Metadata.default_version

        return Metadata(
            path=self._path,
            words=words,
            version=v,
            images=tuple(make_glob(self._folder, Metadata.getImageFilePatterns(self._filename)))
        )

    def _loadPrusaProjectFile(self) -> Optional[Path]:
        prusa_path = self._folder / f"{self._filename}.{self.prusa_project_extension}"
        return prusa_path if prusa_path.exists() else None

    def _loadTranslationFiles(self) -> Sequence[Path]:
        return tuple(make_glob(self._folder, (
            f"{self._filename}.{e}"
            for e in self.transition_extensions
        )))
