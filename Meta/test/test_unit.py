from pathlib import Path

from projectmaster.entities.impl.loader.unit import UnitLoader

root = Path("A:/Projects/OmniCore-Robotics")

p = root / "Модели/Модули/АКБ/АКБ-18650-3S/Закрытый-v1"

unit = UnitLoader(p).load()
print(unit)
