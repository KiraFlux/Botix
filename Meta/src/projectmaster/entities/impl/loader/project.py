"""
ProjectEntityLoader
"""
from pathlib import Path

from projectmaster.attributes.impl.loader.section import SectionAttributesLoader
from projectmaster.entities.abc.loader import EntityLoader
from projectmaster.entities.core.project import ProjectEntity
from projectmaster.entities.impl.loader.section import SectionEntityLoader
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
