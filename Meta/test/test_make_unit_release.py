import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable
from typing import Optional

from botix.core.entities import PartEntity
from botix.core.entities import UnitEntity
from botix.core.registries import PartEntityRegistry
from botix.impl.loaders import UnitEntityLoader


def _date() -> str:
    return datetime.now().strftime("%Y.%m.%d")


def _makeUnitAssemblyFiles(output_folder: Path, unit: UnitEntity) -> None:
    assert unit.attributes is not None, f"Attributes (.unit) must exists"

    part_registry = PartEntityRegistry(unit)

    unit_release_folder = output_folder / unit.metadata.getEntityName()

    def _move(p: Optional[Path], name_transformer: Callable[[str], str] = str) -> None:
        if p:
            shutil.copyfile(p, unit_release_folder / name_transformer(p.name))

    archive_path = output_folder / f"{unit.metadata.getEntityName()}--{_date()}"

    if unit_release_folder.exists():
        shutil.rmtree(unit_release_folder)

    unit_release_folder.mkdir(parents=True)

    _move(unit.transition_assembly)

    for image in unit.metadata.images:
        _move(image)

    for part_key, count in unit.attributes.part_count_map.items():
        part: Optional[PartEntity] = part_registry.get(part_key)

        if part is None:
            print(f"cannot find: {part_key}")

        else:
            def _nameTransformer(s: str) -> str:
                return f"{count}x--{s}"

            for transition in part.transitions:
                _move(transition, _nameTransformer)

            for image in part.metadata.images:
                _move(image, _nameTransformer)

            if part.prusa_project:
                _move(part.prusa_project, _nameTransformer)

    shutil.make_archive(
        base_name=str(archive_path),
        format="zip",
        root_dir=str(unit_release_folder),
        base_dir="."
    )

    return


def _main() -> None:
    root = Path("A:/Projects/Botix/Meta/test/Mock")

    p = root / "Модели/Шасси/Тест/Вариант-v2"

    unit = UnitEntityLoader(p).load()
    print(unit.attributes)
    _makeUnitAssemblyFiles(root / "Производство", unit)

    return


if __name__ == "__main__":
    _main()
