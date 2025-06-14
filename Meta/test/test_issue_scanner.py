import sys
from pathlib import Path

from engines.text import FormatTextIOAdapter
from projectmaster.impl.loaders import ProjectEntityLoader
from projectmaster.impl.visitor.scanner.issue import IssueScannerEntityVisitor

path = Path(r"A:\Projects\OmniCore-Robotics\Модели")

p = ProjectEntityLoader(path).load()

v = IssueScannerEntityVisitor()
v.visitProjectEntity(p)

v.write(FormatTextIOAdapter(sys.stdout))
