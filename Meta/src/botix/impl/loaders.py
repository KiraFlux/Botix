from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import Any
from typing import ClassVar
from typing import Mapping
from typing import Optional

from botix.abc.loaders import AttributesLoader
from botix.abc.loaders import EntityLoader
from botix.core.attributes import PartsSectionAttributes
from botix.core.attributes import UnitAttributes
from botix.core.attributes import UnitsSectionAttributes
from botix.core.entities import MetadataEntity
from botix.core.entities import PartEntity
from botix.core.entities import PartsSectionEntity
from botix.core.entities import ProjectEntity
from botix.core.entities import UnitEntity
from botix.core.entities import UnitsSectionEntity
from botix.core.key import PartKey
from botix.tools import ExtensionsMatcher
from botix.tools import iterDirs


class MetadataEntityLoader(EntityLoader[MetadataEntity]):
    """Загрузчик Метаданных"""

    default_version: ClassVar = 1
    """Версия, если префикс отсутствует"""
    image_extensions: ClassVar = ExtensionsMatcher(("png", "jpg", "jpeg"))
    """Расширение файла изображения"""

    def load(self) -> MetadataEntity:
        words = self.name().split(MetadataEntity.parse_words_delimiter)

        if words[-1].lower().startswith(MetadataEntity.version_prefix):
            *words, version_string = words
            pure_version_string = version_string[slice(len(MetadataEntity.version_prefix), None)]
            v = int(pure_version_string)
        else:
            v = self.default_version

        return MetadataEntity(
            path=self._path,
            words=words,
            version=v,
            images=tuple(chain(
                (
                    path
                    for e in self.image_extensions.extensions
                    if (path := Path(self.folder() / f"{self.name()}.{e}")).exists()
                ), self.image_extensions.find(self.folder(), f"{self.name()}{MetadataEntity.parse_words_delimiter}*")
            ))
        )


class PartEntityLoader(EntityLoader[PartEntity]):
    """Загрузчик сущности представления детали"""

    prusa_project_extension: ClassVar = "prusa.3mf"
    """Расширение проекта Prusa"""
    orca_project_extension: ClassVar = "orca.3mf"
    """Расширение проекта Orca"""
    transition_extensions: ClassVar = ExtensionsMatcher(("stp", "step", "stl", "obj", "dxf"))
    """Переходные форматы деталей"""

    def load(self) -> PartEntity:
        """Создать представление детали"""
        return PartEntity(
            metadata=MetadataEntityLoader(self._path).load(),
            transitions=tuple(self.transition_extensions.find(self.folder(), self.name())),
            prusa_project=self._tryLoadProjectFile(self.prusa_project_extension),
            orca_project=self._tryLoadProjectFile(self.orca_project_extension)
        )

    def _tryLoadProjectFile(self, extension: str) -> Optional[Path]:
        project_path = self.folder() / f"{self.name()}.{extension}"
        return project_path if project_path.exists() else None


class PartsSectionAttributesLoader(AttributesLoader[PartsSectionAttributes]):
    """Загрузчик атрибутов раздела общих деталей"""

    def parse(self, data: Mapping[str, Any]) -> PartsSectionAttributes:
        return PartsSectionAttributes(
            name=self._path.name,
            level=int(data['level'])
        )

    def getSuffix(self) -> str:
        return "parts-section"


class PartsSectionEntityLoader(EntityLoader[PartsSectionEntity]):
    """Загрузчик раздела общих деталей"""

    part_extensions: ClassVar = ExtensionsMatcher(("m3d",))

    def load(self) -> PartsSectionEntity:
        attributes = PartsSectionAttributesLoader(self.folder()).load()
        return PartsSectionEntity(
            attributes=attributes,
            parts=tuple(
                PartEntityLoader(part_path).load()
                for category_path in iterDirs(self.folder(), attributes.level)
                for part_path in self.part_extensions.find(category_path, "*")
            )
        )

    def folder(self) -> Path:
        return self._path


class UnitsSectionAttributesLoader(AttributesLoader[UnitsSectionAttributes]):
    """Загрузчик атрибутов сборочной единиц"""

    def parse(self, data: Mapping[str, Any]) -> UnitsSectionAttributes:
        return UnitsSectionAttributes(
            name=self._path.name,
            level=int(data['level']),
            desc=str(data['desc'])
        )

    def getSuffix(self) -> str:
        return "units-section"


class UnitsSectionEntityLoader(EntityLoader[UnitsSectionEntity]):
    """Загрузчик разделов сборочных единиц"""

    def load(self) -> UnitsSectionEntity:
        attributes = UnitsSectionAttributesLoader(self.folder()).load()

        return UnitsSectionEntity(
            attributes=attributes,
            units=tuple(
                UnitEntityLoader(unit_path).load()
                for unit_path in iterDirs(self.folder(), attributes.level)
            )
        )

    def folder(self) -> Path:
        return self._path


class UnitAttributesLoader(AttributesLoader[UnitAttributes]):
    """Загрузчик атрибутов сборочной единицы"""

    def getSuffix(self) -> str:
        return "unit"

    def parse(self, data: Mapping[str, Any]) -> UnitAttributes:
        return UnitAttributes(
            part_count_map={
                PartKey(key): count
                for key, count in data['parts'].items()
            }
        )


class UnitMetadataEntityLoader(MetadataEntityLoader):
    """Метаданные сборочной единицы"""

    def name(self) -> str:
        return f"{self._path.parent.name}{MetadataEntity.parse_words_delimiter}{self._path.name}"


class UnitEntityLoader(EntityLoader[UnitEntity]):
    """Загрузчик сборочных единиц"""

    part_extensions: ClassVar = ExtensionsMatcher(("m3d",))
    transition_assembly_extensions: ClassVar = ExtensionsMatcher(("stp", "step"))

    def load(self) -> UnitEntity:
        metadata = UnitMetadataEntityLoader(self._path).load()
        return UnitEntity(
            metadata=metadata,
            transition_assembly=self._tryLoadTransitionAssembly(metadata.getEntityName()),
            parts=tuple(
                PartEntityLoader(path).load()
                for path in
                chain(
                    self.part_extensions.find(self.folder(), "*"),
                    self.part_extensions.find(self.folder().parent, "*"),
                )
            ),
            attributes=self._tryLoadAttributes()
        )

    def name(self) -> str:
        return self._path.name

    def folder(self) -> Path:
        return self._path

    def _tryLoadTransitionAssembly(self, assembly_name: str) -> Optional[Path]:
        e = tuple(self.transition_assembly_extensions.find(self.folder(), assembly_name))
        return e[0] if e else None

    def _tryLoadAttributes(self) -> Optional[UnitAttributes]:
        a = UnitAttributesLoader(self.folder())
        return a.load() if a.exists() else None


class ProjectEntityLoader(EntityLoader[ProjectEntity]):
    """Загрузчик проекта"""

    def load(self) -> ProjectEntity:
        units_sections = list()
        parts_sections = list()

        for p in iterDirs(self.folder()):
            if UnitsSectionAttributesLoader(p).exists():
                units_sections.append(UnitsSectionEntityLoader(p).load())

            if PartsSectionAttributesLoader(p).exists():
                parts_sections.append(PartsSectionEntityLoader(p).load())

        return ProjectEntity(
            units_sections=units_sections,
            parts_sections=parts_sections
        )

    def folder(self) -> Path:
        return self._path
