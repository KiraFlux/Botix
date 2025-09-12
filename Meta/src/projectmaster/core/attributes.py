from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, kw_only=True)
class SectionAttributes:
    """Атрибуты раздела"""

    name: str
    """Наименование раздела"""
    level: int
    """Уровень вложенности раздела"""
    desc: str
    """Описание раздела"""

    def __post_init__(self) -> None:
        assert self.level >= 0


@dataclass(frozen=True, kw_only=True)
class UnitAttributes:
    """Атрибуты сборочной единицы"""

    part_count_map: Mapping[str, int]
    """Кол-во деталей"""

    def __post_init__(self) -> None:
        for part, count in self.part_count_map.items():
            assert count >= 0, f"{part} Должно иметь натуральное кол-во значений"
