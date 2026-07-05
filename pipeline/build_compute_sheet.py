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
EVIDENCE_CSV = ROOT / "data" / "evidence.csv"
OUT_CSV = ROOT / "data" / "compute_sites.csv"

# facility_type: self_build / colo / cloud / hybrid / undisclosed
COMPUTE_SPECS = {
    "T3-001": {
        "firm": "XTX Markets",
        "facility_type": "self_build",
        "gpu_count": "25000",
        "gpu_type": "GPUs (type undisclosed; firmwide research cluster)",
        "compute_note": "Building 1: 15,000 sqm, 22.5MW IT across 3 halls (XTX's own publication). Not yet energised — first phase to begin operations 2026 (Yle/YIT). Firmwide 25,000+ GPU research cluster (still runs from Iceland). Campus ~250MW full build is press-only (absent from XTX materials + its 400kV grid EIA filing).",
        "energy_note": "No public annual energy figure. XTX filed a ~30km 400kV line EIA (Apr 2026) to connect the campus to Fingrid's grid.",
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
        "compute_note": "Firm's own site: 50,000 compute cores, 200+ Gbps global connectivity, research database growing 40TB/day (firmwide). East Setauket on-prem compute long-reported (Zuckerman); no site-specific MW/GPU figure — Brookhaven permit records cover only office expansion.",
        "energy_note": "",
    },
    "T3-005": {
        "firm": "High-Flyer Quant (幻方量化)",
        "facility_type": "self_build",
        "gpu_count": "10000",
        "gpu_type": "NVIDIA A100 (PCIe)",
        "compute_note": "Fire-Flyer 2 (2021): ~10,000 PCIe A100s, RMB 1bn; 56.7M GPU-hours across 1.35M jobs in 2022 at >96% occupancy; trained DeepSeek's early models. Predecessor Fire-Flyer 1 (2019, 1,100 cards, RMB 200m, 0.4MW) historical. Firmwide est. ~50,000 Hopper GPUs shared with DeepSeek (SemiAnalysis).",
        "energy_note": "Operator's SC24 paper: Fire-Flyer 2 total draw 'approximately just over 3 MW' (<4 MW). Fire-Flyer 1 was 0.4 MW.",
    },
    "T3-006": {
        "firm": "DeepSeek (High-Flyer lineage)",
        "facility_type": "self_build",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Self-build signalled by Ulanqab job ads (Apr 2026: DC delivery/O&M; Jun 2026: IDC design-planning engineer). DeepSeek closed its first external round Jun 2026 (~RMB 51bn at ~RMB 400bn valuation), earmarked for compute. No facility MW/GPU/address public. Firmwide (shared with High-Flyer): ~50,000 Hopper GPUs est. (SemiAnalysis).",
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
        "gpu_count": "1500",
        "gpu_type": "GPU cards (type undisclosed)",
        "compute_note": "China Securities Journal (Sep 2022): 1,500 GPU cards, 30k CPU cores, 1PB RAM, ~5PB disk, ~400 PFlops AI compute (end-2022 target); cluster claimed within global TOP500 top-200 at end-2021. Location undisclosed.",
        "energy_note": "",
    },
    "T3-009": {
        "firm": "Jane Street",
        "facility_type": "undisclosed",
        "gpu_count": "4032",
        "gpu_type": "liquid-cooled GPUs (type undisclosed)",
        "compute_note": "Dallas TX facility: 4,032 liquid-cooled GPUs, 56 racks up to 140kW/rack, 8,000km internal fibre, 1+ EB storage (Jane Street's own page + press). Firmwide 'tens of thousands' of GPUs, with a reported ambition to scale ~10x to hundreds of thousands and build/finance its own 100-200MW facility (site TBD).",
        "energy_note": "Up to 140kW per rack across 56 racks; no facility-total MW disclosed.",
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
        "gpu_type": "NVIDIA HGX B200 / Blackwell (Dell PowerEdge XE9685L, AMD EPYC)",
        "compute_note": "AI research deployment at Lefdal Mine Datacenter, 'recently opened' May 2026 (Dell PR). Direct-liquid-cooled racks >125kW/cabinet (HRT's own posts). GPU count, rack count and MW all undisclosed. Firmwide: 100s of PB research storage (Blobby).",
        "energy_note": "100% renewable power; fjord-seawater cooling.",
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
        "compute_note": "Two private datacenters: 1,313 nodes / 31,512 CPU cores as of 2016 (CMU ATLAS traces, firm co-authored). Firm now cites 600+ PB storage, 110,000+ simulations/day, ML GPUs on-demand via Google Cloud. No newer node/GPU count or DC location public.",
        "energy_note": "One trading engine's production hosts: 27 MWh/month (Jan 2023) cut to 10 MWh/month (Jan 2024) — single-team figure, not site-total.",
    },
    "T3-014": {
        "firm": "G-Research",
        "facility_type": "undisclosed",
        "gpu_count": "",
        "gpu_type": "",
        "compute_note": "Firm's own materials describe 'multiple 8 MW data halls' and 'a global estate of data centres with multiple megawatts' (hall count and locations undisclosed). Armada scheduler runs millions of batch jobs/day across tens of thousands of nodes. New Dallas infrastructure hub building/designing data centres.",
        "energy_note": "Multiple 8 MW data halls (count undisclosed) — the only public power granularity.",
    },
    "T3-015": {
        "firm": "Jump Trading",
        "facility_type": "self_build",
        "gpu_count": "",
        "gpu_type": "NVIDIA Vera Rubin NVL72",
        "compute_note": "Vera Rubin NVL72 deployment announced Mar 2026 (rack/GPU count undisclosed). Firm's own site: 3 purpose-built research data centres + 100+ colocated environments near exchanges, 10,000+ compute nodes, 5M+ simulations/day. Cluster locations undisclosed.",
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
    "compute_note", "power_mw", "energy_note", "confidence",
    "evidence_count", "evidence_url",
]


def main() -> None:
    sites = pd.read_csv(SITES_CSV, dtype=str).fillna("")
    research = sites[sites.tier == "research"].set_index("site_id")

    missing = set(research.index) - set(COMPUTE_SPECS)
    extra = set(COMPUTE_SPECS) - set(research.index)
    if missing or extra:
        raise SystemExit(f"COMPUTE_SPECS out of sync: missing={sorted(missing)} extra={sorted(extra)}")

    # Distinct-source counts from the evidence table (defaults to 1).
    counts = {}
    if EVIDENCE_CSV.exists():
        ev = pd.read_csv(EVIDENCE_CSV, dtype=str)
        counts = ev[ev.ref_type == "site"].groupby("ref_id").size().to_dict()

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
            "evidence_count": counts.get(site_id, 1),
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
