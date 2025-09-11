from pathlib import Path

from projectmaster.impl.loaders import ProjectEntityLoader

root = Path("A:/Projects/Botix")

p = root / "Модели"

p1 = ProjectEntityLoader(p).load()

print(p1)
