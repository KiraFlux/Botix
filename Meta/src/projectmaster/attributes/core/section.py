from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class SectionAttributes:
    """Атрибуты раздела"""

    level: int
    """Уровень вложенности раздела"""
    desc: str
    """Описание раздела"""

    def __post_init__(self) -> None:
        assert 0 <= self.level
