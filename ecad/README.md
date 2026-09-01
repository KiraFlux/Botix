# Electronics (KiCad)

KiCad 10 source files for Botix PCBs.

## Directory Structure

| Path                                | Description                                                                               |
| ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `botix.kicad_sym`                   | Symbol library.                                                                           |
| `botix_library.pretty/`             | Footprint library.                                                                        |
| `botix_power_module_v1/`            | Historical version, imported from EasyEDA. Kept for reference.                            |
| `botix_power_module_v2_pcb_order/`  | Version 2, optimized for manufacturing (JLCPCB, PCBWay) – use this for production orders. |
| `botix_power_module_v2_ttm_double/` | Version 2, prepared for double‑sided toner TTM.                                           |
| `botix_power_module_v2_ttm_single/` | Version 2, single‑sided TTM variant – simpler for home fabrication.                       |
## Opening

- Install **KiCad 10**. 
- Open any `.kicad_pro` file in the corresponding folder - that is the main project. Schematics are `.kicad_sch`, PCB is `.kicad_pcb`.

## Notes

- All boards are designed to power the robot from three 14500 cells (3S) and include protection, voltage regulators, and connectors for motors, servos, and sensors.
- The `ttm` folders are specifically prepared for DIY toner transfer (paper + laser printer + iron), with single‑ or double‑sided variants. These are useful for home fabrication.

For detailed electrical schematics and BOM, refer to the [documentation](../docs/).

## Contributing

If you want to add a new board design or modify an existing one, please read the [general contributing guidelines](../CONTRIBUTING.md) first, then refer to the [Hardware section](../CONTRIBUTING.md#hardware-ecad) for specific rules.

## License

This README file is part of the project documentation and is licensed under [CC BY-SA 4.0](../docs/LICENSE).

The hardware design files in this directory (`ecad/`) – including KiCad schematics, PCB layouts, symbols, and footprints – are distributed under [CERN-OHL-S-2.0](LICENSE).

For the complete licensing information of all project components, refer to the [root repository README](../README.md#repository-structure--licensing).
