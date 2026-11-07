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
.v5{stroke:#c2255c}.gndl{stroke:#343a40}.v33{stroke:#e07d00}.tx{stroke:#1971c2}.rx{stroke:#0b7285}.i2c{stroke:#7048e8}.i2c5{stroke:#7048e8;stroke-dasharray:6 3}.relay{stroke:#a05a2c}.sw{stroke:#5f3dc4}
.rail{stroke-width:4}
.dot.v5{fill:#c2255c}.dot.gndl{fill:#343a40}.dot.v33{fill:#e07d00}.dot.tx{fill:#1971c2}.dot.rx{fill:#0b7285}
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


if __name__ == "__main__":
    main()
