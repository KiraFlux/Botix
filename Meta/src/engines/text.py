from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import MutableSequence
from typing import TextIO


class _WritingMethod(ABC):
    """Стратегия записи"""

    @abstractmethod
    def apply(self, s: str) -> str:
        """Записать строку"""


class _MockWritingMethod(_WritingMethod):

    def apply(self, s: str) -> str:
        return s


class _MarkedListWritingMethod(_WritingMethod):
    _mark: ClassVar = '- '

    def apply(self, s: str) -> str:
        return self._mark + s


@dataclass
class _NumericListWritingMethod(_WritingMethod):
    _index: int = field(init=False, default=0)

    def apply(self, s: str) -> str:
        self._index += 1
        return f"{self._index}. {s}"


@dataclass
class FormatTextIOAdapter:
    """Адаптер над TextIO для реализации записи с форматом"""

    _intend: ClassVar = 4
    _intend_string: ClassVar = ' ' * _intend

    _source: TextIO
    _methods: MutableSequence[_WritingMethod] = field(init=False, default_factory=list)

    def use(self, method: _WritingMethod) -> FormatTextIOAdapter:
        """Использовать следующий метод записи"""
        self._methods.append(method)
        return self

    def tab(self) -> FormatTextIOAdapter:
        """Отступ с табуляцией"""
        return self.use(_MockWritingMethod())

    def markedList(self) -> FormatTextIOAdapter:
        """Маркированный список"""
        return self.use(_MarkedListWritingMethod())

    def numericList(self) -> FormatTextIOAdapter:
        """Нумерованный список"""
        return self.use(_NumericListWritingMethod())

    def write(self, s: str = None) -> None:
        """Записать"""

        if s:
            i = len(self._methods)

            for _ in range(i - 1):
                self._source.write(self._intend_string)

            if i > 0:
                s = self._methods[-1].apply(s)

            self._source.write(s)

        self._source.write('\n')

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._methods.pop()
