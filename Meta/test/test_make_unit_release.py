import shutil
from datetime import datetime
from pathlib import Path

from projectmaster.core.entities import UnitEntity
from projectmaster.impl.loaders import UnitEntityLoader


def _date() -> str:
    return datetime.now().strftime("%Y.%m.%d")


def _releaseUnit(unit: UnitEntity, output: Path) -> None:
    assert unit.attributes is not None, f"Attributes (.unit) must exists"

    release_folder = output / unit.metadata.getEntityName()

    print(f"{release_folder=}")

    if release_folder.exists():
        shutil.rmtree(release_folder)

    release_folder.mkdir(parents=True)

    for image in unit.metadata.images:
        shutil.copyfile(image, release_folder / image.name)

    for part in unit.parts:

        entity_name = part.metadata.getEntityName()
        if (count := unit.attributes.part_count_map.get(entity_name)) is None:
            print(f"Cannot find '{entity_name}' (local)")
            continue

        def _nameTransformer(s: str) -> str:
            return f"{count}x--{s}"

        for transition in part.transitions:
            shutil.copyfile(transition, release_folder / _nameTransformer(transition.name))

        for image in part.metadata.images:
            shutil.copyfile(image, release_folder / image.name)

        if part.prusa_project:
            shutil.copyfile(part.prusa_project, release_folder / _nameTransformer(part.prusa_project.name))

    archive_folder = release_folder.parent / f"{release_folder.name}--{_date()}"

    shutil.make_archive(
        base_name=str(archive_folder),
        format="zip",
        root_dir=str(release_folder),
        base_dir="."
    )

    return


def _main() -> None:
    root = Path("A:/Projects/Botix/Meta/test/Mock")

    p = root / "Модели/Шасси/Тест/Вариант-v2"

    unit = UnitEntityLoader(p).load()
    print(unit.attributes)
    _releaseUnit(unit, root / "Производство")

    return


if __name__ == "__main__":
    _main()
