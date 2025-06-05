import sys
from pathlib import Path

from projectmaster.entities.impl.loader.section import SectionEntityLoader
from projectmaster.entities.impl.visitor.render.text import TextRenderEntityVisitor

path = Path(r"A:\Projects\OmniCore-Robotics\Модели\Модули")

s = SectionEntityLoader(path).load()

o = sys.stdout

v = TextRenderEntityVisitor(o)
v.visitSectionEntity(s)
