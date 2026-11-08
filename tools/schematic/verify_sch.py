"""Independent checks on the generated .sch. Exits non-zero on any failure."""
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

# Expected netlist, written from the bench wiring and ev-charger.yaml, not from the generator.
EXPECTED = {
    "AC_L": {"J1.L", "F1.1"},
    "AC_L_F": {"F1.2", "PS1.AC1", "J10.L", "J11.L"},
    "AC_N": {"J1.N", "PS1.AC2", "J10.N", "J11.N"},
    "+5V": {"PS1.+VO", "U1.EXT_5V", "J2.VCC", "J3.VCC", "J4.VCC", "J5.DC+", "J6.DC+", "U2.HV"},
    "GND": {"PS1.-VO", "U1.GND1", "U1.GND2", "U1.GND3", "J2.GND", "J3.GND", "J4.GND", "J5.DC-", "J6.DC-",
            "J7.GND", "U2.GND@1", "U2.GND@2"},
    "+3V3": {"U1.3V3", "R1.1", "U2.LV"},
    "PZEM_TX": {"U1.IO16", "D1.A", "D2.A", "R1.2"},       # GPIO16 = UART RX
    "PZEM1_TX": {"J2.TX", "D1.C"},                         # cathode toward PZEM
    "PZEM2_TX": {"J3.TX", "D2.C"},
    "PZEM_RX": {"U1.IO17", "J2.RX", "J3.RX"},              # GPIO17 = UART TX
    "RELAY1": {"U1.IO25", "J5.IN"},
    "RELAY2": {"U1.IO26", "J6.IN"},
    "SW1": {"U1.IO32", "J7.SW1"},
    "SW2": {"U1.IO33", "J7.SW2"},
    "SDA_3V3": {"U1.IO22", "U2.LV1"},
    "SCL_3V3": {"U1.IO23", "U2.LV2"},
    "SDA_5V": {"U2.HV1", "J4.SDA"},
    "SCL_5V": {"U2.HV2", "J4.SCL"},
}
MAINS = {"AC_L", "AC_L_F", "AC_N"}
# physical pad expectations from the SnapEDA parts read out of Fusion
PAD_EXPECT = {("HLK-PM01", "AC1"): "1", ("HLK-PM01", "AC2"): "2", ("HLK-PM01", "-VO"): "3", ("HLK-PM01", "+VO"): "4",
              ("ESP32-DEVKITC", "3V3"): "1", ("ESP32-DEVKITC", "EXT_5V"): "19", ("ESP32-DEVKITC", "GND1"): "14",
              ("ESP32-DEVKITC", "IO16"): "27", ("ESP32-DEVKITC", "IO17"): "28", ("ESP32-DEVKITC", "IO22"): "36",
              ("ESP32-DEVKITC", "IO23"): "37", ("ESP32-DEVKITC", "IO25"): "9", ("ESP32-DEVKITC", "IO26"): "10",
              ("ESP32-DEVKITC", "IO32"): "7", ("ESP32-DEVKITC", "IO33"): "8", ("ESP32-DEVKITC", "GND2"): "32",
              ("ESP32-DEVKITC", "GND3"): "38",
              ("BSS138-4CH", "LV1"): "1", ("BSS138-4CH", "LV"): "3", ("BSS138-4CH", "GND@1"): "4",
              ("BSS138-4CH", "HV1"): "7", ("BSS138-4CH", "HV"): "9", ("BSS138-4CH", "GND@2"): "10"}

fails = []


def fail(msg):
    fails.append(msg)


def rnd(p):
    return (round(p[0], 3), round(p[1], 3))


root = ET.parse(sys.argv[1]).getroot()
lib = root.find(".//libraries/library")
symbols = {s.get("name"): s for s in lib.find("symbols")}
packages = {p.get("name"): p for p in lib.find("packages")}
devsets = {d.get("name"): d for d in lib.find("devicesets")}

# library integrity
for dname, ds in devsets.items():
    sym = symbols[ds.find("gates/gate").get("symbol")]
    sym_pins = [p.get("name") for p in sym.findall("pin")]
    if len(sym_pins) != len(set(sym_pins)):
        fail(f"{dname}: duplicate symbol pin names")
    dev = ds.find("devices/device")
    pkg = packages[dev.get("package")]
    pads = [p.get("name") for p in pkg.findall("pad")]
    if len(pads) != len(set(pads)):
        fail(f"{dname}: duplicate pad names")
    conns = {c.get("pin"): c.get("pad") for c in dev.findall("connects/connect")}
    if set(conns) != set(sym_pins):
        fail(f"{dname}: connects {sorted(set(sym_pins) ^ set(conns))} mismatch")
    if sorted(conns.values()) != sorted(pads) or len(set(conns.values())) != len(conns):
        fail(f"{dname}: pads not mapped one-to-one ({sorted(conns.values())} vs {sorted(pads)})")
    for (d, pin), pad in PAD_EXPECT.items():
        if d == dname and conns.get(pin) != pad:
            fail(f"{dname}.{pin} maps to pad {conns.get(pin)}, expected {pad}")

# level shifter: each LV pad must sit directly across from its HV pad
ds = devsets["BSS138-4CH"]; dev = ds.find("devices/device")
conns = {c.get("pin"): c.get("pad") for c in dev.findall("connects/connect")}
padxy = {p.get("name"): (float(p.get("x")), float(p.get("y"))) for p in packages[dev.get("package")].findall("pad")}
for lv, hv in [("LV1", "HV1"), ("LV2", "HV2"), ("LV", "HV"), ("GND@1", "GND@2"), ("LV3", "HV3"), ("LV4", "HV4")]:
    if abs(padxy[conns[lv]][0] - padxy[conns[hv]][0]) > 1e-6:
        fail(f"level shifter {lv} is not across from {hv}")

# placed pin positions
parts = {p.get("name"): p for p in root.find(".//parts")}
inst = {i.get("part"): (float(i.get("x")), float(i.get("y"))) for i in root.find(".//instances")}
pin_pos = {}       # "U1.IO16" -> (x, y)
bodies = {}        # part -> bbox of symbol body
for name, part in parts.items():
    sym = symbols[devsets[part.get("deviceset")].find("gates/gate").get("symbol")]
    ox, oy = inst[name]
    for p in sym.findall("pin"):
        pin_pos[f"{name}.{p.get('name')}"] = rnd((ox + float(p.get("x")), oy + float(p.get("y"))))
    xs, ys = [], []
    for w in sym.findall("wire"):
        xs += [float(w.get("x1")), float(w.get("x2"))]
        ys += [float(w.get("y1")), float(w.get("y2"))]
    bodies[name] = (ox + min(xs), oy + min(ys), ox + max(xs), oy + max(ys))

# nets
actual = {}
wires = []  # (net, x1, y1, x2, y2)
for net in root.find(".//nets"):
    nn = net.get("name")
    members = set()
    for seg in net.findall("segment"):
        refs = seg.findall("pinref")
        segw = seg.findall("wire")
        if len(refs) != 1 or len(segw) != 1:
            fail(f"{nn}: segment should hold one pinref and one wire")
        for r in refs:
            key = f"{r.get('part')}.{r.get('pin')}"
            if key not in pin_pos:
                fail(f"{nn}: pinref {key} does not exist")
                continue
            if key in members:
                fail(f"{nn}: {key} listed twice")
            members.add(key)
            for w in segw:
                ends = {rnd((float(w.get("x1")), float(w.get("y1")))), rnd((float(w.get("x2")), float(w.get("y2"))))}
                if pin_pos[key] not in ends:
                    fail(f"{nn}: stub for {key} does not start on the pin")
        for w in segw:
            wires.append((nn, float(w.get("x1")), float(w.get("y1")), float(w.get("x2")), float(w.get("y2"))))
        for lb in seg.findall("label"):
            lp = rnd((float(lb.get("x")), float(lb.get("y"))))
            if not any(lp in {rnd((w[1], w[2])), rnd((w[3], w[4]))} for w in wires if w[0] == nn):
                fail(f"{nn}: label not on its wire")
    if nn in actual:
        fail(f"net {nn} defined twice")
    actual[nn] = members
    if (net.get("class") == "1") != (nn in MAINS):
        fail(f"{nn}: wrong net class {net.get('class')}")

# netlist comparison
for nn in sorted(set(EXPECTED) | set(actual)):
    if EXPECTED.get(nn) != actual.get(nn):
        fail(f"net {nn}: expected {sorted(EXPECTED.get(nn, []))}, got {sorted(actual.get(nn, []))}")
all_pins = [p for m in actual.values() for p in m]
if len(all_pins) != len(set(all_pins)):
    fail("a pin is on more than one net")


def on_seg(pt, w):
    _, x1, y1, x2, y2 = w
    px, py = pt
    if abs(y1 - y2) < 1e-6:
        return abs(py - y1) < 1e-3 and min(x1, x2) - 1e-3 <= px <= max(x1, x2) + 1e-3
    return abs(px - x1) < 1e-3 and min(y1, y2) - 1e-3 <= py <= max(y1, y2) + 1e-3


# no wire touches a pin of another net or an unconnected pin, other than its own
pin_net = {p: nn for nn, m in actual.items() for p in m}
for w in wires:
    for p, pos in pin_pos.items():
        if on_seg(pos, w) and pin_net.get(p) != w[0]:
            fail(f"wire of {w[0]} touches {p} ({pin_net.get(p, 'unconnected')})")
# no two wires of different nets touch or overlap
for i, a in enumerate(wires):
    for b in wires[i + 1:]:
        if a[0] == b[0]:
            continue
        for pt in ((b[1], b[2]), (b[3], b[4])):
            if on_seg(pt, a):
                fail(f"wires of {a[0]} and {b[0]} touch at {pt}")
        for pt in ((a[1], a[2]), (a[3], a[4])):
            if on_seg(pt, b):
                fail(f"wires of {a[0]} and {b[0]} touch at {pt}")
# no stub runs through another part's body, no bodies overlap
for w in wires:
    for name, (bx1, by1, bx2, by2) in bodies.items():
        _, x1, y1, x2, y2 = w
        if by1 < y1 < by2 and max(min(x1, x2), bx1) < min(max(x1, x2), bx2):
            owner = None
            fail(f"wire of {w[0]} at y={y1} crosses body of {name}")
names = list(bodies)
for i, a in enumerate(names):
    for b in names[i + 1:]:
        A, B = bodies[a], bodies[b]
        if A[0] < B[2] and B[0] < A[2] and A[1] < B[3] and B[1] < A[3]:
            fail(f"symbols {a} and {b} overlap")

print(f"parts={len(parts)} nets={len(actual)} connected pins={len(all_pins)} wires={len(wires)}")
if fails:
    print("FAIL")
    for m in fails:
        print(" -", m)
    sys.exit(1)
print("PASS: netlist matches the bench wiring; no shared points, crossings or overlaps")
