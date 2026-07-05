# PLAN.md — phased milestones

## Phase 1 — Foundation hygiene
- [ ] Geocode-verify all seed coordinates against documented addresses; set
      coord_precision=exact where verified
- [ ] Replace verify_url_hint with real evidence_url for all 19 seed records
- [ ] Add pytest data-validation suite (schema, coordinate bounds, confidence
      enum, URL presence for confirmed records) — run in CI

## Phase 2 — Tier 2 extraction (the towers)
- [ ] pipeline/fcc_uls.py: pull FCC ULS Part 101 licenses for known
      licensee shells on the Chicago–NJ corridor; output tower coords +
      paths.csv arc pairs
- [ ] FCC experimental license pull (shortwave sites)
- [ ] Ofcom fixed-links register extraction (London–Slough–coast paths)
- [ ] ANFR Cartoradio: French relay sites on the London–Frankfurt corridor
- [ ] Add kepler arc layer for paths.csv

## Phase 3 — Tier 3 expansion (the compute story)
- [ ] XTX: pin Kajaani precisely (Sokajärventie site), add second building,
      Iceland (Verne Global) with sources
- [ ] Job-ad triangulation pass: Jane Street, HRT, Two Sigma, DE Shaw, Jump —
      infrastructure roles with locations
- [ ] Renaissance: Brookhaven planning/permit search; document the null result
      if null
- [ ] Power-capacity column normalization (MW where public)

## Phase 4 — Publication build
- [ ] Decide renderer: kepler standalone vs MapLibre page (embed weight, link
      behavior in tooltips)
- [ ] Static fallback image (matplotlib/plotly) for social cards + RSS
- [ ] Final source audit: every pin → working evidence_url
- [ ] Essay draft sections keyed to map tiers
