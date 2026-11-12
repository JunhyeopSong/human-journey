# Human Journey · 인류의 여정

**▶ Live (prototype): https://junhyeopsong.github.io/human-journey/**

[English](#english) · [한국어](#한국어)

![Human Journey](docs/og.png)

---

## English

An interactive 3D globe that follows people across the world over the last 2 million years — from Homo habilis and Homo ergaster to us — on an Earth whose coastlines move with ice-age sea level. Built on published dated sites, sea-level and climate records. A sister product of the [Continental Time Machine](https://junhyeopsong.github.io/earth-time-machine/), sharing its design through [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui).

### Features
- **Travel through 2 million years** — a log timeline (linear in settings) with colour bands for each stage, three playback speeds, shortcut chips to key moments, and back/forward buttons that stop at each event. *Follow events while playing* turns to every event as it happens.
- **Ice-age Earth** — coastlines drawn from the sea level of each moment, so land bridges such as Beringia, Sunda and Sahul appear and drown; Northern Hemisphere ice sheets; global mean temperature in °C or °F.
- **13 human species, from dated sites only** — each species' range is a light fill around sites dated to that time, with an outline, and stripes where species overlap. After 50,000 years ago Homo sapiens spreads on foot over the land of each moment from accepted dated sites, never across sea, so islands and continents reached by boat fill only from their own sites.
- **44 events with their evidence** — fossils, tools, art, ancient DNA, farming origins and climate events, each with its date range and sources; disputed claims show both sides, and a setting hides them.
- **Evolution tree** — unfold the event row into a lane per species, with its dated span, its events and the lanes it probably branched from.
- **Globe or world map** — switch to an equal-area (Mollweide) map of the whole world; optional polar axis on the globe.
- **Korean and English** — follows your device language.

### Controls
| Action | Mouse / touch | Keyboard |
|---|---|---|
| Rotate the globe | Drag | Shift + ← → ↑ ↓ |
| Zoom | Scroll / pinch, double-click a spot | + / − |
| Play / pause | ▶ button | Space |
| Step back / forward (stops at each event) | ◀ ▶ buttons | ← → |
| Playback speed | Slow · Normal · Fast | 1 · 2 · 3 |
| Events by species | Branch button under the globe controls | — |

### Data sources
| Data | Source | License |
|---|---|---|
| Sea level | Spratt & Lisiecki (2016), *Clim. Past* — [doi:10.5194/cp-12-1079-2016](https://doi.org/10.5194/cp-12-1079-2016) ([NOAA](https://www.ncei.noaa.gov/access/paleo-search/study/19982)), 0–800 ka; LR04 benthic δ18O stack, Lisiecki & Raymo (2005) — [doi:10.1029/2004PA001071](https://doi.org/10.1029/2004PA001071), for 0.8–2 Ma | NOAA open data |
| Relief | ETOPO1 (NOAA NCEI) via [ERDDAP etopo180](https://coastwatch.pfeg.noaa.gov/erddap/griddap/etopo180.html), reduced to 0.25° | Free use and redistribution |
| Ice sheets | Batchelor et al. (2019), *Nat. Commun.* — [doi:10.1038/s41467-019-11601-2](https://doi.org/10.1038/s41467-019-11601-2) ([OSF 7jen3](https://osf.io/7jen3/)), 12 time slices | CC BY 4.0 |
| Mean temperature | EPICA Dome C, Jouzel et al. (2007), *Science* — [doi:10.1126/science.1141038](https://doi.org/10.1126/science.1141038), scaled to Tierney et al. (2020), *Nature* — [doi:10.1038/s41586-020-2617-x](https://doi.org/10.1038/s41586-020-2617-x); LR04 before 800 ka | NOAA open data |
| Dated sites (species ranges) | Timmermann et al. (2022), *Nature*, Supplementary Table 1 — [doi:10.1038/s41586-022-04600-9](https://doi.org/10.1038/s41586-022-04600-9); ROAD, ROCEEH Out of Africa Database — [Zenodo 7669784](https://doi.org/10.5281/zenodo.7669784); a curated list of published sites with DOIs in `docs/data/sites.json` | CC BY 4.0; CC BY-SA 4.0 → `sites.json` is CC BY-SA 4.0 |
| Events | Published studies, cited in each event and in `docs/data/events.json` | Cited research results |
| 3D rendering · icons | [three.js](https://threejs.org) r128 · [Lucide](https://lucide.dev) | MIT · ISC |

**Notes.** This is a prototype; event dates and summaries are still being reviewed. Sea level and temperature older than 800,000 years are estimates from the LR04 stack. Ice sheets older than MIS 8 reuse the nearest reconstruction scaled with sea level, and Patagonia is a hand-drawn schematic. The Homo sapiens spread after 50 ka is a model (about 500 km per thousand years from dated sites), and the evolution tree is a rough picture of relationships that are still debated. The data files are built by the scripts in `tools/` (`build_sites.py`, `build_arrival.py`, `build_climate.py`). Corrections are welcome.

### Feedback
Found a mistake, have an idea, or want an event added? Email **sapu0000@gmail.com** or [open an issue](https://github.com/JunhyeopSong/human-journey/issues).

### Run locally
```bash
cd docs && python3 -m http.server 8000
```
Then open http://localhost:8000.

---

## 한국어

200만 년 전 호모 하빌리스·에르가스테르부터 지금의 우리까지, 빙하기 해수면에 따라 해안선이 바뀌는 지구 위에서 인류가 세계로 퍼져 나간 길을 3D 지구본으로 따라가는 웹 시뮬레이터입니다. 연대가 측정된 유적과 해수면·기후 기록을 바탕으로 만들었습니다. [지구 대륙 타임머신](https://junhyeopsong.github.io/earth-time-machine/)의 자매 제품이며, 공용 디자인 [time-machine-ui](https://github.com/JunhyeopSong/time-machine-ui)를 함께 씁니다.

### 기능
- **200만 년 시간 여행** — 시대별 색 띠가 있는 로그 타임라인(설정에서 선형), 세 가지 재생 속도, 주요 순간으로 가는 바로가기 칩, 사건마다 멈추는 이전·다음 버튼. *재생 중 따라가기*를 켜면 사건이 일어날 때마다 그곳으로 이동합니다.
- **빙하기 지구** — 그 시기 해수면으로 그린 해안선으로 베링기아·순다·사훌 같은 땅다리가 드러났다 잠깁니다. 북반구 빙상, 지구 평균 기온(°C/°F)도 보여줍니다.
- **연대 유적만으로 그린 13종의 분포** — 종마다 그 시기 연대 유적 주변을 옅은 칠과 외곽선으로, 여러 종이 겹치면 줄무늬로 그립니다. 5만 년 전 이후 현생인류는 인정된 연대 유적에서 그 시기의 육지를 따라 걸어서 퍼지며 바다는 건너지 않으므로, 배로 건너간 섬과 대륙은 그곳의 유적이 있어야 칠해집니다.
- **근거를 갖춘 사건 44개** — 화석·도구·예술·고대 DNA·농경의 기원·기후 사건마다 연대 범위와 출처가 있습니다. 논쟁 중인 주장은 양쪽을 함께 보여주며, 설정에서 숨길 수 있습니다.
- **종별 계통도** — 사건 줄을 펼치면 종마다 칸이 생겨, 유적 연대 범위와 사건, 갈라져 나왔다고 보는 칸이 함께 보입니다.
- **지구본 또는 전체 지도** — 면적이 정확한 몰바이데 세계지도로 바꿀 수 있고, 지구본에서는 자전축을 켤 수 있습니다.
- **한국어·영어** — 기기 언어를 따릅니다.

### 조작법
| 동작 | 마우스 / 터치 | 키보드 |
|---|---|---|
| 지구 돌리기 | 드래그 | Shift + ← → ↑ ↓ |
| 확대·축소 | 휠 / 핀치, 원하는 곳 더블클릭 | + / − |
| 재생 / 정지 | ▶ 버튼 | Space |
| 이전·다음 (사건마다 멈춤) | ◀ ▶ 버튼 | ← → |
| 재생 속도 | 느리게 · 보통 · 빠르게 | 1 · 2 · 3 |
| 사건을 종별로 펼치기 | 지구본 조작 아래 갈래 버튼 | — |

### 데이터 출처
| 자료 | 출처 | 라이선스 |
|---|---|---|
| 해수면 | Spratt & Lisiecki (2016), *Clim. Past* — [doi:10.5194/cp-12-1079-2016](https://doi.org/10.5194/cp-12-1079-2016) ([NOAA](https://www.ncei.noaa.gov/access/paleo-search/study/19982)), 0–80만 년 전; 80만~200만 년 전은 LR04 해저 산소동위원소 기록, Lisiecki & Raymo (2005) — [doi:10.1029/2004PA001071](https://doi.org/10.1029/2004PA001071) | NOAA 공개 자료 |
| 지형 | ETOPO1 (NOAA NCEI), [ERDDAP etopo180](https://coastwatch.pfeg.noaa.gov/erddap/griddap/etopo180.html), 0.25°로 줄임 | 자유 이용·재배포 |
| 빙상 | Batchelor 외 (2019), *Nat. Commun.* — [doi:10.1038/s41467-019-11601-2](https://doi.org/10.1038/s41467-019-11601-2) ([OSF 7jen3](https://osf.io/7jen3/)), 12개 시기 | CC BY 4.0 |
| 평균 기온 | EPICA Dome C, Jouzel 외 (2007), *Science* — [doi:10.1126/science.1141038](https://doi.org/10.1126/science.1141038), Tierney 외 (2020), *Nature* — [doi:10.1038/s41586-020-2617-x](https://doi.org/10.1038/s41586-020-2617-x)에 맞춰 환산; 80만 년 이전은 LR04 | NOAA 공개 자료 |
| 연대 유적 (종 분포) | Timmermann 외 (2022), *Nature*, 보충표 1 — [doi:10.1038/s41586-022-04600-9](https://doi.org/10.1038/s41586-022-04600-9); ROAD, ROCEEH Out of Africa Database — [Zenodo 7669784](https://doi.org/10.5281/zenodo.7669784); `docs/data/sites.json`에 DOI를 붙인 유적 목록 | CC BY 4.0; CC BY-SA 4.0 → `sites.json`은 CC BY-SA 4.0 |
| 사건 | 공개된 연구, 각 사건과 `docs/data/events.json`에 출처 표기 | 논문 결과 인용 |
| 3D 렌더링 · 아이콘 | [three.js](https://threejs.org) r128 · [Lucide](https://lucide.dev) | MIT · ISC |

**참고.** 프로토타입이며, 사건의 연대와 요약은 검토 중입니다. 80만 년보다 오래된 해수면·기온은 LR04 기록으로 추정한 값입니다. MIS 8보다 오래된 빙상은 가장 가까운 복원을 해수면에 맞춰 쓰며, 파타고니아는 직접 그린 개략도입니다. 5만 년 전 이후 현생인류의 확산은 연대 유적에서 천 년에 약 500 km씩 퍼진다고 본 모델이고, 종별 계통도의 관계는 학계에서도 논쟁 중인 대략적인 모습입니다. 데이터 파일은 `tools/`의 스크립트(`build_sites.py`, `build_arrival.py`, `build_climate.py`)로 만듭니다. 틀린 부분을 알려주시면 고치겠습니다.

### 피드백
틀린 내용, 아이디어, 추가하고 싶은 사건이 있다면 **sapu0000@gmail.com** 으로 메일을 보내주시거나 [이슈](https://github.com/JunhyeopSong/human-journey/issues)를 남겨주세요.

### 로컬에서 실행
```bash
cd docs && python3 -m http.server 8000
```
브라우저에서 http://localhost:8000 을 엽니다.
