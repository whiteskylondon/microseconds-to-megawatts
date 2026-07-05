"""
Nominatim geocoder for verifying site coordinates against documented addresses.

Source: OpenStreetMap Nominatim public API (https://nominatim.openstreetmap.org).
Terms of use: https://operations.osmfoundation.org/policies/nominatim/
  - hard limit of 1 request/second: enforced here with a 1.1s sleep between
    uncached requests
  - descriptive User-Agent with contact details is required (set below)
  - bulk geocoding of large datasets is discouraged; this project geocodes
    tens of addresses, once, with results cached
Caching: raw responses cached in data/raw/geocode_cache.json (keyed by query
string) so re-runs never re-hit the API.

Usage:
    python pipeline/geocode.py "350 E Cermak Rd, Chicago, IL, USA"
    python pipeline/geocode.py --batch queries.json --out results.json
        (queries.json: JSON list of query strings)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "geocode_cache.json"
USER_AGENT = "quant-infra-map/0.1 (research project; daniroy@gmail.com)"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def _save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=1, ensure_ascii=False), encoding="utf-8")


def geocode(query: str, cache: dict | None = None) -> dict | None:
    """Return the top Nominatim hit for `query` as a dict
    {lat, lon, display_name, type, class}, or None if no hit."""
    own_cache = cache is None
    if own_cache:
        cache = _load_cache()

    if query in cache:
        result = cache[query]
    else:
        params = urllib.parse.urlencode(
            {"q": query, "format": "jsonv2", "limit": 3, "addressdetails": 0}
        )
        req = urllib.request.Request(
            f"{NOMINATIM_URL}?{params}", headers={"User-Agent": USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        cache[query] = result
        if own_cache:
            _save_cache(cache)
        time.sleep(1.1)  # Nominatim usage policy: max 1 req/s

    if not result:
        return None
    top = result[0]
    return {
        "lat": float(top["lat"]),
        "lon": float(top["lon"]),
        "display_name": top.get("display_name", ""),
        "type": top.get("type", ""),
        "class": top.get("category", top.get("class", "")),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", help="address or place to geocode")
    parser.add_argument("--batch", type=Path, help="JSON file: list of query strings")
    parser.add_argument("--out", type=Path, help="write batch results to this JSON file")
    args = parser.parse_args()

    if args.batch:
        queries = json.loads(args.batch.read_text(encoding="utf-8"))
        cache = _load_cache()
        results = {}
        for q in queries:
            results[q] = geocode(q, cache=cache)
            _save_cache(cache)
            hit = results[q]
            print(f"{'OK ' if hit else 'MISS'} {q}"
                  + (f" -> {hit['lat']:.5f},{hit['lon']:.5f} ({hit['display_name'][:80]})" if hit else ""))
        if args.out:
            args.out.write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    elif args.query:
        hit = geocode(args.query)
        print(json.dumps(hit, indent=2, ensure_ascii=False) if hit else "no result", file=sys.stdout)
    else:
        parser.error("provide a query or --batch")


if __name__ == "__main__":
    main()
