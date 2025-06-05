from io import StringIO
from pathlib import Path

from projectmaster.entities.impl.loader.metadata import MetadataEntityLoader
from projectmaster.entities.impl.visitor.render.text import TextRenderEntityVisitor

m = MetadataEntityLoader(Path(r"A:/Projects/OmniCore-Robotics/Модели/Конструктив/Рамки/Рамка-V3.m3d")).load()
print(m)

o = StringIO()

v = TextRenderEntityVisitor(o)
v.visitMetadataEntity(m)

print(o.getvalue())
