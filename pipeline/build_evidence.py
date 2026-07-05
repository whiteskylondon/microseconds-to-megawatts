"""
Build data/evidence.csv — the normalized multi-source evidence table.

Every mapped record carries at least one public source (CLAUDE.md rule 1),
but many carry several: the enrichment pass collected and adversarially
verified 2-10 distinct sources per record, which the flat sites_seed.csv
collapses to a single strongest `evidence_url`. This table restores the
full set — one row per (record, distinct source URL) — so the map can flag
how well-corroborated each pin is and a reader can follow every source.

Inputs (all local, no network):
  - data/sites_seed.csv / data/paths.csv   (the canonical single evidence_url)
  - data/raw/enrichment_results.json       (full per-record evidence arrays)
  - data/raw/tokyo_osaka_rerun.json
  - pipeline/assemble_enrichment.PROMOTIONS (site_id -> which JSON record)

Dedup is by URL within a record (the same page can be cited for several
facts). Usage:
    python pipeline/build_evidence.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_enrichment import PROMOTIONS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITES_CSV = ROOT / "data" / "sites_seed.csv"
PATHS_CSV = ROOT / "data" / "paths.csv"
RESULTS = ROOT / "data" / "raw" / "enrichment_results.json"
RERUN = ROOT / "data" / "raw" / "tokyo_osaka_rerun.json"
OUT_CSV = ROOT / "data" / "evidence.csv"

COLUMNS = ["ref_id", "ref_type", "source_no", "url", "publisher", "supports", "quote"]


def _load_by_key() -> dict:
    by_key = {r["candidate_key"]: r for r in json.loads(RESULTS.read_text())["results"]}
    if RERUN.exists():
        rerun = json.loads(RERUN.read_text())
        by_key[rerun["candidate_key"]] = rerun
    return by_key


def _record_evidence(by_key: dict) -> dict[str, list[dict]]:
    """site_id -> ordered, URL-deduped list of evidence dicts from the JSON."""
    out: dict[str, list[dict]] = {}

    def attach(site_id, evidence):
        bucket = out.setdefault(site_id, [])
        seen = {e["url"] for e in bucket}
        for e in evidence or []:
            if e["url"] not in seen:
                bucket.append(e)
                seen.add(e["url"])

    # Promoted records: site_id -> (candidate_key, record_index).
    for site_id, key, idx, _ov in PROMOTIONS:
        recs = by_key[key]["final"]["records"]
        if idx < len(recs):
            attach(site_id, recs[idx].get("evidence"))

    # Merge records: any JSON record tagged with merge_with_existing_site_id
    # enriches an existing pin — attach its sources to that pin too.
    for res in by_key.values():
        for rec in res["final"]["records"] or []:
            tgt = rec.get("merge_with_existing_site_id")
            if tgt:
                attach(tgt, rec.get("evidence"))

    return out


def main() -> None:
    by_key = _load_by_key()
    json_evidence = _record_evidence(by_key)

    sites = pd.read_csv(SITES_CSV, dtype=str).fillna("")
    paths = pd.read_csv(PATHS_CSV, dtype=str).fillna("")

    rows: list[dict] = []

    def emit(ref_id, ref_type, url, publisher, supports, quote):
        rows.append({
            "ref_id": ref_id, "ref_type": ref_type, "source_no": 0,
            "url": url, "publisher": publisher,
            "supports": supports, "quote": quote,
        })

    for _, s in sites.iterrows():
        seen: set[str] = set()
        # The canonical strongest source (from the flat CSV) leads.
        if s.evidence_url:
            emit(s.site_id, "site", s.evidence_url, "", s.evidence_note, "")
            seen.add(s.evidence_url)
        for e in json_evidence.get(s.site_id, []):
            if e["url"] not in seen:
                emit(s.site_id, "site", e["url"], e.get("publisher", ""),
                     e.get("supports", ""), e.get("quote", ""))
                seen.add(e["url"])

    # Paths are single-source by nature; include them for a uniform table.
    for _, p in paths.iterrows():
        if p.evidence_url:
            emit(p.path_id, "path", p.evidence_url, "", p.evidence_note, "")

    df = pd.DataFrame(rows)
    # Number sources within each record (1..n) for stable ordering/citation.
    df["source_no"] = df.groupby("ref_id").cumcount() + 1
    df = df[COLUMNS].sort_values(["ref_type", "ref_id", "source_no"])
    df.to_csv(OUT_CSV, index=False)

    per_site = df[df.ref_type == "site"].groupby("ref_id").size()
    multi = (per_site >= 2).sum()
    print(f"Wrote {OUT_CSV.name}: {len(df)} source rows across "
          f"{df.ref_id.nunique()} records; "
          f"{multi}/{len(per_site)} sites carry >=2 distinct sources "
          f"(max {per_site.max()})")


if __name__ == "__main__":
    main()
