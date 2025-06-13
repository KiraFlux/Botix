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
    def apply(self, s: str = "") -> str:
        """Записать строку"""


class NewLineWritingMethod(WritingMethod):

    def apply(self, s: str = "") -> str:
        return s + '\n'


class IntendWritingMethod(WritingMethod):
    _intend: ClassVar = 4
    _intend_string: ClassVar = ' ' * _intend

    def apply(self, s: str = "") -> str:
        return self._intend_string + s


@dataclass
class FormatTextIOAdapter:
    """Адаптер над TextIO для реализации записи с форматом"""

    _source: TextIO
    _methods: MutableSequence[WritingMethod] = field(init=False, default_factory=lambda: [NewLineWritingMethod()])

    def use(self, method: WritingMethod) -> FormatTextIOAdapter:
        """Использовать следующий метод записи"""
        self._methods.append(method)
        return self

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._methods.pop()
        assert len(self._methods) > 0

    def write(self, s: str = None) -> None:
        """Записать"""

        for method in self._methods:
            s = method.apply(s)

        self._source.write(s)
