from pathlib import Path

from projectmaster.impl.loaders import UnitEntityLoader

root = Path("A:/Projects/Botix")

p = root / "Модели/Модули/Манипуляторы/Манипулятор-2DOF-548"

unit = UnitEntityLoader(p).load()
print(unit)
print(unit.metadata)
