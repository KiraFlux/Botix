from pathlib import Path

from projectmaster.entities.impl.loader.section import SectionLoader

root = Path("A:/Projects/OmniCore-Robotics") / "Модели"

p1 = root / "Модули"
p2 = root / "Шасси"

section = SectionLoader(p2).load()
print(section)
