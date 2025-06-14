from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import MutableSequence
from typing import TextIO


class WritingMethod(ABC):
    """Стратегия записи"""

    @abstractmethod
    def apply(self, s: str) -> str:
        """Записать строку"""


class MockWritingMethod(WritingMethod):

    def apply(self, s: str) -> str:
        return s


class MarkedListWritingMethod(WritingMethod):
    _mark: ClassVar = '- '

    def apply(self, s: str) -> str:
        return self._mark + s


@dataclass
class NumericListWritingMethod(WritingMethod):
    _index: int = field(init=False, default=0)

    def apply(self, s: str) -> str:
        self._index += 1
        return f"{self._index:02} {s}"


@dataclass
class FormatTextIOAdapter:
    """Адаптер над TextIO для реализации записи с форматом"""

    _intend: ClassVar = 4
    _intend_string: ClassVar = ' ' * _intend

    _source: TextIO
    _methods: MutableSequence[WritingMethod] = field(init=False, default_factory=list)

    def use(self, method: WritingMethod) -> FormatTextIOAdapter:
        """Использовать следующий метод записи"""
        self._methods.append(method)
        return self

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._methods.pop()

    def write(self, s: str = None) -> None:
        """Записать"""

        i = len(self._methods)

        for _ in range(i - 1):
            self._source.write(self._intend_string)

        if i > 0:
            s = self._methods[-1].apply(s)

        self._source.write(s)

        self._source.write('\n')
