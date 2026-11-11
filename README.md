# Human Journey · 인류의 여정

**▶ Prototype: https://junhyeopsong.github.io/human-journey/**

A 3D globe that follows people across the world over the last 300,000 years, on an Earth whose coastlines move with ice-age sea level. A sister product of the [Continental Time Machine](https://junhyeopsong.github.io/earth-time-machine/), built on the shared [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui).

30만 년 전부터 지금까지, 빙하기 해수면에 따라 해안선이 바뀌는 지구 위에서 인류가 세계로 퍼져 나간 길을 따라가는 3D 지구본입니다. [지구 대륙 타임머신](https://junhyeopsong.github.io/earth-time-machine/)의 자매 제품이며, 공용 디자인 [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui) 위에 만들었습니다.

## Status · 진행 상황

Prototype · 프로토타입
- ✅ Globe, timeline (linear / log scale), playback, Korean and English · 지구본, 타임라인(선형/로그), 재생, 한국어·영어
- ✅ Coastlines from sea level (land bridges such as Sunda, Sahul and Beringia appear in glacial times) · 해수면에 따른 해안선(빙기에 순다·사훌·베링 땅다리)
- ✅ 34 events and sites with dated ranges, disputed claims shown with both sides and sources · 연대 범위가 있는 사건·유적 34개, 논쟁은 양쪽 주장과 출처 함께
- ✅ Ice sheets as a schematic that grows and shrinks with sea level (to be replaced by published reconstructions) · 해수면에 맞춰 커지고 줄어드는 빙상 개략도(실제 복원 자료로 바꿀 예정)
- ⏳ Species ranges, routes, 10 languages · 종 분포, 이동 경로, 10개 언어

## Data sources · 데이터 출처

| Data · 자료 | Source · 출처 | Licence · 라이선스 |
|---|---|---|
| Sea level · 해수면 | Spratt & Lisiecki (2016), *Clim. Past* 12:1079 — [doi:10.5194/cp-12-1079-2016](https://doi.org/10.5194/cp-12-1079-2016), [NOAA study 19982](https://www.ncei.noaa.gov/access/paleo-search/study/19982). Short PC1 stack, 0–430 ka, shifted so today = 0 m | NOAA open data |
| Relief · 지형 | ETOPO1 (NOAA NCEI) via [ERDDAP etopo180](https://coastwatch.pfeg.noaa.gov/erddap/griddap/etopo180.html), reduced to 0.25° | Free use and redistribution |
| Ice sheets · 빙상 | Hand-drawn schematic of the Last Glacial Maximum extent, scaled with sea level — not a dataset · 마지막 빙기 최성기 범위를 직접 그린 개략도를 해수면에 맞춰 조절 (자료가 아님) | — |
| Events and sites · 사건·유적 | Published studies cited in each event's popover and in `docs/data/events.json` (dates and summaries still to be reviewed) · 각 사건 팝업과 `docs/data/events.json`에 출처 표기 (연대·요약 검토 예정) | — |
| 3D rendering | [three.js](https://threejs.org) r128 | MIT |
| Icons · 아이콘 | [Lucide](https://lucide.dev) | ISC |

## Feedback · 피드백

**sapu0000@gmail.com** · [Issues](https://github.com/JunhyeopSong/human-journey/issues)
