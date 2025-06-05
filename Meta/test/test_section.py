from pathlib import Path

from projectmaster.attributes.impl.loader.section import SectionAttributesLoader
from projectmaster.entities.impl.loader.section import SectionEntityLoader

root = Path("A:/Projects/OmniCore-Robotics") / "Модели"

p1 = root / "Модули"
p2 = root / "Шасси"
p3 = root / "Колеса"

section = SectionEntityLoader(p1).load()
# print(section)

sl = SectionAttributesLoader(p1)

print(sl, sl.exists())
