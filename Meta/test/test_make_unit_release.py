import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Sequence

from botix.core.entities import PartEntity
from botix.core.entities import UnitEntity
from botix.core.key import UnitKey
from botix.core.registries import PartEntityRegistry
from botix.core.registries import PartsSectionRegistry
from botix.core.registries import UnitEntityRegistry
from botix.impl.loaders import ProjectEntityLoader


def _link(s: str, path: str) -> str:
    return f"[`{s}`]({path})"


def _img(src: str, height: int) -> str:
    return f'<img src="{src}" height="{height}">'


def _date() -> str:
    return datetime.now().strftime("%Y.%m.%d")


def _makeImagesTable(images: Sequence[Path], main_height: int) -> str:
    images_total = len(images)

    if images_total == 0:
        return ""

    main_image, *other_images = (i.name for i in images)

    main_img_tag = _img(main_image, main_height)

    if len(other_images) == 0:
        return main_img_tag

    other_image_height = main_height // (images_total - 1)

    other_images_tags_string = '\n'.join((
        _img(i, other_image_height) + "<br>"
        for i in other_images
    ))

    return f"""
<table>
<tr valign="top">
<td>
{main_img_tag}
</td>
<td>
{other_images_tags_string}
</td>
</tr>
</table>
    """


def _makeHeader(unit: UnitEntity, current_date: str) -> str:
    transitions = [
        ('zip', f'./../{unit.metadata.getEntityName()}--{current_date}.zip'),
    ]

    if unit.transition_assembly:
        transitions.append(('step', unit.transition_assembly.name))

    transitions_string = ' '.join(
        _link(name, path)
        for name, path in transitions
    )

    return f"""
# [{unit.metadata.getDisplayName()} {unit.metadata.getDisplayVersion()}](.)

[Выпуск от {current_date}](.) {transitions_string}

{_makeImagesTable(unit.metadata.images, 360)}

# Детали

"""


def _makePartBlock(part: PartEntity, count: int, name_transformer: Callable[[str], str]) -> str:
    images_html = '\n'.join(
        f'<td>{_img(name_transformer(i.name), 180)}</td>'
        for i in part.metadata.images
    )

    transitions = list(
        (t.suffix, name_transformer(t.name))
        for t in part.transitions
    )

    def _addProject(path: Optional[Path], slicer: str) -> None:
        if path:
            transitions.append((f"{path.suffix} ({slicer})", name_transformer(path.name)))

    _addProject(part.prusa_project, "PrusaSlicer")
    _addProject(part.orca_project, "OrcaSlicer")

    transitions_string = ' '.join(
        _link(name, path)
        for name, path in transitions
    )

    return f"""
<blockquote>

## {part.metadata.getDisplayName()} - {count} шт.

<table>
<tr valign="top">
{images_html}
</tr>
</table>

{transitions_string}

</blockquote>
"""


def _makeFooter() -> str:
    return """
---

<sub>
Файл сгенерирован инструментами проекта.

[LICENCE](https://github.com/KiraFlux/Botix/blob/main/LICENSE)

</sub>
"""


def _makeUnitAssemblyFiles(output_folder: Path, unit: UnitEntity, parts_registry: PartsSectionRegistry) -> None:
    assert unit.attributes is not None, f"Attributes (.unit) must exists"

    unit_release_folder = output_folder / unit.metadata.getEntityName()

    #

    if unit_release_folder.exists():
        shutil.rmtree(unit_release_folder)

    unit_release_folder.mkdir(parents=True)

    #

    def _move(p: Optional[Path], name_transformer: Callable[[str], str] = str) -> None:
        if p:
            shutil.copyfile(p, unit_release_folder / name_transformer(p.name))

    current_date = _date()

    with open(unit_release_folder / "README.md", "wt") as out:

        out.write(_makeHeader(unit, current_date))

        _move(unit.transition_assembly)

        for image in unit.metadata.images:
            _move(image)

        part_registry = PartEntityRegistry(unit, parts_registry)

        for part_key, count in unit.attributes.part_count_map.items():
            part: Optional[PartEntity] = part_registry.get(part_key)

            if part is None:
                print(f"cannot find: {part_key}")

            else:
                def _nameTransformer(s: str) -> str:
                    return f"{count}x--{s}"

                out.write(_makePartBlock(part, count, _nameTransformer))

                for transition in part.transitions:
                    _move(transition, _nameTransformer)

                for image in part.metadata.images:
                    _move(image, _nameTransformer)

                if part.prusa_project:
                    _move(part.prusa_project, _nameTransformer)

        out.write(_makeFooter())

    #

    archive_path = output_folder / f"{unit.metadata.getEntityName()}--{current_date}"
    shutil.make_archive(
        base_name=str(archive_path),
        format="zip",
        root_dir=str(unit_release_folder),
        base_dir="."
    )

    return


def _main() -> None:
    root = Path("A:/Projects/Botix")
    output_folder = root / "Производство"

    project = ProjectEntityLoader(root / "Модели").load()
    units = UnitEntityRegistry(project)
    print('\n'.join(map(str, units.getAll().keys())))
    parts = PartsSectionRegistry(project)
    print('\n'.join(map(str, units.getAll().keys())))

    unit = units.get(UnitKey("Шасси/MidiQ-Всош-v2"))

    _makeUnitAssemblyFiles(output_folder, unit, parts)

    return


if __name__ == "__main__":
    _main()
