"""
Assemble data/firm_datacenters.csv — the deep firm -> data-centre mapping.

Source: data/raw/firm_datacenters_research.json (deep research + adversarial
verification over all 137 firms; each site carries an evidence array whose
URLs a verifier re-fetched). This flattens the verified sites into one row
per firm-datacentre, faithfully preserving the honesty nuances the verify
stage recorded (power_basis, confidence, coord_precision).

Curation is minimal and explicit (FIXES below) — the only hand-edit is the
NorthMark 'Project Moc-1' attribution, which the research agent filed under
G-Research on a former-COO link that no source confirms as ownership.

No network. Usage:
    python pipeline/assemble_datacenters.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "firm_datacenters_research.json"
OUT = ROOT / "data" / "firm_datacenters.csv"

COLUMNS = [
    "firm", "site_name", "role", "operator", "city", "country", "address",
    "lat", "lon", "coord_precision", "status", "gpu_count", "gpu_type",
    "power_mw", "power_basis", "capacity_note", "confidence",
    "evidence_count", "evidence_url",
]

# Targeted, documented corrections keyed by (firm, site_name substring).
FIXES = {
    ("G-Research", "Project Moc-1"): {
        "firm": "NorthMark Strategies (ex-G-Research founders)",
        "note_prefix": "ATTRIBUTION: NorthMark venture; G-Research link is a former-COO connection only, not confirmed ownership. ",
    },
}


def main() -> None:
    results = json.loads(SRC.read_text())["result"]["results"]

    rows = []
    for r in results:
        firm = r["firm"]
        for s in (r.get("sites") or []):
            fix = next((v for (f, key), v in FIXES.items()
                        if f == firm and key in s["site_name"]), None)
            note = s.get("capacity_note", "") or ""
            if fix:
                note = fix.get("note_prefix", "") + note
            ev = s.get("evidence") or []
            rows.append({
                "firm": fix["firm"] if fix else firm,
                "site_name": s["site_name"],
                "role": s["role"],
                "operator": s.get("operator", ""),
                "city": s.get("city", ""),
                "country": s.get("country", ""),
                "address": s.get("address") or "",
                "lat": s.get("lat"),
                "lon": s.get("lon"),
                "coord_precision": s["coord_precision"],
                "status": s["status"],
                "gpu_count": s.get("gpu_count") or "",
                "gpu_type": s.get("gpu_type") or "",
                "power_mw": s.get("power_mw"),
                "power_basis": (s.get("power_basis") or "").replace("\n", " "),
                "capacity_note": note.replace("\n", " ")[:400],
                "confidence": s["confidence"],
                "evidence_count": len(ev),
                "evidence_url": ev[0]["url"] if ev else "",
            })

    df = pd.DataFrame(rows)[COLUMNS]
    # Stable order: firms with disclosed MW first (by MW desc), then the rest.
    df["_mw"] = pd.to_numeric(df.power_mw, errors="coerce").fillna(-1)
    df = df.sort_values(["_mw", "firm", "site_name"], ascending=[False, True, True]).drop(columns="_mw")
    df.to_csv(OUT, index=False)

    n_mw = pd.to_numeric(df.power_mw, errors="coerce").notna().sum()
    n_gpu = (df.gpu_count.astype(str) != "").sum()
    print(f"Wrote {OUT.name}: {len(df)} sites across {df.firm.nunique()} firms; "
          f"{n_mw} with MW, {n_gpu} with GPU count; "
          f"roles={df.role.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
