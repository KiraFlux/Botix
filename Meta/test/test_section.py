from pathlib import Path

from projectmaster.impl.attributes.loader.section import SectionAttributesLoader
from projectmaster.impl.entities.loader.section import SectionEntityLoader

root = Path("A:/Projects/OmniCore-Robotics") / "Модели"

p1 = root / "Модули"
p2 = root / "Шасси"
p3 = root / "Колеса"

section = SectionEntityLoader(p1).load()
# print(section)

sl = SectionAttributesLoader(p1)

print(sl, sl.exists())
