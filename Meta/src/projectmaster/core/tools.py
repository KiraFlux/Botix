from itertools import chain
from pathlib import Path
from typing import Iterable


def make_glob(path: Path, patterns: Iterable[str]) -> Iterable[Path]:
    """Создать генератор путей по родительскому каталогу с указанными шаблонами"""
    return chain(*(map(path.rglob, patterns)))
