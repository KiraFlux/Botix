"""
Мастер для управления проектов.

"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from typing import MutableMapping
from typing import Optional
from typing import Sequence

from CleanupUtill import make_glob


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
        return f"V{self.version} :: {self.name()}"


@dataclass(frozen=True)
class Element:
    """Элемент моделирования"""

    metadata: MetaData
    """Метаданные"""

    def display(self, index: int) -> str:
        """Отобразить элемент"""
        return f"{index:>02}: {self.__str__()}"

    @staticmethod
    def applyEnumerators(items: Sequence[Element]) -> Iterable[str]:
        if len(items) == 1:
            return (items[0].__str__(),)

        return (i.display(index + 1) for index, i in enumerate(items))

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

    @classmethod
    def load(cls, path: Path) -> Part:
        metadata = MetaData.load(path)
        return cls(metadata)

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
    def load(cls, source_path: Path, part_patterns: Sequence[str]) -> AsmUnit:
        metadata = MetaData.load(source_path)

        total_elements = tuple(map(Part.load, make_glob(source_path, part_patterns)))
        actual_elements = Element.filterElements(total_elements)

        return cls(metadata, actual_elements, len(total_elements) - len(actual_elements))

    def _getTitle(self) -> str:
        ret = self.metadata.__str__()

        parts = len(self.parts)

        if parts > 1:
            ret += f" :: ("

            if self.deprecated_parts == 0:
                ret += f"деталей: {parts}"

            else:
                ret += f"актуальных: {parts}, устаревших: {self.deprecated_parts}"

            ret += ")"

        return f"[ {ret} ]"

    def __str__(self) -> str:
        return f"{self._getTitle()}\n{'\n'.join(
            (
                f"{' ' * 4 + s}"
                for s in Element.applyEnumerators(self.parts)
            )
        )}\n"


def _iterDirs(root: Path) -> Iterable[Path]:
    return (p for p in root.iterdir() if p.is_dir())


@dataclass(frozen=True)
class UnitManager:
    """Данные проекта"""

    path: Path
    """Путь"""
    units: Sequence[AsmUnit]
    """Единицы"""

    @classmethod
    def load(cls, path: Path, part_patterns: Sequence[str]) -> UnitManager:
        return cls(
            path,
            tuple(map(
                lambda p: AsmUnit.load(p, part_patterns),
                _iterDirs(path)
            ))
        )

    def name(self) -> str:
        """Получить наименование коллекции"""
        return self.path.name

    def __repr__(self) -> str:
        return f"{(' <<< ' + self.name() + f': {len(self.units)} >>> '):-^80}\n\n{'\n'.join(
            Element.applyEnumerators(self.units)
        )}\n"


def _test():
    part_patterns = ("*.m3d",)

    print(UnitManager.load(Path("Модели/Шасси"), part_patterns))
    print(UnitManager.load(Path("Модели/Модули"), part_patterns))

    return


_test()
