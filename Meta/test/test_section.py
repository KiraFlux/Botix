from pathlib import Path

from projectmaster.impl.loaders import SectionAttributesLoader
from projectmaster.impl.loaders import SectionEntityLoader

root = Path("A:/Projects/Botix") / "Модели"

p1 = root / "Модули"
p2 = root / "Шасси"
p3 = root / "Колеса"

section = SectionEntityLoader(p1).load()
# print(section)

sl = SectionAttributesLoader(p1)

print(sl, sl.exists())
