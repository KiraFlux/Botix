"""
Мастер для управления проектов.

"""
from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Final
from typing import Iterable
from typing import MutableMapping
from typing import Optional
from typing import Sequence

from CleanupUtill import make_glob

EXT_3MF: Final[str] = "3mf"
EXT_STP: Final[str] = "stp"
EXT_M3D: Final[str] = "m3d"


def _exists_with_ext(original_path: Path, ext: str) -> bool:
    return (original_path.parent / f"{original_path.stem}.{ext}").exists()


@dataclass(frozen=True)
class MetaData:
    """Метаданные объекта"""

    path: Path
    """Путь к элементу"""
    version: int
    """Версия элемента"""
    words: Sequence[str]
    """Наименование элемента"""

    @classmethod
    def load(cls, path: Path) -> MetaData:
        """Создать на основе пути"""
        filename = path.stem
        split = filename.split('-')

        if "V" in split[-1]:
            *words, (_, *version_token) = split
            return cls(path, int("".join(version_token)), words)

        else:
            return cls(path, 1, split)

    def name(self) -> str:
        """Собрать наименование"""
        return " ".join(self.words)

    def __repr__(self) -> str:
        return f"{self.name()} - V{self.version}"


@dataclass(frozen=True)
class Element:
    """Элемент моделирования"""

    metadata: MetaData
    """Метаданные"""

    @staticmethod
    def filterElements[T: Element](elements: Iterable[T]) -> Sequence[T]:
        elements_map: MutableMapping[str, Element] = dict()

        for e in elements:
            current_element: Optional[Element] = elements_map.get(e.metadata.name())

            if current_element is None:
                elements_map[e.metadata.name()] = e

            elif current_element.metadata.version < e.metadata.version:
                elements_map[e.metadata.name()] = e

        return tuple(elements_map.values())


@dataclass(frozen=True)
class Part(Element):
    """Деталь"""

    has_stp: bool
    """Имеет stp представление"""
    has_3mf: bool
    """Имеет 3mf представление"""

    @classmethod
    def load(cls, path: Path) -> Part:
        return cls(
            metadata=MetaData.load(path),
            has_stp=_exists_with_ext(path, EXT_STP),
            has_3mf=_exists_with_ext(path, EXT_3MF)
        )

    def __str__(self) -> str:
        return self.metadata.__str__()


@dataclass(frozen=True)
class AsmUnit(Element):
    """Сборочная единица"""

    parts: Sequence[Part]
    """Актуальные детали, входящие в состав"""
    deprecated_parts: int
    """Количество устаревших деталей"""

    @classmethod
    def load(cls, source_path: Path) -> AsmUnit:
        metadata = MetaData.load(source_path)

        total_elements = tuple(map(Part.load, make_glob(source_path, (f"*.{EXT_M3D}",))))
        actual_elements = Element.filterElements(total_elements)

        return cls(metadata, actual_elements, len(total_elements) - len(actual_elements))


def _iterDirs(root: Path) -> Iterable[Path]:
    return (p for p in root.iterdir() if p.is_dir())


# noinspection PyMissingOrEmptyDocstring
class MD:

    @staticmethod
    def img(src: Path, width: int = 400) -> str:
        return f'<img src="{src}" width="{width}">'

    @staticmethod
    def collapsingHeader(title: str, items: Sequence[str]) -> str:
        return f'<details><summary><strong>{title}</strong></summary>{'\n\n'.join(items)}</details>'

    @staticmethod
    def link(title: str, p: Path) -> str:
        return f'[{title}]({p})'

    @staticmethod
    def header(s: str, level: int = 1) -> str:
        return f'{'#' * level} {s}'

    @staticmethod
    def quote(s: str) -> str:
        return f"> {s}"


@dataclass(frozen=True)
class UnitManager:
    """Данные проекта"""

    path: Path
    """Путь"""
    units: Sequence[AsmUnit]
    """Единицы"""

    @classmethod
    def load(cls, path: Path) -> UnitManager:
        return cls(
            path,
            tuple(map(
                lambda p: AsmUnit.load(p),
                _iterDirs(path)
            ))
        )

    def name(self) -> str:
        """Получить наименование коллекции"""
        return self.path.name

    def toMD(self) -> str:
        """Преобразовать в MarkDown"""
        s = StringIO()

        s.write(MD.header(MD.link(self.name(), self.path)))

        return s.getvalue()


def _test():
    print(UnitManager.load(Path("Модели/Шасси")).toMD())

    return


_test()
