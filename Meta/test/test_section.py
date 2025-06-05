from pathlib import Path

from projectmaster.entities.impl.loader.section import SectionEntityLoader

root = Path("A:/Projects/OmniCore-Robotics") / "Модели"

p1 = root / "Модули"
p2 = root / "Шасси"
p3 = root / "Колеса"

section = SectionEntityLoader(_path=p1).load()
print(section)
