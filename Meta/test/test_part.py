from pathlib import Path

from botix.impl.loaders import PartEntityLoader

root = Path("A:/Projects/Botix/Meta/test/Mock")

p = root / "Модели/Конструктив/Уголки/Уголок.m3d"

part = PartEntityLoader(p).load()
print(part)
