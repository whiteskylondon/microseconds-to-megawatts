# CLAUDE.md — Quant Infrastructure Map

## What this project is

Research + interactive map for a published essay: **"Mapping the Physical
Footprint of Quantitative Finance"** — where hedge funds and quant/HFT firms
actually put their machines. Author: Daniel Roy. Output: a kepler.gl (or
MapLibre) interactive map embedded in a blog post, backed by a rigorously
sourced CSV inventory.

The thesis: the latency arms race consumed microseconds; the ML arms race
consumes megawatts — and megawatts leave a public paper trail.

## Core structure: three tiers

1. **execution** — exchange colocation sites (NYSE Mahwah, Nasdaq Carteret,
   Equinix NY4/5 Secaucus, CME/CyrusOne Aurora, LD4 Slough, Equinix FR2
   Frankfurt, Aruba IT3 Bergamo, HKEX TKO, JPX Tokyo...).
2. **network** — microwave/millimeter/shortwave relay infrastructure
   (Chicago–NJ corridor, Channel crossing masts at Richborough/Houtem,
   London–Frankfurt paths). Operators: McKay Brothers, New Line Networks
   (Jump/Virtu), Vigilant Global (DRW), Anova.
3. **research** — ML compute campuses. Anchor case: XTX Kajaani (€1bn+,
   22.5MW first building, ~250MW reported at full build). Contrast: Citadel
   Securities on Google Cloud, Renaissance's undisclosed on-prem setup.

## Non-negotiable rules

1. **Every pin must carry a public source.** Nothing gets mapped that is not
   already in the public record (spectrum license, planning filing, corporate
   announcement, credible press). This is both the intellectual standard and
   the legal safety margin of the piece.
2. **Confidence grading is mandatory**: `confirmed` (primary source) /
   `reported` (credible press) / `inferred` (triangulated). Never upgrade a
   record's confidence without a new source URL in `evidence_url`.
3. **Coordinates**: all seed coordinates are `approximate` (from memory) and
   MUST be verified by geocoding against a documented address before any
   publication build. Track status in `coord_precision`
   (exact/approximate/city_level/symbolic).
4. Do not state or imply non-public information about any firm's
   infrastructure. When evidence is absent, absence is the finding (e.g.
   Renaissance Technologies: campus known, compute inferred — say so).

## Data schema

`data/sites_seed.csv` columns: site_id, site_name, tier, operator_or_venue,
firms_linked, lat, lon, coord_precision, city, country, capacity_note,
evidence_type, evidence_note, confidence, verify_url_hint (to be replaced by
`evidence_url` with real URLs).

Planned second file: `data/paths.csv` for Tier-2 arc pairs
(origin_site_id, dest_site_id, operator, medium, evidence_url) — feeds a
kepler arc layer.

## Evidence pipeline (strength order)

1. Spectrum licenses: FCC ULS (Part 101 + experimental), Ofcom fixed-links
   register, ANFR Cartoradio (FR), BIPT (BE). Licensee shells trace back to
   firms via Companies House / state registries.
2. Planning applications (councils/municipalities).
3. Corporate + contractor disclosure (e.g. YIT/Granlund pages on XTX Kajaani).
4. Job postings / LinkedIn location signals.
5. Network forensics: PeeringDB, ASN registrations, exchange connectivity docs.
6. Industry databases: DataCenterMap, DCD archives.

Key references: Alexandre Laumonier (*Sniper in Mahwah*), Donald MacKenzie
(*Trading at the Speed of Light*), Shkilko & Sokolov (microwave outages paper),
Zuckerman (*The Man Who Solved the Market*).

## Tech conventions

- Python 3.11+, pandas; keep dependencies minimal (see requirements.txt).
- `build_map.py` is the single build entry point: CSV → standalone kepler HTML.
- The kepler HTML export is ~11MB (bundled library). If embed weight becomes a
  problem for the blog, build a lean MapLibre page reading the same CSV — the
  dataset is the asset, the renderer is swappable.
- kepler tooltip URLs may not be clickable depending on version — test before
  publication; MapLibre popup fallback if needed.
- Every scraper/extractor goes in `pipeline/` with a docstring stating source,
  terms-of-use considerations, and rate limiting. Cache raw pulls in
  `data/raw/` (gitignored if large).

## Working style

- Small, reviewable commits; one data source or feature per branch.
- When adding records, prefer fewer well-sourced pins over many weak ones.
- Update PLAN.md checkboxes as milestones complete.
