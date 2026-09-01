# Contributing to Botix

Thank you for your interest in contributing to Botix! Whether you are fixing a typo, proposing a new feature, or improving the hardware design – your help is invaluable. This document outlines the workflow and expectations for all contributors.

---

## General Rules

- **Be respectful** – follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
- **Use issues** – before starting significant work, open an issue to discuss your idea. This avoids duplicate efforts and ensures alignment with the project direction.
- **One logical change per pull request** – keep PRs focused and easy to review.
- **Respect licenses** – each component has its own license (see the root `README.md`). Ensure your contributions are compatible.

---

## Branching Model

- `main` – stable branch. Merges only via pull requests.
- Long‑lived development branches for each subsystem:
  - `ecad` – hardware (KiCad)
  - `mcad` – 3D models (FreeCAD)
  - `docs` – documentation
  - `firmware-esp32` – ESP32 firmware
  - `tools` – repository scripts
- Feature/fix branches are created **from the corresponding dev branch** and named with a prefix:
  - `ecad/feat/add-<description>`
  - `firmware-esp32/fix/<description>`
  - `docs/fix/typo-<description>`
  - etc.
- When work is complete, open a pull request **against the corresponding dev branch**. The PR will be **squashed** into the dev branch to keep history clean.
- When a dev branch is ready, it is merged into `main` (also squashed if desired).
- For trivial changes (typos, small fixes), you may open a PR directly against `main` or the relevant dev branch – use your judgement.

---

## Hardware (`ecad/`)

- **Strongly discouraged** – modifying existing board designs. It almost always leads to merge conflicts that are tedious to resolve.
- If a change is absolutely necessary, **create a new version** of the module (e.g., `botix_power_module_v2_my_feature_foo`) and leave the old one untouched. This preserves compatibility with already‑manufactured boards.
- New symbols, footprints, or 3D models should be added to the respective library directories (`botix.kicad_sym`, `botix_library.pretty/`).

---

## 3D Models (`mcad/`)

- **Do not modify `mcad/botix.fcstd`** (the main assembly) via pull request. Instead, **open an issue** describing your proposed change – the maintainer will handle the integration.
- Contributions are welcome in:
  - `mcad/models/` – adding STEP models of off‑the‑shelf components (motors, sensors, etc.).
- If you propose a new printable part, provide the model separately and explain in the PR how it should be integrated.

---

## Documentation (`docs/`)

- **Language:** English is the primary language; Russian is allowed for `*.ru.md` translated pages.
- **Style:** neutral, clear, and consistent with existing documents (avoid excessive emojis).
- **Format:** Markdown, with correct relative links.
- **Images:** place in `docs/assets/` and reference them with relative paths.
- **Check** spelling, grammar, and that all links work.

---

## Firmware (`botix-esp32/`)

**Brief summary:**
- C++20, built via PlatformIO.
- Changes go through pull requests against `firmware-esp32` (or `main` for critical fixes).

**For detailed guidelines** (code style, V‑codes, testing, architecture, etc.), please first read the firmware’s [`README.md`](botix-esp32/README.md) to understand the project, and then refer to the [dedicated contributing guide](docs/firmware_contributing.md). All firmware‑specific details are encapsulated there.

---

## Tools (`tools/`)

- Scripts (Python/shell) should be cross‑platform and documented.
- When adding a new script, update `tools/README.md` with a description.
- License: GPL‑3.0‑or‑later.

---

## Commit and Pull Request Guidelines

- **One logical commit per feature/fix** (or squash during merge).
- **Commit messages:** use the format `<type>: <short description>` (e.g., `feat: add new lidar driver`, `fix: correct servo limits`, `docs: update assembly guide`).
- In the PR description, mention the affected subsystem and link to any related issue (`Closes #...`).

## License

This file is part of the project documentation and is licensed under [CC BY-SA 4.0](docs/LICENSE).

---

If you have any questions, feel free to open an issue or reach out to the maintainers.
