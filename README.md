# Human Journey · 인류의 여정

**▶ Prototype: https://junhyeopsong.github.io/human-journey/**

A 3D globe that follows people across the world over the last 2 million years — from Homo habilis and Homo ergaster to us — on an Earth whose coastlines move with ice-age sea level. A sister product of the [Continental Time Machine](https://junhyeopsong.github.io/earth-time-machine/), built on the shared [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui).

200만 년 전(호모 하빌리스·에르가스테르)부터 지금까지, 빙하기 해수면에 따라 해안선이 바뀌는 지구 위에서 인류가 세계로 퍼져 나간 길을 따라가는 3D 지구본입니다. [지구 대륙 타임머신](https://junhyeopsong.github.io/earth-time-machine/)의 자매 제품이며, 공용 디자인 [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui) 위에 만들었습니다.

## Status · 진행 상황

Prototype · 프로토타입
- ✅ Globe, timeline (linear / log scale), playback, Korean and English · 지구본, 타임라인(선형/로그), 재생, 한국어·영어
- ✅ Coastlines from sea level (land bridges such as Sunda, Sahul and Beringia appear in glacial times) · 해수면에 따른 해안선(빙기에 순다·사훌·베링 땅다리)
- ✅ 44 events and sites with dated ranges, disputed claims shown with both sides and sources · 연대 범위가 있는 사건·유적 44개, 논쟁은 양쪽 주장과 출처 함께
- ✅ Ice sheets: published Northern Hemisphere reconstructions for 12 time slices, scaled with sea level in between · 빙상: 12개 시기의 북반구 복원 자료, 그 사이는 해수면으로 조절
- ✅ Species ranges drawn from dated sites: one light fill per species with an outline in its colour, stripes where species overlap; areas grow in and shrink away smoothly with each site's dates; disputed sites included with the "show disputed dates" setting. After 50 ka Homo sapiens spreads on foot from accepted dated sites (~500 km per thousand years) over the land of each moment, waiting for ice-age land bridges, never across sea or the Bering Strait — so continents and islands reached by boat fill only from their own dated sites (`docs/data/arrival.png`, built by `tools/build_arrival.py`) · 연대 유적으로 그린 종 분포: 종마다 옅은 칠 + 외곽선, 겹치면 줄무늬, 유적 연대에 따라 부드럽게 퍼지고 줄어듦; 현생인류는 5만 년 전 이후 인정된 유적에서 그 시기 육지를 따라 천 년에 약 500 km씩 걸어 퍼짐(바다·베링 해협은 건너지 않음)
- ✅ Global mean temperature, °C / °F · 지구 평균 기온 (°C/°F)
- ⏳ 10 languages, product switcher, pausing at events · 10개 언어, 제품 전환 메뉴, 재생 중 사건에서 멈추기

## Data sources · 데이터 출처

| Data · 자료 | Source · 출처 | Licence · 라이선스 |
|---|---|---|
| Sea level · 해수면 | Spratt & Lisiecki (2016), *Clim. Past* 12:1079 — [doi:10.5194/cp-12-1079-2016](https://doi.org/10.5194/cp-12-1079-2016), [NOAA study 19982](https://www.ncei.noaa.gov/access/paleo-search/study/19982). Short PC1 stack 0–430 ka and long PC1 stack 430–798 ka, shifted so today = 0 m; 0.8–2 Ma estimated from the LR04 benthic δ18O stack (Lisiecki & Raymo 2005, *Paleoceanography* 20:PA1003, [doi:10.1029/2004PA001071](https://doi.org/10.1029/2004PA001071)) by a linear fit over 0–798 ka — less certain. Built by `tools/build_climate.py` | NOAA open data |
| Relief · 지형 | ETOPO1 (NOAA NCEI) via [ERDDAP etopo180](https://coastwatch.pfeg.noaa.gov/erddap/griddap/etopo180.html), reduced to 0.25° | Free use and redistribution |
| Species ranges · 종 분포 | `docs/data/sites.json` (3,986 dated sites of 13 species, built by `tools/build_sites.py`) from: Timmermann et al. 2022, *Nature* 604:495, Supplementary Table 1 ([doi:10.1038/s41586-022-04600-9](https://doi.org/10.1038/s41586-022-04600-9)) for 30 ka – 2 Ma; ROAD, ROCEEH Out of Africa Database ([Zenodo 7669784](https://doi.org/10.5281/zenodo.7669784)) for Homo sapiens after 30 ka; and a short curated list of published sites (Americas, Sahul, Oceania, island species) with DOIs in the file. Homo sapiens areas reached after 50 ka stay shown as inferred to the present · 위 자료로 만든 유적 3,707곳; 현생인류가 5만 년 전 이후 도달한 지역은 현재까지 추정 영역으로 유지 | Timmermann S1: CC BY 4.0; ROAD: CC BY-SA 4.0 → `sites.json` is CC BY-SA 4.0 |
| Mean temperature · 평균 기온 | EPICA Dome C temperature (Jouzel et al. 2007, *Science* 317:793, [doi:10.1126/science.1141038](https://doi.org/10.1126/science.1141038); NOAA) scaled so the Last Glacial Maximum is 6.1 °C below today (Tierney et al. 2020, *Nature* 584:569, [doi:10.1038/s41586-020-2617-x](https://doi.org/10.1038/s41586-020-2617-x)) — an approximation of the global mean, 0–800 ka; 0.8–2 Ma estimated from LR04 · 남극 기온을 LGM −6.1 °C에 맞춰 지구 평균으로 바꾼 근사치, 80만 년 이전은 LR04로 추정 | NOAA open data |
| Ice sheets · 빙상 | Batchelor, C.L. et al. (2019) The configuration of Northern Hemisphere ice sheets through the Quaternary. *Nat. Commun.* 10, 3713 — [doi:10.1038/s41467-019-11601-2](https://doi.org/10.1038/s41467-019-11601-2); best-estimate reconstructions for LGM, 30, 35, 40, 45 ka, MIS 4, 5a–5d, 6 and 8 from [OSF 7jen3](https://osf.io/7jen3/), rasterised to 0.25° (`docs/data/ice_nh.png`). Between slices the nearest one is shrunk or grown with sea level. Present Greenland and Antarctic ice from the relief; Patagonia is a hand-drawn schematic · 12개 시기 최적 추정 복원을 0.25°로 변환, 그 사이는 해수면으로 조절. 그린란드·남극 현재 빙상은 지형에서, 파타고니아는 개략도 | CC BY 4.0 |
| Events and sites · 사건·유적 | Published studies cited in each event's popover and in `docs/data/events.json` (dates and summaries still to be reviewed) · 각 사건 팝업과 `docs/data/events.json`에 출처 표기 (연대·요약 검토 예정) | — |
| 3D rendering | [three.js](https://threejs.org) r128 | MIT |
| Icons · 아이콘 | [Lucide](https://lucide.dev) | ISC |

## Feedback · 피드백

**sapu0000@gmail.com** · [Issues](https://github.com/JunhyeopSong/human-journey/issues)
