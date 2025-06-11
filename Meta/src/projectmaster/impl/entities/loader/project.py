"""
ProjectEntityLoader
"""
from pathlib import Path

from projectmaster.impl.attributes.loader.section import SectionAttributesLoader
from projectmaster.abc.entities.loader import EntityLoader
from projectmaster.core.entities import ProjectEntity
from projectmaster.impl.entities.loader.section import SectionEntityLoader
from projectmaster.tools import iterDirs


class ProjectEntityLoader(EntityLoader[ProjectEntity]):
    def load(self) -> ProjectEntity:
        return ProjectEntity(
            sections=tuple(
                SectionEntityLoader(p).load()
                for p in iterDirs(self.folder())
                if SectionAttributesLoader(self.folder() / p).exists()
            )
        )

    def folder(self) -> Path:
        return self._path
