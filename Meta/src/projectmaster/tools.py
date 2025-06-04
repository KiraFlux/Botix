from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Iterable
from typing import Sequence


@dataclass(frozen=True)
class ExtensionsMatcher:
    """Сопоставляет расширения файлов"""

    _extensions: Sequence[str]
    """Целевые расширения файлов"""

    def find(self, folder: Path, filename_pattern: str) -> Iterable[Path]:
        """Получить все пути к файлам по шаблону имени с данными расширениями"""
        patterns = (
            f"{filename_pattern}.{e}"
            for e in self._extensions
        )
        return chain(*(map(folder.rglob, patterns)))
