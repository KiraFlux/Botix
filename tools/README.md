# Tools

This directory contains automation scripts for repetitive tasks in the Botix monorepo: exporting printable models, generating renders, checking file integrity, and other maintenance routines.

All scripts are written in Python 3 and are licensed under GPL‑3.0‑or‑later.

---

## Requirements

- **Python 3.14+**
- **FreeCAD** (with Python bindings) – required for scripts that process CAD files.
- Additional Python packages may be listed in a `requirements.txt` (if present). For now, the scripts rely only on the standard library and FreeCAD’s Python API.

Make sure FreeCAD’s Python module is available in your `PYTHONPATH` or installed system‑wide.

---

## Available Scripts

### `export_printable_models.py`

**Purpose:**  
Exports all 3D‑printable parts from the main FreeCAD assembly (`mcad/botix.fcstd`) into STEP files, ready for slicing. It also counts how many times each part is used (via `App::Link` objects) and writes the results to the `artifacts/` directory.

**Usage:**
```bash
cd /path/to/botix
python3 tools/export_printable_models.py
```

**What it does:**
1. Opens `mcad/botix.fcstd`.
2. Scans all objects that have a custom property `Printable = True`.
3. Extracts the shape from each printable object (handles `App::Part`, `PartDesign::Body`, and `Part::Feature`).
4. Counts the number of instances by examining `App::Link` objects referencing each part.
5. Exports each unique shape as a STEP file into `artifacts/` (named `<label>.stp`).
6. Prints a summary of all exported models and their instance counts.

**Notes:**
- The script expects the repository structure to be preserved (i.e., `tools/` and `mcad/` are siblings).
- If a model cannot be processed, an error message is printed, and the script continues with the next object.
- The `artifacts/` directory is created automatically if it does not exist.

---

### Future Scripts

Other scripts may be added later, for example:
- `render_views.py` – generate rendered images of the robot from different angles.
- `validate_links.py` – check for broken external references in FreeCAD files.
- `update_docs.py` – synchronise documentation with the latest assets.

When adding a new script, please update this `README.md` with a brief description, usage, and any special requirements.

---

## License

All scripts in this directory are distributed under the **GNU General Public License v3.0 or later**.  
See the [LICENSE](LICENSE) file for the full text.

This `README.md` file itself is part of the project documentation and is licensed under [CC BY‑SA 4.0](../../docs/LICENSE). For the complete licensing information of all project components, refer to the [root repository README](../README.md#repository-structure--licensing).

---

## Contributing

If you want to add or improve a script, please follow the general [contributing guidelines](../CONTRIBUTING.md#tools-tools).  
Make sure your script is cross‑platform, well‑documented, and includes appropriate error handling. Update this `README.md` accordingly.