from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import MutableSequence

from engines.text import FormatTextIOAdapter
from botix.abc.visitor import EntityVisitor
from botix.core.entities import MetadataEntity
from botix.core.entities import PartEntity
from botix.core.entities import ProjectEntity
from botix.core.entities import UnitsSectionEntity
from botix.core.entities import UnitEntity


@dataclass(frozen=True)
class Issue:
    """Проблема"""

    entity_path: Path
    """Путь источника"""
    entity_name: str
    """Наименование источника"""
    problem_message: str
    """Описание проблемы"""

    @classmethod
    def fromMetadata(cls, metadata: MetadataEntity, problem_message: str) -> Issue:
        """Создать проблему по метаданным"""
        return cls(
            entity_path=metadata.path,
            entity_name=metadata.getEntityName(),
            problem_message=problem_message
        )


@dataclass(frozen=True)
class IssueScannerEntityVisitor(EntityVisitor):
    """Сканирующий посетитель на предмет наличия недостатков"""

    _issues: MutableSequence[Issue] = field(init=False, default_factory=list)

    def write(self, out: FormatTextIOAdapter) -> None:
        """Записать"""

        title = f"ISSUES ({len(self._issues)})"

        out.write(title)
        out.write()

        with out.numericList():
            for issue in self._issues:
                out.write(issue.entity_name)

                with out.markedList():
                    out.write(f"Путь    : {issue.entity_path}")
                    out.write(f"Проблема: {issue.problem_message}")

                out.write()

        out.write(title)

    def _warn(self, i: Issue) -> None:
        self._issues.append(i)

    def visitMetadataEntity(self, metadata: MetadataEntity) -> None:
        if not metadata.images:
            self._warn(Issue.fromMetadata(metadata, "Отсутствуют иллюстрации"))

    def visitPartEntity(self, part: PartEntity) -> None:
        self.visitMetadataEntity(part.metadata)

        if not part.prusa_project:
            self._warn(Issue.fromMetadata(part.metadata, "Отсутствует проект PrusaSlicer"))

        if not part.transitions:
            self._warn(Issue.fromMetadata(part.metadata, "Отсутствуют файлы обменного формата"))

    def visitUnitEntity(self, unit: UnitEntity) -> None:
        self.visitMetadataEntity(unit.metadata)

        for p in unit.parts:
            self.visitPartEntity(p)

    def visitUnitsSectionEntity(self, section: UnitsSectionEntity) -> None:
        for u in section.units:
            self.visitUnitEntity(u)

    def visitProjectEntity(self, project: ProjectEntity) -> None:
        for s in project.units_sections:
            self.visitUnitsSectionEntity(s)
