"""
Assemble verified enrichment-pass-1 records into the site/path CSVs.

Source: data/raw/enrichment_results.json — output of the research +
adversarial-verification workflow over ENRICHMENT.md candidates (each record
carries evidence URLs that a verifier agent re-fetched and confirmed).
Curation: PROMOTIONS/MERGES/ARCS below are hand-reviewed editorial decisions
(which verified records ship, with which confidence/precision corrections,
per the audit notes) — this script makes them reproducible, it does not
decide them.
Terms of use / rate limiting: only network access is via pipeline.geocode
(Nominatim, 1 req/s, cached in data/raw/geocode_cache.json).

Usage:
    python pipeline/assemble_enrichment.py          # rewrites data/*.csv
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from geocode import geocode  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "data" / "raw" / "enrichment_results.json"
RERUN = ROOT / "data" / "raw" / "tokyo_osaka_rerun.json"  # optional second input
SITES_CSV = ROOT / "data" / "sites_seed.csv"
PATHS_CSV = ROOT / "data" / "paths.csv"


def km(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return 6371 * 2 * math.asin(math.sqrt(a))


# ---------------------------------------------------------------------------
# Curated promotions: (site_id, candidate_key, record_index, overrides)
# overrides keys: any sites CSV column, plus ev=<evidence index for
# evidence_url> and note=<evidence_note text>.
# ---------------------------------------------------------------------------
PROMOTIONS = [
    # ---- Tier 1 ----
    ("T1-011", "equinix-ch1-cermak", 0, {
        "note": "Equinix CH4 IBX spec (address, floors, CME/ICE gateways); CME client wiki still lists 350 E Cermak among colo access facilities (Dec 2025)"}),
    ("T1-012", "tmx-markham", 0, {
        "note": "TMX Datalinx co-location services page; DC completion announced June 2010 (Canada Newswire)"}),
    ("T1-013", "b3-sao-paulo", 0, {
        "note": "B3 official co-location FAQ states 10 MW site power; PUMA matching + colo at Santana de Parnaiba"}),
    ("T1-014", "bmv-kio-mexico", 0, {
        "note": "BMV 2012 annual report places co-location in KIO Networks facilities; specific facility never publicly named — city-level pin"}),
    ("T1-015", "bmv-kio-mexico", 1, {
        "ev": 2,
        "note": "KIO operator pages: Santa Fe 2 (MEX 2) facility specs and BIVA customer page"}),
    ("T1-016", "nse-mumbai-bkc", 0, {
        "note": "NSE press release (Jan 2025): 1,200+ full-rack-equivalents at Exchange Plaza BKC; SEBI co-location case orders (2019) document the facility's unfair-access history"}),
    ("T1-017", "bse-mumbai", 0, {
        "note": "BSE colocation documents (bseindia.com) place the colo in P.J. Towers, Dalal Street"}),
    ("T1-018", "krx-busan", 0, {
        "note": "Koscom official pages: Busan data centre runs derivatives matching (Seoul/Busan centres back each other up)"}),
    ("T1-019", "krx-busan", 1, {
        "note": "Koscom Busan Proximity DC pages (opened June 2012, within 100 m of KRX derivatives computing centre); Colt Busan datasheet"}),
    ("T1-020", "sgx-tier1-dc", 0, {
        "coord_precision": "approximate",
        "note": "SGX news release (2015) for the SGX Data Centre; Keppel Digihub identification via DCD/industry databases — hence reported"}),
    ("T1-021", "asx-alc-gordon", 0, {
        "note": "ASX ALC service pages; opened Feb 2012 at Gore Hill (Artarmon), not Gordon as commonly misremembered"}),
    ("T1-022", "asx-alc-gordon", 1, {
        "power_mw": None,
        "note": "Cboe CXA connectivity manual: Cboe Australia matching engine in Equinix SY5; Baxtel lists 54MW whole-site design capacity (industry database, not venue-specific)"}),
    ("T1-023", "twse-taipei", 0, {
        "note": "TWSE official co-location pages; Banqiao DC opened Jan 2016 (NT$3.55bn), documented to road-intersection level only"}),
    ("T1-024", "jse-johannesburg", 0, {
        "note": "JSE colocation service pages + brochure: colo housed in the JSE building, One Exchange Square, Sandton (launched May 2014)"}),
    ("T1-025", "tase-tel-aviv", 0, {
        "note": "TASE Q2-2020 results announce colocation at TASE Data Centre; Electra (contractor) project page places the building at Ahuzat Bait 2"}),
    ("T1-026", "fx-ebs-lseg-trisite", 2, {
        "note": "LSEG FX venues colo connectivity guide (2026) + CME Globex Hub Tokyo page; ex-EBS Tokyo matching engine site, still Asia FX colo hub"}),
    ("T1-027", "fx-ebs-lseg-trisite", 3, {
        "note": "LSEG NDF Matching primary engine in SG3 per LSEG connectivity guide + May 2022 launch release"}),
    ("T1-028", "moex-m1-historical", 0, {
        "note": "MOEX colocation connectivity guide names DataSpace1 (primary DC + colo since Nov 2016); 9.5MW per DCD. Flagged historical: international HFT colo story ended with the 2022 sanctions exodus"}),
    ("T1-029", "moex-m1-historical", 1, {
        "note": "MOEX network access page + 2012-2015 trade press: M1 hosted MICEX-RTS/MOEX colo before the DataSpace1 move"}),

    # ---- Tier 2 ----
    ("T2-006", "chicago-nj-chain", 1, {
        "site_name": "World Class Wireless / New Line Networks Aurora antenna parcel",
        "lat": 41.7815, "lon": -88.2455,
        "firms_linked": "Jump Trading;Virtu (New Line Networks JV; World Class Wireless is the Jump-affiliated licensee)",
        "note": "Bloomberg (via Data Center Knowledge): 31-acre parcel bought for $14M across from the CME Aurora DC; antenna pole documented"}),
    ("T2-007", "chicago-nj-chain", 2, {
        "note": "Bloomberg (via DCK): 350-ft CyrusOne tower adjacent to the Aurora I/II halls, first antenna 2018; same campus as site T1-004"}),
    ("T2-008", "channel-swingate-dunkirk", 0, {
        "coord_precision": "exact",
        "note": "Kent HER designation record (OS grid ref TR 3347 4287) for the Chain Home towers; HFT dish tenants (McKay, Optiver, Jump) per Sniper in Mahwah fieldwork"}),
    ("T2-009", "channel-swingate-dunkirk", 1, {
        "evidence_type": "spectrum_license",
        "note": "ANFR-derived radio-site record (RNC Mobile, support 0590990306, 97m) + Sniper in Mahwah fieldwork on the Dunkerque Channel head-end"}),
    ("T2-010", "london-frankfurt-hops", 2, {
        "note": "Sniper in Mahwah (2016): McKay Brothers dishes on a Dunkerque port grain elevator; exact silo not identified — city-level pin"}),
    ("T2-011", "london-frankfurt-hops", 3, {
        "note": "Sniper in Mahwah (2016): Belgian end of Vigilant's proposed direct crossing to Richborough (Ofcom path data, Apr 2015 licenses); UK mast refused — historical"}),
    ("T2-012", "london-frankfurt-hops", 5, {
        "note": "Sniper in Mahwah / Visionscarto: preferred UK landing area for shorter Channel crossings; documented via 2014-2016 planning applications, individual masts not singly located"}),
    ("T2-013", "london-frankfurt-hops", 0, {
        "note": "Sniper in Mahwah V: ex-US Army DCS tower on the London-Frankfurt line; HFT dish colocations documented 2014-2015 via Belgian cadastre dossiers"}),
    ("T2-014", "london-frankfurt-hops", 8, {
        "note": "Sniper in Mahwah ('the last tower'): McKay dishes on the Norkring broadcast tower, documented Feb 2015"}),
    ("T2-015", "london-frankfurt-hops", 9, {
        "note": "Sniper in Mahwah II: three Jump-owned dishes photographed 2014, two pointing to Hannut"}),
    ("T2-016", "london-frankfurt-hops", 10, {
        "note": "Sniper in Mahwah II: hop on Jump's Belgian chain toward Frankfurt; Jump dishes + Optiver colocation via cadastre dossiers (2014)"}),
    ("T2-017", "london-frankfurt-hops", 11, {
        "note": "Sniper in Mahwah II: eastern Belgian hop toward Frankfurt; three competing operators within ~1 km (2014). German-side relays not yet mapped"}),
    ("T2-018", "shortwave-counterparts", 1, {
        "note": "Van Valzah Shortwave Trading II: coordinates from FCC experimental license (10Band LLC); 20kW transmitter, ERP 808kW, heading 48deg toward Europe"}),
    ("T2-019", "shortwave-counterparts", 2, {
        "confidence": "inferred",
        "note": "Van Valzah Shortwave Trading III: silo-top antennas near CME; licensee undisclosed — trading attribution triangulated, hence inferred"}),
    ("T2-020", "shortwave-counterparts", 3, {
        "note": "Van Valzah Shortwave Trading II: FCC-license coordinates (County Information Services LLC); 10kW, ERP 768kW toward Europe"}),
    ("T2-021", "shortwave-counterparts", 4, {
        "note": "Van Valzah Shortwave Trading III: legacy ARINC HF station reused (Skycast Services WI2XER per FCC filings)"}),
    ("T2-022", "shortwave-counterparts", 5, {
        "note": "FCC filings + drmna.info: WK2XJK (Rockland Wireless, Tower Research subsidiary) and WIPE (Turms Tech) at the Alpine Armstrong Tower"}),
    ("T2-023", "two-sigma-dc", 1, {
        "note": "PeeringDB: Two Sigma AS22175 lists this single facility (network forensics per evidence pipeline; interconnection presence only, not compute)"}),
    ("T2-024", "hibernia-express", 0, {
        "note": "submarinenetworks.com + TeleGeography: western landing of Hibernia Express (now EXA Express), built 2015 for NY-London latency (~58.95ms NY4-LD4 tested RTD)"}),
    ("T2-025", "hibernia-express", 1, {
        "note": "The Register on-site report confirms Brean landing station; TeleGeography landing-point record"}),

    # ---- Tier 3 ----
    ("T3-005", "high-flyer-fire-flyer", 0, {
        "note": "Operator-authored SC24 paper (arXiv 2408.14158): 10,000 PCIe A100s, ~3MW (<4MW); Reuters: RMB 1bn, built 2021, pre-export-ban; physical location not public — symbolic pin at Hangzhou HQ"}),
    ("T3-006", "ubiquant-chinese-quants", 1, {
        "note": "SCMP + Chinese tech press: DeepSeek job ads (Apr 2026) for data-centre delivery/O&M roles in Ulanqab, Inner Mongolia — job-ad triangulation"}),
    ("T3-007", "ubiquant-chinese-quants", 2, {
        "note": "China Fund interview (GM Wang Chen): >RMB 100m invested 2020 in 'Bei Ming' AI supercomputing cluster; location undisclosed — symbolic pin at Beijing HQ"}),
    ("T3-008", "ubiquant-chinese-quants", 3, {
        "note": "CLS.cn (Feb 2025) firm statement: thousands of GPUs, ~400 PFlops claimed; location undisclosed — symbolic pin at Shanghai HQ"}),
    ("T3-009", "jane-street-gpu", 0, {
        "ev": 1,
        "note": "Jane Street careers page: 4,032 liquid-cooled GPUs (with public video tour); Dallas location per DCD citing Bloomberg — city-level"}),
    ("T3-010", "jane-street-gpu", 1, {
        "note": "CoreWeave press release (Apr 2026): $6bn AI-cloud agreement incl. NVIDIA Vera Rubin 'across multiple facilities' — symbolic pin at NYC HQ"}),
    ("T3-011", "hrt-research-compute", 0, {
        "note": "HRT's own posts place AI research compute at Lefdal Mine Datacenter (Norway), >125kW/rack liquid-cooled; Dell press release corroborates the deployment"}),
    ("T3-012", "hrt-research-compute", 1, {
        "note": "Google Cloud press release (2024) + Lambda announcement (2026): HRT research compute on cloud GPU providers — symbolic pin at NYC HQ"}),
    ("T3-013", "two-sigma-dc", 0, {
        "evidence_type": "academic",
        "note": "USENIX ATC'18 / CMU ATLAS traces (Two Sigma co-authored): two private datacenters, 31,512 cores as of 2016; plus Google Cloud per TS engineering blog — symbolic pin at NYC HQ"}),
    ("T3-014", "g-research-uk", 0, {
        "coord_precision": "symbolic",
        "confidence": "inferred",
        "evidence_type": "job_posting",
        "ev": 2,
        "site_name": "G-Research ML compute (cluster locations undisclosed; London research lab)",
        "note": "G-Research's own (archived) job ads describe 'a global estate of data centres'; locations undisclosed — symbolic pin at the 1 Soho Place research lab"}),
    ("T3-015", "jump-hpc", 0, {
        "ev": 1,
        "note": "NVIDIA financial-services page + Jump's own posts: early Vera Rubin NVL72 deployment; cluster location undisclosed — symbolic pin at Chicago HQ"}),
    ("T3-016", "jump-hpc", 1, {
        "evidence_type": "job_posting",
        "note": "Jump's own job board (live Jul 2026): on-site HPC Data Center Technician in Carrollton, TX; high-density liquid-cooled cabinets — job-ad triangulation"}),
    ("T3-017", "xtx-kajaani-building2", 0, {
        "note": "YIT (contractor) press/investor releases + project page for XTX Kajaani data center 2; same Renforsin Ranta campus as T3-001; IT load not yet public"}),

    # From the Tokyo-Osaka re-run: the corridor premise is disproven (J-GATE
    # matches in Tokyo alongside arrowhead — no Osaka execution site); what
    # exists is JPX's Kansai BACKUP centre + proximity service.
    ("T1-030", "tokyo-osaka-rerun", 1, {
        "note": "JPX news releases (2021-2023): Kansai backup matching site (J-GATE3.0 2021, cash equities 2022) + Kansai Proximity Service at arrownet AP4; facility address not published — city-level"}),
]

# Merges into existing rows: site_id -> dict of column updates (applied last).
MERGES = {
    "T1-003": {
        "firms_linked": "Cboe equities/options matching; EBS Market NY FX engines (CME); LSEG FX venues colo; broad buy/sell-side ecosystem",
        "capacity_note": "Multi-tenant; Cboe US markets hosted here. EBS Market 'New York FX Spot'/'Metals' engines primary in NY5 (DR in Slough LD4.2); LSEG FX venue colo per 2026 connectivity guide.",
        "evidence_url": "https://cmegroupclientsite.atlassian.net/wiki/display/EPICSANDBOX/EBS+Market+on+CME+Globex+Market+Functionality",
    },
    "T1-005": {
        "firms_linked": "LSE Turquoise;Cboe Europe;EBS London matching (CME);LSEG Spot & Forwards Matching primary;broad ecosystem",
        "capacity_note": "Major European trading colo hub. LSEG (Refinitiv) Spot & Forwards Matching primary engine in LD4 since 2019 relocation; EBS London matching.",
        "evidence_url": "https://www.lseg.com/en/media-centre/press-releases/refinitiv/2019/may/refinitiv-enables-greater-cost-efficiencies-and-reduced-latency-for-customers-with-matching-and-fxall-migration",
    },
    "T1-004": {
        "_geocode": "2905 E Diehl Road, Aurora, IL 60502, USA",
    },
    "T2-001": {
        "status": "historical",
        "capacity_note": "Proposed ~322m Vigilant (DRW) Channel-path mast; refused by Dover District Council Jan 2017, Vigilant confirmed no appeal (Aug 2017). Mapped as a refused-proposal site, not an active mast.",
        "evidence_note": "Vigilant press release (no appeal) + Dover DC planning record via Sniper in Mahwah part 6",
        "evidence_url": "https://www.prnewswire.com/news-releases/vigilant-confirms-it-will-not-appeal-richborough-mast-planning-decision-300504911.html",
    },
    "T2-002": {
        "confidence": "reported",
        "capacity_note": "243m (800ft) ex-US-forces microwave tower bought by Jump for ~EUR 5m (2013) for the Channel microwave path.",
        "evidence_note": "Bloomberg (via Traders Magazine) on the tower purchase; Laumonier fieldwork",
        "evidence_url": "https://www.tradersmagazine.com/departments/brokerage/wall-street-grabs-nato-towers-in-traders-speed-of-light-quest/",
    },
    "T2-003": {
        "site_name": "McKay Brothers / Quincy Data Aurora head-end",
        "firms_linked": "quant/HFT subscriber base (Quincy Data = McKay market-data arm)",
        "capacity_note": "Chicago-side head-end of McKay's Aurora-NJ microwave route, live since July 2012; QED delivers Aurora-sourced CME data at Carteret in 3.982ms, Secaucus 4.015ms (operator-published).",
        "evidence_note": "Quincy Data global coverage page + launch/upgrade press releases",
        "evidence_url": "https://www.quincy-data.com/global-coverage",
        "_geocode": "2905 E Diehl Road, Aurora, IL 60502, USA",
    },
    "T2-004": {
        "firms_linked": "Toggle Communications LLC (FCC licensee; IMC B.V. real party of interest per Bloomberg)",
        "evidence_url": "https://sniperinmahwah.wordpress.com/2018/05/07/shortwave-trading-part-i-the-west-chicago-tower-mystery/",
        "evidence_note": "Van Valzah Shortwave Trading part I; Bloomberg follow-up (via DCK); FCC experimental license",
    },
    "T1-010": {
        "site_name": "JPX Primary Data Center (arrowhead + J-GATE), @Tokyo CC2",
        "operator_or_venue": "JPX (facility: AT TOKYO @Tokyo CC2 per Colt case study)",
        "lat": 35.6454, "lon": 139.7933,
        "coord_precision": "approximate",
        "capacity_note": "TSE arrowhead AND OSE/TOCOM J-GATE matching + colocation at one site (J-GATE median order latency 40us; colo-to-engine ~3us). Key finding: 'Osaka' derivatives match in Tokyo — TSE-OSE arbitrage is intra-data-center, hence no Tokyo-Osaka HFT microwave corridor exists.",
        "evidence_type": "exchange_docs",
        "evidence_note": "JPX FAQ/system pages (colo connects directly to arrowhead + J-GATE); Colt case study names @Tokyo CC2 (archived); PeeringDB fac/738 coords",
        "evidence_url": "https://www.jpx.co.jp/faq/system_relation.html",
        "confidence": "confirmed",
    },
    "T3-002": {
        "site_name": "Verne Global Keflavik campus (XTX Markets + HPC tenants)",
        "operator_or_venue": "Verne (campus operator)",
        "firms_linked": "XTX Markets;Nscale;other HPC/AI tenants",
        "lat": 63.9778, "lon": -22.5758,
        "coord_precision": "exact",
        "capacity_note": "Former NATO base at Asbru; operator states >140MW campus capacity, 100% hydro/geothermal. XTX's pre-Kajaani research cluster location per FT/press.",
        "power_mw": 140,
        "evidence_type": "operator_docs",
        "evidence_note": "Verne operator site (address, capacity); DCD expansion coverage; FT/press for XTX tenancy",
        "evidence_url": "https://www.verne.co/iceland",
        "confidence": "confirmed",
    },
}

# Arcs: (path_id, origin, dest, operator, medium, status, confidence, note, url)
ARCS = [
    ("P-001", "T2-003", "T1-001", "McKay Brothers", "microwave", "active", "confirmed",
     "Aurora-Mahwah leg of McKay's Chicago-NJ network (operator latency page)",
     "https://mckay-brothers.com/media"),
    ("P-002", "T2-003", "T1-002", "McKay Brothers / Quincy Data (QED)", "microwave", "active", "confirmed",
     "Aurora-Carteret: QED delivers CME data in 3.982ms (operator-published)",
     "https://www.prnewswire.com/news-releases/quincy-data-lowers-latency-with-mckay-brothers-upgrades-300942526.html"),
    ("P-003", "T2-003", "T1-003", "McKay Brothers / Quincy Data (QED)", "microwave", "active", "confirmed",
     "Aurora-Secaucus microwave route (launch release)",
     "https://www.prnewswire.com/news-releases/quincy-data-announces-launch-of-ultra-low-latency-wireless-service-between-aurora-and-secaucus-161388565.html"),
    ("P-004", "T1-004", "T1-002", "Webline Holdings (DRW)", "microwave", "active", "reported",
     "DRW-affiliated Aurora-NJ microwave route per Bloomberg",
     "https://www.datacenterknowledge.com/business/furious-land-war-erupts-outside-cme-data-center"),
    ("P-005", "T1-011", "T1-003", "McKay Brothers", "microwave", "active", "confirmed",
     "350 E Cermak to NY5: 3.885ms one-way (operator media page, 2015)",
     "https://mckay-brothers.com/media"),
    ("P-006", "T1-011", "T1-002", "McKay Brothers", "microwave", "active", "reported",
     "Cermak POP clients reach Carteret in 7.82ms round trip (A-Team Insight, 2014)",
     "https://a-teaminsight.com/blog/mckay-brothers-builds-out-low-latency-microwave-connectivity/"),
    ("P-007", "T1-004", "T1-011", "CME Group (Bulk Transport)", "fiber", "active", "reported",
     "CME fiber between Aurora and the old 350 E Cermak matching/colo centre",
     "https://a-teaminsight.com/blog/cmes-aurora-co-lo-quick-facts/?brand=tti"),
    ("P-008", "T1-001", "T1-012", "McKay Brothers", "microwave", "active", "confirmed",
     "Mahwah-Toronto(TMX) route on McKay's network (operator latency page)",
     "https://mckay-brothers.com/media"),
    ("P-009", "T1-004", "T1-012", "McKay Brothers", "microwave", "active", "confirmed",
     "Aurora-Toronto(TMX) route on McKay's network (operator latency page)",
     "https://mckay-brothers.com/media"),
    ("P-010", "T1-013", "T1-002", "Seaborn Networks (SeaSpeed)", "fiber", "active", "confirmed",
     "Low-latency B3-Nasdaq Carteret route on Seabras-1 (operator product page)",
     "https://seabornnetworks.com/products/seaspeed/"),
    ("P-011", "T1-013", "T1-004", "Seaborn Networks + Anova Financial Networks", "fiber", "active", "confirmed",
     "B3-CME route (Seaborn/Anova partnership announcement)",
     "https://seabornnetworks.com/seaborn-networks-and-anova-financial-networks-partner-to-deliver-ultra-low-latency-route-between-b3-and-cme/"),
    ("P-012", "T1-014", "T1-003", "Grupo BMV (Equinix NY5 POP)", "fiber", "active", "confirmed",
     "BMV market-data/connectivity POP at Equinix NY (BMV vendors price list)",
     "https://www.bmv.com.mx/work/models/Grupo_BMV/Resource/2000/28/images/2024%20Vendors%20Price%20List%20V1.pdf"),
    ("P-013", "T1-020", "T1-009", "BSO", "fiber", "active", "confirmed",
     "SGX-HKEX low-latency route marketed by BSO (operator page)",
     "https://www.bso.co/all-insights/low-latency-hkex-sgx-traders"),
    ("P-014", "T1-021", "T1-022", "Cboe Australia (Cboe Connect) / Nexthop dark fibre", "fiber", "active", "confirmed",
     "ALC-SY5 connectivity per Cboe CXA connectivity manual",
     "https://cdn.cboe.com/resources/membership/CXA_Connectivity_Manual.pdf"),
    ("P-015", "T1-005", "T1-003", "LSEG (Refinitiv) Spot & Forwards Matching", "fiber", "active", "confirmed",
     "LD4 primary / NY4 venue pair per LSEG FX colo connectivity guide",
     "https://thesource.lseg.com/TheSource/getfile/download/840e069d-969a-4b99-b663-1a67046ab6ed"),
    ("P-016", "T1-003", "T1-005", "CME Group (EBS Market on Globex)", "fiber", "active", "confirmed",
     "EBS NY engines primary in NY5, DR in Slough LD4.2 (CME client wiki)",
     "https://cmegroupclientsite.atlassian.net/wiki/display/EPICSANDBOX/EBS+Market+on+CME+Globex+Market+Functionality"),
    ("P-017", "T1-026", "T1-003", "CME Group (Globex Hub Tokyo)", "fiber", "active", "confirmed",
     "TY3 Globex hub to NY (CME client wiki)",
     "https://cmegroupclientsite.atlassian.net/wiki/display/EPICSANDBOX/CME+Globex+Hub+-+Tokyo"),
    ("P-018", "T1-027", "T1-005", "LSEG NDF Matching", "fiber", "active", "confirmed",
     "SG3 NDF Matching primary; LD4 in the venue mesh (LSEG connectivity guide)",
     "https://thesource.lseg.com/TheSource/getfile/download/840e069d-969a-4b99-b663-1a67046ab6ed"),
    ("P-019", "T1-005", "T1-028", "Avelacom (MOEX international PoP program)", "fiber", "historical", "confirmed",
     "London-Moscow low-latency route for MOEX access (MOEX announcement); historical post-2022",
     "https://www.moex.com/n23779"),
    ("P-020", "T1-001", "T1-002", "Anova Financial Networks", "laser", "active", "confirmed",
     "Mahwah-Carteret free-space-optics link (trade press on Anova activation)",
     "https://www.fibre-systems.com/news/free-space-optics-speed-stock-exchange"),
    ("P-021", "T1-002", "T1-003", "Anova Financial Networks", "laser", "active", "reported",
     "Carteret-Secaucus laser link (A-Team Insight)",
     "https://a-teaminsight.com/blog/anova-goes-live-with-low-latency-laser-link-between-nasdaq-and-nyse/"),
    ("P-022", "T1-001", "T1-003", "Anova Financial Networks", "laser", "active", "confirmed",
     "Mahwah-Secaucus wireless link (Anova press release)",
     "https://www.prnewswire.com/news-releases/anova-financial-networks-activates-wireless-connectivity-between-mahwah-and-secaucus-301209914.html"),
    ("P-023", "T2-008", "T2-002", "Jump Trading", "microwave", "active", "reported",
     "Swingate-Houtem Channel crossing (Sniper in Mahwah II)",
     "https://sniperinmahwah.wordpress.com/2014/09/25/hft-in-my-backyard-ii/"),
    ("P-024", "T2-009", "T2-008", "multiple HFT operators", "microwave", "active", "reported",
     "Dunkerque(Reuze)-Swingate crossing used by most Channel competitors (Laumonier)",
     "https://sniperinmahwah.wordpress.com/2014/09/25/hft-in-my-backyard-ii/"),
    ("P-025", "T1-005", "T1-006", "McKay Brothers International", "microwave", "active", "confirmed",
     "Slough-Frankfurt microwave route launch (operator release)",
     "https://www.prnewswire.com/news-releases/mckay-brothers-launches-route-between-slough-frankfurt-289533021.html"),
    ("P-026", "T2-002", "T2-012", "Jump Trading", "microwave", "active", "reported",
     "Houtem-Ramsgate crossing (Sniper in Mahwah I)",
     "https://sniperinmahwah.wordpress.com/2014/09/22/hft-in-my-backyard-part-i/"),
    ("P-027", "T2-015", "T2-016", "Jump Trading", "microwave", "active", "reported",
     "Wavre-Hannut hop on Jump's Belgian chain (dish azimuths documented)",
     "https://sniperinmahwah.wordpress.com/2014/09/25/hft-in-my-backyard-ii/"),
    ("P-028", "T2-009", "T2-012", "McKay Brothers; Optiver", "microwave", "active", "reported",
     "Dunkerque-Ramsgate crossing (Visionscarto/Laumonier)",
     "https://www.visionscarto.net/hft-in-the-jungle"),
    ("P-029", "T2-011", "T2-001", "Vigilant Global (DRW)", "microwave", "historical", "reported",
     "Proposed Oostduinkerke-Richborough direct crossing; UK mast refused 2017",
     "https://sniperinmahwah.wordpress.com/2016/01/26/hft-in-the-banana-land/"),
    ("P-030", "T2-004", "T1-004", "Toggle Communications (IMC)", "microwave", "active", "reported",
     "West Chicago site's dish aimed at CME Aurora (Van Valzah/Bloomberg)",
     "https://sniperinmahwah.wordpress.com/2018/05/07/shortwave-trading-part-i-the-west-chicago-tower-mystery/"),
    ("P-031", "T2-020", "T1-004", "County Information Services LLC", "microwave", "active", "inferred",
     "Wanatah site backhaul toward Aurora (inferred from Van Valzah fieldwork)",
     "https://sniperinmahwah.wordpress.com/2018/06/07/shortwave-trading-part-ii-faq-and-other-chicago-area-sites/"),
    ("P-032", "T2-019", "T1-004", "undisclosed FCC experimental licensee", "microwave", "active", "reported",
     "Maple Park silo dish pointed at CME Aurora (Van Valzah part III)",
     "https://sniperinmahwah.wordpress.com/2018/07/13/shortwave-trading-part-iii-fourth-chicago-site-east-coast-sites-europe-and-questions/"),
    ("P-033", "T1-004", "T1-006", "Raft Technologies", "shortwave", "active", "confirmed",
     "Chicago-Frankfurt HF service route (operator page; endpoints are served venues, not antenna sites)",
     "https://raft-tech.com/hf_shortwave-adoption/"),
    ("P-034", "T1-004", "T1-005", "Raft Technologies", "shortwave", "active", "confirmed",
     "Chicago-London HF service route (operator page; endpoints are served venues, not antenna sites)",
     "https://raft-tech.com/hf_shortwave-adoption/"),
    ("P-035", "T1-004", "T1-010", "Raft Technologies", "shortwave", "active", "confirmed",
     "Chicago-Tokyo HF service route (operator page; endpoints are served venues, not antenna sites)",
     "https://raft-tech.com/hf_shortwave-adoption/"),
    ("P-036", "T2-024", "T2-025", "EXA Infrastructure (ex Hibernia/GTT)", "fiber", "active", "reported",
     "Hibernia Express (EXA Express): 4,600km latency-optimized transatlantic cable",
     "https://www.submarinecablemap.com/api/v3/cable/exa-express.json"),
    ("P-037", "T1-003", "T2-024", "EXA Infrastructure (ex Hibernia/GTT)", "fiber", "active", "reported",
     "NY-side backhaul: cable marketed as NY4 Secaucus-LD4 Slough sub-59ms RTD",
     "https://www.lightwaveonline.com/network-design/high-speed-networks/article/16651312/hibernia-express-transatlantic-cable-ready-for-service"),
    ("P-038", "T2-025", "T1-005", "EXA Infrastructure (ex Hibernia/GTT)", "fiber", "active", "reported",
     "UK-side backhaul from Brean to Slough LD4 (sub-59ms NY4-LD4 marketed RTD)",
     "https://www.lightwaveonline.com/network-design/high-speed-networks/article/16651312/hibernia-express-transatlantic-cable-ready-for-service"),
    ("P-039", "T1-010", "T1-030", "JPX (arrownet)", "fiber", "active", "confirmed",
     "Exchange-operated WDM fiber ring linking the Tokyo primary centre with the Kansai backup/proximity site",
     "https://www.jpx.co.jp/systems/network/index.html"),
]

CAP_NOTE_MAX = 400


def build_row(site_id, rec, ov):
    ev_idx = ov.pop("ev", 0)
    evidence = rec["evidence"][ev_idx]
    cap = rec.get("capacity_note") or ""
    if len(cap) > CAP_NOTE_MAX:
        cap = cap[:CAP_NOTE_MAX - 1].rsplit(" ", 1)[0] + "…"
    row = {
        "site_id": site_id,
        "site_name": rec["site_name"],
        "tier": rec["tier"],
        "operator_or_venue": rec["operator_or_venue"],
        "firms_linked": rec["firms_linked"],
        "lat": rec.get("lat"),
        "lon": rec.get("lon"),
        "coord_precision": rec["coord_precision"],
        "city": rec["city"],
        "country": rec["country"],
        "capacity_note": cap,
        "power_mw": rec.get("power_mw"),
        "status": rec["status"],
        "evidence_type": rec["evidence_type"],
        "evidence_note": ov.pop("note", f"{evidence['publisher']}: {evidence['supports']}"[:200]),
        "evidence_url": evidence["url"],
        "confidence": rec["confidence"],
        "verify_url_hint": None,
        "_address": rec.get("address"),
    }
    row.update(ov)
    return row


def main():
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    by_key = {r["candidate_key"]: r for r in data["results"]}
    if RERUN.exists():
        rerun = json.loads(RERUN.read_text(encoding="utf-8"))
        by_key[rerun["candidate_key"]] = rerun

    rows = []
    for site_id, key, idx, ov in PROMOTIONS:
        rec = by_key[key]["final"]["records"][idx]
        rows.append(build_row(site_id, rec, dict(ov)))

    # Geocode documented addresses; adopt the geocoded point when it agrees
    # with the researcher's placement (<2.5km), otherwise keep and note.
    for row in rows:
        addr = row.pop("_address", None)
        if not addr or row["coord_precision"] in ("symbolic", "city_level"):
            continue
        hit = geocode(addr)
        if not hit:
            print(f"  geocode MISS: {row['site_id']} {addr!r}")
            continue
        if row["lat"] is None or km(row["lat"], row["lon"], hit["lat"], hit["lon"]) < 2.5:
            row["lat"], row["lon"] = round(hit["lat"], 5), round(hit["lon"], 5)
        else:
            print(f"  geocode DISAGREES (> 2.5km), keeping researcher coords: "
                  f"{row['site_id']} {addr!r} -> {hit['lat']:.4f},{hit['lon']:.4f}")

    sites = pd.read_csv(SITES_CSV, dtype=str)
    # Idempotent re-runs: drop previously assembled versions of promoted ids.
    sites = sites[~sites.site_id.isin({p[0] for p in PROMOTIONS})]
    new_df = pd.DataFrame(rows)[list(sites.columns)]
    sites = pd.concat([sites, new_df.astype(str).replace({"None": "", "nan": ""})],
                      ignore_index=True)

    for site_id, updates in MERGES.items():
        updates = dict(updates)
        addr = updates.pop("_geocode", None)
        if addr:
            hit = geocode(addr)
            if hit:
                updates["lat"], updates["lon"] = round(hit["lat"], 5), round(hit["lon"], 5)
        mask = sites.site_id == site_id
        assert mask.any(), f"merge target {site_id} not found"
        for col, val in updates.items():
            sites.loc[mask, col] = str(val)

    sites = sites.sort_values("site_id").reset_index(drop=True)
    sites.to_csv(SITES_CSV, index=False)

    paths = pd.DataFrame(ARCS, columns=[
        "path_id", "origin_site_id", "dest_site_id", "operator", "medium",
        "status", "confidence", "evidence_note", "evidence_url"])
    known = set(sites.site_id)
    refs = set(paths.origin_site_id) | set(paths.dest_site_id)
    assert refs <= known, f"unknown arc endpoints: {sorted(refs - known)}"
    paths.to_csv(PATHS_CSV, index=False)

    print(f"sites: {len(sites)} records ({sites.tier.value_counts().to_dict()})")
    print(f"paths: {len(paths)} arcs")


if __name__ == "__main__":
    main()
