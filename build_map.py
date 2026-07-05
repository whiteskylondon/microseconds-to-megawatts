"""
Quant/HFT infrastructure map — build script.

Reads data/sites_seed.csv (point pins) and data/paths.csv (Tier-2 arcs,
joined to site coordinates via origin/dest site_ids), enriches them
(Google Maps deep links, tier labels), and exports a standalone kepler.gl
HTML map suitable for embedding in a blog post.

Usage:
    python build_map.py [--csv data/sites_seed.csv] [--paths data/paths.csv]
                        [--out quant_dc_map.html]
"""

from __future__ import annotations

import argparse
import re
import urllib.parse
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
  .map-popover {
    border: 1px solid rgba(255, 255, 255, 0.28) !important;
    border-radius: 6px !important;
  }
</style>
<script>
  window.addEventListener('load', function () {
    setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 100);
  });
</script>
"""

TIER_LABELS = {
    "execution": "Layer 1 — Execution (exchange colo)",
    "network": "Layer 2 — Network sites (towers & antennas)",
    "research": "Layer 3 — Research (ML compute)",
}

# Column names -> human labels shown in the kepler tooltip (kepler displays
# raw column names, so the display DataFrames are renamed before add_data).
SITE_DISPLAY = {
    "site_name": "Site",
    "operator_or_venue": "Operator / venue",
    "firms_linked": "Firms linked",
    "capacity_note": "Notes",
    "power_mw": "Power (MW)",
    "status": "Status",
    "coord_precision": "Pin precision",
    "confidence": "Confidence",
    "evidence_count": "Sources (#)",
    "evidence_note": "Evidence",
    "evidence_url": "Source URL",
    "gmaps_url": "Google Maps",
}
PATH_DISPLAY = {
    "route": "Route",
    "operator": "Operator",
    "medium": "Medium",
    "status": "Status",
    "confidence": "Confidence",
    "evidence_count": "Sources (#)",
    "evidence_note": "Evidence",
    "evidence_url": "Source URL",
}

# Hex colors per tier, referenced in the kepler config below.
TIER_COLORS = {
    "execution": [230, 80, 60],   # red — the latency layer
    "network": [250, 190, 60],    # amber — the towers
    "research": [70, 130, 240],   # blue — the compute layer
}

PATHS_LABEL = "Layer 2 — Network paths (routes)"
PATHS_COLOR = [250, 190, 60]      # amber, matching the network layer


def evidence_counts(evidence_csv: Path) -> pd.Series:
    """ref_id -> number of distinct public sources, from evidence.csv.

    Empty Series when the file is absent (evidence_count then defaults to 1
    since every mapped record carries at least its own evidence_url)."""
    if not evidence_csv.exists():
        return pd.Series(dtype="int64")
    ev = pd.read_csv(evidence_csv, dtype=str)
    return ev.groupby("ref_id").size()


def load_sites(csv_path: Path, counts: pd.Series | None = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required = {"site_id", "site_name", "tier", "lat", "lon", "confidence"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")

    # How many distinct public sources back each pin (defaults to 1: every
    # record carries at least its own evidence_url).
    counts = pd.Series(dtype="int64") if counts is None else counts
    df["evidence_count"] = (
        df["site_id"].map(counts).fillna(1).astype(int).astype(str))

    # Google Maps handoff, honest about pin precision: coordinate deep link
    # only where the pin is placed (exact/approximate); a name+city text
    # search for city-level pins (the coords are a centroid, not the site);
    # nothing for symbolic pins (they mark a firm, not a place).
    def gmaps(row):
        if row.coord_precision in ("exact", "approximate"):
            return ("https://www.google.com/maps/search/?api=1&query="
                    f"{row.lat:.6f},{row.lon:.6f}")
        if row.coord_precision == "city_level":
            q = urllib.parse.quote_plus(f"{row.site_name} {row.city}")
            return f"https://www.google.com/maps/search/?api=1&query={q}"
        return ""

    df["gmaps_url"] = df.apply(gmaps, axis=1)
    df["tier_label"] = df["tier"].map(TIER_LABELS).fillna(df["tier"])

    # Fail loudly on bad coordinates rather than silently dropping pins.
    bad = df[(df["lat"].abs() > 90) | (df["lon"].abs() > 180) | df["lat"].isna()]
    if not bad.empty:
        raise ValueError(f"Bad coordinates for: {bad['site_id'].tolist()}")

    # Tooltip hygiene: no NaN in display fields, no trailing ".0" on power.
    df["power_mw"] = df["power_mw"].map(
        lambda v: "" if pd.isna(v) else f"{v:g}")
    return df.fillna("")


def load_paths(paths_csv: Path, sites: pd.DataFrame,
               counts: pd.Series | None = None) -> pd.DataFrame | None:
    """Load Tier-2 arcs and join origin/dest coordinates from the sites table.

    Returns None when the paths file is absent or has no rows."""
    if not paths_csv.exists():
        return None
    paths = pd.read_csv(paths_csv)
    if paths.empty:
        return None

    coords = sites.set_index("site_id")[["lat", "lon", "site_name"]]
    unknown = (set(paths["origin_site_id"]) | set(paths["dest_site_id"])) - set(coords.index)
    if unknown:
        raise ValueError(f"paths.csv references unknown site_ids: {sorted(unknown)}")

    for end, col in (("origin", "origin_site_id"), ("dest", "dest_site_id")):
        joined = coords.loc[paths[col]].reset_index(drop=True)
        paths[f"{end}_lat"] = joined["lat"]
        paths[f"{end}_lon"] = joined["lon"]
        paths[f"{end}_name"] = joined["site_name"]
    paths["route"] = paths["origin_name"] + " → " + paths["dest_name"]

    counts = pd.Series(dtype="int64") if counts is None else counts
    paths["evidence_count"] = (
        paths["path_id"].map(counts).fillna(1).astype(int).astype(str))
    return paths


def kepler_config(df: pd.DataFrame, with_paths: bool = False) -> dict:
    """Minimal kepler config: one point layer per tier (+ an arc layer for
    Tier-2 paths), tooltip with evidence fields."""
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
    if with_paths:
        layers.append(
            {
                "id": "layer_paths",
                "type": "arc",
                "config": {
                    "dataId": "paths",
                    "label": PATHS_LABEL,
                    "columns": {
                        "lat0": "origin_lat",
                        "lng0": "origin_lon",
                        "lat1": "dest_lat",
                        "lng1": "dest_lon",
                    },
                    "isVisible": True,
                    "color": PATHS_COLOR,
                    "visConfig": {"opacity": 0.5, "thickness": 1.5},
                },
            }
        )

    tooltip_fields = [{"name": label} for label in SITE_DISPLAY.values()]
    paths_tooltip = [{"name": label} for label in PATH_DISPLAY.values()]
    fields_to_show = {t: tooltip_fields for t in TIER_COLORS}
    if with_paths:
        fields_to_show["paths"] = paths_tooltip

    return {
        "version": "v1",
        "config": {
            "visState": {
                "layers": layers,
                "interactionConfig": {
                    "tooltip": {
                        "fieldsToShow": fields_to_show,
                        "enabled": True,
                    }
                },
            },
            "mapState": {
                "latitude": center_lat,
                "longitude": center_lon,
                "zoom": 1.7,
            },
            "mapStyle": {
                "styleType": CARTO_DARK["id"],
                "mapStyles": {CARTO_DARK["id"]: CARTO_DARK},
            },
        },
    }


def build(csv_path: Path, out_path: Path, paths_csv: Path | None = None,
          evidence_csv: Path | None = None) -> None:
    counts = evidence_counts(evidence_csv) if evidence_csv else pd.Series(dtype="int64")
    df = load_sites(csv_path, counts=counts)
    paths = load_paths(paths_csv, df, counts=counts) if paths_csv else None

    m = KeplerGl(config=kepler_config(df, with_paths=paths is not None))
    # One dataset per tier so each gets its own layer + legend entry + toggle.
    for tier in TIER_COLORS:
        subset = df[df["tier"] == tier].reset_index(drop=True)
        if not subset.empty:
            m.add_data(data=subset.rename(columns=SITE_DISPLAY), name=tier)
    if paths is not None:
        m.add_data(data=paths.fillna("").rename(columns=PATH_DISPLAY),
                   name="paths")

    m.save_to_html(file_name=str(out_path), read_only=False)

    html = out_path.read_text(encoding="utf-8")
    html, n_stripped = MAPBOX_TOKEN_RE.subn("", html)
    # rsplit: "</body>" also appears inside the bundled JS; only the last
    # occurrence is the real closing tag.
    head, _, tail = html.rpartition("</body>")
    html = head + FULLSCREEN_SNIPPET + "</body>" + tail
    out_path.write_text(html, encoding="utf-8")

    n_paths = 0 if paths is None else len(paths)
    print(f"Wrote {out_path} — {len(df)} sites "
          f"({df['tier'].value_counts().to_dict()}), {n_paths} paths; "
          f"stripped {n_stripped} bundled Mapbox token(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/sites_seed.csv", type=Path)
    parser.add_argument("--paths", default="data/paths.csv", type=Path)
    parser.add_argument("--evidence", default="data/evidence.csv", type=Path)
    parser.add_argument("--out", default="quant_dc_map.html", type=Path)
    args = parser.parse_args()
    build(args.csv, args.out, paths_csv=args.paths, evidence_csv=args.evidence)
