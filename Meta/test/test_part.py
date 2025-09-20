from pathlib import Path

from botix.impl.loaders import PartEntityLoader

root = Path("A:/Projects/Botix")

p = root / "Модели/Конструктив/Рамки/Рамка-v4.m3d"

part = PartEntityLoader(p).load()
print(part)
