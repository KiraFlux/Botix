import sys
from pathlib import Path

from engines.text import FormatTextIOAdapter
from projectmaster.impl.loaders import ProjectEntityLoader
from projectmaster.impl.visitor.render.text import TextRenderEntityVisitor

path = Path(r"A:\Projects\OmniCore-Robotics\Модели")

p = ProjectEntityLoader(path).load()

v = TextRenderEntityVisitor(FormatTextIOAdapter(sys.stdout))

v.visitProjectEntity(p)
