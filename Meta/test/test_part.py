from pathlib import Path

from projectmaster.impl.entities.loader.part import PartEntityLoader

root = Path("A:/Projects/OmniCore-Robotics")

p = root / "Модели/Конструктив/Рамки/Рамка-V3.m3d"

part = PartEntityLoader(p).load()
print(part)
