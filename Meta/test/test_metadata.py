from pathlib import Path

from projectmaster.core.entities.metadata import Metadata
from projectmaster.core.tools import make_glob

root = Path("A:/Projects/OmniCore-Robotics")

a = root / "Модели/Шасси/RegQ/v1/Пластина-Нижняя-V2.m3d"
b = root / "Модели/Шасси/RegQ/v1/Пластина-Нижняя.m3d"
c = root / "Модели/Конструктив/Рамки/Рамка-V3.m3d"


def _load_part(path: Path) -> Metadata:
    filename = path.stem

    words = filename.split(Metadata.parse_words_delimiter)

    if words[-1].lower().startswith(Metadata.version_prefix):
        *words, version_string = words
        v = Metadata.extractVersion(version_string)
    else:
        v = Metadata.default_version

    return Metadata(
        path=path,
        words=words,
        version=v,
        images=(tuple(make_glob(path.parent, Metadata.getImageFilePatterns(filename))))
    )


print(_load_part(c))
# print(_load_part(b))
