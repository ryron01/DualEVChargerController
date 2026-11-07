import sys

W, H = 1280, 970
HOP = 5

out = []          # component + text svg
wires_svg = []    # wire paths
drawn = []        # previously drawn segments: (x1,y1,x2,y2)
dots = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, cls="lbl", anchor="start", fill=None):
    f = f' fill="{fill}"' if fill else ""
    out.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{f}>{esc(s)}</text>')


def seg_cross(a, b):
    """a,b segments; return crossing point if perpendicular and interior to both."""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ah = ay1 == ay2
    bh = by1 == by2
    if ah == bh:
        return None
    if ah:
        hx1, hx2, hy = min(ax1, ax2), max(ax1, ax2), ay1
        vx, vy1, vy2 = bx1, min(by1, by2), max(by1, by2)
    else:
        hx1, hx2, hy = min(bx1, bx2), max(bx1, bx2), by1
        vx, vy1, vy2 = ax1, min(ay1, ay2), max(ay1, ay2)
    if hx1 + 0.5 < vx < hx2 - 0.5 and vy1 + 0.5 < hy < vy2 - 0.5:
        return (vx, hy)
    return None


def wire(cls, pts, hop=True):
    d = f"M{pts[0][0]} {pts[0][1]}"
    segs = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        s = (x1, y1, x2, y2)
        cps = []
        if hop:
            for o in drawn:
                c = seg_cross(s, o)
                if c:
                    cps.append(c)
        if y1 == y2:  # horizontal
            sign = 1 if x2 > x1 else -1
            cps.sort(key=lambda p: p[0] * sign)
            for cx, cy in cps:
                d += f" L{cx - sign*HOP} {cy} A{HOP} {HOP} 0 0 {1 if sign > 0 else 0} {cx + sign*HOP} {cy}"
        else:
            sign = 1 if y2 > y1 else -1
            cps.sort(key=lambda p: p[1] * sign)
            for cx, cy in cps:
                d += f" L{cx} {cy - sign*HOP} A{HOP} {HOP} 0 0 {1 if sign > 0 else 0} {cx} {cy + sign*HOP}"
        d += f" L{x2} {y2}"
        segs.append(s)
    drawn.extend(segs)
    wires_svg.append(f'<path class="w {cls}" d="{d}"/>')


def dot(x, y, cls):
    dots.append(f'<circle class="dot {cls}" cx="{x}" cy="{y}" r="3.6"/>')

# ------------------------------------------------------------------ components

def pcb(x, y, w, h, fill="#2f7d4a", stroke="#1d5631", rx=6):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')


def holes(x, y, w, h, inset=9, col="#d9c27a"):
    for hx, hy in [(x+inset, y+inset), (x+w-inset, y+inset), (x+inset, y+h-inset), (x+w-inset, y+h-inset)]:
        out.append(f'<circle cx="{hx}" cy="{hy}" r="3.4" fill="none" stroke="{col}" stroke-width="1.4"/>')


def screw(x, y):
    out.append(f'<circle cx="{x}" cy="{y}" r="6.2" fill="#c9ccd1" stroke="#5c6168" stroke-width="1"/>')
    out.append(f'<line x1="{x-4}" y1="{y}" x2="{x+4}" y2="{y}" stroke="#5c6168" stroke-width="1.4"/>')


def pin(x, y):
    out.append(f'<rect x="{x-3.5}" y="{y-3.5}" width="7" height="7" fill="#d4b14a" stroke="#7a6320" stroke-width="0.8"/>')


def feed(x, y, w, h):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#e9e6dc" stroke="#8f8a7a" stroke-width="1.2"/>')
    # prongs on right side
    for py in (y+30, y+50):
        out.append(f'<rect x="{x+w}" y="{py-3}" width="16" height="6" fill="#b9bcc2" stroke="#6b6f76"/>')
    out.append(f'<circle cx="{x+w+10}" cy="{y+68}" r="5" fill="#b9bcc2" stroke="#6b6f76"/>')
    text(x+14, y+28, "Feed cord", "cname", fill="#2b2a26")
    text(x+14, y+46, "GFCI-protected", "csub", fill="#5a574d")
    text(x+14, y+62, "20 A circuit", "csub", fill="#5a574d")


def wago(x, y, w, h, ports, name, part):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#eef3f6" stroke="#8aa0ad" stroke-width="1.2"/>')
    lw = 12
    gap = (w - 16 - ports*lw) / max(ports-1, 1)
    for i in range(ports):
        lx = x + 8 + i*(lw+gap)
        out.append(f'<rect x="{lx}" y="{y-6}" width="{lw}" height="12" rx="2" fill="#f08a24" stroke="#a85a10" stroke-width="0.8"/>')
    text(x+w/2, y+h/2+3, name, "cname", "middle", fill="#1f2b33")
    text(x+w/2, y+h/2+16, part, "csub", "middle", fill="#4f6370")


def fuse(x, y, w, h):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#26292e" stroke="#000" stroke-width="1"/>')
    out.append(f'<rect x="{x+w/2-26}" y="{y+h/2-6}" width="52" height="12" rx="3" fill="#cfd8dc" stroke="#7b868c"/>')
    text(x+10, y+h/2+4, "1 A", "cname", fill="#ffffff")
    text(x+w-10, y+h/2+4, "fuse", "csub", "end", fill="#c7ccd2")


def relay(x, y, w, h, name):
    pcb(x, y, w, h)
    holes(x, y, w, h)
    # screw block on left edge
    out.append(f'<rect x="{x+2}" y="{y+16}" width="26" height="{h-32}" fill="#1b1d20" rx="2"/>')
    for i, lab in enumerate(["NO", "COM", "NC"]):
        sy = y + 30 + 30*i
        screw(x+15, sy)
        text(x+34, sy+4, lab, "pinw")
    # blue relay cube
    out.append(f'<rect x="{x+72}" y="{y+14}" width="100" height="{h-28}" rx="4" fill="#2f6fd0" stroke="#1d4a8f"/>')
    text(x+122, y+h/2-10, name, "cnamew", "middle")
    text(x+122, y+h/2+8, "SONGLE", "csubw", "middle")
    text(x+122, y+h/2+22, "SLA-05VDC 30 A", "csubw", "middle")
    # control terminal on right edge
    out.append(f'<rect x="{x+w-24}" y="{y+18}" width="22" height="{h-36}" fill="#35b36b" stroke="#1d6b3d" rx="2"/>')
    for i, lab in enumerate(["DC+", "DC−", "IN"]):
        sy = y + 30 + 30*i
        screw(x+w-13, sy)
        text(x+w-30, sy+4, lab, "pinw", "end")


def ct(cx, cy, name):
    out.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="#2a2c30" stroke-width="13"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="#45484e" stroke-width="1"/>')
    text(cx-34, cy+4, name, "cname2", "end")


def outlet(x, y, w, h, name):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f1ede1" stroke="#9b9481" stroke-width="1.2"/>')
    # face
    fx, fy = x+w-62, y+h/2
    out.append(f'<rect x="{fx-26}" y="{fy-34}" width="52" height="68" rx="16" fill="#e4dfcf" stroke="#a9a28d"/>')
    out.append(f'<rect x="{fx-13}" y="{fy-18}" width="4" height="15" fill="#3b3a35"/>')
    out.append(f'<rect x="{fx+9}" y="{fy-18}" width="4" height="15" fill="#3b3a35"/>')
    out.append(f'<path d="M{fx-5} {fy+18} a5 5 0 0 1 10 0 v5 h-10 z" fill="#3b3a35"/>')
    # terminal screws: hot on top edge (brass), N + G on left edge
    out.append(f'<circle cx="{x+60}" cy="{y+12}" r="6" fill="#d4a43a" stroke="#8a6a1c"/>')
    text(x+72, y+16, "Hot", "pin")
    out.append(f'<circle cx="{x+12}" cy="{y+60}" r="6" fill="#d7dade" stroke="#80858c"/>')
    text(x+22, y+64, "N", "pin")
    out.append(f'<circle cx="{x+12}" cy="{y+90}" r="6" fill="#3fa65a" stroke="#22663a"/>')
    text(x+22, y+94, "G", "pin")
    text(x+w-8, y-7, name, "cname2", "end")


def pzem(x, y, w, h, name, addr):
    pcb(x, y, w, h, fill="#1f8a4c", stroke="#14592f")
    holes(x, y, w, h)
    # 4 screw terminal block on top edge (N L CT CT)
    out.append(f'<rect x="{x+104}" y="{y+2}" width="106" height="24" fill="#38c27a" stroke="#1d6b3d" rx="2"/>')
    for i, lab in enumerate(["N", "L", "CT", "CT"]):
        sx = x + 120 + 25*i
        screw(sx, y+14)
        text(sx, y+40, str(i+1), "pinw", "middle")
        text(sx, y+52, lab, "pinw", "middle")
    # header on bottom edge
    out.append(f'<rect x="{x+44}" y="{y+h-22}" width="152" height="20" fill="#f2f2ef" stroke="#a7a7a0" rx="2"/>')
    for i, lab in enumerate(["VCC", "RX", "TX", "GND"]):
        px = x + 60 + 40*i
        pin(px, y+h-8)
        text(px, y+h-28, lab, "pinw", "middle")
    text(x+14, y+24, name, "cnamew")
    text(x+14, y+40, "004T-100A V4.0", "csubw")
    text(x+14, y+56, f"addr {addr}", "csubw")


def hlk(x, y, w, h):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#1d1f22" stroke="#000"/>')
    text(x+w/2, y+30, "HLK-PM01", "cnamew", "middle")
    text(x+w/2, y+45, "120 VAC → 5 V", "csubw", "middle")
    for px, lab in [(x+50, "AC"), (x+110, "AC")]:
        pin(px, y)
        text(px, y+13, lab, "pinw", "middle")
    for px, lab in [(x+50, "−Vo"), (x+110, "+Vo")]:
        pin(px, y+h)
        text(px, y+h-6, lab, "pinw", "middle")


def esp32(x, y, w, h, top_pins, left_pins):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#16181b" stroke="#000"/>')
    # module can
    out.append(f'<rect x="{x+w-170}" y="{y+30}" width="120" height="80" rx="3" fill="#b9bec4" stroke="#7d838a"/>')
    text(x+w-110, y+66, "WROOM-32U", "csub", "middle", fill="#2c3036")
    text(x+w-110, y+82, "u.FL antenna", "csub", "middle", fill="#2c3036")
    out.append(f'<circle cx="{x+w-36}" cy="{y+70}" r="7" fill="#d4b14a" stroke="#7a6320"/>')
    out.append(f'<rect x="{x+60}" y="{y+h-2}" width="26" height="14" rx="3" fill="#9aa0a6"/>')
    text(x+73, y+h+26, "USB", "zone", "middle")
    text(x+90, y+66, "ESP32 DevKitC", "cnamew")
    text(x+90, y+82, "external antenna", "csubw")
    for px, lab in top_pins:
        pin(px, y)
        text(px, y+20, lab, "pinw", "middle")
    for py, lab in left_pins:
        pin(x, py)
        text(x+10, py+4, lab, "pinw")


def lcd(x, y, w, h):
    pcb(x, y, w, h, fill="#2f7d4a", stroke="#1d5631")
    out.append(f'<rect x="{x+86}" y="{y+16}" width="{w-140}" height="{h-32}" rx="3" fill="#24357a" stroke="#141f4a"/>')
    out.append(f'<rect x="{x+96}" y="{y+28}" width="{w-160}" height="{h-56}" fill="#3550b8"/>')
    text(x+86+(w-140)/2, y+h/2+4, "1602 LCD", "cnamew", "middle")
    # backpack header: pins on right edge
    for py, lab in [(y+20, "GND"), (y+40, "VCC"), (y+60, "SDA"), (y+80, "SCL")]:
        pin(x+w, py)
    text(x+14, y+20, "PCF8574", "csubw")
    text(x+14, y+34, "I2C 0x27", "csubw")
    for py, lab in [(y+20, "GND"), (y+40, "VCC"), (y+60, "SDA"), (y+80, "SCL")]:
        text(x+w-12, py+4, lab, "pinw", "end")


def switches(x, y, w, h):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#e9ecef" stroke="#8d949b" stroke-width="1.2"/>')
    text(x+w/2, y+20, "Panel switches", "cname", "middle", fill="#1f2328")
    for i, lab in enumerate(["Car 1", "Car 2"]):
        sy = y + 44 + 26*i
        out.append(f'<circle cx="{x+30}" cy="{sy}" r="3" fill="#495057"/>')
        out.append(f'<line x1="{x+30}" y1="{sy}" x2="{x+52}" y2="{sy-8}" stroke="#495057" stroke-width="1.6"/>')
        out.append(f'<circle cx="{x+58}" cy="{sy}" r="3" fill="#495057"/>')
        text(x+70, sy+4, lab, "csub", fill="#3a4047")
    pin(x, y+44); pin(x, y+70); pin(x+75, y)


def shifter(x, y, w, h):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#1b4f9c" stroke="#0f3268" stroke-width="1.2"/>')
    text(x+w/2, y+42, "Level shifter", "cnamew", "middle")
    text(x+w/2, y+57, "BSS138, 4-ch", "csubw", "middle")
    for px, lab in [(x+20, "HV"), (x+55, "GND"), (x+130, "LV")]:
        pin(px, y)
        text(px, y+16, lab, "pinw", "middle")
    for py, lab in [(y+50, "HV1"), (y+70, "HV2")]:
        pin(x, py)
        text(x+8, py+4, lab, "pinw")
    for py, lab in [(y+50, "LV1"), (y+70, "LV2")]:
        pin(x+w, py)
        text(x+w-8, py+4, lab, "pinw", "end")


def rails(x1, x2):
    out.append(f'<rect x="{x1-12}" y="678" width="{x2-x1+58}" height="60" rx="4" class="bb"/>')
    text(x2+8, 694, "+5V", "railt")
    text(x2+8, 712, "GND", "railt")
    text(x2+8, 730, "+3V3", "railt")

# ------------------------------------------------------------------ layout
AX, BX = 330, 780

# isolation boundary
out.append('<line x1="20" y1="642" x2="1260" y2="642" class="iso"/>')
text(1258, 634, "120 VAC side", "zone", "end")
text(1258, 658, "Low-voltage side", "zone", "end")

feed(80, 40, 150, 80)
wago(80, 160, 150, 40, 5, "L bus", "Wago 221-415")
fuse(80, 225, 150, 34)
wago(80, 285, 150, 40, 5, "L tap", "Wago 221-415")
wago(80, 360, 150, 40, 5, "N bus", "Wago 221-415")
wago(80, 425, 150, 40, 5, "N tap", "Wago 221-415")
wago(80, 500, 150, 40, 3, "Ground bus", "Wago 221-413")

for ox, n in [(AX, "A"), (BX, "B")]:
    relay(ox, 40, 230, 120, f"Relay {n}")
    outlet(ox, 290, 160, 110, f"Outlet {n}")
    pzem(ox, 490, 230, 110, f"PZEM {n}", "0x01" if n == "A" else "0x02")
    ct(ox+60, 225, f"CT {n}")

hlk(80, 606, 150, 68)
rails(260, 1210)
esp32(620, 790, 420, 140,
      [(640, "G25"), (700, "G16"), (740, "G17"), (800, "G26"), (970, "5V"), (995, "GND"), (1020, "3V3")],
      [(880, "G22"), (900, "G23")])
lcd(60, 820, 280, 100)
shifter(400, 830, 150, 90)
out.append('<rect x="1040" y="855" width="0" height="0"/>')
switches(1100, 830, 150, 96)
for py, lab in [(874, "G32"), (900, "G33")]:
    pin(1040, py)
    text(1030, py+4, lab, "pinw", "end")

# ------------------------------------------------------------------ wires (order matters for hops)
# breadboard rails first
wire("v5 rail", [(260, 690), (1210, 690)], hop=False)
wire("gnd rail", [(260, 708), (1210, 708)], hop=False)
wire("v33 rail", [(260, 726), (1210, 726)], hop=False)

# feed to buses
wire("hot heavy", [(80, 100), (60, 100), (60, 180), (80, 180)])
wire("neu heavy", [(80, 80), (45, 80), (45, 380), (80, 380)])
wire("gnd_ac heavy", [(80, 60), (30, 60), (30, 520), (80, 520)])
# bus to fuse to tap, n bus to n tap
wire("hot", [(155, 200), (155, 225)])
wire("hot", [(155, 259), (155, 285)])
wire("neu", [(155, 400), (155, 425)])

# L bus to relay COM
wire("hot heavy", [(230, 172), (270, 172), (270, 100), (AX, 100)])
wire("hot heavy", [(230, 188), (280, 188), (280, 24), (BX-15, 24), (BX-15, 100), (BX, 100)])
# relay NO -> through CT -> outlet hot
for ox in (AX, BX):
    wire("hot heavy", [(ox, 70), (ox-25, 70), (ox-25, 190), (ox+60, 190), (ox+60, 302)])
# outlet A neutral / ground
wire("neu heavy", [(230, 374), (290, 374), (290, 350), (AX+12, 350)])
wire("gnd_ac heavy", [(230, 514), (300, 514), (300, 380), (AX+12, 380)])
# outlet B neutral / ground via corridors
wire("neu heavy", [(230, 386), (276, 386), (276, 424), (BX-35, 424), (BX-35, 350), (BX+12, 350)])
wire("gnd_ac heavy", [(230, 526), (286, 526), (286, 412), (BX-45, 412), (BX-45, 380), (BX+12, 380)])
# CT leads
for ox in (AX, BX):
    wire("ctl", [(ox+82, 219), (ox+170, 219), (ox+170, 503)])
    wire("ctl", [(ox+82, 231), (ox+195, 231), (ox+195, 503)])
# fused taps to PZEMs
wire("hot", [(230, 298), (252, 298), (252, 436), (AX+145, 436), (AX+145, 503)])
wire("neu", [(230, 440), (262, 440), (262, 448), (AX+120, 448), (AX+120, 503)])
wire("hot", [(230, 312), (244, 312), (244, 460), (BX+145, 460), (BX+145, 503)])
wire("neu", [(230, 452), (268, 452), (268, 472), (BX+120, 472), (BX+120, 503)])
# taps to HLK
wire("hot", [(80, 318), (70, 318), (70, 594), (130, 594), (130, 606)])
wire("neu", [(230, 458), (238, 458), (238, 598), (190, 598), (190, 606)])

# HLK output to rails
wire("v5", [(190, 674), (190, 690), (260, 690)])
dot(260, 690, "v5")
wire("gndl", [(130, 674), (130, 708), (260, 708)])
dot(260, 708, "gndl")

# relay control
for ox, gpio_x, in_y in [(AX, 640, 772), (BX, 800, 770)]:
    rx = ox + 230
    wire("v5", [(rx-13, 70), (rx+40, 70), (rx+40, 690)])
    dot(rx+40, 690, "v5")
    wire("gndl", [(rx-13, 100), (rx+28, 100), (rx+28, 708)])
    dot(rx+28, 708, "gndl")
    wire("relay", [(rx-13, 130), (rx+16, 130), (rx+16, in_y), (gpio_x, in_y), (gpio_x, 790)])

# PZEM power
for ox in (AX, BX):
    wire("v33", [(ox+60, 592), (ox+60, 726)])
    dot(ox+60, 726, "v33")
    wire("gndl", [(ox+180, 592), (ox+180, 708)])
    dot(ox+180, 708, "gndl")
# UART: PZEM TX -> junction -> G16 ; G17 -> junction -> PZEM RX
wire("tx", [(AX+140, 592), (AX+140, 760), (700, 760)])
wire("tx", [(BX+140, 592), (BX+140, 760), (700, 760)])
wire("tx", [(700, 760), (700, 790)])
dot(700, 760, "tx")
wire("rx", [(AX+100, 592), (AX+100, 748), (740, 748)])
wire("rx", [(BX+100, 592), (BX+100, 748), (740, 748)])
wire("rx", [(740, 748), (740, 790)])
dot(740, 748, "rx")
# ESP power
wire("v5", [(970, 790), (970, 690)])
dot(970, 690, "v5")
wire("gndl", [(995, 790), (995, 708)])
dot(995, 708, "gndl")
wire("v33", [(1020, 790), (1020, 726)])
dot(1020, 726, "v33")
# LCD
wire("i2c5", [(340, 880), (400, 880)])
wire("i2c5", [(340, 900), (400, 900)])
wire("i2c", [(550, 880), (620, 880)])
wire("i2c", [(550, 900), (620, 900)])
wire("v5", [(340, 860), (358, 860), (358, 800), (300, 800), (300, 690)])
dot(300, 690, "v5")
wire("gndl", [(340, 840), (348, 840), (348, 812), (330, 812), (330, 708)])
dot(330, 708, "gndl")
# level shifter supplies
wire("v5", [(420, 830), (420, 690)])
dot(420, 690, "v5")
wire("gndl", [(455, 830), (455, 708)])
dot(455, 708, "gndl")
wire("v33", [(530, 830), (530, 726)])
dot(530, 726, "v33")

# panel switches (INPUT_PULLUP, switch to GND)
wire("sw", [(1040, 874), (1100, 874)])
wire("sw", [(1040, 900), (1070, 900), (1070, 900), (1100, 900)])
wire("gndl", [(1175, 830), (1175, 708)])
dot(1175, 708, "gndl")
# junction callout
out.append('<rect x="752" y="926" width="0" height="0"/>')

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="dt dd">%%STYLE%%
<title id="dt">Dual PZEM EV charger bench wiring</title>
<desc id="dd">120 VAC feed into Wago L, N and ground buses; each relay switches its outlet hot, which passes through a solid-core CT; both PZEM-004T V4 modules take fused L and N on terminals 1 and 2 and CT leads on 3 and 4; low-voltage side runs on breadboard rails from an HLK-PM01, with both PZEMs sharing one UART to the ESP32 and an I2C LCD behind a 3.3 V to 5 V level shifter.</desc>
{''.join(out[:1])}
{''.join(wires_svg)}
{''.join(out[1:])}
{''.join(dots)}
</svg>'''

# components should sit above wires (wires end at their edges); re-order: wires first then components then dots
svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="dt dd">%%STYLE%%
<title id="dt">Dual PZEM EV charger bench wiring</title>
<desc id="dd">120 VAC feed into Wago L, N and ground buses; each relay switches its outlet hot, which passes through a solid-core CT; both PZEM-004T V4 modules take fused L and N on terminals 1 and 2 and CT leads on 3 and 4; low-voltage side runs on breadboard rails from an HLK-PM01, with both PZEMs sharing one UART to the ESP32 and an I2C LCD behind a 3.3 V to 5 V level shifter.</desc>
<g class="comp-under">{''.join(o for o in out if 'class="bb"' in o or 'class="iso"' in o)}</g>
<g class="wires">{''.join(wires_svg)}</g>
<g class="comps">{''.join(o for o in out if 'class="bb"' not in o and 'class="iso"' not in o)}</g>
<g>{''.join(dots)}</g>
</svg>'''
open(sys.argv[1], "w").write(svg)
