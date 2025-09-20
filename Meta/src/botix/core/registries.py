from __future__ import annotations

from abc import ABC
from itertools import chain
from typing import Mapping
from typing import Optional

from botix.core.entities import PartEntity
from botix.core.entities import PartsSectionEntity
from botix.core.entities import ProjectEntity
from botix.core.entities import UnitEntity
from botix.core.entities import UnitsSectionEntity
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
                self._makeUnitKey(section, unit): unit
                for section in project.units_sections
                for unit in section.units
            }
        )

    @staticmethod
    def _makeUnitKey(units_section: UnitsSectionEntity, unit: UnitEntity) -> UnitKey:
        return UnitKey(f"{units_section.attributes.name}/{unit.metadata.getEntityName()}")


class PartsSectionRegistry(EntityRegistry[PartKey, PartEntity]):
    """Реестр общих деталей"""

    def __init__(self, project: ProjectEntity) -> None:
        super().__init__({
            self._makeSharedPartKey(section, part): part
            for section in project.parts_sections
            for part in section.parts
        })

    @staticmethod
    def _makeSharedPartKey(parts_section: PartsSectionEntity, part: PartEntity) -> PartKey:
        return PartKey(f"{parts_section.attributes.name}/{part.metadata.getEntityName()}")


class PartEntityRegistry(EntityRegistry[PartKey, PartEntity]):
    """Реестр деталей"""

    def __init__(self, unit: UnitEntity, parts_registry: PartsSectionRegistry) -> None:
        super().__init__(
            dict(chain(
                (
                    (PartKey(part.metadata.getEntityName()), part)
                    for part in unit.parts
                ),
                parts_registry.getAll().items()
            ))
        )
