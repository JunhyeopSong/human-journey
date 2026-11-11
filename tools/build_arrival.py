#!/usr/bin/env python3
"""When Homo sapiens first reached each place over land, from dated sites (docs/data/arrival.png).

Usage: python3 tools/build_arrival.py docs/data

Inputs (in the data folder): relief.png (ETOPO1, 0.25°, R*256+G-12000 m), sealevel.json (Spratt & Lisiecki 2016,
1 kyr steps), sites.json.

Model
- Seeds: accepted (not disputed) Homo sapiens sites; each seeds its cell at its oldest date, or at 50 ka for older
  sites (the model starts at 50 ka; before that the app shows only the areas around dated sites).
- From a reached cell people walk to the 8 neighbouring cells at SPEED km per thousand years, only over dry land at
  that moment (relief above the sea level of the time; they can wait for a land bridge to open). No sea crossings:
  islands and continents reached by boat (Sahul, the Pacific, Madagascar, ...) fill only from their own dated sites.
- Barriers: no walking across the Bering Strait meridian (the Americas fill only from American sites, so they are
  never reached earlier than the record shows), and none over Antarctica.

Output: arrival.png, 720 x 361 grey, the same cells as the app's range grid (row i = relief row 2i, column k = relief
column 2k+1). Value 0 = never reached; otherwise arrival age = (value - 1) / 5 ka (0.2 kyr steps, 0–50 ka).
"""
import heapq
import json
import math
import sys

from PIL import Image

SPEED = 500.0          # km per thousand years (about 0.5 km a year)
START = 50.0           # ka
BERING_LON, BERING_LAT = (-168.75, (55.0, 75.0))

data = sys.argv[1]
rel = Image.open(f'{data}/relief.png').convert('RGB')
RW, RH = rel.size
px = rel.load()
sea = json.load(open(f'{data}/sealevel.json'))['sea']
sites = json.load(open(f'{data}/sites.json'))
SAP = sites['species'].index('sapiens')

DW, DH = 720, 361
N = DW * DH
elev = [0.0] * N
lon = [0.0] * DW
lat = [0.0] * DH
for i in range(DH):
    ri = min(RH - 1, i * 2)
    lat[i] = 90 - ri * 180 / (RH - 1)
    for k in range(DW):
        ck = min(RW - 1, k * 2 + 1)
        r, g, _ = px[ck, ri]
        elev[i * DW + k] = r * 256 + g - 12000
for k in range(DW):
    lon[k] = -180 + min(RW - 1, k * 2 + 1) * 360 / (RW - 1)


def sea_at(a):
    a = max(0.0, min(len(sea) - 1, a))
    i = int(a)
    f = a - i
    return sea[i] * (1 - f) + sea[i + 1] * f if i + 1 < len(sea) else sea[i]


STEP = 0.1
AGES = [round(START - n * STEP, 1) for n in range(int(START / STEP) + 1)]     # 50.0 … 0.0
SEA_T = [sea_at(a) for a in AGES]
SMAX, SMIN = max(SEA_T), min(SEA_T)


def latest_land(e, x):
    """Latest age a <= x (ka) at which a cell of elevation e is dry land, or None."""
    if e > SMAX:
        return x
    if e <= SMIN:
        return None
    n = max(0, int(math.ceil((START - x) / STEP - 1e-9)))
    for m in range(n, len(AGES)):
        if SEA_T[m] < e:
            return min(x, AGES[m])
    return None


def blocked(j1, j2):
    i1, k1 = divmod(j1, DW)
    i2, k2 = divmod(j2, DW)
    if lat[i1] < -60 or lat[i2] < -60:
        return True
    if BERING_LAT[0] <= lat[i1] <= BERING_LAT[1] or BERING_LAT[0] <= lat[i2] <= BERING_LAT[1]:
        w1, w2 = lon[k1] < BERING_LON, lon[k2] < BERING_LON
        if w1 != w2 and abs(lon[k1] - lon[k2]) < 10:
            return True
    return False


arr = [-1.0] * N
heap = []
for st in sites['sites']:
    if st[0] != SAP or st[5]:
        continue
    k = int((st[1] + 180) / 360 * DW) % DW
    i = min(DH - 1, max(0, int(round((90 - st[2]) / 180 * (DH - 1)))))
    a0 = min(st[4], START)
    best = None                                   # sites often sit on the coast: take the nearest land cell around
    for di in range(-2, 3):
        for dk in range(-2, 3):
            ii = i + di
            if not 0 <= ii < DH:
                continue
            j = ii * DW + (k + dk) % DW
            a = latest_land(elev[j], a0)
            if a is not None and (best is None or (abs(di) + abs(dk), -a) < best[0]):
                best = ((abs(di) + abs(dk), -a), j, a)
    if best:
        heapq.heappush(heap, (-best[2], best[1]))

NB = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
while heap:
    na, j = heapq.heappop(heap)
    a = -na
    if arr[j] >= a:
        continue
    arr[j] = a
    i, k = divmod(j, DW)
    for di, dk in NB:
        ii = i + di
        if not 0 <= ii < DH:
            continue
        j2 = ii * DW + (k + dk) % DW
        if arr[j2] >= 0 or blocked(j, j2):
            continue
        dy = 0.5 * 111.2 * di
        dx = 0.5 * 111.2 * dk * math.cos(math.radians((lat[i] + lat[ii]) / 2))
        a2 = latest_land(elev[j2], a - math.hypot(dx, dy) / SPEED)
        if a2 is not None and a2 >= 0 and a2 > arr[j2]:
            heapq.heappush(heap, (-a2, j2))

out = Image.new('L', (DW, DH))
out.putdata([0 if v < 0 else 1 + int(round(v * 5)) for v in arr])
out.save(f'{data}/arrival.png', optimize=True)
reached = sum(1 for v in arr if v >= 0)
print(f'reached {reached} of {N} cells; seeds from {SPEED:.0f} km/ka model written to {data}/arrival.png')
