from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Iterable
from typing import Sequence


@dataclass(frozen=True)
class ExtensionsMatcher:
    """Сопоставляет расширения файлов"""

    extensions: Sequence[str]
    """Целевые расширения файлов"""

    def find(self, folder: Path, filename_pattern: str) -> Iterable[Path]:
        """Получить все пути к файлам по шаблону имени с данными расширениями"""
        patterns = (
            f"{filename_pattern}.{e}"
            for e in self.extensions
        )
        return chain(*(map(folder.rglob, patterns)))


def iterDirs(root: Path, level: int = 0) -> Iterable[Path]:
    """Итерация по каталогам до указанного уровня вложенности"""
    assert level >= 0

    def _subs(_dir: Path) -> Iterable[Path]:
        return filter(lambda p: p.is_dir(), _dir.iterdir())

    yield from (
        _subs(root)
        if level == 0 else
        chain(*map(_subs, iterDirs(root, level - 1)))
    )
