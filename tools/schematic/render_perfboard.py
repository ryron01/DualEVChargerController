"""Render the perfboard layout as top/bottom SVGs and an interactive soldering guide.

Usage: python render_perfboard.py layout.json OUTDIR
Writes OUTDIR/perfboard-top.svg, OUTDIR/perfboard-bottom.svg, OUTDIR/perfboard-guide.html
"""
import json
import os
import sys
from html import escape

P = 22            # hole pitch in px
M = 34            # margin for labels
COLS = "ABCDEFGHIJKLMNOPQRSTUVWX"

NET_COLOR = {
    "AC_L": "#b23a12", "AC_N": "#1e3a8a",
    "+5V": "#d6336c", "GND": "#1f2328", "+3V3": "#e8590c",
    "PZEM_TX": "#0b7285", "PZEM1_TX": "#1098ad", "PZEM2_TX": "#15aabf", "PZEM_RX": "#5c7cfa",
    "RELAY1": "#2f9e44", "RELAY2": "#66a80f", "SW1": "#9c36b5", "SW2": "#cc5de8",
    "SDA_3V3": "#7048e8", "SCL_3V3": "#845ef7", "SDA_5V": "#ae3ec9", "SCL_5V": "#be4bdb",
}
STEP = {"AC_L": 1, "AC_N": 1, "+5V": 2, "GND": 2, "+3V3": 2}
STEP_NAMES = {1: "Mains wiring", 2: "Power and ground", 3: "Signals"}


def hole(x, y):
    return f"{COLS[x]}{y + 1}"


def px(x, y, mirror, W):
    return (M + ((W - 1 - x) if mirror else x) * P, M + y * P)


def svg(d, mirror):
    W, H = d["board"]["cols"], d["board"]["rows"]
    w, h = M * 2 + (W - 1) * P, M * 2 + (H - 1) * P
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
         f'class="pb {"bottom" if mirror else "top"}" role="img" aria-label="Perfboard {"bottom (wiring) side, mirrored" if mirror else "top (component) side"}">']
    o.append('<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             '<line x1="0" y1="0" x2="0" y2="6" stroke="#b42318" stroke-width="2" stroke-opacity="0.35"/></pattern></defs>')
    o.append(f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="8" fill="#d8c48f" stroke="#a8935c"/>')
    # mains zone
    x1, y1 = px(0, 0, mirror, W)
    x2, y2 = px(*d["board"]["mains_zone"], mirror, W)
    zx, zy = min(x1, x2) - P / 2, y1 - P / 2
    o.append(f'<rect x="{zx}" y="{zy}" width="{abs(x2 - x1) + P}" height="{y2 - y1 + P}" fill="url(#hatch)" stroke="#b42318" stroke-dasharray="5 4" rx="4"/>')
    # labels
    for x in range(W):
        cx, _ = px(x, 0, mirror, W)
        o.append(f'<text x="{cx}" y="{M - 16}" class="ax">{COLS[x]}</text>')
        o.append(f'<text x="{cx}" y="{h - M + 24}" class="ax">{COLS[x]}</text>')
    for y in range(H):
        _, cy = px(0, y, mirror, W)
        o.append(f'<text x="{M - 18}" y="{cy + 4}" class="ax">{y + 1}</text>')
        o.append(f'<text x="{w - M + 18}" y="{cy + 4}" class="ax">{y + 1}</text>')
    pins = {(p["x"], p["y"]): p for p in d["pins"]}
    net_of = {}
    for n, nd in d["nets"].items():
        for m in nd["members"]:
            net_of[m] = n
    # holes
    for x in range(W):
        for y in range(H):
            cx, cy = px(x, y, mirror, W)
            if (x, y) in pins:
                continue
            o.append(f'<circle cx="{cx}" cy="{cy}" r="4.2" fill="#c08a4a"/><circle cx="{cx}" cy="{cy}" r="1.8" fill="#4a3b22"/>')
    # top view: part bodies
    if not mirror:
        for name, b in d["bodies"].items():
            (bx1, by1), (bx2, by2) = px(b["x1"], b["y1"], False, W), px(b["x2"], b["y2"], False, W)
            mod = name in ("U1", "U2", "PS1")
            fill = "#1d2b53" if name == "U1" else "#2b2d31" if name == "PS1" else "#2052b8" if name == "U2" else "#f4f1e8"
            op = 0.22 if mod else 0.85
            o.append(f'<g class="body" data-part="{name}"><rect x="{min(bx1, bx2)}" y="{by1}" width="{abs(bx2 - bx1)}" height="{by2 - by1}" '
                     f'rx="4" fill="{fill}" fill-opacity="{op}" stroke="#2b2d31" stroke-width="1.2"/>'
                     f'<title>{escape(name)}: {escape(b["label"])}</title></g>')
    # wires
    for n, nd in d["nets"].items():
        col = NET_COLOR[n]
        for i, wdef in enumerate(nd["wires"]):
            pts = " ".join(f"{px(x, y, mirror, W)[0]},{px(x, y, mirror, W)[1]}" for x, y in wdef["path"])
            wid = f"w-{n}-{i}"
            if mirror:
                o.append(f'<polyline class="wire" data-w="{escape(wid)}" data-net="{escape(n)}" points="{pts}" fill="none" stroke="{col}" '
                         f'stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><title>{escape(n)}: {escape(wdef["from"])} to {escape(wdef["to"])}</title></polyline>')
            else:
                o.append(f'<polyline class="wire ghost" data-w="{escape(wid)}" data-net="{escape(n)}" points="{pts}" fill="none" stroke="{col}" '
                         f'stroke-width="1.6" stroke-dasharray="4 3" stroke-opacity="0.75"><title>{escape(n)}: {escape(wdef["from"])} to {escape(wdef["to"])}</title></polyline>')
    # pads on top of wires
    for (x, y), p in pins.items():
        cx, cy = px(x, y, mirror, W)
        key = f'{p["part"]}.{p["pin"]}'
        n = net_of.get(key)
        ring = NET_COLOR.get(n, "#7a6a4a")
        o.append(f'<g class="pad" data-net="{escape(n or "")}"><circle cx="{cx}" cy="{cy}" r="6" fill="#e3c27a" stroke="{ring}" stroke-width="{2.4 if n else 1}"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="2" fill="#3b2f1a"/><title>{escape(key)} at {hole(x, y)}{" (" + escape(n) + ")" if n else " (unused)"}</title></g>')
    # part labels (top view only)
    if not mirror:
        for name, b in d["bodies"].items():
            (bx1, by1) = px(b["x1"], b["y1"], False, W)
            (bx2, by2) = px(b["x2"], b["y2"], False, W)
            cx, cy = (bx1 + bx2) / 2, (by1 + by2) / 2
            dark = name in ("U1", "PS1")
            tx = cy if name not in ("U1", "PS1", "U2") else (by1 + 10 if name != "U1" else by2 + 4)
            o.append(f'<text x="{cx}" y="{tx}" class="plabel">{escape(name)}</text>')
    o.append('</svg>')
    return "\n".join(o)


def build(d, outdir):
    os.makedirs(outdir, exist_ok=True)
    top, bottom = svg(d, False), svg(d, True)
    css_svg = ('.ax{font:600 10px ui-monospace,Menlo,monospace;fill:#5a4a2a;text-anchor:middle}'
               '.plabel{font:700 11px system-ui,sans-serif;fill:#14161a;text-anchor:middle;paint-order:stroke;stroke:#f4f1e8;stroke-width:3px}')
    for name, s in (("perfboard-top.svg", top), ("perfboard-bottom.svg", bottom)):
        open(os.path.join(outdir, name), "w").write(s.replace(">", f"><style>{css_svg}</style>", 1).replace("<svg ", '<svg ', 1))

    pins = {(p["x"], p["y"]): p for p in d["pins"]}
    hole_of = {f'{p["part"]}.{p["pin"]}': hole(p["x"], p["y"]) for p in d["pins"]}
    rows = []
    for n, nd in d["nets"].items():
        step = STEP.get(n, 3)
        for i, w in enumerate(nd["wires"]):
            route = " → ".join(hole(x, y) for x, y in w["path"])
            rows.append((step, n, i, w, route))
    rows.sort(key=lambda r: (r[0], list(d["nets"]).index(r[1]), r[2]))

    def part_holes(part):
        return {p["pin"]: hole(p["x"], p["y"]) for p in d["pins"] if p["part"] == part}

    D1, D2, R1 = part_holes("D1"), part_holes("D2"), part_holes("R1")
    U1, U2, PS1 = part_holes("U1"), part_holes("U2"), part_holes("PS1")
    J = {k: part_holes(k) for k in ("J1", "J2", "J3", "J4", "J5", "J6", "J7")}

    def span(ph):
        hs = sorted(ph.values(), key=lambda h: (int(h[1:]), h[0]))
        return f"{hs[0]}–{hs[-1]}"

    place = [
        ("D1", "BAT43 Schottky", f"Cathode band at {D1['C']} (next to PZEM1 TX), anode at {D1['A']}"),
        ("D2", "BAT43 Schottky", f"Cathode band at {D2['C']} (next to PZEM2 TX), anode at {D2['A']}"),
        ("R1", "10 kΩ", f"{R1['1']} (3V3 side) to {R1['2']} (diode junction), standing or flat"),
        ("U1", "2 × 1×19 female headers for the ESP32", f"Inner row {U1['EXT_5V']}–{U1['3V3']} (5V end at {U1['EXT_5V']}, 3V3 at {U1['3V3']}); outer row {U1['CLK']}–{U1['GND3']}. USB faces the left edge."),
        ("U2", "2 × 1×6 female headers for the level shifter", f"HV row {U2['HV1']}–{U2['HV4']} (HV1 at {U2['HV1']}), LV row {U2['LV1']}–{U2['LV4']}"),
        ("J4", "1×4 header, LCD", f"GND {J['J4']['GND']}, VCC {J['J4']['VCC']}, SDA {J['J4']['SDA']}, SCL {J['J4']['SCL']}"),
        ("J2", "1×4 header, PZEM1", f"VCC {J['J2']['VCC']}, RX {J['J2']['RX']}, TX {J['J2']['TX']}, GND {J['J2']['GND']}"),
        ("J3", "1×4 header, PZEM2", f"VCC {J['J3']['VCC']}, RX {J['J3']['RX']}, TX {J['J3']['TX']}, GND {J['J3']['GND']}"),
        ("J5", "1×3 header, relay 1", f"DC+ {J['J5']['DC+']}, DC− {J['J5']['DC-']}, IN {J['J5']['IN']}"),
        ("J6", "1×3 header, relay 2", f"DC+ {J['J6']['DC+']}, DC− {J['J6']['DC-']}, IN {J['J6']['IN']}"),
        ("J7", "1×3 header, panel buttons", f"SW2 {J['J7']['SW2']}, SW1 {J['J7']['SW1']}, GND {J['J7']['GND']} (pin 1 = GND at the right end)"),
        ("J1", "2-way 5.08 mm screw terminal, AC in from the inline fuse", f"L {J['J1']['L']}, N {J['J1']['N']}"),
        ("PS1", "HLK-PM01", f"AC1 {PS1['AC1']}, AC2 {PS1['AC2']}, −Vo {PS1['-VO']}, +Vo {PS1['+VO']}. Its pins are 29.4 mm end to end and the holes 30.5 mm, so bend each pin out about 0.5 mm."),
    ]
    return top, bottom, rows, place


if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    top, bottom, rows, place = build(d, sys.argv[2])
    json.dump({"rows": [{"step": s, "net": n, "i": i, "from": w["from"], "to": w["to"], "fromHole": w["from_hole"],
                         "toHole": w["to_hole"], "route": r, "holes": w["holes"]} for s, n, i, w, r in rows],
               "place": place, "colors": NET_COLOR, "steps": STEP_NAMES},
              open(os.path.join(sys.argv[2], "guide-data.json"), "w"), indent=1)
    open(os.path.join(sys.argv[2], "top-inline.svg"), "w").write(top)
    open(os.path.join(sys.argv[2], "bottom-inline.svg"), "w").write(bottom)
    print("rendered", len(rows), "wires")
