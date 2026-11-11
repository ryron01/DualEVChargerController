"""Perfboard layout for the EV charger controller on a 70 x 90 mm plain perfboard.

The board is drawn as it sits in the enclosure: the 90 mm side runs left to
right. That is the printed board turned a quarter turn left, so printed row
numbers 1..31 run left to right and printed letters A..Z run bottom to top.
A hole is named the way the board prints it, letter then number (A1 is the
bottom-left hole).

Parts sit on top; every connection is an insulated wire on the bottom between
two pins. Wires may cross each other but never pass over another net's pad.
Mains stays in the bottom-left zone and every low-voltage hole keeps 3 holes
(7.6 mm) from any mains hole.

Usage: python perfboard.py layout.json [tries]
"""
import json
import random
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from gen_sch import NETS, ESP_LEFT, ESP_RIGHT_BOTTOM_UP  # same netlist as the schematic

W, H = 31, 26                       # x: printed numbers 1..31, y: printed letters Z..A (top to bottom)
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAINS = {n for n, (cls, _) in NETS.items() if cls == 1}
CLEAR = 3.0                         # holes between mains and low voltage (7.62 mm)
MAINS_RECT = (0, 20, 8, 25)         # x1, y1, x2, y2 in board coordinates, bottom-left corner
MAINS_ZONE = lambda x, y: MAINS_RECT[0] <= x <= MAINS_RECT[2] and MAINS_RECT[1] <= y <= MAINS_RECT[3]

# ------------------------------------------------------------------ placement
# board coordinates: x = 0..30 left to right, y = 0..25 top to bottom
PLACE = {}
# ESP32 (Lonely Binary, WROOM-32UE) across the top on female headers.
# Pads 20-38 form the top row along the board's upper edge, so the u.FL antenna
# connector (beside pad 38) sits near the top-left corner of the module.
# Pads 1-19 form the lower row, facing the rest of the board. USB-C is at the right end.
for k, nm in enumerate(ESP_LEFT, start=1):               # pad k: lower row, pad 1 at the left
    PLACE[("U1", nm)] = (11 + k, 10)
for i, nm in enumerate(ESP_RIGHT_BOTTOM_UP):             # pad 20 + i: top row, pad 38 at the left
    PLACE[("U1", nm)] = (30 - i, 0)
PLACE.update({
    # mains, bottom left: J1 feeds the HLK-PM01's AC pins (HLK stands vertically, AC end down)
    ("J1", "N"): (0, 22), ("J1", "L"): (0, 24),
    ("PS1", "AC1"): (5, 24), ("PS1", "AC2"): (7, 24), ("PS1", "-VO"): (3, 12), ("PS1", "+VO"): (9, 12),
    # buttons and relays along the bottom edge, each signal pin straight below its GPIO
    ("J7", "GND"): (17, 25), ("J7", "SW1"): (18, 25), ("J7", "SW2"): (19, 25),
    ("J5", "IN"): (20, 25), ("J5", "DC-"): (21, 25), ("J5", "DC+"): (22, 25),
    ("J6", "IN"): (24, 25), ("J6", "DC-"): (25, 25), ("J6", "DC+"): (26, 25),
    # PZEM headers on the right edge
    ("J2", "VCC"): (30, 13), ("J2", "RX"): (30, 14), ("J2", "TX"): (30, 15), ("J2", "GND"): (30, 16),
    ("J3", "VCC"): (30, 19), ("J3", "RX"): (30, 20), ("J3", "TX"): (30, 21), ("J3", "GND"): (30, 22),
    # LCD header on the left edge beside the level shifter
    ("J4", "GND"): (0, 2), ("J4", "VCC"): (0, 3), ("J4", "SDA"): (0, 4), ("J4", "SCL"): (0, 5),
    # PZEM TX diode-OR and pull-up, beside the PZEM headers
    ("D1", "A"): (24, 15), ("D1", "C"): (27, 15),
    ("D2", "A"): (24, 17), ("D2", "C"): (27, 17),
    ("R1", "1"): (22, 13), ("R1", "2"): (22, 17),
})
# level shifter in the top-left corner: LV row on the right (toward GPIO22/23 and 3V3),
# HV row on the left (toward the LCD header and the HLK's 5 V); channel 1 at the bottom
for i, nm in enumerate(["LV1", "LV2", "LV", "GND@1", "LV3", "LV4"]):
    PLACE[("U2", nm)] = (9, 6 - i)
for i, nm in enumerate(["HV1", "HV2", "HV", "GND@2", "HV3", "HV4"]):
    PLACE[("U2", nm)] = (5, 6 - i)

# body outlines on top, in hole units (x1, y1, x2, y2, label)
BODIES = {
    "U1": (11.25, -0.6, 31.5, 10.6, "ESP32 WROOM-32UE on female headers (USB-C at the right end)"),
    "PS1": (2.02, 11.3, 9.98, 24.7, "HLK-PM01"),
    "U2": (4.36, 0.45, 9.64, 6.55, "Level shifter"),
    "J1": (-1.5, 21.0, 1.5, 25.0, "AC in (from inline fuse)"),
    "J4": (-0.5, 1.5, 0.5, 5.5, "LCD"),
    "J7": (16.5, 24.5, 19.5, 25.5, "Buttons"), "J5": (19.5, 24.5, 22.5, 25.5, "Relay 1"), "J6": (23.5, 24.5, 26.5, 25.5, "Relay 2"),
    "J2": (29.5, 12.5, 30.5, 16.5, "PZEM1"), "J3": (29.5, 18.5, 30.5, 22.5, "PZEM2"),
    "D1": (24.7, 14.6, 26.3, 15.4, "D1"), "D2": (24.7, 16.6, 26.3, 17.4, "D2"), "R1": (21.5, 13.7, 22.5, 16.3, "R1"),
}
UNDER_MODULE = set()


def hole(p):
    """Printed hole name: letter (A at the bottom) then number (1 at the left)."""
    return f"{LETTERS[H - 1 - p[1]]}{p[0] + 1}"


def runs(path):
    """Compress a hole path into straight runs [(start, end), ...]."""
    out, start = [], path[0]
    for i in range(1, len(path)):
        last = i == len(path) - 1
        if last or (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]) != (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]):
            out.append((start, path[i]))
            start = path[i]
    return out


def pin_owner():
    owner = {}
    for (part, pin), xy in PLACE.items():
        owner[xy] = "__nc__"
        for n, (_, mem) in NETS.items():
            if (part, pin) in mem:
                owner[xy] = n
    return owner


def mst(points):
    """Prim's MST on Manhattan distance; returns list of (a, b)."""
    pts = list(dict.fromkeys(points))
    inn, edges = {pts[0]}, []
    while len(inn) < len(pts):
        a, b = min(((a, b) for a in inn for b in pts if b not in inn),
                   key=lambda e: (abs(e[0][0] - e[1][0]) + abs(e[0][1] - e[1][1]), e))
        edges.append((a, b))
        inn.add(b)
    return edges


def route_all(order):
    """Each net becomes pin-to-pin insulated wires (MST edges). A wire may cross
    other wires but never passes over another net's pad; LV wires keep CLEAR
    holes from every mains hole; mains wires stay in MAINS_ZONE."""
    import heapq
    owner = pin_owner()
    used = {}            # hole -> set of nets whose wire passes through
    mains_pts = [xy for xy, n in owner.items() if n in MAINS]
    wires = {n: [] for n in NETS}

    def ok(n, xy, ends):
        x, y = xy
        if not (0 <= x < W and 0 <= y < H):
            return False
        o = owner.get(xy)
        if o is not None and o != "__nc__" and xy not in ends:
            return False                     # never run over another connected pad
        if n in MAINS:
            return MAINS_ZONE(x, y) or xy in ends
        if MAINS_ZONE(x, y):
            return False
        return all((x - a) ** 2 + (y - b) ** 2 >= CLEAR ** 2 for a, b in mains_pts)

    for n in order:
        pts = [PLACE[m] for m in NETS[n][1]]
        for a, b in mst(pts):
            ends = {a, b}
            dist = {(a, None): 0}
            prev = {}
            pq = [(0, a, None)]
            goal = None
            while pq:
                d, c, dr = heapq.heappop(pq)
                if d > dist.get((c, dr), 1e9):
                    continue
                if c == b:
                    goal = (c, dr)
                    break
                for nd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nb = (c[0] + nd[0], c[1] + nd[1])
                    if not ok(n, nb, ends):
                        continue
                    cost = 1 + (2 if dr is not None and nd != dr else 0)
                    if owner.get(nb) == "__nc__":
                        cost += 4                      # passing over an unused pin
                    others = used.get(nb, set()) - {n}
                    if others:
                        cost += 12 * len(others)      # crossing another wire
                    key = (nb, nd)
                    if d + cost < dist.get(key, 1e9):
                        dist[key] = d + cost
                        prev[key] = (c, dr)
                        heapq.heappush(pq, (d + cost, nb, nd))
            if goal is None:
                raise RuntimeError(f"cannot route {n} {a}->{b}")
            path, k = [], goal
            while k in prev:
                path.append(k[0])
                k = prev[k]
            path.append(a)
            path.reverse()
            for c in path[1:-1]:
                used.setdefault(c, set()).add(n)
            wires[n].append(path)
    return wires


def score(wires):
    cells = {}
    for n, ps in wires.items():
        for p in ps:
            for c in p[1:-1]:
                cells.setdefault(c, set()).add(n)
    crossings = sum(len(v) - 1 for v in cells.values() if len(v) > 1)
    length = sum(len(p) - 1 for ps in wires.values() for p in ps)
    bends = sum(len(runs(p)) - 1 for ps in wires.values() for p in ps)
    return crossings, bends, length


def best_layout(tries=300):
    nets = list(NETS)
    rnd = random.Random(7)
    best = None
    for t in range(tries):
        order = sorted(nets, key=lambda n: (n not in MAINS, rnd.random()))
        w = route_all(order)
        sc = score(w)
        if best is None or sc < best[0]:
            best = (sc, order, w)
    return best


if __name__ == "__main__":
    (crossings, bends, length), order, wires = best_layout(int(sys.argv[2]) if len(sys.argv) > 2 else 300)
    data = {
        "board": {"cols": W, "rows": H, "clearance_holes": CLEAR, "mains_rect": list(MAINS_RECT)},
        "pins": [{"part": p, "pin": pin, "hole": hole(xy), "x": xy[0], "y": xy[1]} for (p, pin), xy in PLACE.items()],
        "bodies": {k: {"x1": v[0], "y1": v[1], "x2": v[2], "y2": v[3], "label": v[4], "under_module": k in UNDER_MODULE} for k, v in BODIES.items()},
        "nets": {},
    }
    pin_at = {xy: f"{p}.{pin}" for (p, pin), xy in PLACE.items()}
    for n in NETS:
        ws = []
        for path in wires[n]:
            corners = [path[0]] + [b for a, b in runs(path)]
            ws.append({"from": pin_at[path[0]], "to": pin_at[path[-1]], "from_hole": hole(path[0]), "to_hole": hole(path[-1]),
                       "path": [list(c) for c in corners], "holes": len(path) - 1})
        data["nets"][n] = {"mains": n in MAINS, "members": [f"{p}.{pin}" for p, pin in NETS[n][1]], "wires": ws}
    json.dump(data, open(sys.argv[1], "w"), indent=1)
    print(f"wires={sum(len(v) for v in wires.values())} crossings={crossings} bends={bends} length={length} holes")
