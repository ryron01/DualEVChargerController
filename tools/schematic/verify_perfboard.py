"""Independent checks on the perfboard layout JSON. Exits non-zero on any failure.

Uses the expected netlist from verify_sch.py (written from the bench wiring),
not the generator's netlist.
"""
import json
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("vs", os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_sch.py"))
src = open(spec.origin).read()
EXPECTED = {}
exec(src[src.index("EXPECTED = {"):src.index("MAINS = ")], {}, globals_ := {})
EXPECTED = globals_["EXPECTED"]
MAINS = {"AC_L", "AC_N"}
CLEAR = 3.0

d = json.load(open(sys.argv[1]))
W, H = d["board"]["cols"], d["board"]["rows"]
fails = []
fail = fails.append

# pins: unique holes, on the board
pin_at, where = {}, {}
for p in d["pins"]:
    xy = (p["x"], p["y"])
    key = f'{p["part"]}.{p["pin"]}'
    if not (0 <= xy[0] < W and 0 <= xy[1] < H):
        fail(f"{key} is off the board at {xy}")
    if xy in pin_at:
        fail(f"{key} and {pin_at[xy]} share hole {p['hole']}")
    pin_at[xy] = key
    where[key] = xy

net_of = {m: n for n, ms in EXPECTED.items() for m in ms}

# every expected member is placed
for n, ms in EXPECTED.items():
    for m in ms:
        if m not in where:
            fail(f"{n}: {m} not placed")
if set(d["nets"]) != set(EXPECTED):
    fail(f"net names differ: {sorted(set(d['nets']) ^ set(EXPECTED))}")


def cells(path):
    out = []
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        if x1 != x2 and y1 != y2:
            fail(f"diagonal run {(x1, y1)}->{(x2, y2)}")
        steps = max(abs(x2 - x1), abs(y2 - y1))
        for i in range(steps + (1 if (x2, y2) == tuple(path[-1]) else 0)):
            out.append((x1 + (x2 - x1) * i // max(steps, 1), y1 + (y2 - y1) * i // max(steps, 1)))
    return out


mains_holes = {where[m] for n in MAINS for m in EXPECTED[n]}
lv_holes = {}
joints = {}
for n, nd in d["nets"].items():
    parent = {m: m for m in EXPECTED.get(n, [])}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for w in nd["wires"]:
        path = [tuple(c) for c in w["path"]]
        a, b = pin_at.get(path[0]), pin_at.get(path[-1])
        for end, name in ((path[0], a), (path[-1], b)):
            if name is None or net_of.get(name) != n:
                fail(f"{n}: wire end at {end} is {name}, not a {n} pin")
            joints[end] = joints.get(end, 0) + 1
        if a in parent and b in parent:
            parent[find(a)] = find(b)
        cs = cells(path)
        for c in cs[1:-1]:
            if not (0 <= c[0] < W and 0 <= c[1] < H):
                fail(f"{n}: wire leaves the board at {c}")
            other = pin_at.get(c)
            if other and net_of.get(other) not in (None, n):
                fail(f"{n}: wire passes over {other} ({net_of.get(other)})")
            if other and net_of.get(other) == n:
                pass
        if n in MAINS:
            mains_holes.update(cs)
        else:
            for c in cs:
                lv_holes.setdefault(c, n)
    roots = {find(m) for m in parent}
    if len(roots) != 1:
        fail(f"{n}: not fully connected ({len(roots)} separate groups)")

# low-voltage pins also count as low-voltage holes
for key, xy in where.items():
    if net_of.get(key) not in MAINS:
        lv_holes.setdefault(xy, net_of.get(key, "unconnected"))
worst = min((math.dist(a, b), a, b) for a in lv_holes for b in mains_holes)
if worst[0] < CLEAR:
    fail(f"low voltage at {worst[1]} is {worst[0]:.2f} holes from mains at {worst[2]}")
for xy, k in joints.items():
    if k > 3:
        fail(f"{pin_at[xy]} has {k} wires soldered to it")

# top-side bodies must not overlap (modules on headers may overhang low parts)
b = d["bodies"]
names = list(b)
for i, p in enumerate(names):
    for q in names[i + 1:]:
        A, B = b[p], b[q]
        if A["under_module"] or B["under_module"]:
            continue
        if A["x1"] < B["x2"] and B["x1"] < A["x2"] and A["y1"] < B["y2"] and B["y1"] < A["y2"]:
            fail(f"bodies {p} and {q} overlap")

print(f"pins={len(where)} nets={len(d['nets'])} wires={sum(len(v['wires']) for v in d['nets'].values())} "
      f"min mains clearance={worst[0]:.2f} holes ({worst[0] * 2.54:.1f} mm)")
if fails:
    print("FAIL")
    for m in fails:
        print(" -", m)
    sys.exit(1)
print("PASS: every net connected as on the bench, no wire over another net's pad, mains clearance held")
