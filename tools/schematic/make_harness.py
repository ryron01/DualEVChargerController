"""Build the signal-harness guide from the perfboard layout.

Usage: python make_harness.py layout.json OUTDIR
Writes OUTDIR/harness-guide.html (full document) and OUTDIR/harness-guide-body.html (page body for publishing).
Board-end hole names come from the layout, so they always match the soldering guide.
"""
import json
import os
import sys

layout = json.load(open(sys.argv[1]))
out = sys.argv[2]
hole = {f"{p['part']}.{p['pin']}": p["hole"] for p in layout["pins"]}

RED, BLK, GRN, YEL, BLU, WHT = "red", "black", "green", "yellow", "blue", "white"

# far-end pin order is the order printed on each module, top to bottom / left to right
HARNESSES = [
    {
        "id": "pzem1", "name": "PZEM 1", "wires": 4, "board": "J2", "edge": "right edge",
        "board_conn": "4-pin XH socket", "far": "PZEM 1 TTL header", "far_conn": "4-way housing to suit the PZEM's TTL header (Dupont if it has bare pins)",
        "far_order": ["VCC", "RX", "TX", "GND"], "est_cm": 9, "cut_cm": 15,
        "map": "pzem1",
        "pins": [("VCC", "VCC", RED, "+5 V"), ("RX", "RX", GRN, "ESP32 GPIO17 → PZEM"),
                 ("TX", "TX", YEL, "PZEM → diode D1 → GPIO16"), ("GND", "GND", BLK, "Ground")],
        "notes": ["The PZEM prints its supply pin as 5V; that is the VCC wire.", "Straight through: each wire goes to the pin with the same name. The board already crosses TX and RX, so don't swap them in the cable.",
                  "Address 0x01 (car 1)."],
        "test": "With the PZEM unplugged and the board powered, VCC to GND at the PZEM end reads about 5 V. TX at the PZEM end reads 0 V, because the diode blocks 3.3 V from flowing back out of the board.",
    },
    {
        "id": "pzem2", "name": "PZEM 2", "wires": 4, "board": "J3", "edge": "right edge",
        "board_conn": "4-pin XH socket", "far": "PZEM 2 TTL header", "far_conn": "4-way housing to suit the PZEM's TTL header (Dupont if it has bare pins)",
        "far_order": ["VCC", "RX", "TX", "GND"], "est_cm": 4, "cut_cm": 10,
        "map": "pzem2",
        "pins": [("VCC", "VCC", RED, "+5 V"), ("RX", "RX", GRN, "ESP32 GPIO17 → PZEM"),
                 ("TX", "TX", YEL, "PZEM → diode D2 → GPIO16"), ("GND", "GND", BLK, "Ground")],
        "notes": ["Straight through, same as PZEM 1.", "Address 0x02 (car 2)."],
        "test": "Same as PZEM 1: about 5 V from VCC to GND at the PZEM end with the board powered.",
    },
    {
        "id": "relay2", "name": "Relay 2", "wires": 3, "board": "J6", "edge": "bottom edge",
        "board_conn": "3-way screw terminal", "far": "Relay 2 control terminal", "far_conn": "ferrules or tinned ends into the screw terminal",
        "far_order": ["DC+", "DC-", "IN"], "est_cm": 10, "cut_cm": 16,
        "map": "relay2",
        "pins": [("DC+", "DC+", RED, "+5 V coil supply"), ("DC-", "DC-", BLK, "Ground"), ("IN", "IN", BLU, "ESP32 GPIO26")],
        "notes": ["The board terminal runs IN, DC−, DC+ left to right, the reverse of the relay module. Match by name, not by position.",
                  "Relay module trigger jumper on H."],
        "test": "Turn on Car 2 Switch in Home Assistant: IN reads about 3.3 V to DC−, and the relay clicks.",
    },
    {
        "id": "relay1", "name": "Relay 1", "wires": 3, "board": "J5", "edge": "bottom edge",
        "board_conn": "3-way screw terminal", "far": "Relay 1 control terminal", "far_conn": "ferrules or tinned ends into the screw terminal",
        "far_order": ["DC+", "DC-", "IN"], "est_cm": 14, "cut_cm": 20,
        "map": "relay1",
        "pins": [("DC+", "DC+", RED, "+5 V coil supply"), ("DC-", "DC-", BLK, "Ground"), ("IN", "IN", BLU, "ESP32 GPIO25")],
        "notes": ["Same reversed order as relay 2: match by name.", "Relay module trigger jumper on H."],
        "test": "Turn on Car 1 Switch in Home Assistant: IN reads about 3.3 V to DC−, and the relay clicks. Relay 2 should drop out.",
    },
    {
        "id": "lcd", "name": "LCD", "wires": 4, "board": "J4", "edge": "left edge",
        "board_conn": "4-pin XH socket", "far": "LCD backpack header (PCF8574)", "far_conn": "4-way Dupont female housing",
        "far_order": ["GND", "VCC", "SDA", "SCL"], "est_cm": None, "cut_cm": None,
        "map": "door",
        "pins": [("GND", "GND", BLK, "Ground"), ("VCC", "VCC", RED, "+5 V"),
                 ("SDA", "SDA", BLU, "5 V I2C data, from level shifter HV1"), ("SCL", "SCL", YEL, "5 V I2C clock, from level shifter HV2")],
        "notes": ["Straight through by name. These are the 5 V side of the level shifter, which is correct for the backpack.",
                  "Goes to the door: measure with the door fully open, and add a loop at the hinge so the cable bends there rather than at the connectors."],
        "test": "With the LCD unplugged and the board powered, VCC to GND at the LCD end reads about 5 V. Plug in, power up: the ESPHome log's I2C scan finds 0x27.",
    },
    {
        "id": "buttons", "name": "Panel buttons", "wires": 3, "board": "J7", "edge": "left edge",
        "board_conn": "3-pin XH socket", "far": "Two momentary buttons on the door", "far_conn": "solder or spade terminals on the buttons",
        "far_order": ["Car 1 button", "Car 2 button", "GND (both buttons)"], "est_cm": None, "cut_cm": None,
        "map": "door",
        "pins": [("SW1", "Car 1 button", GRN, "ESP32 GPIO32"), ("SW2", "Car 2 button", WHT, "ESP32 GPIO33"),
                 ("GND", "GND (both buttons)", BLK, "Common ground")],
        "notes": ["Each button has two legs: one to its SW wire, the other to GND. Run GND to one button and add a short black jumper to the other.",
                  "Use normally-open buttons. Bundle this cable with the LCD cable through the same hinge loop."],
        "test": "With the board powered and nothing pressed, SW1 and SW2 read about 3.3 V to GND. Pressing a button pulls its line to 0 V, and the ESPHome log shows Panel Button Car 1 or 2.",
    },
]

for h in HARNESSES:
    h["board_pins"] = [{"name": b, "hole": hole[f"{h['board']}.{b}"], "far": f, "color": c, "func": fn} for b, f, c, fn in h["pins"]]
    # board-side physical order follows the hole positions along the edge
    pts = {p["pin"]: (p["x"], p["y"]) for p in layout["pins"] if p["part"] == h["board"]}
    edge_vertical = len({x for x, _ in pts.values()}) == 1
    h["board_order"] = sorted(pts, key=lambda n: pts[n][1] if edge_vertical else pts[n][0])
    h["board_order_holes"] = [hole[f"{h['board']}.{n}"] for n in h["board_order"]]
    del h["pins"]

data = json.dumps(HARNESSES)

page = '''<title>EV Charger Harnesses</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
/* Layout: bench card per harness. Box map up top, then one card per cable in the order you'd build them, each with an end-to-end pin diagram, a wire table and a test. */
:root{
  --bg:#f3f2ee; --panel:#ffffff; --fg:#1c1f1d; --muted:#626a64; --line:#d9d7cf; --accent:#1f6f43; --hl:#fff3bf; --box:#e9e7e1; --boxline:#b9b5aa;
  --w-red:#d23b2a; --w-black:#2b2d31; --w-green:#2f9e44; --w-yellow:#e5b100; --w-blue:#1c7ed6; --w-white:#f8f9fa; --w-edge:#868e96;
  --display:"IBM Plex Sans Condensed","Arial Narrow",Arial,sans-serif;
  --body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#131614; --panel:#1b1f1c; --fg:#e6e9e4; --muted:#9ba39c; --line:#2e342f; --accent:#5ccf8a; --hl:#3b3418; --box:#202520; --boxline:#3c443d;
  --w-black:#c9ced3; --w-white:#f1f3f5; --w-edge:#adb5bd; color-scheme:dark}}
:root[data-theme="dark"]{--bg:#131614; --panel:#1b1f1c; --fg:#e6e9e4; --muted:#9ba39c; --line:#2e342f; --accent:#5ccf8a; --hl:#3b3418; --box:#202520; --boxline:#3c443d;
  --w-black:#c9ced3; --w-white:#f1f3f5; --w-edge:#adb5bd; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.55;margin:0}
.wrap{max-width:1100px;margin:0 auto;padding-block:28px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:22px}
header{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 20px}
h1{font-family:var(--display);font-weight:600;font-size:1.9rem;margin:0;text-wrap:balance}
h2{font-family:var(--display);font-weight:600;font-size:1.3rem;margin:0}
h3{font-family:var(--display);font-weight:600;font-size:1rem;margin:0}
.meta{font-family:var(--mono);font-size:.78rem;color:var(--muted);letter-spacing:.04em;text-transform:uppercase}
p{margin:0;max-width:75ch}
.muted{color:var(--muted)} .mono{font-family:var(--mono);font-size:.86em}
.top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:18px;align-items:start}
@media (max-width:820px){.top{grid-template-columns:minmax(0,1fr)}}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;min-width:0}
.rules{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px;font-size:.92rem}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.82rem;margin-top:10px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.sw{display:inline-block;width:22px;height:6px;border-radius:3px;border:1px solid var(--w-edge)}
.map svg{display:block;width:100%;height:auto}
.map .bx{fill:var(--box);stroke:var(--boxline)}
.map .mod{fill:var(--panel);stroke:var(--fg);stroke-width:1}
.map .brd{fill:#2f7d4a;stroke:#1d5631}
.map text{font-family:var(--body);font-size:12px;fill:var(--fg)}
.map .lbl-w{fill:#ffffff;font-weight:600}
.map .route{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;opacity:.9}
.map .route.dim{opacity:.18}
.map a{cursor:pointer}
.cards{display:flex;flex-direction:column;gap:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0;scroll-margin-top:12px}
.card.flash{box-shadow:0 0 0 2px var(--accent)}
.chead{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 16px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font:500 .76rem var(--mono);padding:3px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.chip.done{border-color:var(--accent);color:var(--accent)}
.ends{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;font-size:.88rem}
@media (max-width:560px){.ends{grid-template-columns:minmax(0,1fr)}}
.ends div{min-width:0}
.ends b{display:block;font-family:var(--mono);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:500}
.diag{overflow-x:auto}
.diag svg{display:block;min-width:420px;max-width:760px;width:100%;height:auto}
.diag text{font-family:var(--mono);font-size:12px;fill:var(--fg)}
.diag .hd{font-family:var(--body);font-weight:600;font-size:12px;fill:var(--muted)}
.diag .pin{fill:var(--panel);stroke:var(--fg);stroke-width:1}
.diag .hole{fill:var(--muted)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:.88rem}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:middle}
tbody tr:last-child td{border-bottom:none}
th{font-family:var(--mono);font-weight:500;font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
td:first-child,th:first-child{width:34px}
tr.done td:not(:first-child){opacity:.45;text-decoration:line-through}
input[type=checkbox]{width:17px;height:17px;accent-color:var(--accent)}
input[type=text]{font:500 .9rem var(--mono);width:5.5em;padding:3px 6px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
input:focus-visible,button:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.notes{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:4px;font-size:.88rem}
.test{font-size:.88rem;border-left:3px solid var(--accent);padding:6px 10px;border-radius:0;background:color-mix(in srgb,var(--accent) 8%,transparent)}
.test b{font-weight:600}
.len{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;font-size:.86rem;color:var(--muted)}
.len label{display:inline-flex;gap:6px;align-items:center}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
button.reset{font:500 .8rem var(--body);padding:5px 10px;border-radius:6px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}
</style>
<div class="wrap">
  <header>
    <h1>EV Charger Harnesses</h1>
    <span class="meta">Signal side · 6 cables · 21 wires</span>
  </header>
  <p>One card per cable, in build order: the short runs to the modules first, then the two door cables. Board-end hole names match the perfboard soldering guide (printed letter, then number). Lengths are rough, measured from your photo of the box; dry-fit each cable before you cut it.</p>

  <div class="top">
    <section class="panel map" aria-label="Box map">
      <h2>Box as mounted</h2>
      <p class="muted" style="font-size:.85rem;margin:4px 0 8px">Your photo turned a quarter turn left. Click a cable to jump to its card.</p>
      <svg viewBox="0 0 420 470" role="img" aria-label="Enclosure layout with harness routes">
        <rect class="bx" x="4" y="4" width="412" height="462" rx="10"/>
        <rect class="brd" x="20" y="20" width="180" height="118" rx="4"/>
        <text class="lbl-w" x="110" y="74" text-anchor="middle">Controller board</text>
        <text class="lbl-w" x="110" y="92" text-anchor="middle" style="font-weight:400;font-size:11px">ESP32 along the top</text>
        <rect class="mod" x="20" y="158" width="120" height="58" rx="4"/><text x="80" y="191" text-anchor="middle">PZEM 2</text>
        <rect class="mod" x="20" y="226" width="120" height="58" rx="4"/><text x="80" y="259" text-anchor="middle">PZEM 1</text>
        <rect class="mod" x="20" y="294" width="120" height="68" rx="4"/><text x="80" y="332" text-anchor="middle">Relay 2</text>
        <rect class="mod" x="20" y="372" width="120" height="68" rx="4"/><text x="80" y="410" text-anchor="middle">Relay 1</text>
        <rect class="mod" x="300" y="40" width="100" height="120" rx="4" style="stroke-dasharray:5 4"/>
        <text x="350" y="92" text-anchor="middle">Door</text>
        <text x="350" y="110" text-anchor="middle" class="muted" style="font-size:11px">LCD, buttons</text>
        <g id="routes"></g>
      </svg>
      <div class="legend" id="maplegend"></div>
    </section>
    <section class="panel">
      <h2>Rules for every cable</h2>
      <ol class="rules" style="margin-top:8px">
        <li>Match wires by pin name, never by position. Two of the board connectors run in the opposite order to the module they feed.</li>
        <li>Every cable is straight through. TX and RX are already crossed on the board, so no cable swaps them.</li>
        <li>Use 22–24 AWG stranded wire, and keep these cables clear of the mains wiring and CT leads, crossing them at right angles where they have to cross.</li>
        <li>Label both ends of each cable (PZEM 1, Relay 2…). The PZEM and relay cables look alike.</li>
        <li>Test each cable with a meter before plugging in a module. Every card ends with its test.</li>
      </ol>
      <div class="legend" aria-label="Wire colours">
        <span><i class="sw" style="background:var(--w-red)"></i>+5 V</span>
        <span><i class="sw" style="background:var(--w-black)"></i>Ground</span>
        <span><i class="sw" style="background:var(--w-green)"></i>To module / button 1</span>
        <span><i class="sw" style="background:var(--w-yellow)"></i>From module / SCL</span>
        <span><i class="sw" style="background:var(--w-blue)"></i>Relay IN / SDA</span>
        <span><i class="sw" style="background:var(--w-white)"></i>Button 2</span>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px;gap:10px;flex-wrap:wrap">
        <span class="mono muted" id="prog"></span>
        <button type="button" class="reset" id="reset">Clear all ticks</button>
      </div>
    </section>
  </div>

  <div class="cards" id="cards"></div>
</div>
<script>
var H = ''' + data + ''';
(function(){
  var COL={red:'var(--w-red)',black:'var(--w-black)',green:'var(--w-green)',yellow:'var(--w-yellow)',blue:'var(--w-blue)',white:'var(--w-white)'};
  var KEY='ev-harness-v1', st={ticks:{},len:{}};
  try{var s=JSON.parse(localStorage.getItem(KEY)||'null'); if(s&&s.ticks) st=s;}catch(e){}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(st));}catch(e){}}
  function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  // ----- box map routes (schematic, not to scale)
  var R={pzem2:{c:'#0b7285',d:'M140 187 H215 V113 H200'},pzem1:{c:'#1098ad',d:'M140 255 H228 V86 H200'},
    relay2:{c:'#2f9e44',d:'M140 330 H168 V138'},relay1:{c:'#66a80f',d:'M140 405 H150 V138'},
    lcd:{c:'#7048e8',d:'M20 40 H12 V12 H300 V70'},buttons:{c:'#ae3ec9',d:'M20 56 H8 V8 H310 V40'}};
  var g=document.getElementById('routes'), lg=document.getElementById('maplegend'), svgns='http://www.w3.org/2000/svg';
  H.forEach(function(h){
    var r=R[h.id]; if(!r) return;
    var a=document.createElementNS(svgns,'a'); a.setAttribute('href','#'+h.id); a.setAttribute('aria-label',h.name+' cable');
    var p=document.createElementNS(svgns,'path'); p.setAttribute('d',r.d); p.setAttribute('class','route'); p.setAttribute('stroke',r.c); p.setAttribute('data-h',h.id);
    var t=document.createElementNS(svgns,'title'); t.textContent=h.name+': '+h.board+' ('+h.edge+')'; p.appendChild(t);
    a.appendChild(p); g.appendChild(a);
    var s=document.createElement('a'); s.href='#'+h.id; s.style.color='inherit'; s.style.textDecoration='none';
    s.innerHTML='<span><i class="sw" style="background:'+r.c+'"></i>'+esc(h.name)+'</span>'; lg.appendChild(s);
  });
  // ----- cards
  var cards=document.getElementById('cards');
  H.forEach(function(h){
    var n=h.board_pins.length, rowH=30, top=34, hgt=top+n*rowH+8;
    // board side in physical order; far side in module order
    var bY={}, fY={};
    h.board_order.forEach(function(nm,i){bY[nm]=top+i*rowH+12;});
    h.far_order.forEach(function(nm,i){fY[nm]=top+i*rowH+12;});
    var svg='<svg viewBox="0 0 640 '+hgt+'" role="img" aria-label="'+esc(h.name)+' pin diagram">';
    svg+='<text class="hd" x="10" y="16">Board '+esc(h.board)+', '+esc(h.edge)+'</text>';
    svg+='<text class="hd" x="630" y="16" text-anchor="end">'+esc(h.far)+'</text>';
    h.board_order.forEach(function(nm,i){var y=bY[nm]; var bp=h.board_pins.filter(function(p){return p.name===nm;})[0];
      svg+='<circle class="hole" cx="18" cy="'+y+'" r="3"/><text x="28" y="'+(y+4)+'">'+esc(bp.hole)+'</text>';
      svg+='<rect class="pin" x="70" y="'+(y-10)+'" width="58" height="20" rx="3"/><text x="99" y="'+(y+4)+'" text-anchor="middle">'+esc(nm)+'</text>';});
    h.far_order.forEach(function(nm,i){var y=fY[nm];
      svg+='<rect class="pin" x="470" y="'+(y-10)+'" width="160" height="20" rx="3"/><text x="550" y="'+(y+4)+'" text-anchor="middle">'+esc(nm)+'</text>';});
    h.board_pins.forEach(function(p){var y1=bY[p.name], y2=fY[p.far];
      var stroke=COL[p.color], edge=(p.color==='white')?'<path d="M128 '+y1+' C300 '+y1+' 300 '+y2+' 470 '+y2+'" fill="none" stroke="var(--w-edge)" stroke-width="6" stroke-linecap="round"/>':'';
      svg+=edge+'<path d="M128 '+y1+' C300 '+y1+' 300 '+y2+' 470 '+y2+'" fill="none" stroke="'+stroke+'" stroke-width="4" stroke-linecap="round"><title>'+esc(p.name+' → '+p.far+': '+p.func)+'</title></path>';});
    svg+='</svg>';
    var rows=h.board_pins.map(function(p,i){var id=h.id+'-'+i;
      return '<tr data-id="'+id+'"><td><input type="checkbox" id="chk-'+id+'" aria-label="Done: '+esc(p.name)+'"></td>'+
        '<td><i class="sw" style="background:'+COL[p.color]+'"></i> '+esc(p.color)+'</td>'+
        '<td class="mono">'+esc(p.hole)+' · '+esc(p.name)+'</td><td class="mono">'+esc(p.far)+'</td><td>'+esc(p.func)+'</td></tr>';}).join('');
    var est=h.est_cm?('About '+h.est_cm+' cm in a straight line; suggested cut '+h.cut_cm+' cm with slack.'):'Measure to the door with it fully open, then add 10–15 cm for the hinge loop.';
    var c=document.createElement('section'); c.className='card'; c.id=h.id;
    c.innerHTML='<div class="chead"><h2>'+esc(h.name)+'</h2><div class="chips"><span class="chip">'+h.wires+' wires</span>'+
      '<span class="chip">'+esc(h.board)+' · '+esc(h.edge)+'</span><span class="chip" id="st-'+h.id+'">0 of '+h.wires+' done</span></div></div>'+
      '<div class="ends"><div><b>Board end</b>'+esc(h.board_conn)+', holes '+esc(h.board_order_holes.join(', '))+'</div><div><b>Far end</b>'+esc(h.far)+': '+esc(h.far_conn)+'</div></div>'+
      '<div class="diag">'+svg+'</div>'+
      '<div class="tbl"><table><thead><tr><th scope="col"><span class="sr">Done</span></th><th scope="col">Wire</th><th scope="col">Board end</th><th scope="col">Far end</th><th scope="col">Carries</th></tr></thead><tbody>'+rows+'</tbody></table></div>'+
      '<div class="len"><span>'+esc(est)+'</span><label for="len-'+h.id+'">Your cut length <input type="text" id="len-'+h.id+'" inputmode="decimal" placeholder="cm"></label></div>'+
      '<ul class="notes">'+h.notes.map(function(t){return '<li>'+esc(t)+'</li>';}).join('')+'</ul>'+
      '<div class="test"><b>Test before plugging in.</b> '+esc(h.test)+'</div>';
    cards.appendChild(c);
  });
  function progress(){
    var total=0, done=0;
    H.forEach(function(h){var d=0; h.board_pins.forEach(function(p,i){total++; if(st.ticks[h.id+'-'+i]){done++;d++;}});
      var chip=document.getElementById('st-'+h.id); chip.textContent=d+' of '+h.wires+' done'; chip.classList.toggle('done',d===h.wires);});
    document.getElementById('prog').textContent=done+' of '+total+' wires done';
  }
  document.querySelectorAll('tr[data-id]').forEach(function(r){
    var id=r.getAttribute('data-id'), cb=r.querySelector('input');
    if(st.ticks[id]){cb.checked=true;r.classList.add('done');}
    cb.addEventListener('change',function(){if(cb.checked) st.ticks[id]=true; else delete st.ticks[id]; r.classList.toggle('done',cb.checked); save(); progress();});
  });
  H.forEach(function(h){var el=document.getElementById('len-'+h.id); if(st.len[h.id]) el.value=st.len[h.id];
    el.addEventListener('input',function(){st.len[h.id]=el.value; save();});});
  document.getElementById('reset').addEventListener('click',function(){
    st.ticks={}; save();
    document.querySelectorAll('tr[data-id]').forEach(function(r){r.classList.remove('done'); r.querySelector('input').checked=false;});
    progress();
  });
  function flash(){var id=(location.hash||'').slice(1); var el=id&&document.getElementById(id);
    document.querySelectorAll('.map .route').forEach(function(p){p.classList.toggle('dim',!!el&&p.getAttribute('data-h')!==id);});
    if(el&&el.classList.contains('card')){el.classList.add('flash'); setTimeout(function(){el.classList.remove('flash');},1600);}}
  window.addEventListener('hashchange',flash); flash();
  progress();
})();
</script>
'''
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "harness-guide-body.html"), "w").write(page)
open(os.path.join(out, "harness-guide.html"), "w").write(
    '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + page.replace("</style>", "</style>\n</head><body>", 1) + "</body></html>\n")
print("harness guide written:", ", ".join(f"{h['name']} {h['board']} {h['board_order_holes']}" for h in HARNESSES))
