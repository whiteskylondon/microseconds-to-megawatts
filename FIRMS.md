# FIRMS.md — the firm universe

The universe of quant/HFT firms worth considering for the map — **137 firms**
(11 already mapped, 126 candidates), to agree before per-firm compute research.
One flat list; classification lives in the fields, not in sections. Each row
carries a public `source_url` in `data/raw/firm_enumeration.json`; the regional
sweep (China ≥¥10bn tier, India, Japan/Korea, Middle East, plus a Western-gap
and rest-of-world pass) is captured there.

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
- **website** — official homepage (verified; `—` where none is public, e.g.
  a defunct firm)
- **notes** — HQ city, compute signal, caveats. `★` = best public-paper-trail
  odds (suggested for the first research pass).

Mapping question per firm: *is there a public paper trail for its
research/ML compute* (announcement, contractor/grid filing, planning record,
job ad, vendor case study)? Every firm here — including the `MM/HFT` market
makers whose main footprint is exchange colocation (Layer 1) — is in scope for
a compute (Layer 3) research pass; where a firm turns out to be execution-only,
that's recorded as the finding.

## The universe

| firm | country | continent | firm_type | mapped | website | notes |
|---|---|---|---|---|---|---|
| Akuna Capital | USA | North America | MM/HFT | — | [akunacapital.com](https://akunacapital.com) | Chicago; options MM |
| AQR Capital | USA | North America | Quant AM | — | [aqr.com](https://www.aqr.com) | Greenwich CT; factor/risk-premia, more CPU than GPU |
| Aquatic Capital Management | United States | North America | Systematic | — | [aquatic.com](https://www.aquatic.com) | Chicago; none public (high-performance R&D platform stated; no DC/GPU disclosure) |
| Arrowstreet Capital | United States | North America | Quant AM | — | [arrowstreetcapital.com](https://www.arrowstreetcapital.com) | Boston; none public |
| Balyasny (BAM) | USA | North America | Multi-mgr | — | [bamfunds.com](https://www.bamfunds.com) | Chicago; quant pods |
| Belvedere Trading | United States | North America | MM/HFT | — | [belvederetrading.com](https://www.belvederetrading.com) | Chicago; execution-only |
| Bridgewater | USA | North America | Systematic | — | [bridgewater.com](https://www.bridgewater.com) | Westport CT; systematic macro, not a GPU-ML story |
| Castle Ridge Asset Management | Canada | North America | ML-native | — | [castleridgemgt.com](https://castleridgemgt.com) | ★ Toronto; on-prem AI supercomputer 'WALLACE' publicly announced (2023): fluorinert liquid-cooled proprietary system, datacentre-level cooling;… |
| Chicago Trading Co (CTC) | USA | North America | MM/HFT | — | [chicagotrading.com](https://www.chicagotrading.com) | Chicago; options |
| Citadel (hedge fund) | USA | North America | Multi-mgr | — | [citadel.com](https://www.citadel.com) | Miami/Chicago; distinct from Citadel Securities |
| Citadel Securities | USA | North America | MM/HFT | T3-003 | [citadelsecurities.com](https://www.citadelsecurities.com) | ★ Miami HQ; Google Cloud (1M+ cores) |
| Cumberland (DRW) | USA | North America | Crypto MM | — | [cumberland.io](https://www.cumberland.io) | Chicago; DRW's crypto arm |
| D.E. Shaw | USA | North America | Multi-mgr | — | [deshaw.com](https://www.deshaw.com) | ★ NYC; Anton supercomputers published (but molecular-dynamics research, not trading) |
| DRW | USA | North America | MM/HFT | — | [drw.com](https://www.drw.com) | Chicago; Vigilant Global towers (Layer 2) |
| Eagle Seven | United States | North America | MM/HFT | — | [eagleseven.com](https://www.eagleseven.com) | Chicago; execution-only |
| Eladian Partners | United States | North America | MM/HFT | — | — | New York; execution-only |
| Engineers Gate | United States | North America | Systematic | — | [eglp.com](https://www.eglp.com) | New York; none public |
| ExodusPoint | USA | North America | Multi-mgr | — | [exoduspoint.com](https://www.exoduspoint.com) | NYC |
| Five Rings | USA | North America | MM/HFT | — | [fiverings.com](https://fiverings.com) | NYC |
| Graham Capital Management | United States | North America | Systematic | — | [grahamcapital.com](https://www.grahamcapital.com) | Rowayton; none public |
| Group One Trading | United States | North America | MM/HFT | — | [group1.com](https://group1.com) | Chicago; execution-only |
| GTS | USA | North America | MM/HFT | — | [gtsx.com](https://gtsx.com) | NYC; NYSE DMM |
| Hard Eight Trading | United States | North America | MM/HFT | — | [hard8trading.com](https://www.hard8trading.com) | Chicago; execution-only |
| Headlands Technologies | USA | North America | MM/HFT | — | [headlandstech.com](https://headlandstech.com) | Chicago |
| Hudson River Trading | USA | North America | MM/HFT | T3-011/012 | [hudsonrivertrading.com](https://www.hudsonrivertrading.com) | ★ NYC; Lefdal Mine (Norway) + cloud |
| Jane Street | USA | North America | MM/HFT | T3-009/010 | [janestreet.com](https://www.janestreet.com) | ★ NYC; Dallas GPU DC + CoreWeave |
| Jump Trading | USA | North America | MM/HFT | T3-015/016 | [jumptrading.com](https://www.jumptrading.com) | ★ Chicago; Vera Rubin + Carrollton TX |
| Millburn Ridgefield | United States | North America | ML-native | — | [millburn.com](https://millburn.com) | New York; none public (statistical-learning framework stated; no DC/GPU disclosure) |
| Millennium | USA | North America | Multi-mgr | — | [mlp.com](https://www.mlp.com) | NYC |
| Old Mission | USA | North America | MM/HFT | — | [oldmissioncapital.com](https://www.oldmissioncapital.com) | Chicago/NYC |
| PDT Partners | USA | North America | Systematic | — | [pdtpartners.com](https://pdtpartners.com) | NYC; ex-Morgan Stanley quant |
| PEAK6 Capital Management | United States | North America | MM/HFT | — | [peak6.com](https://peak6.com) | Austin; execution-only |
| Point72 / Cubist | USA | North America | Multi-mgr | — | [point72.com](https://point72.com) | ★ Stamford CT; Cubist systematic; public AI push |
| Quantitative Investment Management (QIM) | United States | North America | ML-native | — | [quantitative.com](https://quantitative.com) | Charlottesville; none public (ML-forward stated; no DC/GPU disclosure) |
| Quantlab | USA | North America | MM/HFT | — | [quantlab.com](https://www.quantlab.com) | Houston |
| Radix Trading | USA | North America | MM/HFT | — | [radixtrading.co](https://radixtrading.co) | Chicago |
| Renaissance Technologies | USA | North America | Systematic | T3-004 | [rentec.com](https://www.rentec.com) | East Setauket NY; 50k cores (firm-published), site scale undisclosed |
| SBB Research Group | United States | North America | Systematic | — | [sbbrg.com](https://www.sbbrg.com) | Northbrook; none public |
| Schonfeld Strategic Advisors | United States | North America | Multi-mgr | — | [schonfeld.com](https://www.schonfeld.com) | New York; none public |
| Susquehanna (SIG) | USA | North America | MM/HFT | — | [sig.com](https://sig.com) | ★ Bala Cynwyd PA |
| Teza Technologies (Teza Group) | United States | North America | Systematic | — | [teza.com](https://www.teza.com) | Chicago; none public (alt-data / quant research stated; no DC/GPU disclosure) |
| TGS Management | United States | North America | Systematic | — | [tgsmc.com](https://www.tgsmc.com) | Irvine; none public |
| Tower Research Capital | USA | North America | MM/HFT | — | [tower-research.com](https://tower-research.com) | NYC; shortwave (Alpine, Layer 2) |
| Two Sigma | USA | North America | Systematic | T3-013 | [twosigma.com](https://www.twosigma.com) | NYC; private DCs + Google Cloud |
| Vatic Labs (Vatic Investments) | United States | North America | MM/HFT | — | [vaticlabs.ai](https://www.vaticlabs.ai) | ★ New York; AI/ML research signal (autonomous trading agents, continuous-learning models per company site); no public DC/GPU disclosure |
| Verition Fund Management | United States | North America | Multi-mgr | — | [verition.com](https://www.verition.com) | Greenwich; none public |
| Virtu Financial | USA | North America | MM/HFT | — | [virtu.com](https://www.virtu.com) | NYC; New Line Networks towers (Layer 2) |
| Voleon Group | USA | North America | ML-native | — | [voleon.com](https://voleon.com) | ★ Berkeley CA; ML-first |
| Walleye Capital | United States | North America | Multi-mgr | — | [walleyecapital.com](https://walleyecapital.com) | New York; none public |
| Wolverine Trading | USA | North America | MM/HFT | — | [wolve.com](https://www.wolve.com) | Chicago |
| WorldQuant | USA | North America | Systematic | — | [worldquant.com](https://www.worldquant.com) | ★ Old Greenwich CT; alpha factory |
| XR Trading | United States | North America | MM/HFT | — | [xrtrading.com](https://www.xrtrading.com) | Chicago; execution-only |
| Aspect Capital | UK | Europe | Systematic | — | [aspectcapital.com](https://www.aspectcapital.com) | London; CTA |
| Assenagon | Germany | Europe | Quant AM | — | [assenagon.com](https://www.assenagon.com) | Munich; ~€50bn; likely a documented null (not a GPU-ML/DC shop) |
| Cantab (GAM Systematic) | UK | Europe | Systematic | — | [gam.com](https://www.gam.com/en/our-capabilities/gam-cantab) | Cambridge |
| Capital Fund Management (CFM) | France | Europe | Systematic | — | [cfm.fr](https://www.cfm.fr) | ★ Paris; Bouchaud; academic-grade research compute |
| Da Vinci Trading (Da Vinci Derivatives) | Netherlands | Europe | MM/HFT | — | [davincitrading.com](https://davincitrading.com) | Amsterdam; execution-only |
| Florin Court | UK | Europe | Systematic | — | [florincourt.com](https://florincourt.com) | London; alt-markets CTA |
| Flow Traders | Netherlands | Europe | MM/HFT | — | [flowtraders.com](https://www.flowtraders.com) | Amsterdam |
| G-Research | UK | Europe | Systematic | T3-014 | [gresearch.com](https://www.gresearch.com) | London; multiple 8MW halls; Dallas infra hub |
| GSA Capital | UK | Europe | Systematic | — | [gsacapital.com](https://www.gsacapital.com) | London |
| IMC Trading | Netherlands | Europe | MM/HFT | — | [imc.com](https://www.imc.com) | ★ Amsterdam; shortwave (West Chicago, Layer 2) |
| Man Group (AHL/Numeric) | UK | Europe | Systematic | — | [man.com](https://www.man.com) | ★ London; public tech talks |
| Marshall Wace (TOPS) | UK | Europe | Systematic | — | [mwam.com](https://www.mwam.com) | London; signals engine |
| Maven Securities | United Kingdom | Europe | MM/HFT | — | [mavensecurities.com](https://www.mavensecurities.com) | London; execution-only |
| Optiver | Netherlands | Europe | MM/HFT | — | [optiver.com](https://www.optiver.com) | ★ Amsterdam |
| Quadrature Capital | UK | Europe | Systematic | — | [quadrature.ai](https://www.quadrature.ai) | London |
| Quantica Capital | Switzerland | Europe | Systematic | — | [quantica-capital.com](https://quantica-capital.com) | Zurich; none public |
| Qube Research & Technologies | UK | Europe | Systematic | — | [qube-rt.com](https://www.qube-rt.com) | ★ London/Geneva; ex-Credit Suisse systematic, ~$28bn |
| RSJ Securities | Czech Republic | Europe | MM/HFT | — | [rsj.com](https://www.rsj.com) | Prague; execution-only |
| Squarepoint Capital | UK | Europe | Systematic | — | [squarepoint-capital.com](https://www.squarepoint-capital.com) | London/Paris/NY |
| Systematica | Switzerland | Europe | Systematic | — | [systematica.com](https://www.systematica.com) | Geneva/Jersey |
| Wintermute | UK | Europe | Crypto MM | — | [wintermute.com](https://www.wintermute.com) | London; crypto, in scope |
| Winton | UK | Europe | Systematic | — | [winton.com](https://www.winton.com) | London |
| XTX Markets | UK | Europe | MM/HFT | T3-001/002/017 | [xtxmarkets.com](https://www.xtxmarkets.com) | London; Kajaani campus + Verne (Iceland) |
| AlphaGrep Securities | India | Asia | MM/HFT | — | [alpha-grep.com](https://www.alpha-grep.com) | Mumbai; none public |
| Amber Group | Singapore | Asia | Crypto MM | — | [ambergroup.io](https://www.ambergroup.io) | Singapore/HK; crypto, in scope |
| APT Portfolio (A.P.T. Portfolio) | India | Asia | MM/HFT | — | [aptportfolio.com](https://aptportfolio.com) | New Delhi; none public (ML/technology emphasis stated, no DC/GPU disclosure) |
| Auros | Hong Kong | Asia | Crypto MM | — | [auros.global](https://www.auros.global) | Hong Kong; execution-only |
| Baiont Quant | China | Asia | ML-native | — | [baiont.ai](https://baiont.ai) | Nanjing; ML-first |
| Blackwing Asset Management (黑翼资产) | China | Asia | Systematic | — | [blackwingasset.com](https://www.blackwingasset.com) | ★ Shanghai; Founder describes full-process AI from signal discovery to model construction, using LLMs to parse text data; recruits ML researchers with… |
| Century Frontier Asset Management (世纪前沿) | China | Asia | Systematic | — | [centuryfrontier.com](https://www.centuryfrontier.com) | ★ Shenzhen; Recruits quant researchers (Python/C++, 3yr+); part of 2025 quant-AI hiring wave. No public DC/GPU quantification. |
| Chengqi Asset Management (诚奇资产) | China | Asia | ML-native | — | [cqfunds.com](https://www.cqfunds.com) | ★ Shenzhen; Publicly stated 2023 shift to an ML-centred non-linear modelling framework; ~80% of ~80 staff are R&D/IT across Beijing/Shenzhen/Shanghai.… |
| Dharma Capital (ダルマ・キャピタル株式会社) | Japan | Asia | MM/HFT | — | [dharmacapital.co.jp](https://www.dharmacapital.co.jp) | Tokyo; execution-only (JPX/PTS co-location, latency-first) plus a notable public R&D signal: 2021 joint experiment with Toshiba applying the… |
| Dolat Capital | India | Asia | MM/HFT | — | [dolatcapital.com](https://www.dolatcapital.com) | Mumbai; none public |
| Eclipse Trading | Hong Kong | Asia | MM/HFT | — | [eclipsetrading.com](https://www.eclipsetrading.com) | Hong Kong; execution-only |
| Estee Advisors | India | Asia | Quant AM | — | [esteeadvisors.com](https://esteeadvisors.com) | Gurugram; execution-only |
| Evolution Asset Management (进化论资产) | China | Asia | Systematic | — | [jhlfund.com](https://www.jhlfund.com) | Shanghai; none public |
| Fount (파운트) | South Korea | Asia | Quant AM | — | [fount.co](https://fount.co) | ★ Seoul; ML-based platform: robo-advisor engine using ML + asset-allocation algorithms with dynamic rebalancing; Series C ($33.4m, 2021) to develop the… |
| GCI Asset Management (株式会社GCIアセット・マネジメント) | Japan | Asia | Systematic | — | [gci.jp](https://www.gci.jp) | ★ Tokyo; Public ML/AI signal: firm turned a refurbished Kyoto temple into a big-data / AI research lab (Bloomberg, 2019); markets itself as translating… |
| Genk Capital | Singapore | Asia | MM/HFT | — | [genkcapital.com](https://genkcapital.com) | Singapore; none public |
| Grasshopper | Singapore | Asia | MM/HFT | — | [grasshopperasia.com](https://grasshopperasia.com) | ★ Singapore; Cloud/ML compute — public Google Cloud customer case study describes using cloud CPU/GPU scale-out to develop quant signals and expand ML… |
| Graviton Research Capital | India | Asia | MM/HFT | — | [gravitontrading.com](https://www.gravitontrading.com) | ★ Gurugram; HPC job ads — public HPC Engineer / ML Researcher postings; in-house high-performance clusters |
| GSR | Hong Kong | Asia | Crypto MM | — | [gsr.io](https://www.gsr.io) | Hong Kong; execution-only |
| High-Flyer / DeepSeek | China | Asia | Systematic + ML-native | T3-005/006 | [high-flyer.cn](https://www.high-flyer.cn) | Hangzhou; Fire-Flyer clusters + Ulanqab |
| Inno Asset Management (因诺资产) | China | Asia | Systematic | — | [innoam.com](http://www.innoam.com) | ★ Beijing; Publicly cited (with Ubiquant) as among first Chinese quants to build out AI teams and compete for AI talent; ~116-person team. No DC/GPU… |
| iRage (iRageCapital Advisory) | India | Asia | MM/HFT | — | [irage.in](https://irage.in) | Mumbai; none public |
| Jinge Liangrui (金戈量锐) | China | Asia | Systematic | — | [jingefund.com](http://jingefund.com) | Ningbo; none public |
| Lingjun Investment (灵均) | China | Asia | Systematic | — | [lingjuninvest.com](https://www.lingjuninvest.com) | Beijing |
| Linitics | Singapore | Asia | MM/HFT | — | [linitics.com](https://linitics.com) | Singapore; none public |
| Longqi Technology (龙旗科技) | China | Asia | Systematic | — | [sci-inv.com](https://sci-inv.com) | ★ Hangzhou; Job ads for 'AI Lab researcher' / 'AI algorithm engineer' on financial time-series prediction, alpha-factor mining and portfolio… |
| Minghong (明汯) | China | Asia | Systematic | T3-008 | [mhfunds.com](https://www.mhfunds.com) | Shanghai; 1,500 GPU / 400 PFlops |
| Mingshi Fund (鸣石基金) | China | Asia | Systematic | — | [mingshiim.com](https://www.mingshiim.com) | ★ Shanghai; Founder frames strategy around 'AI and continuous innovation'; model system blends linear and non-linear. No DC/GPU disclosure. |
| Mingshi Investment (Mengxi) (蒙玺投资) | China | Asia | MM/HFT | — | [mxifund.com](https://www.mxifund.com) | ★ Shanghai; Strongest public compute signal in tier: cumulative ~RMB 200m on GPUs/servers since 2016; relocated its 'Constellation' supercomputer base… |
| NK Securities Research | India | Asia | MM/HFT | — | [nksecurities.com](https://www.nksecurities.com) | ★ Gurugram; self-reported research compute — 'petabyte-scale data infrastructure and millions of compute cores' for research/backtesting |
| Open Futures | India | Asia | MM/HFT | — | [openfutures.in](https://openfutures.in) | Delhi / Gurugram; execution-only |
| Optimus Prime Securities and Research | India | Asia | Systematic | — | [optimusprimeresearch.com](https://www.optimusprimeresearch.com) | Bengaluru; none public |
| Ortus Capital Management | Hong Kong | Asia | Systematic | — | [ortuscapital.com](https://ortuscapital.com) | Hong Kong; none public |
| Qilin Investment (启林投资) | China | Asia | ML-native | — | [70capital.com](https://www.70capital.com) | ★ Shanghai; Self-describes as focused on 'AI quantitative investment'; stock model uses 10,000+ factors incl. alternative data (order-book, sentiment,… |
| Qraft Technologies (크래프트테크놀로지스) | South Korea | Asia | ML-native | — | [qraftec.com](https://www.qraftec.com) | ★ Seoul; Explicitly ML/deep-learning-first: proprietary deep-neural-net stock-selection engine (built with LG AI Research), Kirin API data pipeline,… |
| Quadeye Securities | India | Asia | MM/HFT | — | [quadeye.com](https://www.quadeye.com) | Gurugram; none public |
| Quantbox Research | India | Asia | MM/HFT | — | [quantboxresearch.com](https://www.quantboxresearch.com) | Mumbai; none public (systematic-alpha / AI-ML stated, no DC/GPU disclosure) |
| Quantedge Capital | Singapore | Asia | Systematic | — | [quantedge.com](https://www.quantedge.com) | Singapore; none public |
| QuantPi (Liangpai Investment) (量派投资) | China | Asia | Systematic | — | [qpalpha.com](https://www.qpalpha.com) | ★ Shanghai; Runs 'Tidal Plan' training program citing an in-house full-stack system and 'massive data support'; recruits quant + AI talent. No DC… |
| Simplex Asset Management (シンプレクス・アセット・マネジメント株式会社) | Japan | Asia | Systematic | — | [simplexasset.com](https://www.simplexasset.com) | Tokyo; none public |
| Timefolio Asset Management (타임폴리오자산운용) | South Korea | Asia | Multi-mgr | — | [timefolio.co.kr](https://www.timefolio.co.kr) | Seoul; none public |
| Ubiquant (九坤) | China | Asia | Systematic | T3-007 | [ubiquant.com](https://www.ubiquant.com) | Beijing; Bei Ming cluster |
| Wanyan Asset Management (顽岩资产) | China | Asia | MM/HFT | — | [wanyantech.com](https://www.wanyantech.com) | ★ Shanghai; Describes math + AI as core tech; ultra-high-frequency futures origin. No public DC/GPU figures. |
| Wenbo Investment (稳博投资) | China | Asia | Systematic | — | [wenbofund.com](https://www.wenbofund.com) | Shanghai; none public |
| Yanfu (衍复) | China | Asia | Systematic | — | [yanfuinvestments.com](https://yanfuinvestments.com) | Shanghai |
| Zhuoshi Private Fund (卓识私募基金) | China | Asia | MM/HFT | — | [zsquant.com](https://www.zsquant.com) | ★ Beijing; Self-describes proprietary low-latency trading system for fully-automated algorithmic trading; index-enhancement focus. Latency-first; no… |
| Abu Dhabi Investment Authority (ADIA) — Quantitative R&D (جهاز أبوظبي للاستثمار) | United Arab Emirates | Middle East | Systematic | — | [adia.ae](https://www.adia.ae) | ★ Abu Dhabi; high-performance & quantum computing named in mandate; runs ADIA Lab (data science / ML / HPC research), but no public… |
| Algoz | Israel | Middle East | Crypto MM | — | [algoz.io](https://algoz.io) | Ra'anana; execution-only (proprietary non-custodial execution tech 'Quant Pro'; crypto-derivative strategies) |
| Barak Capital (ברק קפיטל) | Israel | Middle East | MM/HFT | — | [barakcapital.com](https://www.barakcapital.com) | Tel Aviv; execution-only (in-house latency-sensitive market-making system since 2010; microsecond execution claimed) |
| Continuum Capital Management | United Arab Emirates | Middle East | Systematic | — | — | ★ Abu Dhabi; press notes investment in localized data centers / AI-driven execution engines; nothing primary/confirmed |
| Deep Edge Fund | Israel | Middle East | ML-native | — | [deepedge.fund](https://deepedge.fund) | Tel Aviv; none public (self-describes ML-driven medium-frequency strategies; no DC/GPU disclosure) |
| Efficient Frontier | Israel | Middle East | Crypto MM | — | [efrontier.io](https://efrontier.io) | Tel Aviv; execution-only (algorithmic crypto market-making across CEX/DEX; no DC/GPU disclosure) |
| Final (פיינל) | Israel | Middle East | MM/HFT | — | [final.co.il](https://www.final.co.il) | ★ Herzliya; ML-based HFT platform per own site; hires for high-performance data infrastructure roles, but no public DC/GPU disclosure |
| Muwazana Financial (موازنة) | Saudi Arabia | Middle East | MM/HFT | — | [muwazana.com](https://www.muwazana.com) | Riyadh; execution-only (self-describes proprietary low-latency trading engine + 'best-in-class computing environment'; no DC/GPU disclosure) |
| Epoch Capital | Australia | Oceania | Systematic | — | [epoch.capital](https://epoch.capital) | Sydney; none public |
| Nine Mile Financial | Australia | Oceania | MM/HFT | — | [nmftrading.com](https://www.nmftrading.com) | Sydney; execution-only |
| Tibra Capital | Australia | Oceania | MM/HFT | — | [tibra.com](https://www.tibra.com) | Austinmer (Wollongong region), NSW; execution-only |
| VivCourt Trading (Vivienne Court) | Australia | Oceania | MM/HFT | — | [vivcourt.com](https://www.vivcourt.com) | Sydney; execution-only |
| Giant Steps Capital (Giant Steps Capital (ex-Visia Investimentos)) | Brazil | South America | Systematic | — | [gscap.com.br](https://www.gscap.com.br) | Sao Paulo; none public |
| Kadima Asset Management | Brazil | South America | Systematic | — | [kadimaasset.com.br](https://www.kadimaasset.com.br) | Rio de Janeiro; none public |
| Murano Investimentos | Brazil | South America | Systematic | — | [muranoinvest.com](https://www.muranoinvest.com) | Rio de Janeiro; none public |
| PRACK Asset Management | Argentina | South America | Systematic | — | [prack-am.com](https://www.prack-am.com) | Buenos Aires; none public |

## Scope decisions (locked 2026-07-05)

1. **MM/HFT execution-only firms** — kept, and **researched for compute**;
   execution-only is recorded as a finding, not a reason to exclude.
2. **Crypto MM** — in scope.
3. **Separate legal entities** — kept split (Citadel LLC vs Citadel
   Securities, DRW vs Cumberland).
4. **China depth** — the ≥¥10bn "big tier" (~15–18 firms).
5. **Regional gaps** — India, Japan/Korea, and the Middle East added; the
   sweep also picked up Western gaps (TGS, Schonfeld, Walleye, RSJ, Da Vinci…)
   and a rest-of-world pass (Australia, Brazil, Argentina, Singapore, HK).

## Where the universe stands (137 firms)

- **By continent:** North America 52 · Asia 46 · Europe 23 · Middle East 8 ·
  Oceania 4 · South America 4.
- **By firm_type:** MM/HFT 55 · Systematic 50 · Multi-mgr 10 · ML-native 9 ·
  Crypto MM 7 · Quant AM 5.
- **`★` = 36 firms** with a public compute/GPU/DC signal already visible — the
  natural front of the research queue. Standouts: Mengxi (蒙玺, ~¥200m GPU
  spend), Castle Ridge ("WALLACE" supercomputer), Qraft, Graviton (HPC ads),
  NK Securities (petabyte infra), ADIA Lab (HPC + quantum), GCI (Kyoto-temple
  data centre).

### To prune if you want a tighter universe

The Western-gap and rest-of-world passes were proactive (beyond the three
regions named). Easy to drop if out of scope: Oceania (4), South America (4),
and the long tail of execution-only market makers. Say the word.

