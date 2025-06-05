from pathlib import Path

from projectmaster.tools import iterDirs

root = Path("A:/Projects/OmniCore-Robotics") / "Модели"

dirs = iterDirs(root, 1)

for d in dirs:
    print(d)
