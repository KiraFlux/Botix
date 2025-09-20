from pathlib import Path

from botix.core.registries import UnitEntityRegistry
from botix.impl.loaders import ProjectEntityLoader


def _test() -> None:
    root = Path("A:/Projects/Botix/Meta/test/Mock")

    project = ProjectEntityLoader(root / "Модели").load()

    unit_registry = UnitEntityRegistry(project)

    print("\n".join(map(str, unit_registry.getAll().keys())))

    return


if __name__ == "__main__":
    _test()
