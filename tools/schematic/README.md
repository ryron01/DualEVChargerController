# Schematic tools

The schematic in `hardware/ev-charger-controller.sch` is generated, so wiring changes stay reviewable as code.

```sh
python tools/schematic/gen_sch.py hardware/ev-charger-controller.sch
python tools/schematic/verify_sch.py hardware/ev-charger-controller.sch
python tools/schematic/render_sch.py hardware/ev-charger-controller.sch hardware/schematic-preview.png
```

- `gen_sch.py` holds the parts library, placement and netlist.
- `verify_sch.py` keeps its own copy of the expected netlist and checks the file against it: every net, the ESP32 and HLK-PM01 pin-to-pad mapping, and that no wire touches another net, crosses a part, or lands on an unconnected pin. Change both files when the wiring changes.
- `render_sch.py` draws the preview image (needs matplotlib).

Every pin gets its own short named stub, and connections come from net names, never from wires drawn between parts. An earlier schematic drawn with long wires merged mains, 5 V and ground into one net because wires crossed pins.
