#!/usr/bin/env python3
"""Glacial isostatic adjustment (GIA) correction for the coastlines, from ICE-6G_C (VM5a) (docs/data/gia.png, gia.json).

Usage: python3 tools/build_gia.py <folder with I6_C.VM5a_1deg.<age>.nc, ages 0..26 ka> docs/data

ICE-6G_C (VM5a): Argus, D.F., Peltier, W.R., Drummond, R. & Moore, A.W. (2014) The Antarctica component of postglacial
rebound model ICE-6G_C (VM5a)… Geophys. J. Int. 198, 537–563, doi:10.1093/gji/ggu140; Peltier, W.R., Argus, D.F. &
Drummond, R. (2015) Space geodesy constrains ice age terminal deglaciation: The global ICE-6G_C (VM5a) model.
J. Geophys. Res. Solid Earth 120, 450–487, doi:10.1002/2014JB011176. Data: https://www.atmosp.physics.utoronto.ca/~peltier/data.php
(free for academic, research and non-commercial educational use, with citation).

The app floods today's relief to the sea level of each moment (one global number). ICE-6G_C's paleotopography also
has the land pressed down under the ice sheets and the bulge around them, and the ocean floor tilting under the
weight of water. For each 1 kyr slice t this tool keeps only that regional part:
    C(t) = [bedrock(t) − bedrock(0)] − (its mean over ice-free ocean at time t),   bedrock = Topo − ice thickness
in metres (Topo is the surface relative to the sea level of its time, including ice). Where ICE-6G_C itself has ice at t,
C is 0 (the land is under ice then; the app's own ice map may be smaller) — so the pressed-down bedrock shows as soon
as the ice is gone, which is when it shaped the coast. The app adds C to the relief before
comparing with sea level: elevation(t) = relief − sea(t) + C(t). For older times without a slice, the app uses the
slice whose global sea level is closest (glacial cycles repeat their pattern roughly).

Output: gia.png — 360 × (181 × 27) 8-bit grey, value = 128 + C / 3 m (so ±381 m; deeper only under ice centres),
slices 0, 1, … 26 ka top to bottom,
rows north to south, columns from 180°W; gia.json — slice ages and the mean ocean change of each slice (≈ −eustatic).
"""
import json
import struct
import sys

from PIL import Image

src, out = sys.argv[1], sys.argv[2]
AGES = list(range(0, 27))


def read_nc(path):
    """Minimal reader for classic (CDF-1/CDF-2) netCDF files: returns {name: (dims, values)} for numeric variables."""
    b = open(path, 'rb').read()
    assert b[:3] == b'CDF', path
    ver = b[3]
    p = 4

    def i4():
        nonlocal p
        v = struct.unpack('>i', b[p:p + 4])[0]; p += 4; return v

    def off():
        nonlocal p
        if ver == 2:
            v = struct.unpack('>q', b[p:p + 8])[0]; p += 8; return v
        return i4()

    def name():
        nonlocal p
        n = i4(); s = b[p:p + n].decode('latin-1'); p += (n + 3) // 4 * 4; return s

    SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 4, 6: 8}
    FMT = {1: 'b', 2: 'c', 3: 'h', 4: 'i', 5: 'f', 6: 'd'}

    def atts():
        nonlocal p
        tag = i4(); n = i4()
        if tag == 0:
            return
        for _ in range(n):
            name(); t = i4(); cnt = i4(); p += (cnt * SIZE[t] + 3) // 4 * 4

    i4()                                   # numrecs
    tag = i4(); nd = i4(); dims = []
    for _ in range(nd if tag else 0):
        dims.append((name(), i4()))
    atts()
    tag = i4(); nv = i4(); out = {}
    for _ in range(nv if tag else 0):
        vn = name(); n = i4(); ids = [i4() for _ in range(n)]
        atts()
        t = i4(); vsize = i4(); begin = off()
        shape = [dims[k][1] for k in ids]
        count = 1
        for s in shape:
            count *= s
        if t in (3, 4, 5, 6) and count > 0:
            vals = struct.unpack('>%d%s' % (count, FMT[t]), b[begin:begin + count * SIZE[t]])
            out[vn] = (shape, vals)
    return out


def grid(path):
    d = read_nc(path)
    topo, thick = d['Topo'][1], d['stgit'][1]
    bed = [topo[j] - thick[j] for j in range(len(topo))]
    return topo, bed, d['sftgif'][1], list(d['lat'][1]), list(d['lon'][1]), d['Topo'][0]


topo0, bed0, ice0, LAT, LON, shape = grid(f'{src}/I6_C.VM5a_1deg.0.nc')
NY, NX = shape[-2], shape[-1]
print('grid', NY, NX, 'lat', LAT[0], LAT[-1], 'lon', LON[0], LON[-1])

# output grid: 181 rows (90N … 90S), 360 columns (180W … 179E), nearest source cell
OW, OH = 360, 181
def src_index(i, k):
    la = 90 - i; lo = -180 + k
    si = min(range(NY), key=lambda y: abs(LAT[y] - la))
    lo360 = lo % 360
    sk = min(range(NX), key=lambda x: min(abs(LON[x] % 360 - lo360), 360 - abs(LON[x] % 360 - lo360)))
    return si * NX + sk
MAP = [[src_index(i, k) for k in range(OW)] for i in range(OH)]

img = Image.new('L', (OW, OH * len(AGES)))
px = img.load()
meta = []
for n, a in enumerate(AGES):
    _, bed, ice, *_ = grid(f'{src}/I6_C.VM5a_1deg.{a}.nc')
    d = [bed[j] - bed0[j] for j in range(NY * NX)]
    ocean = [d[j] for j in range(NY * NX) if topo0[j] < -200 and ice[j] < 1 and ice0[j] < 1]
    mean = sum(ocean) / len(ocean)
    for i in range(OH):
        for k in range(OW):
            j = MAP[i][k]
            c = 0.0 if ice[j] >= 50 else d[j] - mean
            px[k, n * OH + i] = max(0, min(255, 128 + int(round(c / 3))))
    meta.append({'ka': a, 'oceanMean_m': round(mean, 1)})
    print(a, 'ka  mean ocean change', round(mean, 1), 'm')

img.save(f'{out}/gia.png', optimize=True)
json.dump({'source': 'ICE-6G_C (VM5a) paleotopography, Peltier et al. 2015 (doi:10.1002/2014JB011176) and Argus et al. 2014 '
                     '(doi:10.1093/gji/ggu140); regional part of the bedrock change (minus the mean ocean change); grey value = '
                     '128 + metres / 3; slices of 181 rows (90N..90S) x 360 columns (180W..179E).',
           'slices': meta, 'rows': OH, 'cols': OW}, open(f'{out}/gia.json', 'w'), separators=(',', ':'))
