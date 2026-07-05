"""Data-validation suite for the site inventory and path arcs.

Encodes the CLAUDE.md non-negotiables as tests: schema, coordinate bounds,
enum discipline, and source-URL presence for records added after the
evidence_url column existed (legacy seed rows may still carry only a
verify_url_hint until Phase 1 replaces them).
"""

from pathlib import Path

import pandas as pd
import pytest

DATA = Path(__file__).resolve().parent.parent / "data"

SITE_COLUMNS = [
    "site_id", "site_name", "tier", "operator_or_venue", "firms_linked",
    "lat", "lon", "coord_precision", "city", "country", "capacity_note",
    "power_mw", "status", "evidence_type", "evidence_note", "evidence_url",
    "confidence", "verify_url_hint",
]
PATH_COLUMNS = [
    "path_id", "origin_site_id", "dest_site_id", "operator", "medium",
    "status", "confidence", "evidence_note", "evidence_url",
]
COMPUTE_COLUMNS = [
    "site_id", "firm", "site_name", "facility_type", "city", "country",
    "lat", "lon", "coord_precision", "status", "gpu_count", "gpu_type",
    "compute_note", "power_mw", "energy_note", "confidence",
    "evidence_count", "evidence_url",
]
FACILITY_TYPES = {"self_build", "colo", "cloud", "hybrid", "undisclosed"}
EVIDENCE_COLUMNS = [
    "ref_id", "ref_type", "source_no", "url", "publisher", "supports", "quote",
]

TIERS = {"execution", "network", "research"}
CONFIDENCE = {"confirmed", "reported", "inferred"}
COORD_PRECISION = {"exact", "approximate", "city_level", "symbolic"}
STATUS = {"active", "historical", "under_construction"}
EVIDENCE_TYPES = {
    "spectrum_license", "planning_docs", "exchange_docs",
    "corporate_announcement", "operator_docs", "press",
    "regulatory_docs", "academic", "job_posting",
}
MEDIA = {"microwave", "mm-wave", "laser", "shortwave", "fiber"}


@pytest.fixture(scope="module")
def sites() -> pd.DataFrame:
    df = pd.read_csv(DATA / "sites_seed.csv", dtype=str)
    for col in ("lat", "lon", "power_mw"):
        df[col] = df[col].astype(float)
    return df


@pytest.fixture(scope="module")
def paths() -> pd.DataFrame:
    return pd.read_csv(DATA / "paths.csv", dtype=str)


def test_site_schema(sites):
    assert list(sites.columns) == SITE_COLUMNS


def test_site_ids_unique(sites):
    dupes = sites[sites.site_id.duplicated()].site_id.tolist()
    assert not dupes, f"duplicate site_ids: {dupes}"


def test_coordinate_bounds(sites):
    bad = sites[
        sites.lat.isna() | sites.lon.isna()
        | (sites.lat.abs() > 90) | (sites.lon.abs() > 180)
    ]
    assert bad.empty, f"bad coordinates: {bad.site_id.tolist()}"


def test_site_enums(sites):
    for col, allowed in [
        ("tier", TIERS), ("confidence", CONFIDENCE),
        ("coord_precision", COORD_PRECISION), ("status", STATUS),
        ("evidence_type", EVIDENCE_TYPES),
    ]:
        bad = sites[~sites[col].isin(allowed)]
        assert bad.empty, f"invalid {col}: {bad[['site_id', col]].values.tolist()}"


def test_evidence_url_wellformed(sites):
    with_url = sites[sites.evidence_url.notna()]
    bad = with_url[~with_url.evidence_url.str.startswith(("http://", "https://"))]
    assert bad.empty, f"malformed evidence_url: {bad.site_id.tolist()}"


def test_new_records_carry_evidence_url(sites):
    # Rows without a legacy verify_url_hint are post-enrichment records:
    # they must carry a real evidence_url (CLAUDE.md rule 1).
    new = sites[sites.verify_url_hint.isna()]
    missing = new[new.evidence_url.isna()]
    assert missing.empty, f"records without any source URL: {missing.site_id.tolist()}"


def test_power_mw_positive(sites):
    with_power = sites[sites.power_mw.notna()]
    assert (with_power.power_mw > 0).all()


def test_path_schema(paths):
    assert list(paths.columns) == PATH_COLUMNS


def test_path_ids_unique(paths):
    if paths.empty:
        return
    dupes = paths[paths.path_id.duplicated()].path_id.tolist()
    assert not dupes, f"duplicate path_ids: {dupes}"


def test_path_endpoints_exist(paths, sites):
    if paths.empty:
        return
    known = set(sites.site_id)
    refs = set(paths.origin_site_id) | set(paths.dest_site_id)
    assert refs <= known, f"paths reference unknown site_ids: {sorted(refs - known)}"


@pytest.fixture(scope="module")
def compute() -> pd.DataFrame:
    return pd.read_csv(DATA / "compute_sites.csv", dtype=str).fillna("")


def test_compute_schema(compute):
    assert list(compute.columns) == COMPUTE_COLUMNS


def test_compute_in_sync_with_sites(compute, sites):
    research = sites[sites.tier == "research"]
    assert set(compute.site_id) == set(research.site_id), \
        "compute_sites.csv must cover exactly the research-tier records; rerun pipeline/build_compute_sheet.py"
    joined = compute.merge(research, on="site_id", suffixes=("_c", ""))
    for col in ("status", "confidence", "coord_precision"):
        mismatched = joined[joined[f"{col}_c"] != joined[col].astype(str)]
        assert mismatched.empty, f"{col} out of sync for: {mismatched.site_id.tolist()}"


def test_compute_enums(compute):
    assert compute.facility_type.isin(FACILITY_TYPES).all()
    assert compute.status.isin(STATUS).all()


def test_compute_gpu_count_numeric(compute):
    nonempty = compute[compute.gpu_count != ""]
    assert nonempty.gpu_count.str.fullmatch(r"\d+").all(), \
        "gpu_count must be a bare integer or empty"


@pytest.fixture(scope="module")
def evidence() -> pd.DataFrame:
    return pd.read_csv(DATA / "evidence.csv", dtype=str).fillna("")


def test_evidence_schema(evidence):
    assert list(evidence.columns) == EVIDENCE_COLUMNS


def test_evidence_refs_exist(evidence, sites, paths):
    known = set(sites.site_id) | set(paths.path_id)
    refs = set(evidence.ref_id)
    assert refs <= known, f"evidence.csv references unknown ids: {sorted(refs - known)}"


def test_evidence_urls_wellformed(evidence):
    bad = evidence[~evidence.url.str.startswith(("http://", "https://"))]
    assert bad.empty, f"malformed evidence url for: {bad.ref_id.tolist()}"


def test_evidence_urls_unique_per_ref(evidence):
    dupes = evidence[evidence.duplicated(["ref_id", "url"])]
    assert dupes.empty, f"duplicate source URLs within a record: {dupes.ref_id.tolist()}"


def test_every_site_has_evidence(evidence, sites):
    site_refs = set(evidence[evidence.ref_type == "site"].ref_id)
    missing = set(sites.site_id) - site_refs
    assert not missing, f"sites with no evidence row: {sorted(missing)}"


def test_compute_evidence_count_matches(compute, evidence):
    per_site = evidence[evidence.ref_type == "site"].groupby("ref_id").size()
    for _, row in compute.iterrows():
        expected = int(per_site.get(row.site_id, 1))
        assert int(row.evidence_count) == expected, \
            f"{row.site_id}: evidence_count {row.evidence_count} != {expected}; rerun build_compute_sheet.py"


def test_path_enums_and_urls(paths):
    if paths.empty:
        return
    assert paths.medium.isin(MEDIA).all()
    assert paths.status.isin(STATUS).all()
    assert paths.confidence.isin(CONFIDENCE).all()
    assert paths.evidence_url.str.startswith(("http://", "https://")).all(), \
        "every arc needs a working evidence_url"
