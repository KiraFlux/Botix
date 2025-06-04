from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Iterable
from typing import Sequence


def _make_glob(path: Path, patterns: Iterable[str]) -> Iterable[Path]:
    """Создать генератор путей по родительскому каталогу с указанными шаблонами"""
    return chain(*(map(path.rglob, patterns)))


@dataclass(frozen=True)
class ExtensionsMatcher:
    """Сопоставляет расширения файлов"""

    _extensions: Sequence[str]
    """Целевые расширения файлов"""

    def find(self, folder: Path, filename_pattern: str) -> Iterable[Path]:
        """Получить все пути к файлам по шаблону имени с данными расширениями"""
        return _make_glob(folder, (
            f"{filename_pattern}.{e}"
            for e in self._extensions
        ))
