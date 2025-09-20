import sys
from pathlib import Path

from engines.text import FormatTextIOAdapter
from botix.impl.loaders import ProjectEntityLoader
from botix.impl.visitor.scanner.issue import IssueScannerEntityVisitor

path = Path(r"A:\Projects\Botix\Модели")

p = ProjectEntityLoader(path).load()

v = IssueScannerEntityVisitor()
v.visitProjectEntity(p)

v.write(FormatTextIOAdapter(sys.stdout))
