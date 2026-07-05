# FIRMS.md — the firm universe

Defining the universe of quant/HFT firms worth considering for the map,
**before** any per-firm research. One flat list; classification lives in the
fields, not in sections.

## Ontology

- **firm_type** (controlled vocabulary):
  - `MM/HFT` — market maker / principal high-frequency trader (latency-first)
  - `Systematic` — systematic hedge fund running its own alpha (stat-arb, CTA)
  - `Multi-mgr` — multi-strategy platform with quant/systematic pods
  - `Quant AM` — quant asset manager (long-only, risk-premia, overlay)
  - `ML-native` — explicitly machine-learning-first fund
  - `Crypto MM` — digital-asset market maker (in scope)
- **continent** — North America · Europe · Asia · Middle East · Oceania ·
  South America
- **mapped** — existing Layer-3 (research/compute) record id(s), or `—` if not
  yet on the map
- **notes** — HQ city, compute signal, caveats. `★` = best public-paper-trail
  odds (suggested for the first research pass).

Mapping question per firm: *is there a public paper trail for its
research/ML compute* (announcement, contractor/grid filing, planning record,
job ad, vendor case study)? Every firm here — including the `MM/HFT` market
makers whose main footprint is exchange colocation (Layer 1) — is in scope for
a compute (Layer 3) research pass; where a firm turns out to be execution-only,
that's recorded as the finding.

## The universe

| firm | country | continent | firm_type | mapped | notes |
|---|---|---|---|---|---|
| AQR Capital | USA | North America | Quant AM | — | Greenwich CT; factor/risk-premia, more CPU than GPU |
| Akuna Capital | USA | North America | MM/HFT | — | Chicago; options MM |
| Balyasny (BAM) | USA | North America | Multi-mgr | — | Chicago; quant pods |
| Bridgewater | USA | North America | Systematic | — | Westport CT; systematic macro, not a GPU-ML story |
| Chicago Trading Co (CTC) | USA | North America | MM/HFT | — | Chicago; options |
| Citadel (hedge fund) | USA | North America | Multi-mgr | — | Miami/Chicago; distinct from Citadel Securities |
| Citadel Securities | USA | North America | MM/HFT | T3-003 | ★ Miami HQ; Google Cloud (1M+ cores) |
| Cumberland (DRW) | USA | North America | Crypto MM | — | Chicago; DRW's crypto arm |
| D.E. Shaw | USA | North America | Multi-mgr | — | ★ NYC; Anton supercomputers published (but molecular-dynamics research, not trading) |
| DRW | USA | North America | MM/HFT | — | Chicago; Vigilant Global towers (Layer 2) |
| ExodusPoint | USA | North America | Multi-mgr | — | NYC |
| Five Rings | USA | North America | MM/HFT | — | NYC |
| GTS | USA | North America | MM/HFT | — | NYC; NYSE DMM |
| Headlands Technologies | USA | North America | MM/HFT | — | Chicago |
| Hudson River Trading | USA | North America | MM/HFT | T3-011/012 | ★ NYC; Lefdal Mine (Norway) + cloud |
| Jane Street | USA | North America | MM/HFT | T3-009/010 | ★ NYC; Dallas GPU DC + CoreWeave |
| Jump Trading | USA | North America | MM/HFT | T3-015/016 | ★ Chicago; Vera Rubin + Carrollton TX |
| Millennium | USA | North America | Multi-mgr | — | NYC |
| Old Mission | USA | North America | MM/HFT | — | Chicago/NYC |
| PDT Partners | USA | North America | Systematic | — | NYC; ex-Morgan Stanley quant |
| Point72 / Cubist | USA | North America | Multi-mgr | — | ★ Stamford CT; Cubist systematic; public AI push |
| Quantlab | USA | North America | MM/HFT | — | Houston |
| Radix Trading | USA | North America | MM/HFT | — | Chicago |
| Renaissance Technologies | USA | North America | Systematic | T3-004 | East Setauket NY; 50k cores (firm-published), site scale undisclosed |
| Susquehanna (SIG) | USA | North America | MM/HFT | — | ★ Bala Cynwyd PA |
| Tower Research Capital | USA | North America | MM/HFT | — | NYC; shortwave (Alpine, Layer 2) |
| Two Sigma | USA | North America | Systematic | T3-013 | NYC; private DCs + Google Cloud |
| Virtu Financial | USA | North America | MM/HFT | — | NYC; New Line Networks towers (Layer 2) |
| Voleon Group | USA | North America | ML-native | — | ★ Berkeley CA; ML-first |
| Wolverine Trading | USA | North America | MM/HFT | — | Chicago |
| WorldQuant | USA | North America | Systematic | — | ★ Old Greenwich CT; alpha factory |
| Aspect Capital | UK | Europe | Systematic | — | London; CTA |
| Assenagon | Germany | Europe | Quant AM | — | Munich; ~€50bn; likely a documented null (not a GPU-ML/DC shop) |
| Cantab (GAM Systematic) | UK | Europe | Systematic | — | Cambridge |
| Capital Fund Management (CFM) | France | Europe | Systematic | — | ★ Paris; Bouchaud; academic-grade research compute |
| Flow Traders | Netherlands | Europe | MM/HFT | — | Amsterdam |
| Florin Court | UK | Europe | Systematic | — | London; alt-markets CTA |
| G-Research | UK | Europe | Systematic | T3-014 | London; multiple 8MW halls; Dallas infra hub |
| GSA Capital | UK | Europe | Systematic | — | London |
| IMC Trading | Netherlands | Europe | MM/HFT | — | ★ Amsterdam; shortwave (West Chicago, Layer 2) |
| Man Group (AHL/Numeric) | UK | Europe | Systematic | — | ★ London; public tech talks |
| Marshall Wace (TOPS) | UK | Europe | Systematic | — | London; signals engine |
| Optiver | Netherlands | Europe | MM/HFT | — | ★ Amsterdam |
| Quadrature Capital | UK | Europe | Systematic | — | London |
| Qube Research & Technologies | UK | Europe | Systematic | — | ★ London/Geneva; ex-Credit Suisse systematic, ~$28bn |
| Squarepoint Capital | UK | Europe | Systematic | — | London/Paris/NY |
| Systematica | Switzerland | Europe | Systematic | — | Geneva/Jersey |
| Winton | UK | Europe | Systematic | — | London |
| Wintermute | UK | Europe | Crypto MM | — | London; crypto, in scope |
| XTX Markets | UK | Europe | MM/HFT | T3-001/002/017 | London; Kajaani campus + Verne (Iceland) |
| Baiont Quant | China | Asia | ML-native | — | Nanjing; ML-first |
| High-Flyer / DeepSeek | China | Asia | Systematic + ML-native | T3-005/006 | Hangzhou; Fire-Flyer clusters + Ulanqab |
| Lingjun Investment (灵均) | China | Asia | Systematic | — | Beijing |
| Minghong (明汯) | China | Asia | Systematic | T3-008 | Shanghai; 1,500 GPU / 400 PFlops |
| Ubiquant (九坤) | China | Asia | Systematic | T3-007 | Beijing; Bei Ming cluster |
| Yanfu (衍复) | China | Asia | Systematic | — | Shanghai |
| Amber Group | Singapore | Asia | Crypto MM | — | Singapore/HK; crypto, in scope |

## Scope decisions (locked 2026-07-05)

1. **MM/HFT execution-only firms** — kept, and **researched for compute**;
   execution-only is recorded as a finding, not a reason to exclude.
2. **Crypto MM** — in scope.
3. **Separate legal entities** — kept split (Citadel LLC vs Citadel
   Securities, DRW vs Cumberland).
4. **China depth** — the ≥¥10bn "big tier" (~15–18 firms).
5. **Regional gaps** — India, Japan/Korea, and the Middle East are in scope;
   being enumerated. Rows land as the regional research completes.

_Table above is being extended with the enumerated regional firms._
