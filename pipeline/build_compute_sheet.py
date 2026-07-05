"""
Build data/compute_sites.csv — the megawatts sheet.

The focused deliverable behind the essay's thesis: ONLY the data/compute
centres of quant/HFT firms (tier=research), with structured compute columns
(gpu_count, gpu_type), power_mw, and an energy_note, split by status
(active vs under_construction).

Source of truth: data/sites_seed.csv supplies identity, coordinates, status,
power_mw, confidence and evidence_url for every research-tier record.
COMPUTE_SPECS below adds the compute-specific fields, hand-curated from the
verifier-checked evidence in data/raw/enrichment_results.json and
data/raw/compute_specs_facts.json (every figure traces to a fetched URL).

No network access. Usage:
    python pipeline/build_compute_sheet.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SITES_CSV = ROOT / "data" / "sites_seed.csv"
OUT_CSV = ROOT / "data" / "compute_sites.csv"

# facility_type: self_build / colo / cloud / hybrid / undisclosed
COMPUTE_SPECS = {
    "T3-001": {
        "firm": "XTX Markets",
        "facility_type": "self_build",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Campus building 1: 15,000 sqm, 22.5MW IT. Firmwide fleet 25k+ GPUs (Jan 2025 announcement). ~250MW full-build figure is DCD-reported, not in XTX's own materials.",
        "energy_note": "",
    },
    "T3-017": {
        "firm": "XTX Markets",
        "facility_type": "self_build",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Campus building 2; IT load and floor area not yet public (building 1 = 22.5MW IT for scale). Up to five buildings originally planned.",
        "energy_note": "",
    },
    "T3-002": {
        "firm": "XTX Markets (tenant)",
        "facility_type": "colo",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "XTX's pre-Kajaani research cluster at Verne's multi-tenant campus; XTX-specific footprint undisclosed. power_mw is the CAMPUS capacity (>140MW), not XTX's share.",
        "energy_note": "Campus runs on 100% hydro/geothermal per operator.",
    },
    "T3-003": {
        "firm": "Citadel Securities",
        "facility_type": "cloud",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Research platform on Google Cloud: 'more than 1 million cores concurrently' (joint case study). No owned facility in the public record.",
        "energy_note": "",
    },
    "T3-004": {
        "firm": "Renaissance Technologies",
        "facility_type": "self_build",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "On-prem compute at East Setauket campus long-reported (Zuckerman); scale entirely undisclosed — the absence of any public figure is the finding.",
        "energy_note": "",
    },
    "T3-005": {
        "firm": "High-Flyer Quant (幻方量化)",
        "facility_type": "self_build",
        "gpu_count": "10000",
        "gpu_type": "NVIDIA A100 (PCIe)",
        "compute_note": "Fire-Flyer 2 (2021): ~10,000 PCIe A100s, ~1,250 GPU nodes, ~200 storage servers, RMB 1bn; trained DeepSeek's early models. Predecessor Fire-Flyer 1 (2020, 1,100 A100s) historical.",
        "energy_note": "Operator's SC24 paper: total draw 'approximately just over 3 MW' (<4 MW).",
    },
    "T3-006": {
        "firm": "DeepSeek (High-Flyer lineage)",
        "facility_type": "self_build",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Self-build signalled by official job ads for data-centre delivery/O&M roles in Ulanqab (Apr 2026); no size, MW, or address public.",
        "energy_note": "IT之家 cites Ulanqab's cheap power, 4.3°C average temperature, PUE below 1.26 as siting rationale.",
    },
    "T3-007": {
        "firm": "Ubiquant (九坤投资)",
        "facility_type": "undisclosed",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "'Bei Ming' AI supercomputing cluster; >RMB 100m invested in 2020 per GM interview. Location and scale undisclosed.",
        "energy_note": "",
    },
    "T3-008": {
        "firm": "Minghong Investment (明汯投资)",
        "facility_type": "undisclosed",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Firm statement (Feb 2025): thousands of GPU cards, tens of thousands of CPU cores, multi-PB storage, ~400 PFlops claimed.",
        "energy_note": "",
    },
    "T3-009": {
        "firm": "Jane Street",
        "facility_type": "undisclosed",
        "gpu_count": "4032",
        "gpu_type": "liquid-cooled GPUs (type undisclosed)",
        "compute_note": "4,032 liquid-cooled GPUs per Jane Street's careers page (public video tour, May 2026); firmwide 'tens of thousands' of high-end GPUs.",
        "energy_note": "",
    },
    "T3-010": {
        "firm": "Jane Street",
        "facility_type": "cloud",
        "gpu_count": "",
        "gpu_type": "NVIDIA Vera Rubin (via CoreWeave)",
        "compute_note": "$6bn AI-cloud agreement with CoreWeave (Apr 2026), next-gen compute 'across multiple facilities', plus $1bn equity investment.",
        "energy_note": "",
    },
    "T3-011": {
        "firm": "Hudson River Trading",
        "facility_type": "colo",
        "gpu_count": "",
        "gpu_type": "NVIDIA HGX B200 (Dell PowerEdge XE9685L)",
        "compute_note": "AI research deployment at Lefdal Mine Datacenter: direct-liquid-cooled racks >125kW per cabinet (HRT's own posts).",
        "energy_note": "Lefdal campus runs on Norwegian hydro; fjord-water cooling.",
    },
    "T3-012": {
        "firm": "Hudson River Trading",
        "facility_type": "cloud",
        "gpu_count": "",
        "gpu_type": "NVIDIA GPUs (Google Cloud); HGX B200 (Lambda)",
        "compute_note": "Google Cloud HPC for research/simulation (2024); Lambda AI-cloud partnership (2026).",
        "energy_note": "",
    },
    "T3-013": {
        "firm": "Two Sigma",
        "facility_type": "hybrid",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Two private datacenters: 1,313 nodes / 31,512 CPU cores / 328 TB RAM as of 2016 (CMU ATLAS traces, firm co-authored); Google Cloud since (engineering blog).",
        "energy_note": "",
    },
    "T3-014": {
        "firm": "G-Research",
        "facility_type": "undisclosed",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Own job ads describe 'a global estate of data centres'; locations and scale undisclosed.",
        "energy_note": "",
    },
    "T3-015": {
        "firm": "Jump Trading",
        "facility_type": "undisclosed",
        "gpu_count": "",
        "gpu_type": "NVIDIA Vera Rubin NVL72",
        "compute_note": "Early Vera Rubin NVL72 rack-scale deployment (~Apr 2026); infrastructure supports 'thousands of CPUs and GPUs' (VAST case study). Cluster location undisclosed.",
        "energy_note": "",
    },
    "T3-016": {
        "firm": "Jump Trading",
        "facility_type": "undisclosed",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "HPC data centre in Carrollton, TX signalled by on-site technician job ads (high-density liquid-cooled cabinets); operator and capacity undisclosed.",
        "energy_note": "",
    },
}

COLUMNS = [
    "site_id", "firm", "site_name", "facility_type", "city", "country",
    "lat", "lon", "coord_precision", "status", "gpu_count", "gpu_type",
    "compute_note", "power_mw", "energy_note", "confidence", "evidence_url",
]


def main() -> None:
    sites = pd.read_csv(SITES_CSV, dtype=str).fillna("")
    research = sites[sites.tier == "research"].set_index("site_id")

    missing = set(research.index) - set(COMPUTE_SPECS)
    extra = set(COMPUTE_SPECS) - set(research.index)
    if missing or extra:
        raise SystemExit(f"COMPUTE_SPECS out of sync: missing={sorted(missing)} extra={sorted(extra)}")

    rows = []
    for site_id, spec in COMPUTE_SPECS.items():
        s = research.loc[site_id]
        rows.append({
            "site_id": site_id,
            "site_name": s.site_name,
            "city": s.city, "country": s.country,
            "lat": s.lat, "lon": s.lon,
            "coord_precision": s.coord_precision,
            "status": s.status,
            "power_mw": s.power_mw,
            "confidence": s.confidence,
            "evidence_url": s.evidence_url,
            **spec,
        })

    df = pd.DataFrame(rows)[COLUMNS]
    # Under-construction sites grouped last — the "in progress" category.
    df["_k"] = df.status.map({"active": 0, "historical": 1, "under_construction": 2})
    df = df.sort_values(["_k", "firm", "site_id"]).drop(columns="_k")
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV.name}: {len(df)} compute sites "
          f"({df.status.value_counts().to_dict()}); "
          f"power stated for {(df.power_mw != '').sum()} sites")


if __name__ == "__main__":
    main()
