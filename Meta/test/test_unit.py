from pathlib import Path

from projectmaster.core.entities import UnitEntity
from projectmaster.impl.loaders import UnitEntityLoader

root = Path("A:/Projects/Botix/Meta/test/Mock")

p = root / "Модели/Шасси/Тест/Вариант-v2"

unit: UnitEntity = UnitEntityLoader(p).load()
print(unit)
