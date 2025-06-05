from pathlib import Path

from projectmaster.entities.impl.loader.unit import UnitEntityLoader

root = Path("A:/Projects/OmniCore-Robotics")

p = root / "Модели/Модули/АКБ/АКБ-18650-3S/Закрытый-v1"

unit = UnitEntityLoader(p).load()
print(unit)
print(unit.metadata)
