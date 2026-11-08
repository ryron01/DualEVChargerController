"""Compose the interactive perfboard soldering guide from render_perfboard.py output.

Usage: python make_guide.py OUTDIR  (expects guide-data.json, top-inline.svg, bottom-inline.svg in OUTDIR)
Writes OUTDIR/perfboard-guide.html (page body for publishing; no <html>/<head> wrapper)
and OUTDIR/perfboard-guide-standalone.html (full document for the repo).
"""
import json
import os
import sys
from html import escape

out = sys.argv[1]
g = json.load(open(os.path.join(out, "guide-data.json")))
top = open(os.path.join(out, "top-inline.svg")).read()
bottom = open(os.path.join(out, "bottom-inline.svg")).read()
nwires = len(g["rows"])

legend = "".join(
    f'<button type="button" class="chip" data-net="{escape(n)}" aria-pressed="false"><i style="background:{c}"></i>{escape(n)}</button>'
    for n, c in g["colors"].items())

place_rows = "".join(
    f'<tr data-id="p-{escape(pid)}"><td><input type="checkbox" id="chk-p-{escape(pid)}" aria-label="Done: {escape(pid)}"></td>'
    f'<td class="mono strong">{escape(pid)}</td><td>{escape(what)}</td><td>{escape(where)}</td></tr>'
    for pid, what, where in g["place"])

wire_sections = []
for step, title in g["steps"].items():
    rs = [r for r in g["rows"] if str(r["step"]) == str(step)]
    body = "".join(
        f'<tr class="wrow" data-w="w-{escape(r["net"])}-{r["i"]}" data-net="{escape(r["net"])}" data-id="w-{escape(r["net"])}-{r["i"]}">'
        f'<td><input type="checkbox" id="chk-w-{escape(r["net"])}-{r["i"]}" aria-label="Done: {escape(r["from"])} to {escape(r["to"])}"></td>'
        f'<td><span class="sw" style="background:{g["colors"][r["net"]]}"></span><span class="mono">{escape(r["net"])}</span></td>'
        f'<td><span class="mono strong">{escape(r["fromHole"])}</span> <span class="muted">{escape(r["from"])}</span></td>'
        f'<td><span class="mono strong">{escape(r["toHole"])}</span> <span class="muted">{escape(r["to"])}</span></td>'
        f'<td class="mono route">{escape(r["route"])}</td></tr>'
        for r in rs)
    wire_sections.append(
        f'<h3>Step {int(step) + 1}: {escape(title)} <span class="count">{len(rs)} wires</span></h3>'
        f'<div class="tbl"><table><thead><tr><th scope="col"><span class="sr">Done</span></th><th scope="col">Net</th><th scope="col">From</th>'
        f'<th scope="col">To</th><th scope="col">Route on the bottom</th></tr></thead><tbody>{body}</tbody></table></div>')

page = f'''<title>EV Charger Perfboard</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
/* Layout: workbench reference. Header and how-to-read, both board views side by side, then a checklist per build step. */
:root{{
  --bg:#f4f2ec; --panel:#ffffff; --fg:#1d1f1b; --muted:#646a60; --line:#dcd8cc; --accent:#1f6f43; --warn:#a6340f; --hl:#fff3bf;
  --display:"IBM Plex Sans Condensed","Arial Narrow",Arial,sans-serif;
  --body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{
  --bg:#141613; --panel:#1c1f1b; --fg:#e7e9e2; --muted:#9ea49a; --line:#30352f; --accent:#5ccf8a; --warn:#f0a35a; --hl:#3b3418; color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#141613; --panel:#1c1f1b; --fg:#e7e9e2; --muted:#9ea49a; --line:#30352f; --accent:#5ccf8a; --warn:#f0a35a; --hl:#3b3418; color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.55;margin:0}}
.wrap{{max-width:1240px;margin:0 auto;padding-block:28px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:22px}}
header{{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 20px}}
h1{{font-family:var(--display);font-weight:600;font-size:1.9rem;margin:0;text-wrap:balance}}
h2{{font-family:var(--display);font-weight:600;font-size:1.25rem;margin:0 0 10px}}
h3{{font-family:var(--display);font-weight:600;font-size:1.05rem;margin:18px 0 8px;display:flex;gap:10px;align-items:baseline}}
.count{{font-family:var(--mono);font-size:.75rem;font-weight:400;color:var(--muted)}}
.meta{{font-family:var(--mono);font-size:.78rem;color:var(--muted);letter-spacing:.04em;text-transform:uppercase}}
p{{margin:0;max-width:75ch}}
.muted{{color:var(--muted)}} .mono{{font-family:var(--mono);font-size:.86em}} .strong{{font-weight:600}}
.notes{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.note{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.9rem;min-width:0}}
.note b{{font-weight:600}}
.note.warn{{border-color:color-mix(in srgb,var(--warn) 55%,var(--line))}}
.note.warn b{{color:var(--warn)}}
.views{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:16px}}
figure{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px;min-width:0}}
figcaption{{font-size:.85rem;color:var(--muted);margin-bottom:8px}}
figcaption b{{color:var(--fg);font-weight:600}}
.scroll{{overflow-x:auto}}
.scroll svg{{display:block;width:100%;height:auto;min-width:480px}}
.legend{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{font:500 .78rem var(--mono);display:inline-flex;align-items:center;gap:6px;padding:4px 9px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}}
.chip i{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.chip[aria-pressed="true"]{{border-color:var(--fg);box-shadow:inset 0 0 0 1px var(--fg)}}
.chip:focus-visible,input:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.tbl{{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:8px}}
table{{border-collapse:collapse;width:100%;font-size:.88rem}}
th,td{{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
tbody tr:last-child td{{border-bottom:none}}
th{{font-family:var(--mono);font-weight:500;font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
td:first-child,th:first-child{{width:34px}}
.route{{color:var(--muted);min-width:200px}}
.sw{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:middle}}
tr.wrow{{cursor:pointer}}
tr.wrow:hover td,tr.wrow.active td{{background:var(--hl)}}
tr.done td:not(:first-child){{opacity:.45;text-decoration:line-through}}
input[type=checkbox]{{width:17px;height:17px;accent-color:var(--accent)}}
.progress{{font-family:var(--mono);font-size:.82rem;color:var(--muted)}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
.tools{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}}
button.reset{{font:500 .8rem var(--body);padding:5px 10px;border-radius:6px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}}
ol.checks{{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;max-width:80ch}}
/* board drawing: fixed physical colors, shared by both themes */
svg.pb .ax{{font:600 10px var(--mono);fill:#5a4a2a;text-anchor:middle}}
svg.pb .plabel{{font:700 11px var(--body);fill:#14161a;text-anchor:middle;paint-order:stroke;stroke:#f4f1e8;stroke-width:3px}}
svg.pb .wire{{transition:opacity .15s}}
.views.focus svg.pb .wire{{opacity:.12}}
.views.focus svg.pb .wire.on{{opacity:1;stroke-width:5}}
.views.focus svg.pb .wire.ghost.on{{stroke-width:3;stroke-dasharray:none}}
@media (prefers-reduced-motion: reduce){{svg.pb .wire{{transition:none}}}}
</style>
<div class="wrap">
  <header>
    <h1>EV Charger Perfboard</h1>
    <span class="meta">24 × 30 plain perfboard · {nwires} wires · from the bench netlist</span>
  </header>
  <p>Parts go on the top. Every connection is an insulated wire on the bottom, soldered at both ends. Holes are named by column letter and row number, as on the board edges. The bottom view is mirrored, so it matches the board when you flip it left to right. Click a wire in the lists to find it on both views.</p>

  <div class="notes">
    <div class="note warn"><b>Mains zone.</b> The hatched area (columns A–I, rows 1–16) carries 120 V. Use insulated wire rated 300 V or more there, and run nothing else through it. Low-voltage parts and wires stay at least 10 mm from any mains hole.</div>
    <div class="note"><b>Wire.</b> 24–26 AWG insulated (silicone or PTFE) for low voltage; 20 AWG rated 300 V for mains. Wires may cross each other on the bottom; the routes shown avoid other nets' pads.</div>
    <div class="note"><b>Diodes.</b> The band (cathode) faces the PZEM header: D1 band at W12, D2 band at W17. Reversed diodes put 5 V on GPIO16 and block replies.</div>
    <div class="note"><b>Modules on headers.</b> The ESP32 and level shifter sit in female headers. Unused ESP32 pins still get a header socket; some wires pass under those joints on the bottom.</div>
  </div>

  <section>
    <div class="tools"><h2>Board views</h2><div class="legend" role="group" aria-label="Highlight a net">{legend}</div></div>
    <div class="views" id="views">
      <figure><figcaption><b>Top, component side.</b> Wires shown dashed, as if seen through the board.</figcaption><div class="scroll">{top}</div></figure>
      <figure><figcaption><b>Bottom, wiring side (mirrored).</b> Flip the board left to right to match.</figcaption><div class="scroll">{bottom}</div></figure>
    </div>
  </section>

  <section>
    <div class="tools"><h2>Step 1: Place and solder parts</h2><span class="progress" id="prog-p"></span></div>
    <div class="tbl"><table><thead><tr><th scope="col"><span class="sr">Done</span></th><th scope="col">Part</th><th scope="col">What</th><th scope="col">Holes</th></tr></thead><tbody id="place">{place_rows}</tbody></table></div>
    <p class="muted" style="margin-top:8px">Solder the lowest parts first: diodes, resistor, fuse, then headers and terminals, then the HLK-PM01.</p>
  </section>

  <section>
    <div class="tools"><h2>Wiring</h2><span class="progress" id="prog-w"></span><button type="button" class="reset" id="reset">Clear all ticks</button></div>
    {"".join(wire_sections)}
  </section>

  <section>
    <h2>Before the first power-up</h2>
    <ol class="checks">
      <li>With nothing plugged in, check for no continuity between J1 L or N and any low-voltage point: +5V, GND, 3V3.</li>
      <li>Check no continuity between +5V and GND, or between 3V3 and GND.</li>
      <li>Check continuity from each header pin to its ESP32 socket, using the wire list.</li>
      <li>Fit the fuse, power from the GFCI bench feed with the ESP32 and modules out, and measure 5 V at J4 VCC.</li>
      <li>Power off, fit the ESP32 and level shifter, power up and confirm the D1/D2 anode junction reads about 3.3 V.</li>
    </ol>
  </section>
</div>
<script>
(function(){{
  var KEY='ev-perfboard-ticks-v1', ticks={{}};
  try{{ticks=JSON.parse(localStorage.getItem(KEY)||'{{}}')||{{}};}}catch(e){{ticks={{}};}}
  function save(){{try{{localStorage.setItem(KEY,JSON.stringify(ticks));}}catch(e){{}}}}
  var rows=document.querySelectorAll('tr[data-id]');
  function progress(){{
    var p=document.querySelectorAll('#place tr'), w=document.querySelectorAll('tr.wrow');
    var pd=[].filter.call(p,function(r){{return r.classList.contains('done');}}).length;
    var wd=[].filter.call(w,function(r){{return r.classList.contains('done');}}).length;
    document.getElementById('prog-p').textContent=pd+' of '+p.length+' placed';
    document.getElementById('prog-w').textContent=wd+' of '+w.length+' wires done';
  }}
  rows.forEach(function(r){{
    var id=r.getAttribute('data-id'), cb=r.querySelector('input');
    if(ticks[id]){{cb.checked=true;r.classList.add('done');}}
    cb.addEventListener('click',function(ev){{ev.stopPropagation();}});
    cb.addEventListener('change',function(){{ticks[id]=cb.checked; if(!cb.checked) delete ticks[id]; r.classList.toggle('done',cb.checked); save(); progress();}});
  }});
  var views=document.getElementById('views');
  function focusSel(sel){{
    document.querySelectorAll('svg.pb .wire.on').forEach(function(e){{e.classList.remove('on');}});
    if(!sel){{views.classList.remove('focus');return;}}
    views.classList.add('focus');
    document.querySelectorAll('svg.pb .wire'+sel).forEach(function(e){{e.classList.add('on');}});
  }}
  var active=null;
  document.querySelectorAll('tr.wrow').forEach(function(r){{
    r.addEventListener('click',function(){{
      var w=r.getAttribute('data-w');
      document.querySelectorAll('tr.wrow.active').forEach(function(x){{x.classList.remove('active');}});
      document.querySelectorAll('.chip').forEach(function(c){{c.setAttribute('aria-pressed','false');}});
      if(active===w){{active=null;focusSel(null);return;}}
      active=w; r.classList.add('active'); focusSel('[data-w="'+w+'"]');
      views.scrollIntoView({{behavior:'smooth',block:'start'}});
    }});
  }});
  document.querySelectorAll('.chip').forEach(function(c){{
    c.addEventListener('click',function(){{
      var on=c.getAttribute('aria-pressed')!=='true';
      document.querySelectorAll('.chip').forEach(function(x){{x.setAttribute('aria-pressed','false');}});
      document.querySelectorAll('tr.wrow.active').forEach(function(x){{x.classList.remove('active');}});
      active=null;
      if(on){{c.setAttribute('aria-pressed','true');focusSel('[data-net="'+c.getAttribute('data-net')+'"]');}} else focusSel(null);
    }});
  }});
  document.getElementById('reset').addEventListener('click',function(){{
    ticks={{}}; save();
    rows.forEach(function(r){{r.classList.remove('done');r.querySelector('input').checked=false;}});
    progress();
  }});
  progress();
}})();
</script>
'''
open(os.path.join(out, "perfboard-guide.html"), "w").write(page)
standalone = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
              + page.replace("</style>", "</style>\n</head><body>", 1) + "</body></html>\n")
open(os.path.join(out, "perfboard-guide-standalone.html"), "w").write(standalone)
print("guide written")
