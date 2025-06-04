from pathlib import Path

from projectmaster.entities.impl.loader.part import PartLoader

root = Path("A:/Projects/OmniCore-Robotics")

p = root / "Модели/Конструктив/Рамки/Рамка-V3.m3d"

part = PartLoader(p).load()
print(part)
