from pathlib import Path

from botix.tools import iterDirs

root = Path("A:/Projects/Botix") / "Модели"

dirs = iterDirs(root, 1)

for d in dirs:
    print(d)
