#!/usr/bin/env python3
"""Biomes of the last 120,000 years for the "environment" map style (docs/data/biome.png, biome.json).

Usage: python3 tools/build_biome.py <Beyer2020_annual_vars_v1.1.0.nc> docs/data      (needs numpy, h5py, Pillow)

Source: Beyer, R.M., Krapp, M. & Manica, A. (2020) High-resolution terrestrial climate, bioclimate and vegetation for
the last 120,000 years. Scientific Data 7, 236, doi:10.1038/s41597-020-0552-1 — BIOME4 run on bias-corrected HadCM3
climate, 0.5°, 72 time slices (every 2 kyr from 120 ka, every 1 kyr from 22 ka). File: the pastclim repackaging
(Leonardi et al. 2023, pastclim), Zenodo record 7062281, CC BY 4.0.

The 28 BIOME4 classes are grouped into 8 that read on a small globe:
  1 tropical forest      BIOME4 1 2
  2 dry forest, savanna  3 12 16
  3 dry shrubland        13 14
  4 desert               21 27
  5 grassland, steppe    19 20
  6 temperate forest     4 5 6 7 8 9 15
  7 boreal forest        10 11 17 18
  8 tundra               22 23 24 25 26
Sea, lakes (0) and the dataset's own land ice (28) are filled from the nearest biome of the same slice, so every cell
has a value: the app keeps its own coastline (relief + sea level + land movement) and its own ice sheets, and only
reads the colour of what it shows as bare land.

Output: biome.png — 720 × (300 × 72) 8-bit grey, value = group 1–8; slices from today (top) to 120 ka, each slice
rows 89.75°N … 59.75°S, columns from 179.75°W; biome.json — slice ages (ka) and the grid.
"""
import json
import sys

import h5py
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
GROUP = {1: 1, 2: 1, 3: 2, 12: 2, 16: 2, 13: 3, 14: 3, 21: 4, 27: 4, 19: 5, 20: 5,
         4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 15: 6, 10: 7, 11: 7, 17: 7, 18: 7,
         22: 8, 23: 8, 24: 8, 25: 8, 26: 8}
LUT = np.zeros(29, np.uint8)
for k, v in GROUP.items():
    LUT[k] = v

f = h5py.File(src, 'r')
years = f['time'][:]
lat = f['latitude'][:]
B = f['biome']
T, H, W = B.shape
assert lat[0] < lat[-1]                                  # south first in the file → flip to north first


def fill(a):
    """nearest-neighbour fill of the zeros (4-neighbour growth; east–west wraps)"""
    a = a.copy()
    while (a == 0).any():
        z = a == 0
        best = np.zeros_like(a)
        for sh in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = np.roll(a, sh, axis=(0, 1))
            if sh[0] == 1: n[0, :] = 0                   # no wrap across the poles
            if sh[0] == -1: n[-1, :] = 0
            best = np.where((best == 0) & (n > 0), n, best)
        if not (z & (best > 0)).any():
            break
        a[z] = best[z]
    return a


order = sorted(range(T), key=lambda i: -years[i])          # today first
img = np.zeros((H * T, W), np.uint8)
ages = []
for n, i in enumerate(order):
    b = B[i][::-1]                                          # north first
    code = np.where(b > -1, np.rint(b), 0).astype(int).clip(0, 28)
    g = LUT[code]
    img[n * H:(n + 1) * H] = fill(g)
    ages.append(round(-int(years[i]) / 1000, 1))
    print(ages[-1], 'ka', np.bincount(g.ravel(), minlength=9)[1:])

Image.fromarray(img, 'L').save(f'{out}/biome.png', optimize=True)
json.dump({'source': 'Beyer, Krapp & Manica 2020 (Scientific Data 7, 236, doi:10.1038/s41597-020-0552-1), BIOME4 biomes, '
                     'pastclim repackaging (Zenodo 7062281, CC BY 4.0); 28 classes grouped into 8; sea, lakes and land ice '
                     'filled from the nearest biome.',
           'groups': ['tropical forest', 'dry forest and savanna', 'dry shrubland', 'desert', 'grassland and steppe',
                      'temperate forest', 'boreal forest', 'tundra'],
           'ka': ages, 'rows': H, 'cols': W, 'north': float(lat[-1]), 'south': float(lat[0]), 'west': -179.75, 'step': 0.5},
          open(f'{out}/biome.json', 'w'), separators=(',', ':'))
