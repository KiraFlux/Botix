from pathlib import Path

from projectmaster.entities.impl.loader.section import SectionLoader

root = Path("A:/Projects/OmniCore-Robotics") / "Модели"

p1 = root / "Модули"
p2 = root / "Шасси"
p3 = root / "Колеса"

section = SectionLoader(_path=p3, _level=1).load()
print(section)
