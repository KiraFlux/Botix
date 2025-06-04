from pathlib import Path

from projectmaster.core.entities.part import PartBuilder

root = Path("A:/Projects/OmniCore-Robotics")

a = root / "Модели/Шасси/RegQ/v1/Пластина-Нижняя-V2.m3d"
b = root / "Модели/Шасси/RegQ/v1/Пластина-Нижняя.m3d"
c = root / "Модели/Конструктив/Рамки/Рамка-V3.m3d"

p = PartBuilder(c).build()
print(p)
