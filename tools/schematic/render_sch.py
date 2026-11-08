"""Render a preview of the generated .sch (symbols, stubs, net labels) to PNG/SVG."""
import sys
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = ET.parse(sys.argv[1]).getroot()
lib = root.find(".//libraries/library")
symbols = {s.get("name"): s for s in lib.find("symbols")}
devsets = {d.get("name"): d for d in lib.find("devicesets")}
parts = {p.get("name"): p for p in root.find(".//parts")}
inst = {i.get("part"): (float(i.get("x")), float(i.get("y"))) for i in root.find(".//instances")}
MAINS_C, NET_C, SYM_C, PIN_C = "#c0392b", "#1f6f43", "#3a3f9e", "#6b6f76"

fig, ax = plt.subplots(figsize=(16, 13), dpi=110)
ax.set_aspect("equal")
ax.axis("off")

for name, part in parts.items():
    sym = symbols[devsets[part.get("deviceset")].find("gates/gate").get("symbol")]
    ox, oy = inst[name]
    for w in sym.findall("wire"):
        ax.plot([ox + float(w.get("x1")), ox + float(w.get("x2"))], [oy + float(w.get("y1")), oy + float(w.get("y2"))], color=SYM_C, lw=1.4)
    xs = [float(w.get("x1")) for w in sym.findall("wire")] + [float(w.get("x2")) for w in sym.findall("wire")]
    ys = [float(w.get("y1")) for w in sym.findall("wire")] + [float(w.get("y2")) for w in sym.findall("wire")]
    ax.text(ox + min(xs), oy + max(ys) + 1.0, name, fontsize=8, color=SYM_C, weight="bold")
    ax.text(ox + min(xs), oy + min(ys) - 2.6, part.get("value"), fontsize=6.5, color=SYM_C)
    for p in sym.findall("pin"):
        x, y = ox + float(p.get("x")), oy + float(p.get("y"))
        L = {"short": 2.54, "middle": 5.08}[p.get("length")]
        d = 1 if p.get("rot") == "R0" else -1
        ax.plot([x, x + d * L], [y, y], color=PIN_C, lw=1)
        ax.text(x + d * (L + 0.5), y, p.get("name"), fontsize=5.2, color=PIN_C, va="center", ha="left" if d > 0 else "right")

for net in root.find(".//nets"):
    nn = net.get("name")
    col = MAINS_C if net.get("class") == "1" else NET_C
    for seg in net.findall("segment"):
        for w in seg.findall("wire"):
            x1, y1, x2, y2 = (float(w.get(k)) for k in ("x1", "y1", "x2", "y2"))
            ax.plot([x1, x2], [y1, y2], color=col, lw=1.6)
            ax.plot([x1], [y1], "o", color=col, ms=2)
        for lb in seg.findall("label"):
            x, y = float(lb.get("x")), float(lb.get("y"))
            left = lb.get("rot") == "R180"
            ax.text(x + (-0.6 if left else 0.6), y, nn, fontsize=5.6, color=col, va="center", ha="right" if left else "left")

for t in root.find(".//plain"):
    if t.tag == "text":
        ax.text(float(t.get("x")), float(t.get("y")), t.text, fontsize=11 if float(t.get("size")) > 3 else 6.5, color="#333")

ax.autoscale()
x0, x1 = ax.get_xlim()
ax.set_xlim(x0 - 15, x1 + 5)
fig.tight_layout()
for out in sys.argv[2:]:
    fig.savefig(out, facecolor="white")
print("rendered", sys.argv[2:])
