"""
Утилита для автоматического наведения порядка в папке с проектом.
- Транслитерация файлов
- Изменение стиля написания
- и другое...
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import TextIO

_WORK_DIR = Path(__file__).parent.absolute()


class Color:
    """ANSI escape цвета"""
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(status: str, message: str) -> None:
    """
    Вывод сообщения
    Args:
        status: Статус задачи
        message: Сообщение
    """
    sys.stdout.write(f"[{Color.OK_GREEN}{f'{status:^10}'}{Color.END}]\t{Color.BOLD}{message}{Color.END}\n")


def _get_workdir_size_bytes() -> int:
    return sum(p.stat().st_size for p in _WORK_DIR.rglob('*'))


def _set_shell_color(color_code: int) -> int:
    return os.system(f"color {color_code:02X}")


def _shell_timeout(duration: int) -> int:
    return os.system(f"timeout {duration}")


def _get_size_str(size: int) -> str:
    step = 2 ** 16

    for unit in ("B", "KB", "MB", "GB"):
        if size < step:
            break

        size >>= 10

    return f"{size} {unit}"


def _make_glob(path: Path, extensions: Sequence[str]):
    return chain(*(path.rglob(f"*.{extension}") for extension in extensions))


@dataclass
class PathTransformer:
    """Обертка над Path"""

    parent: Path
    path: Path

    def transliterate(self) -> PathTransformer:
        """Имя файла будет транслитерировано"""
        self._change_filename(self._transliterate(self.path.stem))
        return self

    def camel_case(self) -> PathTransformer:
        """Имя файла будет форматировано в Camel_Case"""
        self._change_filename(self._camel_case(self.path.stem))
        return self

    def add_parent(self) -> PathTransformer:
        """Добавить к имени файла родительский каталог"""
        self._change_filename(self._add_parent_catalog_path(self.path))
        return self

    __TRANSLITERATE_TABLE = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
        'щ': 'sch', 'ъ': '`', 'ы': 'y', 'ь': '`', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    def _change_filename(self, new_name: str) -> None:
        self.path = self.parent / (new_name + self.path.suffix)

    def _transliterate(self, s: str) -> str:
        return "".join(self.__TRANSLITERATE_TABLE.get(char, char) for char in s.lower())

    @staticmethod
    def _camel_case(s: str) -> str:
        return '_'.join(map(lambda word: word.capitalize(), s.split()))

    @staticmethod
    def _add_parent_catalog_path(path: Path) -> str:
        return f"{path.parent.stem}__{path.stem}"


FileNameTransformer = Callable[[PathTransformer], PathTransformer]


class FileMover:
    """Настройка перемещение файлов"""

    def __init__(self, path: str, target: Sequence[str], transformer: Optional[str] = None) -> None:
        """
        Агент каталога
        path: Относительный путь к целевому каталогу
        target: Целевые расширения файлов
        transformer: Наименование функции трансформации имени перемещаемого файла
        """

        self.dest_path = Path(path).absolute()
        self.transformer = self._get_filename_transformer(transformer)
        self.target_extensions = target

    def run(self, work_dir: Path) -> int:
        """Применить функцию трансформации ко всем целевым файлам в заданном каталоге"""
        if not self.dest_path.exists():
            print(f"MKDIR: {self.dest_path!s}")
            self.dest_path.mkdir(parents=True)

        moved_count = sum(map(self._move, _make_glob(work_dir, self.target_extensions)))
        print(f"Moved: {self.dest_path.absolute().__str__() + ' ':.<100} {moved_count}")
        return moved_count

    def _move(self, path: Path) -> bool:
        if path.parent == self.dest_path:
            return False

        dest = self.transformer(PathTransformer(self.dest_path, path)).path

        if dest.exists():
            os.remove(dest)

        new_path = path.rename(dest)
        print(f"MOVE: {path.name} -> {new_path}")

        return True

    def _get_filename_transformer(self, transformer_name: Optional[str]) -> FileNameTransformer:
        return self.__FILENAME_TRANSFORMER_TABLE[transformer_name]

    __FILENAME_TRANSFORMER_TABLE = {
        None: lambda path: path,
        "translit": lambda path: path.transliterate(),
        "camel_case": lambda path: path.camel_case(),
        "add_parent_catalog": lambda path: path.add_parent(),
        "3d_print_special": lambda path: path.add_parent().camel_case().transliterate()
    }


class FileMoverCollection:
    """Коллекция менеджеров настроек каталогов"""

    def __init__(self, json_file: Path) -> None:
        self._size_begin = _get_workdir_size_bytes()

        with open(json_file, "r") as f:
            self._file_movers: Sequence[FileMover] = tuple(self._get_file_movers(f))

    def get_movers_count(self) -> int:
        """Получить количество менеджеров"""
        return self._file_movers.__len__()

    def get_memory_free_bytes(self) -> int:
        """Получить объем изменения папки проекта"""
        return _get_workdir_size_bytes() - self._size_begin

    def run(self) -> int:
        """Применить всех менеджеров в папке с проектом"""
        return sum(map(lambda m: m.run(_WORK_DIR), self._file_movers))

    @staticmethod
    def _get_file_movers(json_file: TextIO) -> Iterable[FileMover]:
        return (FileMover(path, **data) for path, data in json.load(json_file).items())


def _launch():
    _set_shell_color(0x02)

    file_mover_collection = FileMoverCollection(Path("CleanupConfig.json"))

    print(f"Movers: {file_mover_collection.get_movers_count()}")
    print(f"MOVED TOTAL: {file_mover_collection.run()}")
    print(f"FREE: {_get_size_str(file_mover_collection.get_memory_free_bytes())}")

    _set_shell_color(0x07)

    _shell_timeout(5)
    _set_shell_color(0x00)


_launch()

# log("test", "task complete!")
