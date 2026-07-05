# FIRMS.md — the mapping target list

Scope decision doc for the **compute/data-centre** story (Tier 3). Question
for each firm: *is there a public paper trail for its research/ML compute
footprint* (announcement, contractor filing, planning/grid record, job ad,
vendor case study)? If yes → mappable pin. If the firm only has an
**execution** (exchange-colo) footprint, that's already covered by the Tier 1
venue pins and is noted here but not a Tier 3 target.

Status key: ✅ mapped · 🔬 researched, worth a pass · ⬜ candidate, not yet
researched · ⚠️ likely unmappable (no public compute footprint expected).

---

## A. Already mapped (Tier 3)

| firm | records | note |
|---|---|---|
| XTX Markets | T3-001/002/017 | Kajaani (22.5MW, u/c) + Iceland/Verne + building 2 |
| High-Flyer / DeepSeek | T3-005/006 | Fire-Flyer 2 + Ulanqab |
| Ubiquant | T3-007 | Bei Ming cluster |
| Minghong | T3-008 | 1,500 GPU / 400 PFlops |
| Jane Street | T3-009/010 | Dallas DC + CoreWeave |
| Hudson River Trading | T3-011/012 | Lefdal Mine + cloud |
| Two Sigma | T3-013 | private DCs + GCP |
| G-Research | T3-014 | multiple 8MW halls |
| Jump Trading | T3-015/016 | Vera Rubin + Carrollton |
| Citadel Securities | T3-003 | Google Cloud (1M+ cores) |
| Renaissance Technologies | T3-004 | East Setauket (50k cores) |

## B. Named by Daniel — research next

| firm | HQ | why it matters | expectation |
|---|---|---|---|
| ⬜ Qube Research & Technologies (QRT) | London / Geneva | ~$28bn systematic, spun out of Credit Suisse 2020; heavy compute buyer | real cluster, likely **undisclosed** — job-ad / vendor triangulation |
| ⬜ Capital Fund Management (CFM) | Paris | one of the oldest quant funds (Bouchaud); academic-grade research compute | possible FR planning/press; else symbolic HQ pin |
| ⚠️ Assenagon | Munich | ~€50bn quant/derivatives-overlay asset manager | **not an HFT/GPU-ML shop** — a compute footprint is unlikely to be public; low priority |

## C. Big systematic / ML funds — strong candidates (⬜ unless noted)

| firm | HQ | compute signal |
|---|---|---|
| ⬜ D.E. Shaw | New York | Anton special-purpose supercomputers (molecular dynamics) are *published*; trading compute separate |
| ⬜ Millennium | New York | huge multi-manager; compute mostly undisclosed |
| ⬜ Point72 / Cubist | Stamford CT | systematic unit; Aurora AI push publicised |
| ⬜ Man Group (AHL / Numeric) | London | systematic pioneer; some public tech talks |
| ⬜ Squarepoint Capital | London / NY | large systematic, quiet |
| ⬜ PDT Partners | New York | ex-Morgan Stanley quant |
| ⬜ Voleon Group | Berkeley CA | explicitly ML-first |
| ⬜ WorldQuant | Old Greenwich CT | alpha factory, big compute |
| ⬜ Marshall Wace (TOPS) | London | systematic signals engine |
| ⬜ Winton | London | systematic, research-heavy |
| ⬜ AQR Capital | Greenwich CT | factor/quant, more CPU than GPU |
| ⚠️ Bridgewater | Westport CT | systematic macro, but not a GPU-ML/DC story |

## D. HFT / market makers — mostly a Tier-1 (execution) story

These live in exchange colos (already pinned as Tier 1 tenants). Add a Tier-3
pin **only** if a distinct research/ML compute site is publicly documented.

| firm | Tier-1 presence | Tier-3 compute signal? |
|---|---|---|
| ⬜ Optiver | mapped as colo tenant | Amsterdam/Chicago; watch for GPU build-out |
| ⬜ IMC Trading | colo tenant + shortwave (T2-004) | Amsterdam/Chicago |
| ⬜ Flow Traders | colo tenant | Amsterdam |
| ⬜ Tower Research Capital | colo + shortwave (Alpine) | — |
| ⬜ DRW / Cumberland | colo + towers (Vigilant) | crypto + research |
| ⬜ Susquehanna (SIG) | colo tenant | Bala Cynwyd PA |
| ⬜ Virtu Financial | colo + towers (New Line) | — |
| ⬜ Citadel (the hedge fund) | vs Citadel Securities | distinct research compute |
| ⚠️ GTS, Radix, Headlands, CTC, Akuna, Wolverine, Five Rings, Maven | colo tenants | small; compute footprint unlikely public |

## E. Asian quants beyond the three mapped (⬜)

| firm | note |
|---|---|
| ⬜ Lingjun Investment (灵均) | large Chinese quant |
| ⬜ Baiont / BaiontQuant | ML-native, Nanjing |
| ⬜ Yanfu Investments (衍复) | large Chinese quant |
| ⬜ Zhuke / Zhuoshi, Mingshi (明世) | mid-size, check for public compute |

---

## Recommended first pass (research batch)

Highest odds of a *real public paper trail* → do these first:
**Qube, CFM, D.E. Shaw (Anton), Point72/Cubist, Man Group, WorldQuant,
Voleon, Optiver, IMC, Susquehanna.**

Everything else stays ⬜ until we confirm scope. Firms marked ⚠️ are expected
to yield a documented **null** (absence is a finding) rather than a pin.
