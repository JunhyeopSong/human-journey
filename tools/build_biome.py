#!/usr/bin/env python3
"""Biomes for the "environment" map style (docs/data/biome.png, biome_800k.png, biome_plio.png, biome.json).

Usage: python3 tools/build_biome.py <Beyer2020_annual_vars_v1.1.0.nc> <Krapp2021_biome_v1.2.2.nc> <Plio_enh_mbiome_v1.0.nc> docs/data
       (needs numpy, h5py, Pillow)

Sources
- 0–120 ka: Beyer, R.M., Krapp, M. & Manica, A. (2020) High-resolution terrestrial climate, bioclimate and vegetation for
  the last 120,000 years. Scientific Data 7, 236, doi:10.1038/s41597-020-0552-1 — BIOME4 on bias-corrected HadCM3, 0.5°,
  72 slices (every 2 kyr from 120 ka, every 1 kyr from 22 ka). pastclim repackaging, Zenodo 7062281, CC BY 4.0.
- 124–796 ka: Krapp, M., Beyer, R.M., Edmundson, S.L., Valdes, P.J. & Manica, A. (2021) A statistics-based reconstruction
  of high-resolution global terrestrial climate for the last 800,000 years. Scientific Data 8, 228,
  doi:10.1038/s41597-021-01009-3 — BIOME4, 0.5°, every 1 kyr; kept every 4 kyr. pastclim repackaging, Zenodo 8415273,
  CC BY 4.0.
- mid-Piacenzian (about 3.2 Ma): PRISM4 biome land cover (Plio_enh_mbiome_v1.0.nc, USGS PRISM4 data page), after
  Salzmann, U. et al. (2008) A new global biome reconstruction and data-model comparison for the Middle Pliocene. Global
  Ecology and Biogeography 17, 432–447, doi:10.1111/j.1466-8238.2008.00381.x; Dowsett, H. et al. (2016) The PRISM4
  (mid-Piacenzian) paleoenvironmental reconstruction. Climate of the Past 12, 1519–1538, doi:10.5194/cp-12-1519-2016.
  1°, nearest cell onto the 0.5° grid.

Groups (8, so they read on a small globe)        BIOME4 classes                 PRISM4 classes
  1 tropical forest                               1 2                            1
  2 dry forest, savanna                           3 12 16                        3
  3 dry shrubland                                 13 14                          —
  4 desert                                        21 27                          5
  5 grassland, steppe                             19 20                          4 (grassland and dry shrubland)
  6 temperate forest                              4 5 6 7 8 9 15                 2 (warm-temperate) 6
  7 boreal forest                                 10 11 17 18                    7
  8 tundra                                        22 23 24 25 26                 8 9
Sea, lakes, land ice and cells without a reconstruction are filled from the nearest biome of the same slice, so every
cell has a value: the app keeps its own coastline and ice sheets and only reads the colour of what it shows as land.

Output: 8-bit grey PNGs, value = group 1–8, 720 columns from 179.75°W, slices of 300 rows (89.75°N … 59.75°S) stacked
from the youngest; biome.json lists each file with the ages (ka) of its slices.
"""
import json
import struct
import sys

import h5py
import numpy as np
from PIL import Image

beyer, krapp, prism, out = sys.argv[1:5]
NORTH, SOUTH, STEP, W = 89.75, -59.75, 0.5, 720
H = int(round((NORTH - SOUTH) / STEP)) + 1                      # 300 rows

B4 = np.zeros(64, np.uint8)
for k, v in {1: 1, 2: 1, 3: 2, 12: 2, 16: 2, 13: 3, 14: 3, 21: 4, 27: 4, 19: 5, 20: 5, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6,
             15: 6, 10: 7, 11: 7, 17: 7, 18: 7, 22: 8, 23: 8, 24: 8, 25: 8, 26: 8}.items():
    B4[k] = v
P4 = np.zeros(64, np.uint8)
for k, v in {1: 1, 3: 2, 5: 4, 4: 5, 2: 6, 6: 6, 7: 7, 8: 8, 9: 8}.items():
    P4[k] = v


def fill(a):
    """nearest-neighbour fill of the zeros (4-neighbour growth; east–west wraps)"""
    a = a.copy()
    while (a == 0).any():
        z = a == 0
        best = np.zeros_like(a)
        for sh in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = np.roll(a, sh, axis=(0, 1))
            if sh[0] == 1: n[0, :] = 0
            if sh[0] == -1: n[-1, :] = 0
            best = np.where((best == 0) & (n > 0), n, best)
        if not (z & (best > 0)).any():
            break
        a[z] = best[z]
    return a


def rows_north_first(lat):
    """indices of the source rows for 89.75 … -59.75"""
    want = NORTH - STEP * np.arange(H)
    return np.array([int(np.argmin(np.abs(lat - w))) for w in want])


def group(raw, lut):
    code = np.where((raw > -1) & (raw < 64), np.rint(raw), 0).astype(int)
    return lut[code]


def save(name, slices):
    Image.fromarray(np.vstack(slices), 'L').save(f'{out}/{name}', optimize=True)


files = []
# --- Beyer 2020: all 72 slices ---
f = h5py.File(beyer, 'r'); yrs = f['time'][:]; R = rows_north_first(f['latitude'][:])
order = sorted(range(len(yrs)), key=lambda i: -yrs[i])
sl, ka = [], []
for i in order:
    sl.append(fill(group(f['biome'][i][R], B4))); ka.append(round(-int(yrs[i]) / 1000, 1))
save('biome.png', sl); files.append({'src': 'biome.png', 'ka': ka})
print('Beyer', len(ka), 'slices', ka[0], '…', ka[-1])
# --- Krapp 2021: every 4 kyr, 124 … 796 ka ---
f = h5py.File(krapp, 'r'); yrs = f['time'][:]; R = rows_north_first(f['latitude'][:])
assert abs(float(f['longitude'][0]) + 179.75) < 1e-3
sl, ka = [], []
for a in range(124, 800, 4):
    i = int(np.argmin(np.abs(yrs + a * 1000)))
    sl.append(fill(group(f['biome'][i][R], B4))); ka.append(a)
save('biome_800k.png', sl); files.append({'src': 'biome_800k.png', 'ka': ka})
print('Krapp', len(ka), 'slices', ka[0], '…', ka[-1])


# --- PRISM4 (classic netCDF): one slice ---
def read_nc(path):
    b = open(path, 'rb').read(); assert b[:3] == b'CDF'; ver = b[3]; p = 4
    def i4():
        nonlocal p; v = struct.unpack('>i', b[p:p + 4])[0]; p += 4; return v
    def off():
        nonlocal p
        if ver == 2: v = struct.unpack('>q', b[p:p + 8])[0]; p += 8; return v
        return i4()
    def name():
        nonlocal p; n = i4(); s = b[p:p + n].decode('latin-1'); p += (n + 3) // 4 * 4; return s
    SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 4, 6: 8}; FMT = {1: 'b', 2: 'c', 3: 'h', 4: 'i', 5: 'f', 6: 'd'}
    def atts():
        nonlocal p; tag = i4(); n = i4()
        if tag == 0: return
        for _ in range(n): name(); t = i4(); cnt = i4(); p += (cnt * SIZE[t] + 3) // 4 * 4
    i4(); tag = i4(); nd = i4(); dims = [(name(), i4()) for _ in range(nd if tag else 0)]
    atts(); tag = i4(); nv = i4(); res = {}
    for _ in range(nv if tag else 0):
        vn = name(); n = i4(); ids = [i4() for _ in range(n)]; atts(); t = i4(); i4(); begin = off()
        shape = [dims[k][1] for k in ids]; cnt = int(np.prod(shape)) if shape else 1
        if t in (3, 4, 5, 6): res[vn] = np.array(struct.unpack('>%d%s' % (cnt, FMT[t]), b[begin:begin + cnt * SIZE[t]])).reshape(shape)
    return res


d = read_nc(prism)
lat, lon = d['lat'], d['lon']
var = [k for k in d if k not in ('lat', 'lon') and d[k].ndim == 2][0]
v = d[var]
print('PRISM4', var, v.shape, 'lat', lat[0], lat[-1], 'lon', lon[0], lon[-1])
g = np.zeros((H, W), np.uint8)
for r in range(H):
    la = NORTH - STEP * r; si = int(np.argmin(np.abs(lat - la)))
    for c in range(W):
        lo = -179.75 + STEP * c; sk = int(np.argmin(np.abs(((lon - lo + 180) % 360) - 180)))
        g[r, c] = P4[int(v[si, sk])] if 0 <= v[si, sk] < 64 else 0
save('biome_plio.png', [fill(g)]); files.append({'src': 'biome_plio.png', 'ka': [3200]})

json.dump({'source': 'Beyer, Krapp & Manica 2020 (Sci. Data 7, 236) 0–120 ka and Krapp et al. 2021 (Sci. Data 8, 228) '
                     '124–796 ka, BIOME4, pastclim repackaging (Zenodo 7062281, 8415273; CC BY 4.0); mid-Piacenzian: PRISM4 '
                     'biome land cover (Dowsett et al. 2016) after Salzmann et al. 2008. Grouped into 8; sea, lakes, ice filled '
                     'from the nearest biome.',
           'groups': ['tropical forest', 'dry forest and savanna', 'dry shrubland', 'desert', 'grassland and steppe',
                      'temperate forest', 'boreal forest', 'tundra'],
           'files': files, 'rows': H, 'cols': W, 'north': NORTH, 'south': SOUTH, 'west': -179.75, 'step': STEP},
          open(f'{out}/biome.json', 'w'), separators=(',', ':'))
