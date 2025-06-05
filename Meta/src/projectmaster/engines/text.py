from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import ClassVar
from typing import TextIO


@dataclass
class IntendTextIOAdapter:
    """Адаптер над TextIO для реализации записи с отступами"""

    _intend: ClassVar = 4
    _intend_string: ClassVar = ' ' * _intend

    _source: TextIO
    _intend_level: int = field(init=False, default=0)

    def push(self) -> None:
        """Внести отступ"""
        self._intend_level += 1

    def pop(self) -> None:
        """Вынести отступ"""
        self._intend_level -= 1
        assert self._intend_level >= 0

    def _write(self, s: str) -> None:
        self._source.write(s)

    def write(self, s: str = None) -> None:
        """Записать"""

        if s is not None:
            self._write(self._intend_string * self._intend_level)
            self._write(s)

        self._source.write('\n')
