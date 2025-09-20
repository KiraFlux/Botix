from pathlib import Path

from botix.tools import iterDirs

p = Path('A:/Projects/Botix/Meta/test/Mock/Модели/Конструктив')

print(tuple(iterDirs(p)))
