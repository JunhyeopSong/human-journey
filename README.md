# Human Journey · 인류의 여정

**▶ Prototype: https://junhyeopsong.github.io/human-journey/**

A 3D globe that follows people across the world over the last 300,000 years, on an Earth whose coastlines move with ice-age sea level. A sister product of the [Continental Time Machine](https://junhyeopsong.github.io/earth-time-machine/), built on the shared [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui).

30만 년 전부터 지금까지, 빙하기 해수면에 따라 해안선이 바뀌는 지구 위에서 인류가 세계로 퍼져 나간 길을 따라가는 3D 지구본입니다. [지구 대륙 타임머신](https://junhyeopsong.github.io/earth-time-machine/)의 자매 제품이며, 공용 디자인 [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui) 위에 만들었습니다.

## Status · 진행 상황

Prototype · 프로토타입
- ✅ Globe, timeline (linear / log scale), playback, Korean and English · 지구본, 타임라인(선형/로그), 재생, 한국어·영어
- ✅ Coastlines from sea level (land bridges such as Sunda, Sahul and Beringia appear in glacial times) · 해수면에 따른 해안선(빙기에 순다·사훌·베링 땅다리)
- ✅ 34 events and sites with dated ranges, disputed claims shown with both sides and sources · 연대 범위가 있는 사건·유적 34개, 논쟁은 양쪽 주장과 출처 함께
- ✅ Ice sheets: published Northern Hemisphere reconstructions for 12 time slices, scaled with sea level in between · 빙상: 12개 시기의 북반구 복원 자료, 그 사이는 해수면으로 조절
- ✅ Ranges of six archaic species as soft areas around sites dated to the time; Homo sapiens filling the land it reaches as it spreads from Africa along the migration routes · 연대가 맞는 유적 주변을 흐린 영역으로 그린 고인류 6종의 분포, 아프리카에서 이동 경로를 따라 퍼지며 땅을 채우는 현생인류
- ✅ Global mean temperature, °C / °F · 지구 평균 기온 (°C/°F)
- ⏳ 10 languages, product switcher, pausing at events · 10개 언어, 제품 전환 메뉴, 재생 중 사건에서 멈추기

## Data sources · 데이터 출처

| Data · 자료 | Source · 출처 | Licence · 라이선스 |
|---|---|---|
| Sea level · 해수면 | Spratt & Lisiecki (2016), *Clim. Past* 12:1079 — [doi:10.5194/cp-12-1079-2016](https://doi.org/10.5194/cp-12-1079-2016), [NOAA study 19982](https://www.ncei.noaa.gov/access/paleo-search/study/19982). Short PC1 stack, 0–430 ka, shifted so today = 0 m | NOAA open data |
| Relief · 지형 | ETOPO1 (NOAA NCEI) via [ERDDAP etopo180](https://coastwatch.pfeg.noaa.gov/erddap/griddap/etopo180.html), reduced to 0.25° | Free use and redistribution |
| Species ranges · 종 분포 | Curated dated sites (`docs/data/species.json`), sources in each species popover; areas join sites within ~2,200 km — rough outlines, not population maps · 연대가 있는 유적 목록, 출처는 각 종 팝업에; 2,200 km 안의 유적을 이은 대략적 범위 | — |
| Spread of Homo sapiens · 현생인류의 확산 | Dated waypoints of possible routes (`docs/data/routes.json`, with sources) and early African sites; each land cell fills from the time people could first reach it (Africa ~120 km, elsewhere ~600 km per thousand years, staying on its landmass; crossings only along the routes) · 가능한 경로의 연대 지점과 아프리카 초기 유적에서 천 년에 약 1,000 km씩 퍼지는 모델 | — |
| Mean temperature · 평균 기온 | EPICA Dome C temperature (Jouzel et al. 2007, *Science* 317:793, [doi:10.1126/science.1141038](https://doi.org/10.1126/science.1141038); NOAA) scaled so the Last Glacial Maximum is 6.1 °C below today (Tierney et al. 2020, *Nature* 584:569, [doi:10.1038/s41586-020-2617-x](https://doi.org/10.1038/s41586-020-2617-x)) — an approximation of the global mean · 남극 기온을 LGM −6.1 °C에 맞춰 지구 평균으로 바꾼 근사치 | NOAA open data |
| Ice sheets · 빙상 | Batchelor, C.L. et al. (2019) The configuration of Northern Hemisphere ice sheets through the Quaternary. *Nat. Commun.* 10, 3713 — [doi:10.1038/s41467-019-11601-2](https://doi.org/10.1038/s41467-019-11601-2); best-estimate reconstructions for LGM, 30, 35, 40, 45 ka, MIS 4, 5a–5d, 6 and 8 from [OSF 7jen3](https://osf.io/7jen3/), rasterised to 0.25° (`docs/data/ice_nh.png`). Between slices the nearest one is shrunk or grown with sea level. Present Greenland and Antarctic ice from the relief; Patagonia is a hand-drawn schematic · 12개 시기 최적 추정 복원을 0.25°로 변환, 그 사이는 해수면으로 조절. 그린란드·남극 현재 빙상은 지형에서, 파타고니아는 개략도 | CC BY 4.0 |
| Events and sites · 사건·유적 | Published studies cited in each event's popover and in `docs/data/events.json` (dates and summaries still to be reviewed) · 각 사건 팝업과 `docs/data/events.json`에 출처 표기 (연대·요약 검토 예정) | — |
| 3D rendering | [three.js](https://threejs.org) r128 | MIT |
| Icons · 아이콘 | [Lucide](https://lucide.dev) | ISC |

## Feedback · 피드백

**sapu0000@gmail.com** · [Issues](https://github.com/JunhyeopSong/human-journey/issues)
