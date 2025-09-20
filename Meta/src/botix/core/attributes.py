from dataclasses import dataclass
from typing import Mapping

from botix.core.key import PartKey


@dataclass(frozen=True, kw_only=True)
class PartsSectionAttributes:
    """Атрибуты раздела общих деталей"""

    name: str
    """Наименование раздела"""
    level: int
    """Уровень поиска деталей в данном разделе"""

    def __post_init__(self) -> None:
        assert self.level >= 0


@dataclass(frozen=True, kw_only=True)
class UnitsSectionAttributes:
    """Атрибуты раздела сборочных единиц"""

    name: str
    """Наименование раздела"""
    level: int
    """Уровень поиска сборочных единиц в данном разделе"""
    desc: str
    """Описание раздела"""

    def __post_init__(self) -> None:
        assert self.level >= 0


@dataclass(frozen=True, kw_only=True)
class UnitAttributes:
    """Атрибуты сборочной единицы"""

    part_count_map: Mapping[PartKey, int]
    """Спецификация дубликатов деталей в данной сборочной единице"""

    def __post_init__(self) -> None:
        for part, count in self.part_count_map.items():
            assert count > 0, f"{part} Должно иметь натуральное кол-во значений"
