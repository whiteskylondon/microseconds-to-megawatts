# ENRICHMENT.md — candidate records for verification

Feed this to Claude Code. Workflow per CLAUDE.md: research each candidate,
attach a real evidence_url, geocode the address, then promote into
data/sites_seed.csv with the appropriate confidence grade. Do NOT bulk-add
without sources. Facts below are from working memory — treat all as
candidate-grade until verified.

## Tier 1 — execution (target: global venue coverage)

| candidate | why it matters | evidence trail |
|---|---|---|
| Equinix CH1/CH2, 350 E Cermak, Chicago | Historic heart of Chicago market data/connectivity; pre-Aurora CME home | Equinix docs, DCD archives |
| TMX Markham (Toronto) | Canadian equities matching | TMX colocation docs |
| B3 São Paulo (colo at Equinix SP) | LatAm anchor; proves Tier 1 exists where Tier 3 doesn't | B3 co-location docs |
| BMV Mexico City (KIO) | Second LatAm point | BMV tech docs |
| NSE Mumbai (BKC) | THE colocation-scandal case study (SEBI orders 2019+, tick-data access) | SEBI orders (public), press |
| BSE Mumbai | Completes India | BSE colo docs |
| KRX Busan | Korean derivatives matching; unusual non-capital location | KRX docs |
| SGX (Tier 1 DC, Singapore) | SE Asia hub; also FX ecosystem | SGX co-location docs |
| ASX Gordon (Sydney) | Australia; ALC data centre | ASX docs |
| TWSE Taipei | Adds Taiwan (semis resonance) | TWSE docs |
| JSE Johannesburg colo | Africa's only major colo ecosystem | JSE colocation docs |
| Tel Aviv TASE | Small but documented | TASE docs |
| FX layer: EBS (NY4/LD4/TY3), LSEG Matching (former Refinitiv) | FX matching is tri-site by design — great "follow the sun" visual | vendor docs |
| Moscow Exchange M1 (historical flag only) | Pre-2022 HFT destination; now sanctions case study | archive press |

## Tier 2 — network (target: arcs, not just points)

| candidate | why it matters | evidence trail |
|---|---|---|
| Full Chicago–NJ chain (McKay, New Line, Vigilant relays) | The signature arc set | FCC ULS Part 101 bulk data |
| Anova laser/mm-wave links: Mahwah–Carteret–Secaucus triangle | Metro-scale layer inside NJ | FCC + Anova marketing |
| Swingate/Dover + Dunkirk/Calais crossing sites | Completes Channel narrative with Richborough/Houtem | Ofcom, ANFR Cartoradio, Laumonier |
| London–Frankfurt relay chain (French + Belgian hops) | ANFR open data = French-sourced original work | ANFR bulk data (data.gouv.fr) |
| Tokyo–Osaka microwave corridor | Asia has a Tier 2 too; TSE-OSE arb | academic papers + press |
| Shortwave sites (Elgin/West Chicago area + counterparts) | The exotic frontier; Van Valzah's investigation | FCC experimental licenses |
| Hibernia Express/GTT transatlantic cable (landing points) | The one cable worth mapping: built for latency | press, submarine cable map |
| Quincy Data / DRW Aurora-area head-ends | Completes Aurora story | FCC ULS |

## Tier 3 — research (target: the global compute story)

| candidate | why it matters | evidence trail |
|---|---|---|
| High-Flyer / Fire-Flyer clusters (Hangzhou area) | ~10k A100s pre-export-controls; incubated DeepSeek. The finance-AI merger in one pin | Chinese + Western press, High-Flyer publications |
| Ubiquant + other large Chinese quant GPU clusters | Pattern, not anecdote | press, job ads |
| Jane Street GPU footprint | Major buyer; likely colo — job-ad triangulation | job postings, talks |
| Hudson River Trading research compute | Public engineering blog hints | HRT blog, job ads |
| Two Sigma DC history (NJ colo + cloud) | Long-documented compute culture | press, engineering blog |
| G-Research (UK) compute | Large UK ML fund; recruitment materials discuss cluster | job ads, press |
| Jump Trading GPU/HPC | Also crypto infra angle | press, job ads |
| XTX Kajaani building 2 | Expansion + Finnish electricity-tax review = policy hook | YIT announcement (collected), DCD |
| Verne Global Iceland campus (XTX + others) | The "compute follows power" origin story | Verne marketing, FT |
| Negative-space entries: LatAm=0, Africa=0 documented research compute | The absence IS the finding — consider explicit map annotation | (documented absence) |

## New schema needs

- `paths.csv` for Tier 2 arcs: origin/dest site_ids, operator, medium
  (microwave/mm-wave/laser/shortwave/fiber), evidence_url
- Consider `status` column: active / historical / under_construction
  (Basildon=historical, Kajaani bldg 2=under_construction, Moscow=historical)
- Consider `power_mw` numeric column for Tier 3 where public
