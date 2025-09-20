from __future__ import annotations

from abc import ABC
from typing import Mapping
from typing import Optional

from botix.core.entities import PartEntity
from botix.core.entities import ProjectEntity
from botix.core.entities import SectionEntity
from botix.core.entities import UnitEntity
from botix.core.key import Key
from botix.core.key import PartKey
from botix.core.key import UnitKey


class EntityRegistry[K: Key, T](ABC):
    """Реестр ключ - Сущность"""

    def __init__(self, entities: Mapping[K, T]) -> None:
        self.__entities = entities

    def get(self, key: K) -> Optional[T]:
        """Получить значение"""
        return self.__entities.get(key)

    def getAll(self) -> Mapping[K, T]:
        """Получить вид на данные реестра"""
        return self.__entities


class UnitEntityRegistry(EntityRegistry[UnitKey, UnitEntity]):
    """Реестр сборочных единиц"""

    def __init__(self, project: ProjectEntity) -> None:
        super().__init__(
            {
                UnitKey(self._makeKeyString(section, unit)): unit
                for section in project.sections
                for unit in section.units
            }
        )

    @staticmethod
    def _makeKeyString(section: SectionEntity, unit: UnitEntity) -> str:
        return f"{section.attributes.name}/{unit.metadata.getEntityName()}"


class PartEntityRegistry(EntityRegistry[PartKey, PartEntity]):
    """Реестр деталей"""

    def __init__(self, unit: UnitEntity) -> None:
        super().__init__(
            {
                PartKey(part.metadata.getEntityName()): part
                for part in unit.parts
            }
        )
