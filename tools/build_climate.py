#!/usr/bin/env python3
"""Sea level and global mean temperature, 0–3,300 ka in 1 kyr steps (docs/data/sealevel.json, temperature.json).

Usage: python3 tools/build_climate.py <spratt2016.txt> <edc.txt> <lisiecki2005.txt> docs/data

Sea level (today = 0 m)
- 0–430 ka: Spratt & Lisiecki 2016 short PC1 stack (as before), shifted by its present value.
- 430–798 ka: their long PC1 stack, shifted to meet the short stack at 430 ka.
- 798–3,300 ka: estimated from the LR04 benthic d18O stack (Lisiecki & Raymo 2005) by a linear fit of the
  sea level above against LR04 over 0–798 ka, shifted to meet it at 798 ka. Older values are less certain.
Temperature (°C)
- 0–800 ka: EPICA Dome C Antarctic temperature anomaly (Jouzel et al. 2007), mean of each 1 kyr bin, times 0.644 so
  the Last Glacial Maximum is 6.1 °C below today (Tierney et al. 2020), plus 14.0 °C (as before).
- 800–3,300 ka: the same fit against LR04, shifted to meet it at 800 ka.
"""
import json
import sys

import numpy as np

spratt, edc, lr04, out = sys.argv[1:5]
AMAX = 3300
ages = np.arange(0, AMAX + 1)

# --- Spratt & Lisiecki 2016
sl = []
for line in open(spratt):
    p = line.split()
    if len(p) >= 9 and not line.startswith('#'):
        try:
            sl.append((float(p[0]), float(p[1]), float(p[5])))
        except ValueError:
            pass
sl = np.array(sl)
short = sl[~np.isnan(sl[:, 1])]
OFFSET = float(short[short[:, 0] == 0, 1][0])

# --- LR04 (age ka, d18O)
lr = []
for line in open(lr04):
    if line.startswith('Sedimentation rates'):      # the stack is the first table; later tables are other data
        break
    p = line.split()
    if len(p) == 3:
        try:
            a, d = float(p[0]), float(p[1])
        except ValueError:
            continue
        if 0 <= a <= 5400 and 2.0 < d < 6.0:
            lr.append((a, d))
lr = np.array(sorted(set(lr)))
lr = lr[np.concatenate([[True], np.diff(lr[:, 0]) > 0])]
d18 = np.interp(ages, lr[:, 0], lr[:, 1])

sea = np.full(len(ages), np.nan)
m = ages <= 430
sea[m] = np.interp(ages[m], short[:, 0], short[:, 1]) - OFFSET
lng = sl[(sl[:, 0] >= 400) & (sl[:, 0] <= 798)]
shift = np.interp(430, short[:, 0], short[:, 1]) - np.interp(430, lng[:, 0], lng[:, 2])
m = (ages > 430) & (ages <= 798)
sea[m] = np.interp(ages[m], lng[:, 0], lng[:, 2]) + shift - OFFSET
fit = ages <= 798
b, a0 = np.polyfit(d18[fit], sea[fit], 1)
m = ages > 798
est = a0 + b * d18
sea[m] = est[m] + (sea[798] - est[798])
sea = np.round(sea, 1)

# --- EPICA Dome C
rows = []
for line in open(edc):
    p = line.split()
    if len(p) == 5:
        try:
            rows.append((float(p[2]) / 1000, float(p[4])))
        except ValueError:
            pass
e = np.array(rows)
gm = np.full(len(ages), np.nan)
for k in ages[ages <= 800]:
    sel = (e[:, 0] >= k - 0.5) & (e[:, 0] < k + 0.5)
    v = e[sel, 1].mean() if sel.any() else np.interp(k, e[:, 0], e[:, 1])
    gm[k] = 14.0 + 0.644 * v
fit = ages <= 800
bt, at = np.polyfit(d18[fit], gm[fit], 1)
estt = at + bt * d18
m = ages > 800
gm[m] = estt[m] + (gm[800] - estt[800])
gm = np.round(gm, 2)

sj = json.load(open(f'{out}/sealevel.json'))
sj.update({
    'source': 'Spratt & Lisiecki 2016, Clim. Past 12:1079, doi:10.5194/cp-12-1079-2016 (NOAA study 19982): short PC1 stack '
              '0–430 ka, long PC1 stack 430–798 ka, shifted so today = 0 m; 798–3,300 ka estimated from the LR04 benthic '
              'd18O stack (Lisiecki & Raymo 2005, Paleoceanography 20:PA1003, doi:10.1029/2004PA001071) by a linear fit '
              f'over 0–798 ka (sea = {a0:.1f} {b:+.1f} × d18O m) — less certain.',
    'offset_m': OFFSET, 'step_ka': 1, 'sea': sea.tolist(),
})
sj.pop('sigma', None)
json.dump(sj, open(f'{out}/sealevel.json', 'w'), ensure_ascii=False, separators=(',', ':'))
tj = json.load(open(f'{out}/temperature.json'))
tj['source'] = ('Antarctic temperature anomaly from EPICA Dome C (Jouzel et al. 2007, Science 317:793, '
                'doi:10.1126/science.1141038; NOAA), scaled so the Last Glacial Maximum is −6.1 °C below today (Tierney '
                'et al. 2020, Nature 584:569, doi:10.1038/s41586-020-2617-x), added to 14.0 °C, 0–800 ka; 800–3,300 ka '
                'estimated from the LR04 benthic d18O stack (Lisiecki & Raymo 2005, doi:10.1029/2004PA001071) by a linear '
                f'fit over 0–800 ka ({at:.1f} {bt:+.2f} × d18O °C). An approximation of global mean surface temperature.')
tj['gmst'] = gm.tolist()
json.dump(tj, open(f'{out}/temperature.json', 'w'), ensure_ascii=False, separators=(',', ':'))
r = np.corrcoef(d18[ages <= 798], sea[ages <= 798])[0, 1]
print(f'sea fit {a0:.1f} {b:+.1f}*d18O (r={r:.2f}); temp fit {at:.1f} {bt:+.2f}*d18O; '
      f'sea 798..2000 range {sea[799:].min():.0f}..{sea[799:].max():.0f} m; temp {gm[801:].min():.1f}..{gm[801:].max():.1f} °C')
