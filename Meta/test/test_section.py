from pathlib import Path

from botix.impl.loaders import UnitsSectionAttributesLoader
from botix.impl.loaders import UnitsSectionEntityLoader

root = Path("A:/Projects/Botix") / "Модели"

p1 = root / "Модули"
p2 = root / "Шасси"
p3 = root / "Колеса"

section = UnitsSectionEntityLoader(p1).load()
# print(section)

sl = UnitsSectionAttributesLoader(p1)

print(sl, sl.exists())
