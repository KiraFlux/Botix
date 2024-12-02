"""
Утилита для автоматического наведения порядка в папке с проектом.
- Транслитерация файлов
- Изменение стиля написания
- и другое...
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import Sequence

_WORK_DIR = Path(__file__).parent.absolute()


def __gen_table() -> Dict[str, str]:
    table = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
             'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
             'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
             'ъ': '`', 'ы': 'y', 'ь': '`', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
    table.update({cyrillic.upper(): latin.upper() for cyrillic, latin in table.items()})
    return table


_TABLE = __gen_table()


def to_camel_snake_case(s: str) -> str:
    """Camel_Snake_Case"""
    return '_'.join(map(lambda word: word.capitalize(), s.split()))


def to_camel_case(s: str) -> str:
    """CamelCase"""
    return ''.join(map(lambda word: word.capitalize(), s.replace("_", " ").split()))


def transliterate(s: str) -> str:
    """Bykvi"""
    return "".join(_TABLE.get(char, char) for char in s)


def transliterate_to_camel_snake_case(s: str):
    """Bykvi_Mnogo"""
    return transliterate(to_camel_snake_case(s))


def _get_workdir_size_bytes() -> int:
    return sum(p.stat().st_size for p in _WORK_DIR.rglob('*'))


def _set_shell_color(color_code: int) -> None:
    os.system(f"color {color_code:02X}")


def _get_size_str(size: int) -> str:
    step = 2 ** 16

    for unit in ("B", "KB", "MB", "GB"):
        if size < step:
            break

        size >>= 10

    return f"{size} {unit}"


@dataclass
class FileMover:
    """Настройка перемещение файлов"""
    path: Path
    target: Sequence[str]
    transformer: Callable[[str], str] = to_camel_snake_case

    def __post_init__(self) -> None:
        self.path = Path(self.path).absolute()

        if isinstance(self.transformer, str):
            self.transformer = globals().get(self.transformer)

    def _move(self, path: Path) -> bool:
        if path.suffix not in self.target:
            return False

        dest = self.path / (self.transformer(path.stem) + path.suffix)

        if path == dest:
            return False

        if dest.exists():
            os.remove(dest)

        new_path = path.rename(dest)
        print(f"MOVE: {path.name} -> {new_path}")

        return True

    def run(self, work_dir: Path) -> int:
        """Применить функцию трансформации ко всем целевым файлам в заданном каталоге"""
        moved_count = sum(map(self._move, work_dir.rglob("*")))
        print(f"Moved: {self.path.absolute().__str__() + ' ':.<100} {moved_count}")
        return moved_count


class FileMoverCollection:
    """Коллекция менеджеров настроек каталогов"""
    _file_movers: Sequence[FileMover]

    def __init__(self, json_file: Path) -> None:
        self._size_begin = _get_workdir_size_bytes()

        with open(json_file, "r") as f:
            self._file_movers = tuple(FileMover(path, **data) for path, data in json.load(f).items())

    def getMoversCount(self) -> int:
        """Получить количество менеджеров"""
        return self._file_movers.__len__()

    def getMemoryFreeBytes(self) -> int:
        """Получить объем изменения папки проекта"""
        return _get_workdir_size_bytes() - self._size_begin

    def run(self) -> int:
        """Применить всех менеджеров в папке с проектом"""
        return sum(map(lambda m: m.run(_WORK_DIR), self._file_movers))


def main():
    """Запуск скрипта"""
    _set_shell_color(0x02)

    file_mover_collection = FileMoverCollection(Path("config.json"))

    print(f"Movers: {file_mover_collection.getMoversCount()}")
    print(f"MOVED TOTAL: {file_mover_collection.run()}")
    print(f"FREE: {_get_size_str(file_mover_collection.getMemoryFreeBytes())}")

    _set_shell_color(0x07)

    input("DONE:  -> Enter <-")
    _set_shell_color(0x00)


main()
