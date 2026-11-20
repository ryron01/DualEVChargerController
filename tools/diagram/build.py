"""Regenerate docs/bench-wiring.svg (and .png if rsvg-convert is installed).

Usage, from the repo root:
    python tools/diagram/build.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent.parent / "docs"

standalone_css = '''<style>
.w{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:2}
.heavy{stroke-width:3.6}
.hot{stroke:#d23b2a}.neu{stroke:#7c8794}.gnd_ac{stroke:#2f9e44}.ctl{stroke:#c98a00;stroke-dasharray:5 3}
.v5{stroke:#d23b2a}.gndl{stroke:#2b2d31}.gndw{stroke:#f8f9fa}.casing{stroke:#868e96;stroke-width:4}.v33{stroke:#e8590c}.tx{stroke:#1c7ed6}.rx{stroke:#0ca5a0}.sda{stroke:#1c7ed6}.scl{stroke:#e0a800}.i5{stroke-dasharray:6 3}.relay{stroke:#e0a800}.sw1{stroke:#0ca5a0}.sw2{stroke:#1c7ed6}
.rail{stroke-width:4}
.dot.v5{fill:#d23b2a}.dot.gndl{fill:#2b2d31}.dot.gndw{fill:#f8f9fa;stroke:#868e96}.dot.v33{fill:#e8590c}.dot.tx{fill:#1c7ed6}.dot.rx{fill:#0ca5a0}
text{font-family:"IBM Plex Sans","Segoe UI",Helvetica,Arial,sans-serif}
.lbl{font-size:12px;fill:#1b211d}
.cname{font-size:14px;font-weight:600}.cname2{font-size:14px;font-weight:600;fill:#1b211d}.cnamew{font-size:14px;font-weight:600;fill:#fff}
.csub{font-size:11px}.csubw{font-size:11px;fill:#dfe9e2}
.pin{font-family:Menlo,Consolas,monospace;font-size:10px;fill:#33322d}.pinw{font-family:Menlo,Consolas,monospace;font-size:10px;fill:#fff}
.railt{font-family:Menlo,Consolas,monospace;font-size:10px;fill:#5b665f}
.zone{font-family:Menlo,Consolas,monospace;font-size:11px;fill:#5b665f}
.bb{fill:#f1efe6;stroke:#d2ccb9}.iso{stroke:#5b665f;stroke-dasharray:8 6;stroke-width:1.2}
</style><rect width="100%" height="100%" fill="#ffffff"/>'''

def main():
    raw_path = HERE / "_bench_wiring_raw.svg"
    subprocess.run([sys.executable, str(HERE / "gen_bench_wiring.py"), str(raw_path)], check=True)
    raw = raw_path.read_text()
    raw_path.unlink()
    svg = raw.replace("%%STYLE%%", standalone_css).replace("<svg ", '<svg width="1280" height="970" ', 1)
    out = DOCS / "bench-wiring.svg"
    out.write_text(svg)
    print(f"wrote {out}")
    if shutil.which("rsvg-convert"):
        png = DOCS / "bench-wiring.png"
        subprocess.run(["rsvg-convert", "-z", "2", str(out), "-o", str(png)], check=True)
        print(f"wrote {png}")
    else:
        print("rsvg-convert not found; skipped PNG (brew install librsvg)")
    # keep the interactive page in step: swap in the new drawing, styled by the page's own CSS variables
    page = DOCS / "bench-wiring.html"
    html = page.read_text()
    start = html.index('<div class="sheet">\n') + len('<div class="sheet">\n')
    end = html.index("</svg>", start) + len("</svg>")
    page.write_text(html[:start] + raw.replace("%%STYLE%%", "") + html[end:])
    print(f"updated {page}")


if __name__ == "__main__":
    main()
