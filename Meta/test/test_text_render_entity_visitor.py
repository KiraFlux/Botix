import sys
from pathlib import Path

from projectmaster.entities.impl.loader.project import ProjectEntityLoader
from projectmaster.engines.text import IntendTextIOAdapter
from projectmaster.entities.impl.visitor.render.text import TextRenderEntityVisitor

path = Path(r"A:\Projects\OmniCore-Robotics\Модели")

p = ProjectEntityLoader(path).load()

v = TextRenderEntityVisitor(IntendTextIOAdapter(sys.stdout))

v.visitProjectEntity(p)
