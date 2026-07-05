"""
Quant/HFT infrastructure map — build script.

Reads data/sites_seed.csv, enriches it (Google Maps deep links, tier labels),
and exports a standalone kepler.gl HTML map suitable for embedding in a blog post.

Usage:
    python build_map.py [--csv data/sites_seed.csv] [--out quant_dc_map.html]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
from keplergl import KeplerGl

# keplergl's bundled JS ships kepler.gl's demo Mapbox token, which GitHub
# push protection rejects. We don't need Mapbox at all: use CARTO's free
# Dark Matter basemap (no access token) and strip the bundled token from
# the exported HTML.
CARTO_DARK = {
    "id": "carto_dark",
    "label": "CARTO Dark Matter (no token)",
    "url": "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    "icon": "",
    "custom": True,
    "accessToken": None,
}
MAPBOX_TOKEN_RE = re.compile(r"pk\.eyJ[0-9A-Za-z_-]+\.[0-9A-Za-z_-]+")

# kepler's Jupyter wrapper only measures its container on window resize
# events (initial render falls back to 800x400), so pin the container to the
# viewport and fire a resize once the page loads.
FULLSCREEN_SNIPPET = """<style>
  html, body { width: 100%; height: 100%; }
  .keplergl-widget-container { width: 100vw !important; height: 100vh !important; }
</style>
<script>
  window.addEventListener('load', function () {
    setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 100);
  });
</script>
"""

TIER_LABELS = {
    "execution": "Tier 1 — Execution (exchange colo)",
    "network": "Tier 2 — Network (microwave/shortwave)",
    "research": "Tier 3 — Research (ML compute)",
}

# Hex colors per tier, referenced in the kepler config below.
TIER_COLORS = {
    "execution": [230, 80, 60],   # red — the latency layer
    "network": [250, 190, 60],    # amber — the towers
    "research": [70, 130, 240],   # blue — the compute layer
}


def load_sites(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required = {"site_id", "site_name", "tier", "lat", "lon", "confidence"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")

    # Google Maps deep link per pin — the "zoom in for detail" handoff.
    df["gmaps_url"] = (
        "https://www.google.com/maps/search/?api=1&query="
        + df["lat"].round(6).astype(str)
        + ","
        + df["lon"].round(6).astype(str)
    )
    df["tier_label"] = df["tier"].map(TIER_LABELS).fillna(df["tier"])

    # Fail loudly on bad coordinates rather than silently dropping pins.
    bad = df[(df["lat"].abs() > 90) | (df["lon"].abs() > 180) | df["lat"].isna()]
    if not bad.empty:
        raise ValueError(f"Bad coordinates for: {bad['site_id'].tolist()}")

    return df


def kepler_config(df: pd.DataFrame) -> dict:
    """Minimal kepler config: one point layer per tier, tooltip with evidence fields."""
    center_lat = float(df["lat"].mean())
    center_lon = float(df["lon"].mean())

    layers = []
    for tier, color in TIER_COLORS.items():
        layers.append(
            {
                "id": f"layer_{tier}",
                "type": "point",
                "config": {
                    "dataId": tier,
                    "label": TIER_LABELS[tier],
                    "columns": {"lat": "lat", "lng": "lon"},
                    "isVisible": True,
                    "color": color,
                    "visConfig": {
                        "radius": 14,
                        "opacity": 0.85,
                        "outline": True,
                        "thickness": 2,
                    },
                },
            }
        )

    tooltip_fields = [
        {"name": f}
        for f in [
            "site_name",
            "operator_or_venue",
            "firms_linked",
            "capacity_note",
            "confidence",
            "evidence_note",
            "gmaps_url",
        ]
    ]

    return {
        "version": "v1",
        "config": {
            "visState": {
                "layers": layers,
                "interactionConfig": {
                    "tooltip": {
                        "fieldsToShow": {t: tooltip_fields for t in TIER_COLORS},
                        "enabled": True,
                    }
                },
            },
            "mapState": {
                "latitude": center_lat,
                "longitude": center_lon,
                "zoom": 2.4,
            },
            "mapStyle": {
                "styleType": CARTO_DARK["id"],
                "mapStyles": {CARTO_DARK["id"]: CARTO_DARK},
            },
        },
    }


def build(csv_path: Path, out_path: Path) -> None:
    df = load_sites(csv_path)

    m = KeplerGl(config=kepler_config(df))
    # One dataset per tier so each gets its own layer + legend entry + toggle.
    for tier in TIER_COLORS:
        subset = df[df["tier"] == tier].reset_index(drop=True)
        if not subset.empty:
            m.add_data(data=subset, name=tier)

    m.save_to_html(file_name=str(out_path), read_only=False)

    html = out_path.read_text(encoding="utf-8")
    html, n_stripped = MAPBOX_TOKEN_RE.subn("", html)
    # rsplit: "</body>" also appears inside the bundled JS; only the last
    # occurrence is the real closing tag.
    head, _, tail = html.rpartition("</body>")
    html = head + FULLSCREEN_SNIPPET + "</body>" + tail
    out_path.write_text(html, encoding="utf-8")

    print(f"Wrote {out_path} — {len(df)} sites "
          f"({df['tier'].value_counts().to_dict()}); "
          f"stripped {n_stripped} bundled Mapbox token(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/sites_seed.csv", type=Path)
    parser.add_argument("--out", default="quant_dc_map.html", type=Path)
    args = parser.parse_args()
    build(args.csv, args.out)
