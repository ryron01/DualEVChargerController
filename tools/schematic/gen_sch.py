"""Generate the EV charger controller schematic as an EAGLE 9 .sch file.

Every connection is made by a short named net stub on each pin, so no wire
ever crosses another pin. Run:  python gen_sch.py out.sch
"""
import sys
from xml.sax.saxutils import escape

G = 2.54  # 0.1 inch grid, mm
IN = 25.4

# --------------------------------------------------------------------- library
# symbol pins: (name, x, y, rot, length, direction)
# rot R0 -> body to the right of the connection point; R180 -> body to the left


def conn_symbol(names):
    n = len(names)
    top = {2: 0, 3: G, 4: G, 6: 2 * G}[n]
    pins = [(nm, -5.08, top - i * G, "R0", "short", "pas") for i, nm in enumerate(names)]
    y1, y2 = top - (n - 1) * G - G, top + G
    body = [(-2.54, y1, 5.08, y1), (5.08, y1, 5.08, y2), (5.08, y2, -2.54, y2), (-2.54, y2, -2.54, y1)]
    return pins, body, (-2.54, y2 + 0.8), (-2.54, y1 - 2.6)


def two_pin_symbol(a, b):
    pins = [(a, -5.08, 0, "R0", "short", "pas"), (b, 5.08, 0, "R180", "short", "pas")]
    body = [(-2.54, -1.27, 2.54, -1.27), (2.54, -1.27, 2.54, 1.27), (2.54, 1.27, -2.54, 1.27), (-2.54, 1.27, -2.54, -1.27)]
    return pins, body, (-2.54, 2.0), (-2.54, -3.6)


def diode_symbol():
    pins = [("A", -5.08, 0, "R0", "short", "pas"), ("C", 5.08, 0, "R180", "short", "pas")]
    body = [(-1.27, 1.27, 1.27, 0), (1.27, 0, -1.27, -1.27), (-1.27, -1.27, -1.27, 1.27),
            (1.27, 1.27, 1.27, -1.27), (-2.54, 0, -1.27, 0), (1.27, 0, 2.54, 0)]
    return pins, body, (-2.54, 2.2), (-2.54, -3.8)


ESP_LEFT = ["3V3", "EN", "SENSOR_VP", "SENSOR_VN", "IO34", "IO35", "IO32", "IO33", "IO25", "IO26",
            "IO27", "IO14", "IO12", "GND1", "IO13", "SD2", "SD3", "CMD", "EXT_5V"]          # pads 1..19
ESP_RIGHT_BOTTOM_UP = ["CLK", "SD0", "SD1", "IO15", "IO2", "IO0", "IO4", "IO16", "IO17", "IO5",
                       "IO18", "IO19", "GND2", "IO21", "RXD0", "TXD0", "IO22", "IO23", "GND3"]  # pads 20..38


def esp_symbol():
    pins = []
    for i, nm in enumerate(ESP_LEFT):
        d = "pwr" if nm in ("3V3", "EXT_5V", "GND1") else "io"
        pins.append((nm, -15.24, 22.86 - i * G, "R0", "middle", d))
    for i, nm in enumerate(ESP_RIGHT_BOTTOM_UP):
        d = "pwr" if nm.startswith("GND") else "io"
        pins.append((nm, 15.24, -22.86 + i * G, "R180", "middle", d))
    body = [(-10.16, -25.4, 10.16, -25.4), (10.16, -25.4, 10.16, 25.4), (10.16, 25.4, -10.16, 25.4), (-10.16, 25.4, -10.16, -25.4)]
    return pins, body, (-10.16, 26.4), (-10.16, -28.0)


SHIFT_LV = ["LV1", "LV2", "LV", "GND@1", "LV3", "LV4"]
SHIFT_HV = ["HV1", "HV2", "HV", "GND@2", "HV3", "HV4"]
SHIFT_ROW_SPACING = 10.16  # mm between the LV and HV rows; measured from a photo, confirm on the part


def shifter_symbol():
    pins = [(nm, -12.7, 5.08 - i * G, "R0", "middle", "pas") for i, nm in enumerate(SHIFT_LV)]
    pins += [(nm, 12.7, 5.08 - i * G, "R180", "middle", "pas") for i, nm in enumerate(SHIFT_HV)]
    body = [(-7.62, -10.16, 7.62, -10.16), (7.62, -10.16, 7.62, 7.62), (7.62, 7.62, -7.62, 7.62), (-7.62, 7.62, -7.62, -10.16)]
    return pins, body, (-7.62, 8.6), (-7.62, -12.7)


def hlk_symbol():
    pins = [("AC1", -12.7, 2.54, "R0", "middle", "pas"), ("AC2", -12.7, -2.54, "R0", "middle", "pas"),
            ("+VO", 12.7, 2.54, "R180", "middle", "pas"), ("-VO", 12.7, -2.54, "R180", "middle", "pas")]
    body = [(-7.62, -5.08, 7.62, -5.08), (7.62, -5.08, 7.62, 5.08), (7.62, 5.08, -7.62, 5.08), (-7.62, 5.08, -7.62, -5.08)]
    return pins, body, (-7.62, 6.0), (-7.62, -7.6)


SYMBOLS = {
    "ESP32-DEVKITC": esp_symbol(),
    "HLK-PM01": hlk_symbol(),
    "PZEM-TTL": conn_symbol(["VCC", "RX", "TX", "GND"]),
    "RELAY-IN": conn_symbol(["DC+", "DC-", "IN"]),
    "LCD-I2C": conn_symbol(["GND", "VCC", "SDA", "SCL"]),
    "TOGGLE": conn_symbol(["GND", "SW1", "SW2"]),
    "BSS138-4CH": shifter_symbol(),
    "AC-2": conn_symbol(["L", "N"]),
    "FUSE": two_pin_symbol("1", "2"),
    "RESISTOR": two_pin_symbol("1", "2"),
    "DIODE": diode_symbol(),
}

# packages: name -> (pads [(name, x, y, drill, diameter, shape)], silk lines, description)


def header_pkg(n, pitch=2.54, drill=1.0, dia=1.7):
    x0 = -(n - 1) * pitch / 2
    pads = [(str(i + 1), round(x0 + i * pitch, 4), 0, drill, dia, "square" if i == 0 else "round") for i in range(n)]
    w = n * pitch / 2
    silk = [(-w, -1.27, w, -1.27), (w, -1.27, w, 1.27), (w, 1.27, -w, 1.27), (-w, 1.27, -w, -1.27)]
    return pads, silk


def esp_pkg():
    pads = []
    for i in range(19):
        pads.append((str(i + 1), -12.7, round(22.85 - i * 2.54, 4), 1.0, 1.7, "square" if i == 0 else "round"))
    for i in range(19):
        pads.append((str(20 + i), 12.7, round(-22.87 + i * 2.54, 4), 1.0, 1.7, "round"))
    silk = [(-14.2, -27.1, 14.2, -27.1), (14.2, -27.1, 14.2, 32.9), (14.2, 32.9, -14.2, 32.9), (-14.2, 32.9, -14.2, -27.1)]
    return pads, silk


def hlk_pkg():
    pads = [("1", -14.7, 2.5, 1.2, 2.2, "square"), ("2", -14.7, -2.5, 1.2, 2.2, "round"),
            ("3", 14.7, 7.7, 1.2, 2.2, "round"), ("4", 14.7, -7.7, 1.2, 2.2, "round")]
    silk = [(-17.0, -10.1, 17.0, -10.1), (17.0, -10.1, 17.0, 10.1), (17.0, 10.1, -17.0, 10.1), (-17.0, 10.1, -17.0, -10.1)]
    return pads, silk


def shifter_pkg():
    # top view, module component side up: LV row at -y, HV row at +y, channel 1 on the left
    h = SHIFT_ROW_SPACING / 2
    pads = [(str(i + 1), round(-6.35 + i * 2.54, 4), -h, 1.0, 1.7, "square" if i == 0 else "round") for i in range(6)]
    pads += [(str(7 + i), round(-6.35 + i * 2.54, 4), h, 1.0, 1.7, "round") for i in range(6)]
    silk = [(-7.75, -6.7, 7.75, -6.7), (7.75, -6.7, 7.75, 6.7), (7.75, 6.7, -7.75, 6.7), (-7.75, 6.7, -7.75, -6.7)]
    return pads, silk


def term_pkg():
    pads = [("1", -2.54, 0, 1.3, 2.6, "square"), ("2", 2.54, 0, 1.3, 2.6, "round")]
    silk = [(-5.08, -3.8, 5.08, -3.8), (5.08, -3.8, 5.08, 3.8), (5.08, 3.8, -5.08, 3.8), (-5.08, 3.8, -5.08, -3.8)]
    return pads, silk


def axial_pkg(pitch, body_half):
    pads = [("1", -pitch / 2, 0, 0.8, 1.6, "round"), ("2", pitch / 2, 0, 0.8, 1.6, "round")]
    silk = [(-body_half, -1.0, body_half, -1.0), (body_half, -1.0, body_half, 1.0), (body_half, 1.0, -body_half, 1.0), (-body_half, 1.0, -body_half, -1.0)]
    return pads, silk


def do35_pkg():
    pads = [("A", -3.81, 0, 0.8, 1.6, "round"), ("C", 3.81, 0, 0.8, 1.6, "square")]
    silk = [(-2.0, -0.9, 2.0, -0.9), (2.0, -0.9, 2.0, 0.9), (2.0, 0.9, -2.0, 0.9), (-2.0, 0.9, -2.0, -0.9), (1.4, -0.9, 1.4, 0.9)]
    return pads, silk


def tr5_pkg():
    pads = [("1", -2.54, 0, 0.8, 1.6, "round"), ("2", 2.54, 0, 0.8, 1.6, "round")]
    return pads, []  # circle drawn separately


PACKAGES = {
    "MODULE_ESP32-DEVKITC": (*esp_pkg(), "ESP32-DevKitC V4 footprint, 2x19 at 2.54 mm, rows 25.4 mm apart (from SnapEDA part). Measure your board before ordering."),
    "CONV_HLK-PM01": (*hlk_pkg(), "Hi-Link HLK-PM01, pad positions from SnapEDA part."),
    "PINHD-1X3": (*header_pkg(3), "1x3 pin header, 2.54 mm"),
    "PINHD-1X4": (*header_pkg(4), "1x4 pin header, 2.54 mm"),
    "BSS138-4CH-MODULE": (*shifter_pkg(), "4-channel BSS138 level shifter module, two rows of 6 at 2.54 mm, rows 10.16 mm apart (measure). "
                          "Order per row: 1, 2, V, GND, 3, 4. Module mounts component side up."),
    "TERM-2-5.08": (*term_pkg(), "2-way PCB screw terminal, 5.08 mm, rated for mains"),
    "R-0207-10.16": (*axial_pkg(10.16, 3.2), "Axial resistor 0207, 10.16 mm pitch"),
    "DO-35": (*do35_pkg(), "DO-35 axial diode, 7.62 mm pitch, band = cathode"),
    "FUSE-TR5": (*tr5_pkg(), "TR5 subminiature fuse, 5.08 mm pitch"),
}

# devicesets: name -> (prefix, symbol, package, {pin: pad}, description)


def straight(names):
    return {nm: str(i + 1) for i, nm in enumerate(names)}


DEVICESETS = {
    "ESP32-DEVKITC": ("U", "ESP32-DEVKITC", "MODULE_ESP32-DEVKITC",
                      {**{nm: str(i + 1) for i, nm in enumerate(ESP_LEFT)},
                       **{nm: str(20 + i) for i, nm in enumerate(ESP_RIGHT_BOTTOM_UP)}},
                      "ESP32-DevKitC V4 (38-pin), incl. WROOM-32U external-antenna variant"),
    "HLK-PM01": ("PS", "HLK-PM01", "CONV_HLK-PM01", {"AC1": "1", "AC2": "2", "-VO": "3", "+VO": "4"},
                 "Hi-Link HLK-PM01 AC-DC module, 5 V 600 mA"),
    "PZEM-TTL": ("J", "PZEM-TTL", "PINHD-1X4", straight(["VCC", "RX", "TX", "GND"]), "PZEM-004T TTL header: VCC RX TX GND"),
    "RELAY-IN": ("J", "RELAY-IN", "PINHD-1X3", straight(["DC+", "DC-", "IN"]), "Relay module control header: DC+ DC- IN"),
    "LCD-I2C": ("J", "LCD-I2C", "PINHD-1X4", straight(["GND", "VCC", "SDA", "SCL"]), "PCF8574 LCD backpack: GND VCC SDA SCL"),
    "TOGGLE": ("J", "TOGGLE", "PINHD-1X3", straight(["GND", "SW1", "SW2"]), "Panel switches: common GND, car 1, car 2"),
    "BSS138-4CH": ("U", "BSS138-4CH", "BSS138-4CH-MODULE",
                   {**{nm: str(i + 1) for i, nm in enumerate(SHIFT_LV)}, **{nm: str(7 + i) for i, nm in enumerate(SHIFT_HV)}},
                   "4-channel BSS138 bidirectional level shifter module (LV1-4 / HV1-4)"),
    "AC-2": ("J", "AC-2", "TERM-2-5.08", {"L": "1", "N": "2"}, "Mains L/N screw terminal"),
    "FUSE": ("F", "FUSE", "FUSE-TR5", {"1": "1", "2": "2"}, "TR5 fuse, 1 A time-lag, 250 V"),
    "RESISTOR": ("R", "RESISTOR", "R-0207-10.16", {"1": "1", "2": "2"}, "Axial resistor"),
    "SCHOTTKY": ("D", "DIODE", "DO-35", {"A": "A", "C": "C"}, "Schottky diode, DO-35 (BAT43 or BAT85)"),
}

# --------------------------------------------------------------------- design
PARTS = [  # name, deviceset, value, x, y
    ("U1", "ESP32-DEVKITC", "ESP32-DEVKITC-32U", 127.0, 101.6),
    ("PS1", "HLK-PM01", "HLK-PM01", 101.6, 160.02),
    ("F1", "FUSE", "1A T", 55.88, 170.18),
    ("J1", "AC-2", "AC-IN", 25.4, 170.18),
    ("J10", "AC-2", "PZEM1-AC", 149.86, 175.26),
    ("J11", "AC-2", "PZEM2-AC", 149.86, 152.4),
    ("J5", "RELAY-IN", "RELAY1", 50.8, 124.46),
    ("J6", "RELAY-IN", "RELAY2", 50.8, 104.14),
    ("J7", "TOGGLE", "TOGGLE", 50.8, 83.82),
    ("R1", "RESISTOR", "10k", 180.34, 116.84),
    ("D1", "SCHOTTKY", "BAT43", 180.34, 101.6),
    ("D2", "SCHOTTKY", "BAT43", 180.34, 88.9),
    ("J2", "PZEM-TTL", "PZEM1", 33.02, 50.8),
    ("J3", "PZEM-TTL", "PZEM2", 71.12, 50.8),
    ("J4", "LCD-I2C", "LCD", 109.22, 50.8),
    ("U2", "BSS138-4CH", "BSS138 LEVEL SHIFTER", 165.1, 50.8),
]

NETS = {  # name -> (class, [(part, pin)])
    "AC_L": (1, [("J1", "L"), ("F1", "1")]),
    "AC_L_F": (1, [("F1", "2"), ("PS1", "AC1"), ("J10", "L"), ("J11", "L")]),
    "AC_N": (1, [("J1", "N"), ("PS1", "AC2"), ("J10", "N"), ("J11", "N")]),
    "+5V": (0, [("PS1", "+VO"), ("U1", "EXT_5V"), ("J2", "VCC"), ("J3", "VCC"), ("J4", "VCC"),
                ("J5", "DC+"), ("J6", "DC+"), ("U2", "HV")]),
    "GND": (0, [("PS1", "-VO"), ("U1", "GND1"), ("U1", "GND2"), ("U1", "GND3"), ("J2", "GND"), ("J3", "GND"),
                ("J4", "GND"), ("J5", "DC-"), ("J6", "DC-"), ("J7", "GND"), ("U2", "GND@1"), ("U2", "GND@2")]),
    "+3V3": (0, [("U1", "3V3"), ("R1", "1"), ("U2", "LV")]),
    "PZEM_TX": (0, [("U1", "IO16"), ("D1", "A"), ("D2", "A"), ("R1", "2")]),
    "PZEM1_TX": (0, [("J2", "TX"), ("D1", "C")]),
    "PZEM2_TX": (0, [("J3", "TX"), ("D2", "C")]),
    "PZEM_RX": (0, [("U1", "IO17"), ("J2", "RX"), ("J3", "RX")]),
    "RELAY1": (0, [("U1", "IO25"), ("J5", "IN")]),
    "RELAY2": (0, [("U1", "IO26"), ("J6", "IN")]),
    "SW1": (0, [("U1", "IO32"), ("J7", "SW1")]),
    "SW2": (0, [("U1", "IO33"), ("J7", "SW2")]),
    "SDA_3V3": (0, [("U1", "IO22"), ("U2", "LV1")]),
    "SCL_3V3": (0, [("U1", "IO23"), ("U2", "LV2")]),
    "SDA_5V": (0, [("U2", "HV1"), ("J4", "SDA")]),
    "SCL_5V": (0, [("U2", "HV2"), ("J4", "SCL")]),
}

STUB = 3 * G  # 7.62 mm


def f(v):
    return f"{round(v, 4):g}"


def pin_lookup(dset):
    sym = DEVICESETS[dset][1]
    return {p[0]: p for p in SYMBOLS[sym][0]}


def pin_abs(part):
    name, dset, _, px, py = part
    return {nm: (px + p[1], py + p[2], p[3]) for nm, p in pin_lookup(dset).items()}


def stub(x, y, rot):
    d = -STUB if rot == "R0" else STUB
    return (x, y, x + d, y)


def build():
    o = []
    a = o.append
    a('<?xml version="1.0" encoding="utf-8"?>')
    a('<!DOCTYPE eagle SYSTEM "eagle.dtd">')
    a('<eagle version="9.6.2">')
    a('<drawing>')
    a('<settings><setting alwaysvectorfont="no"/><setting verticaltext="up"/></settings>')
    a('<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>')
    a('<layers>')
    layers = [(1, "Top", 4), (16, "Bottom", 1), (17, "Pads", 2), (18, "Vias", 2), (19, "Unrouted", 6), (20, "Dimension", 24),
              (21, "tPlace", 7), (22, "bPlace", 7), (23, "tOrigins", 15), (24, "bOrigins", 15), (25, "tNames", 7), (26, "bNames", 7),
              (27, "tValues", 7), (28, "bValues", 7), (29, "tStop", 7), (30, "bStop", 7), (31, "tCream", 7), (32, "bCream", 7),
              (35, "tGlue", 7), (36, "bGlue", 7), (39, "tKeepout", 4), (40, "bKeepout", 1), (41, "tRestrict", 4), (42, "bRestrict", 1),
              (43, "vRestrict", 2), (44, "Drills", 7), (45, "Holes", 7), (46, "Milling", 3), (47, "Measures", 7), (48, "Document", 7),
              (49, "Reference", 7), (51, "tDocu", 7), (52, "bDocu", 7), (88, "SimResults", 9), (89, "SimProbes", 9), (90, "Modules", 5),
              (91, "Nets", 2), (92, "Busses", 1), (93, "Pins", 2), (94, "Symbols", 4), (95, "Names", 7), (96, "Values", 7),
              (97, "Info", 7), (98, "Guide", 6)]
    for n, nm, col in layers:
        a(f'<layer number="{n}" name="{nm}" color="{col}" fill="1" visible="yes" active="yes"/>')
    a('</layers>')
    a('<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">')
    a('<description>Dual EV charger controller. Bench-verified netlist, November 2026. '
      'Mains nets are in net class "mains" (6 mm to low voltage).</description>')
    a('<libraries><library name="evcharger">')
    a('<description>Parts for the dual EV charger controller. Footprints for the ESP32 DevKitC and HLK-PM01 follow the SnapEDA parts; '
      'check every footprint against the physical part before ordering a PCB.</description>')
    a('<packages>')
    for pname, (pads, silk, desc) in PACKAGES.items():
        a(f'<package name="{escape(pname)}"><description>{escape(desc)}</description>')
        for nm, x, y, drill, dia, shape in pads:
            a(f'<pad name="{escape(nm)}" x="{f(x)}" y="{f(y)}" drill="{f(drill)}" diameter="{f(dia)}" shape="{shape}"/>')
        for x1, y1, x2, y2 in silk:
            a(f'<wire x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" width="0.2032" layer="21"/>')
        if pname == "FUSE-TR5":
            a('<circle x="0" y="0" radius="4.25" width="0.2032" layer="21"/>')
        ys = [p[2] for p in pads] + [0]
        a(f'<text x="0" y="{f(max(ys) + 2.5)}" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>')
        a(f'<text x="0" y="{f(min(ys) - 2.5)}" size="1.27" layer="27" align="top-center">&gt;VALUE</text>')
        a('</package>')
    a('</packages>')
    a('<symbols>')
    for sname, (pins, body, namepos, valpos) in SYMBOLS.items():
        a(f'<symbol name="{escape(sname)}">')
        for x1, y1, x2, y2 in body:
            a(f'<wire x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" width="0.254" layer="94"/>')
        a(f'<text x="{f(namepos[0])}" y="{f(namepos[1])}" size="1.778" layer="95">&gt;NAME</text>')
        a(f'<text x="{f(valpos[0])}" y="{f(valpos[1])}" size="1.778" layer="96">&gt;VALUE</text>')
        for nm, x, y, rot, length, d in pins:
            vis = "pin" if sname in ("FUSE", "RESISTOR", "DIODE") else "pad" if False else "pin"
            a(f'<pin name="{escape(nm)}" x="{f(x)}" y="{f(y)}" visible="{vis}" length="{length}" direction="{d}" rot="{rot}"/>')
        a('</symbol>')
    a('</symbols>')
    a('<devicesets>')
    for dname, (prefix, sym, pkg, conn, desc) in DEVICESETS.items():
        a(f'<deviceset name="{escape(dname)}" prefix="{prefix}" uservalue="yes"><description>{escape(desc)}</description>')
        a(f'<gates><gate name="G$1" symbol="{escape(sym)}" x="0" y="0"/></gates>')
        a(f'<devices><device name="" package="{escape(pkg)}"><connects>')
        for pin, pad in conn.items():
            a(f'<connect gate="G$1" pin="{escape(pin)}" pad="{escape(pad)}"/>')
        a('</connects><technologies><technology name=""/></technologies></device></devices></deviceset>')
    a('</devicesets>')
    a('</library></libraries>')
    a('<attributes/><variantdefs/>')
    a('<classes><class number="0" name="default" width="0" drill="0"></class>'
      '<class number="1" name="mains" width="0.6096" drill="0"><clearance class="0" value="6"/><clearance class="1" value="2.5"/></class></classes>')
    a('<parts>')
    for name, dset, value, x, y in PARTS:
        a(f'<part name="{name}" library="evcharger" deviceset="{escape(dset)}" device="" value="{escape(value)}"/>')
    a('</parts>')
    a('<sheets><sheet><plain>')
    a('<text x="20.32" y="190.5" size="3.81" layer="97">DUAL EV CHARGER CONTROLLER</text>')
    a('<text x="20.32" y="185.42" size="1.778" layer="97">Mains nets AC_L, AC_L_F, AC_N use net class "mains". Relay load wiring and outlets stay off-board on 12 AWG.</text>')
    a('<text x="20.32" y="182.88" size="1.778" layer="97">PZEM TX diode-OR: cathode (band) toward each PZEM TX, anodes joined at GPIO16 with 10k to 3V3.</text>')
    a('</plain><instances>')
    for name, dset, value, x, y in PARTS:
        a(f'<instance part="{name}" gate="G$1" x="{f(x)}" y="{f(y)}"/>')
    a('</instances><busses/><nets>')
    parts_by_name = {p[0]: p for p in PARTS}
    for net, (cls, members) in NETS.items():
        a(f'<net name="{escape(net)}" class="{cls}">')
        for part, pin in members:
            x, y, rot = pin_abs(parts_by_name[part])[pin]
            x1, y1, x2, y2 = stub(x, y, rot)
            a('<segment>')
            a(f'<pinref part="{part}" gate="G$1" pin="{escape(pin)}"/>')
            a(f'<wire x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" width="0.1524" layer="91"/>')
            rot_lbl = "R180" if rot == "R0" else "R0"
            a(f'<label x="{f(x2)}" y="{f(y2)}" size="1.27" layer="95" rot="{rot_lbl}"/>')
            a('</segment>')
        a('</net>')
    a('</nets></sheet></sheets>')
    a('</schematic></drawing></eagle>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    open(sys.argv[1], "w").write(build())
    print("wrote", sys.argv[1])
