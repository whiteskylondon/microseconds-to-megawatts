"""
Build docs/compute.html — the compute-layer view.

A focused deck.gl page for Layer 3 (research/ML compute): every data centre is
a 3D extruded column whose HEIGHT and orange-red COLOR encode disclosed power
(MW). Sites with no public MW still appear as dots, so absence stays visible.
HQ->data-centre arcs will layer on later (ArcLayer, same page).

Renderer: MapLibre GL basemap (CARTO Dark Matter, no token) + a deck.gl
MapboxOverlay, both from CDN — fine for a GitHub Pages page (no artifact CSP).

Reads data/compute_sites.csv (later: the deep firm_datacenters.csv). Usage:
    python pipeline/build_compute_view.py [--csv data/compute_sites.csv]
                                          [--out docs/compute.html]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DECK = "https://cdn.jsdelivr.net/npm/deck.gl@9.0.32/dist.min.js"
MAPLIBRE_JS = "https://cdn.jsdelivr.net/npm/maplibre-gl@4.5.0/dist/maplibre-gl.js"
MAPLIBRE_CSS = "https://cdn.jsdelivr.net/npm/maplibre-gl@4.5.0/dist/maplibre-gl.css"
BASEMAP = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"


def load(csv_path: Path) -> tuple[list, list]:
    df = pd.read_csv(csv_path, dtype=str).fillna("")
    df = df[(df.lat != "") & (df.lon != "")].copy()
    df["lat"] = df.lat.astype(float)
    df["lon"] = df.lon.astype(float)
    df["mw"] = pd.to_numeric(df.power_mw, errors="coerce")
    df["gpu"] = pd.to_numeric(df.get("gpu_count", ""), errors="coerce")

    note_col = "power_basis" if "power_basis" in df.columns else "capacity_note"

    def rec(r):
        note = getattr(r, note_col, "") or ""
        return {
            "lon": r.lon, "lat": r.lat,
            "firm": r.firm, "site": r.site_name, "city": r.city,
            "status": r.status,
            "mw": None if pd.isna(r.mw) else float(r.mw),
            "gpu": None if pd.isna(r.gpu) else int(r.gpu),
            "note": str(note)[:140],
        }

    points = [rec(r) for r in df.itertuples()]
    columns = [p for p in points if p["mw"]]
    return columns, points


def html(columns: list, points: list) -> str:
    data = json.dumps({"columns": columns, "points": points}, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Quant AI compute — megawatts</title>
<link href="{MAPLIBRE_CSS}" rel="stylesheet" />
<script src="{MAPLIBRE_JS}"></script>
<script src="{DECK}"></script>
<style>
  html, body {{ margin: 0; height: 100%; background: #0a0a0f; }}
  #map {{ position: absolute; inset: 0; }}
  .panel {{ position: absolute; z-index: 2; color: #e8e6e3;
    font: 13px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  #title {{ top: 14px; left: 16px; max-width: 340px; }}
  #title h1 {{ font-size: 16px; font-weight: 600; margin: 0 0 4px; }}
  #title p {{ margin: 0; color: #9a978f; font-size: 12px; }}
  #legend {{ bottom: 16px; left: 16px; background: rgba(16,16,22,0.78);
    border: 1px solid rgba(255,255,255,0.14); border-radius: 8px; padding: 10px 12px; }}
  #legend .bar {{ height: 9px; width: 180px; border-radius: 3px;
    background: linear-gradient(90deg, #fac775, #ef7f2a, #b2182b); margin: 5px 0 3px; }}
  #legend .row {{ display: flex; justify-content: space-between; font-size: 11px; color: #9a978f; }}
  #legend .note {{ margin-top: 7px; font-size: 11px; color: #9a978f; max-width: 210px; }}
  #legend .dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: #7f8a99; border: 1px solid rgba(255,255,255,0.5); vertical-align: 1px; margin-right: 3px; }}
  .deck-tooltip {{ font: 12px/1.45 -apple-system, sans-serif !important;
    background: rgba(16,16,22,0.92) !important; border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 6px !important; color: #e8e6e3 !important; }}
</style>
</head>
<body>
<div id="map"></div>
<div id="title" class="panel">
  <h1>The megawatts of quant AI</h1>
  <p>Each column is a firm's compute site — height &amp; colour = disclosed power (MW).
     Dots are sites with no public MW figure.</p>
</div>
<div id="legend" class="panel">
  <div style="font-weight:600; font-size:12px;">Disclosed power (MW)</div>
  <div class="bar"></div>
  <div class="row"><span id="mwmin">0</span><span id="mwmax">MW</span></div>
  <div class="note">height &amp; colour on a √ scale (small sites stay visible).
    <span class="dot"></span>dot = site with no public MW figure.</div>
</div>
<script>
const DATA = {data};
const {{MapboxOverlay, ColumnLayer, ScatterplotLayer}} = deck;

const mws = DATA.columns.map(d => d.mw);
const MAXMW = Math.max(80, ...mws);
document.getElementById('mwmax').textContent = Math.round(MAXMW) + ' MW';

// orange -> red ramp on sqrt(MW) so small sites stay distinguishable
function mwColor(mw) {{
  const t = Math.sqrt(mw) / Math.sqrt(MAXMW);
  const stops = [[250,199,117],[239,127,42],[178,24,43]];
  const seg = t <= 0.5 ? 0 : 1, f = t <= 0.5 ? t/0.5 : (t-0.5)/0.5;
  const a = stops[seg], b = stops[seg+1];
  return [0,1,2].map(i => Math.round(a[i] + (b[i]-a[i])*f)).concat(255);
}}
const STATUS = {{operational:[90,170,160], under_construction:[232,163,61],
  planned:[130,138,153], historical:[110,110,120]}};

function layers() {{
  return [
    new ScatterplotLayer({{
      id: 'sites', data: DATA.points, radiusUnits: 'pixels',
      getPosition: d => [d.lon, d.lat], getRadius: 6, radiusMinPixels: 4,
      getFillColor: d => (STATUS[d.status] || [130,138,153]).concat(220),
      stroked: true, lineWidthMinPixels: 1, getLineColor: [255,255,255,120],
      pickable: true,
    }}),
    new ColumnLayer({{
      id: 'mw', data: DATA.columns, diskResolution: 24, radius: 34000,
      extruded: true, radiusUnits: 'meters', elevationScale: 620000 / Math.sqrt(MAXMW),
      getPosition: d => [d.lon, d.lat], getElevation: d => Math.sqrt(d.mw),
      getFillColor: d => mwColor(d.mw), pickable: true,
      material: {{ambient: 0.64, diffuse: 0.6, shininess: 28, specularColor: [60,60,60]}},
    }}),
  ];
}}

const map = new maplibregl.Map({{
  container: 'map', style: '{BASEMAP}',
  center: [-38, 42], zoom: 1.15, pitch: 44, bearing: 0, antialias: true,
  maxPitch: 70,
}});
map.addControl(new maplibregl.NavigationControl({{visualizePitch: true}}), 'top-right');
map.on('load', () => {{
  map.addControl(new MapboxOverlay({{
    interleaved: true, layers: layers(),
    getTooltip: ({{object}}) => object && {{html:
      `<b>${{object.firm}}</b><br>${{object.site}}<br>${{object.city}} · ${{object.status}}`
      + `<br>MW: ${{object.mw ?? '—'}}  ·  GPUs: ${{object.gpu ? object.gpu.toLocaleString() : '—'}}`
      + (object.note ? `<br><span style="color:#9a978f">${{object.note}}</span>` : '')}},
  }}));
}});
</script>
</body>
</html>
"""


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default=ROOT / "data" / "firm_datacenters.csv", type=Path)
    p.add_argument("--out", default=ROOT / "docs" / "compute.html", type=Path)
    args = p.parse_args()
    columns, points = load(args.csv)
    args.out.write_text(html(columns, points), encoding="utf-8")
    print(f"Wrote {args.out} — {len(points)} compute sites, "
          f"{len(columns)} with disclosed MW (columns)")


if __name__ == "__main__":
    main()
