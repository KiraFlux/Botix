from pathlib import Path

from projectmaster.entities.impl.loader.section import SectionLoader

root = Path("A:/Projects/OmniCore-Robotics")

p = root / "Модели/Модули/"

section = SectionLoader(p).load()
print(section)
