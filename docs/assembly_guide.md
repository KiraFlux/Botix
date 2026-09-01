# Assembly Guide

> This guide is currently work in progress.

How to assemble Botix robot for **Basic** (Arduino) and **Advanced** (ESP32) variants.

All 3D‑printed parts are in [`mcad/`](../mcad/). Export to STP with [`tools/export_printable_models.py`](../tools/export_printable_models.py).  
Schematics and BOM are in [`ecad/`](../ecad/).

---

## Tools and Materials

- 3D‑printed parts (see `mcad/`)
- Power board (choose variant from `ecad/`)
- Controller: Arduino UNO or ESP32 dev board
- Motor drivers: DRV8871 or compatible H‑bridge
- Motors (GA25 with encoders), wheels, casters
- Fasteners: M3 screws, nuts, standoffs
- Soldering iron, hex keys, screwdrivers, wire strippers, multimeter

---

## Electronics Assembly

### Power Board

Select variant: `botix_power_module_v2_pcb_order` (PCB manufacturing) or `ttm_*` (DIY toner transfer).  
Solder components per silkscreen and schematics.  
Check output voltages: 5V from Mini560, adjustable from LM2596S.

### Controller

- **Basic:** Arduino UNO or compatible
- **Advanced:** ESP32 dev module (ESP32‑D, etc.)

Mount the controller on the deck using standoffs.

### Wiring

Connect motors, encoders, and servos to drivers and controller per pinout in [`ecad/`](../ecad/) and [`botix-esp32/`](../botix-esp32/) firmware docs.

---

## Mechanical Assembly

### Chassis

1. Print: platform, deck, side walls, rear wall, frames.
2. Insert M3 nuts into slots.
3. Assemble: platform → side walls → rear wall → deck.
4. Secure with screws.

### Motors and Wheels

1. Mount GA25 motors on side walls.
2. Attach M4 couplings to motor shafts.
3. Install wheels (D52 RC wheels), secure with set screws.

### Casters

Install ball casters under the platform for smooth movement.  
Add felt pads optionally.

### Manipulator (Optional)

Print arm, gripper, gears.  
Assemble with MG90S or MG995 servos.  
Mount on front deck using the frame.

---

## Final Integration

### Basic (Arduino)

1. Place Arduino on deck.
2. Connect motor shield.
3. Wire power board → motor shield → sensors → servos.
4. Upload Arduino sketch.

### Advanced (ESP32)

1. Place ESP32 on deck.
2. Connect power board, motor drivers, servos, LIDAR, encoders.
3. Flash [`botix-esp32/`](../botix-esp32/) firmware via PlatformIO.
4. Configure via CLI (UART) or WiFi.

---

## Testing and First Run

Power on.  
For Basic: test motors and servos with a simple sketch.  
For Advanced: connect via serial, use `help`, test units with `unit init`.  
Check encoders and LIDAR readings (if installed).

---

## Troubleshooting

| Issue | Likely Cause |
|-------|--------------|
| Motors don't move | Power, wiring, driver enable |
| No serial output | Baud rate (115200), USB cable |
| LIDAR not spinning | Power or UART connection |
| Manipulator jitter | Servo pulse range in config |

---

## References

- [Electronics and BOM](../ecad/README.md)
- [Firmware docs](../botix-esp32/README.md)
- [Gallery with photos](../docs/gallery.md)