from pathlib import Path

from projectmaster.impl.entities.loader.project import ProjectEntityLoader

root = Path("A:/Projects/OmniCore-Robotics")

p = root / "Модели"

p1 = ProjectEntityLoader(p).load()

print(p1)
