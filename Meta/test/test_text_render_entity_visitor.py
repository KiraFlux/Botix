import sys
from pathlib import Path

from engines.text import IntendTextIOAdapter
from projectmaster.impl.entities.loader.project import ProjectEntityLoader
from projectmaster.impl.entities.visitor.render.text import TextRenderEntityVisitor

path = Path(r"A:\Projects\OmniCore-Robotics\Модели")

p = ProjectEntityLoader(path).load()

v = TextRenderEntityVisitor(IntendTextIOAdapter(sys.stdout))

v.visitProjectEntity(p)
