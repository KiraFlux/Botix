from io import StringIO
from pathlib import Path

from projectmaster.entities.impl.loader.part import PartEntityLoader
from projectmaster.entities.impl.visitor.render.text import TextRenderEntityVisitor

path = Path(r"A:/Projects/OmniCore-Robotics/Модели/Конструктив/Рамки/Рамка-V3.m3d")

p = PartEntityLoader(path).load()

o = StringIO()

v = TextRenderEntityVisitor(o)
v.visitPartEntity(p)

print(o.getvalue())
