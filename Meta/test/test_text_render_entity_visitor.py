from io import StringIO
from pathlib import Path

from projectmaster.entities.impl.loader.unit import UnitEntityLoader
from projectmaster.entities.impl.visitor.render.text import TextRenderEntityVisitor

path = Path(r"A:\Projects\OmniCore-Robotics\Модели\Модули\АКБ\АКБ-18650-3S\Закрытый-v1")

u = UnitEntityLoader(path).load()

o = StringIO()

v = TextRenderEntityVisitor(o)
v.visitUnitEntity(u)

print(o.getvalue())
