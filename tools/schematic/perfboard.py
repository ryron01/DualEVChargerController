"""Perfboard layout for the EV charger controller on a 24 x 30 hole plain perfboard.

Parts sit on top; every connection is a wire on the bottom running hole to hole
(orthogonal runs). Nets never share a hole. Mains nets stay in the top-left
mains zone and every low-voltage hole keeps 3 holes (7.6 mm) from any mains hole.
Where a net cannot be routed on the bottom without crossing, it gets an
insulated jumper on the top side.

Usage: python perfboard.py layout.json
"""
import json
import random
import sys
from collections import deque

sys.path.insert(0, __import__("os").path.dirname(__file__))
from gen_sch import NETS, ESP_LEFT, ESP_RIGHT_BOTTOM_UP  # same netlist as the schematic

W, H = 24, 30          # columns A..X, rows 1..30
MAINS = {n for n, (cls, _) in NETS.items() if cls == 1}
CLEAR = 3.0            # holes between mains and low voltage (7.62 mm)
MAINS_ZONE_MAX = (8, 6)  # columns A..I, rows 1..7
MAINS_ZONE = lambda x, y: x <= MAINS_ZONE_MAX[0] and y <= MAINS_ZONE_MAX[1]

# ------------------------------------------------------------------ placement
# board coordinates: x = column (0 = A), y = row (0 = row 1, top edge)
PLACE = {}
# ESP32 on female headers along the bottom, rotated so pads 1-19 form the inner row
# (row 20) and pads 20-38 the outer row (row 30). USB end at the left edge, antenna end right.
for k, nm in enumerate(ESP_LEFT, start=1):               # pad k
    PLACE[("U1", nm)] = (21 - k, 19)
for i, nm in enumerate(ESP_RIGHT_BOTTOM_UP):             # pad 20 + i
    PLACE[("U1", nm)] = (2 + i, 29)
PLACE.update({
    # mains block, top left
    ("J1", "L"): (1, 1), ("J1", "N"): (1, 3),
    ("PS1", "AC1"): (8, 3), ("PS1", "AC2"): (8, 5), ("PS1", "-VO"): (20, 1), ("PS1", "+VO"): (20, 7),
    # relay and switch headers in a row just above the ESP32's inner pin row
    ("J6", "DC+"): (6, 17), ("J6", "DC-"): (7, 17), ("J6", "IN"): (8, 17),
    ("J5", "DC+"): (10, 17), ("J5", "DC-"): (11, 17), ("J5", "IN"): (12, 17),
    ("J7", "SW2"): (13, 17), ("J7", "SW1"): (14, 17), ("J7", "GND"): (15, 17),
    # LCD header beside the level shifter's HV row
    ("J4", "GND"): (13, 9), ("J4", "VCC"): (13, 10), ("J4", "SDA"): (13, 11), ("J4", "SCL"): (13, 12),
    # PZEM headers on the right edge, diode-OR and pull-up beside them
    ("J2", "VCC"): (23, 9), ("J2", "RX"): (23, 10), ("J2", "TX"): (23, 11), ("J2", "GND"): (23, 12),
    ("J3", "VCC"): (23, 14), ("J3", "RX"): (23, 15), ("J3", "TX"): (23, 16), ("J3", "GND"): (23, 17),
    ("D1", "C"): (22, 11), ("D1", "A"): (22, 14),
    ("D2", "C"): (22, 16), ("D2", "A"): (22, 19),
    ("R1", "2"): (21, 14), ("R1", "1"): (21, 18),
})
for i, nm in enumerate(["HV1", "HV2", "HV", "GND@2", "HV3", "HV4"]):
    PLACE[("U2", nm)] = (15 + i, 9)
for i, nm in enumerate(["LV1", "LV2", "LV", "GND@1", "LV3", "LV4"]):
    PLACE[("U2", nm)] = (15 + i, 13)

# body outlines on top, in hole units (x1, y1, x2, y2, label)
BODIES = {
    "U1": (0.3, 18.4, 23.9, 29.6, "ESP32 DevKitC on female headers"),
    "PS1": (7.3, 0.0, 20.7, 7.95, "HLK-PM01"),
    "U2": (14.45, 8.4, 20.55, 13.6, "Level shifter"),
    "J1": (-0.5, 0.0, 2.5, 4.0, "AC in (from inline fuse)"),
    "J6": (5.5, 16.5, 8.5, 17.5, "Relay 2"), "J5": (9.5, 16.5, 12.5, 17.5, "Relay 1"), "J7": (12.5, 16.5, 15.5, 17.5, "Buttons"),
    "J4": (12.5, 8.5, 13.5, 12.5, "LCD"),
    "J2": (22.5, 8.5, 23.5, 12.5, "PZEM1"), "J3": (22.5, 13.5, 23.5, 17.5, "PZEM2"),
    "D1": (21.6, 11.7, 22.4, 13.3, "D1"), "D2": (21.6, 16.7, 22.4, 18.3, "D2"), "R1": (20.5, 14.7, 21.5, 17.3, "R1"),
}
UNDER_MODULE = set()


def colname(x):
    return "ABCDEFGHIJKLMNOPQRSTUVWX"[x]


def hole(p):
    return f"{colname(p[0])}{p[1] + 1}"


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
        "board": {"cols": W, "rows": H, "clearance_holes": CLEAR, "mains_zone": list(MAINS_ZONE_MAX)},
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
