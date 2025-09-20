from pathlib import Path

from engines.text import FormatTextIOAdapter
from botix.impl.loaders import ProjectEntityLoader
from botix.impl.visitor.render.text import TextRenderEntityVisitor

path = Path(r"A:\Projects\Botix\Модели")

p = ProjectEntityLoader(path).load()

with open("./out.md", "wt") as f:
    v = TextRenderEntityVisitor(FormatTextIOAdapter(f))
    v.visitProjectEntity(p)
