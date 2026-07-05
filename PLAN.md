# PLAN.md — phased milestones

## Phase 1 — Foundation hygiene
- [x] Geocode-verify all seed coordinates against documented addresses; set
      coord_precision=exact where verified (all 19 original seed rows done;
      exact where the address resolved to a building/POI; T1-007/T1-008/T3-001
      stay approximate — campus-/postcode-/street-level is the honest limit;
      T1-010/T2-001/T2-002/T2-004 stay approximate — no public precise address)
- [x] Replace verify_url_hint with real evidence_url for all 19 seed records
      (every seed row now carries a fetch-verified URL; hints cleared)
- [x] Add pytest data-validation suite (schema, coordinate bounds, confidence
      enum, URL presence for post-enrichment records) — CI wiring pending

## Phase 2 — Tier 2 extraction (the towers)
- [ ] pipeline/fcc_uls.py: pull FCC ULS Part 101 licenses for known
      licensee shells on the Chicago–NJ corridor; output tower coords +
      paths.csv arc pairs
- [ ] FCC experimental license pull (shortwave sites)
- [ ] Ofcom fixed-links register extraction (London–Slough–coast paths)
- [ ] ANFR Cartoradio: French relay sites on the London–Frankfurt corridor
      (Tour de Reuze pinned from ANFR-derived data; bulk extraction pending;
      German-side relays entirely unmapped)
- [x] Add kepler arc layer for paths.csv (39 arcs shipped in enrichment pass 1)

## Phase 3 — Tier 3 expansion (the compute story)
- [x] XTX: add second building (T3-017, YIT-sourced), Iceland Verne campus
      enriched with operator sources (T3-002); campus now pinned street-level
      at Sokajärventie (Pohjan Sellu plot per Yle); plot-level pin pending
- [ ] Job-ad triangulation pass: Jane Street, HRT, Two Sigma, Jump, G-Research
      done in enrichment pass 1; DE Shaw still outstanding
- [ ] Renaissance: Brookhaven planning/permit search; document the null result
      if null
- [x] Power-capacity column normalization (power_mw column; source-stated
      values only: B3 10, KIO SF2 1.137, MOEX 9.5, Verne 140, XTX 22.5, HF ~3)
- [ ] Negative-space annotation (LatAm/Africa research-compute absence):
      decided NOT to add unsourced symbolic pins — implement as a map/essay
      annotation instead (rule 1 forbids pins without sources)

## Phase 4 — Publication build
- [ ] Decide renderer: kepler standalone vs MapLibre page (embed weight, link
      behavior in tooltips)
- [ ] Static fallback image (matplotlib/plotly) for social cards + RSS
- [ ] Final source audit: every pin → working evidence_url
- [ ] Essay draft sections keyed to map tiers
