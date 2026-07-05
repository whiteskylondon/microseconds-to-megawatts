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


def test_path_enums_and_urls(paths):
    if paths.empty:
        return
    assert paths.medium.isin(MEDIA).all()
    assert paths.status.isin(STATUS).all()
    assert paths.confidence.isin(CONFIDENCE).all()
    assert paths.evidence_url.str.startswith(("http://", "https://")).all(), \
        "every arc needs a working evidence_url"
