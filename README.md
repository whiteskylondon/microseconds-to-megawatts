# Mapping the Physical Footprint of Quantitative Finance

Working repo for the essay + interactive map. Three-tier inventory of publicly
documented quant/HFT infrastructure, with an evidence grade on every record.

## Structure

- `data/sites_seed.csv` — the inventory (19 seed records; target ~80-120)
- `build_map.py` — CSV → standalone kepler.gl HTML
  (`python build_map.py --out docs/index.html`)
- `docs/index.html` — output (tracked; servable via GitHub Pages); embeddable
  in Ghost via iframe or direct upload

## Schema

| column | meaning |
|---|---|
| `tier` | `execution` (exchange colo) / `network` (microwave, shortwave) / `research` (ML compute) |
| `coord_precision` | `exact` (verified address/geocode) / `approximate` (needs verification) / `city_level` / `symbolic` (no single site exists, e.g. cloud usage) |
| `confidence` | `confirmed` (primary source: license, filing, corporate announcement) / `reported` (credible press) / `inferred` (triangulated from job ads, LinkedIn, network data) |
| `evidence_type` | `spectrum_license` / `planning_docs` / `exchange_docs` / `corporate_announcement` / `operator_docs` / `press` |
| `verify_url_hint` | where to find the primary source (replace with real URLs before publication) |

**Publication rule: every pin must carry a public primary or credible secondary
source. Nothing gets mapped that isn't already in the public record.**

## Evidence pipeline (in order of strength)

1. **Spectrum licenses** — FCC ULS (Part 101 + experimental), Ofcom fixed-links
   register, ANFR Cartoradio (FR), BIPT (BE). Exact tower coordinates + licensee
   shells traceable via Companies House / state registries.
2. **Planning applications** — councils/municipalities for towers and DC builds.
3. **Corporate + contractor disclosure** — press releases; contractor project pages.
4. **Job postings / LinkedIn** — location signals for unannounced presence.
5. **Network forensics** — PeeringDB, ASN registrations, exchange connectivity docs.
6. **Industry databases** — DataCenterMap, DCD archives, colo operator case studies.

## Key references

- Alexandre Laumonier, *Sniper in Mahwah* (blog + books "6"/"5") — the Channel
  towers, shortwave series (with Bob Van Valzah)
- Donald MacKenzie, *Trading at the Speed of Light* (2021)
- Shkilko & Sokolov, "Every Cloud Has a Silver Lining" (microwave outages as
  natural experiment)
- Exchange colocation service documents (NYSE, Nasdaq, CME, DB, HKEX, JPX)

## TODO

- [ ] Verify/refine all `approximate` coordinates (geocode against addresses)
- [ ] Replace `verify_url_hint` with real evidence URLs
- [ ] FCC ULS pull: script the Part 101 licensee extraction for known shells
- [ ] Add arc layer: tower-pair paths for Tier 2 (kepler arc layer, needs
      origin/destination pairs in a second CSV)
- [ ] Ofcom fixed-links + ANFR Cartoradio extraction for the London-Frankfurt corridor
- [ ] Expand Tier 3: Jane Street, HRT, Two Sigma, DE Shaw compute footprints
      (job-ad triangulation)
- [ ] Test kepler tooltip URL behavior in target blog; fall back to MapLibre
      popup page if links aren't clickable
