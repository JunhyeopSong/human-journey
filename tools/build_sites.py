"""Build docs/data/sites.json: dated sites attributed to a human species, for the species-range layer.

Sources (download them first; they are not stored in this repository):
  1. Timmermann, A. et al. (2022) Climate effects on archaic human habitats and species successions. Nature 604, 495–501.
     doi:10.1038/s41586-022-04600-9 — Supplementary Table 1 (database of hominin remains and artefacts), CC BY 4.0:
     https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-022-04600-9/MediaObjects/41586_2022_4600_MOESM3_ESM.xlsx
  2. ROAD — ROCEEH Out of Africa Database, data snapshot of Kandel, A.W. et al. (2023), Zenodo 7669784, CC BY-SA 4.0:
     https://zenodo.org/records/7669784  (file Kandel_etal_2023.zip → fig_coverage/road_coverage.csv)
     Used only for records younger than 30 ka with tight dates (≤ 8 kyr wide); by then Homo sapiens is the only human.
  3. A short curated list below (the Americas, Sahul, remote Oceania, Denisovans and island species), each with its
     publication.

Because ROAD is CC BY-SA 4.0, the generated sites.json is released under CC BY-SA 4.0 as well.

usage: python3 tools/build_sites.py <MOESM3_ESM.xlsx> <road_coverage.csv> docs/data/sites.json
"""
import sys, re, csv, json, zipfile

XLSX, ROAD, OUT = sys.argv[1:4]

SPECIES = ['sapiens', 'neanderthal', 'denisovan', 'heidelbergensis', 'erectus', 'floresiensis', 'luzonensis', 'naledi',
           'ergaster', 'habilis', 'antecessor', 'paranthropus', 'sediba']
MAX_KA = 2100       # the app covers the last 2 million years
SOURCES = [
    {'label': 'Timmermann et al. 2022, Nature — Suppl. Table 1 (CC BY 4.0)', 'url': 'https://doi.org/10.1038/s41586-022-04600-9'},
    {'label': 'ROAD, ROCEEH Out of Africa Database — Kandel et al. 2023 (CC BY-SA 4.0)', 'url': 'https://zenodo.org/records/7669784'},
]


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def read_xlsx_first_sheet(path):
    z = zipfile.ZipFile(path)
    ss = z.read('xl/sharedStrings.xml').decode()
    strs = [re.sub(r'<[^>]+>', '', m) for m in re.findall(r'<si>(.*?)</si>', ss, re.S)]
    wb = z.read('xl/workbook.xml').decode()
    rels = z.read('xl/_rels/workbook.xml.rels').decode()
    rid = re.findall(r'<sheet name="[^"]+" sheetId="\d+" r:id="(rId\d+)"', wb)[0]
    tgt = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    tgt.update({r: t for t, r in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)})
    xml = z.read('xl/' + tgt[rid].lstrip('/').replace('xl/', '')).decode()
    rows = []
    for r in re.findall(r'<row[^>]*>(.*?)</row>', xml, re.S):
        cells = {}
        for ref, t, v in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(?:<f>.*?</f>)?<v>([^<]*)</v>', r):
            cells[ref] = strs[int(v)] if 't="s"' in t else v
        rows.append(cells)
    hdr = rows[0]
    keys = sorted(hdr, key=lambda k: (len(k), k))
    return [{hdr[k]: r.get(k) for k in keys} for r in rows[1:]]


sites = {}   # dedupe key -> [species, lon, lat, min_ka, max_ka, disputed, source]


def add(sp, lon, lat, a0, a1, disputed, src):
    if None in (lon, lat, a0, a1) or a1 < a0:
        return
    rec = [SPECIES.index(sp) if sp in SPECIES else -1, round(lon, 2), round(lat, 2), round(a0, 1), round(a1, 1), 1 if disputed else 0, src]
    sites[(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5])] = rec


# 1. Timmermann et al. 2022 — species-attributed; "A/B" attributions are disputed
TMAP = {'Homo sapiens': 'sapiens', 'Homo neanderthalensis': 'neanderthal', 'Homo heidelbergensis': 'heidelbergensis', 'Homo erectus': 'erectus',
        'Homo ergaster': 'ergaster', 'Homo habilis': 'habilis'}
for d in read_xlsx_first_sheet(XLSX):
    sp = d['species'] or ''
    lon, lat, a0, a1 = num(d['long']), num(d['lat']), num(d['min.age']), num(d['max.age'])
    if a0 is None or a1 is None:
        continue
    a0, a1 = a0 / 1000, a1 / 1000
    if a0 > MAX_KA:
        continue
    if '/' in sp:
        first = TMAP.get(sp.split('/')[0].strip())
        add(first or 'sapiens', lon, lat, a0, a1, True, 0)
    elif sp in TMAP:
        add(TMAP[sp], lon, lat, a0, a1, False, 0)

# 2. ROAD — younger than 30 ka, tightly dated: Homo sapiens
for r in csv.DictReader(open(ROAD, encoding='utf-8', errors='ignore')):
    lon, lat, a0, a1 = num(r['locality.x']), num(r['locality.y']), num(r['query_age_min']), num(r['query_age_max'])
    if None in (lon, lat, a0, a1):
        continue
    if a1 <= 30000 and a1 - a0 <= 8000:
        add('sapiens', lon, lat, a0 / 1000, a1 / 1000, False, 1)

# 3. Curated: regions and species the two databases do not cover (ages in ka)
CURATED = [
    # sp, name, lon, lat, min, max, disputed, label, doi
    ('sapiens', 'Madjedbebe (early claim)', 132.9, -12.5, 50, 65, True, 'Clarkson et al. 2017, Nature', '10.1038/nature22968'),
    ('sapiens', 'Madjedbebe / Sahul (accepted)', 132.9, -12.5, 46, 50, False, "O'Connell et al. 2018, PNAS", '10.1073/pnas.1808385115'),
    ('sapiens', "Devil's Lair", 115.1, -34.1, 45, 48, False, 'Turney et al. 2001, Quat. Res.', '10.1006/qres.2000.2195'),
    ('sapiens', 'Lake Mungo', 143.0, -33.7, 40, 42, False, 'Bowler et al. 2003, Nature', '10.1038/nature01383'),
    ('sapiens', 'Ivane Valley, New Guinea', 147.0, -8.0, 43, 49, False, 'Summerhayes et al. 2010, Science', '10.1126/science.1193130'),
    ('sapiens', 'Warratyi rock shelter', 138.3, -30.2, 44, 49, False, 'Hamm et al. 2016, Nature', '10.1038/nature20125'),
    ('sapiens', 'Lida Ajer, Sumatra', 100.6, -0.5, 63, 73, False, 'Westaway et al. 2017, Nature', '10.1038/nature23452'),
    ('sapiens', 'Tam Pa Ling, Laos', 103.4, 20.2, 68, 86, False, 'Freidline et al. 2023, Nat. Commun.', '10.1038/s41467-023-38715-y'),
    ('sapiens', 'Niah Cave, Borneo', 113.8, 3.8, 35, 50, False, 'Barker et al. 2007, J. Hum. Evol.', '10.1016/j.jhevol.2006.08.011'),
    ('sapiens', 'Bluefish Caves (claim)', -140.5, 67.1, 19, 24, True, 'Bourgeon et al. 2017, PLOS ONE', '10.1371/journal.pone.0169486'),
    ('sapiens', 'White Sands footprints', -106.3, 32.8, 21, 23, True, 'Bennett et al. 2021, Science', '10.1126/science.abg7586'),
    ('sapiens', "Cooper's Ferry", -116.4, 45.9, 15.5, 16.5, False, 'Davis et al. 2019, Science', '10.1126/science.aax9830'),
    ('sapiens', 'Paisley Caves', -120.5, 43.3, 14.2, 14.6, False, 'Gilbert et al. 2008, Science', '10.1126/science.1154116'),
    ('sapiens', 'Swan Point', -145.9, 64.3, 14.0, 14.3, False, 'Braje et al. 2017, Science', '10.1126/science.aao5473'),
    ('sapiens', 'Page-Ladson', -84.0, 30.4, 14.4, 14.6, False, 'Halligan et al. 2016, Sci. Adv.', '10.1126/sciadv.1600375'),
    ('sapiens', 'Meadowcroft (early claim)', -80.5, 40.5, 16, 19, True, 'Braje et al. 2017, Science', '10.1126/science.aao5473'),
    ('sapiens', 'Huaca Prieta', -79.3, -7.9, 13.5, 15, False, 'Dillehay et al. 2017, Sci. Adv.', '10.1126/sciadv.1602778'),
    ('sapiens', 'Monte Verde', -73.2, -41.5, 14.2, 14.6, False, 'Dillehay et al. 2015, PLOS ONE', '10.1371/journal.pone.0141923'),
    ('sapiens', 'Arroyo Seco 2', -60.2, -38.4, 13.5, 14.1, False, 'Politis et al. 2016, PLOS ONE', '10.1371/journal.pone.0162870'),
    ('sapiens', 'Blackwater Draw (Clovis)', -103.3, 34.3, 12.8, 13.1, False, 'Waters & Stafford 2007, Science', '10.1126/science.1137166'),
    ('sapiens', 'Anzick', -110.4, 45.8, 12.6, 12.9, False, 'Rasmussen et al. 2014, Nature', '10.1038/nature13025'),
    ('sapiens', 'Fell Cave', -69.8, -52.0, 10.5, 12.5, False, 'Braje et al. 2017, Science', '10.1126/science.aao5473'),
    ('sapiens', 'Kennewick', -119.2, 46.2, 8.5, 9.5, False, 'Rasmussen et al. 2015, Nature', '10.1038/nature14625'),
    ('sapiens', 'Teouma, Vanuatu (Lapita)', 168.4, -17.8, 2.9, 3.0, False, 'Bedford et al. 2006, Antiquity', '10.1017/S0003598X00094448'),
    ('sapiens', 'Nukuleka, Tonga (Lapita)', -175.2, -21.1, 2.8, 2.9, False, 'Burley, Weisler & Zhao 2012, PLOS ONE', '10.1371/journal.pone.0048769'),
    ('sapiens', 'Society Islands', -151.5, -16.5, 0.83, 0.93, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    ('sapiens', 'Hawaiʻi', -155.5, 19.6, 0.75, 0.95, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    ('sapiens', 'Rapa Nui', -109.4, -27.1, 0.7, 0.8, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    ('sapiens', 'Aotearoa (Wairau Bar)', 174.0, -41.5, 0.65, 0.70, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    # islands and regions reached by boat or without a dated site in the databases (the arrival model never crosses sea)
    ('sapiens', 'Aotearoa (North Island)', 175.5, -37.8, 0.65, 0.70, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    ('sapiens', 'Hawaiʻi (Maui)', -156.3, 20.8, 0.75, 0.95, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    ('sapiens', 'Hawaiʻi (Oʻahu)', -158.0, 21.45, 0.75, 0.95, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    ('sapiens', 'Hawaiʻi (Kauaʻi)', -159.5, 22.05, 0.75, 0.95, False, 'Wilmshurst et al. 2011, PNAS', '10.1073/pnas.1015876108'),
    ('sapiens', 'Caverna da Pedra Pintada, Amazon', -54.2, -2.0, 11.4, 13.0, False, 'Roosevelt et al. 1996, Science', '10.1126/science.272.5260.373'),
    ('sapiens', 'Lapa do Santo, Lagoa Santa', -44.03, -19.48, 8.0, 11.7, False, 'Strauss et al. 2015, PLOS ONE', '10.1371/journal.pone.0137456'),
    ('sapiens', 'Cuba', -79.5, 21.8, 4.79, 5.06, False, 'Napolitano et al. 2019, Sci. Adv.', '10.1126/sciadv.aar7806'),
    ('sapiens', 'Puerto Rico', -66.5, 18.2, 4.39, 4.58, False, 'Napolitano et al. 2019, Sci. Adv.', '10.1126/sciadv.aar7806'),
    ('sapiens', 'Hispaniola', -70.7, 19.0, 4.04, 4.39, False, 'Napolitano et al. 2019, Sci. Adv.', '10.1126/sciadv.aar7806'),
    ('sapiens', 'Jamaica', -77.3, 18.1, 0.58, 0.98, False, 'Napolitano et al. 2019, Sci. Adv.', '10.1126/sciadv.aar7806'),
    ('sapiens', 'Madagascar', 46.8, -19.0, 1.1, 1.35, False, 'Anderson et al. 2018, PLOS ONE', '10.1371/journal.pone.0204368'),
    ('sapiens', 'Madagascar (early Holocene claim)', 44.5, -22.0, 10.0, 10.5, True, 'Hansford et al. 2018, Sci. Adv.', '10.1126/sciadv.aat6925'),
    ('sapiens', 'Qeqertasussuk, Greenland (Saqqaq)', -51.3, 68.8, 3.9, 4.1, False, 'Rasmussen et al. 2010, Nature', '10.1038/nature08835'),
    ('sapiens', 'Leang Tedongnge, Sulawesi', 119.6, -4.9, 45.5, 46.0, False, 'Brumm et al. 2021, Sci. Adv.', '10.1126/sciadv.abd4648'),
    ('sapiens', 'Jerimalai, Timor', 127.2, -8.4, 38.0, 42.0, False, "O'Connor et al. 2011, Science", '10.1126/science.1207703'),
    ('sapiens', 'Knossos, Crete', 25.16, 35.3, 8.7, 9.0, False, 'Douka et al. 2017, Antiquity', '10.15184/aqy.2017.29'),
    ('sapiens', 'New Caledonia (Lapita)', 165.0, -21.5, 2.9, 3.05, False, 'Sand 1997, Antiquity', '10.1017/s0003598x00085318'),
    ('sapiens', 'Bourewa, Fiji (Lapita)', 177.6, -18.2, 2.8, 2.9, False, 'Nunn & Petchey 2013, J. Pac. Archaeol.', '10.70460/jpa.v4i2.118'),
    ('sapiens', 'Mulifanua, Samoa (Lapita)', -172.0, -13.8, 2.7, 2.88, False, 'Petchey 2001, Radiocarbon', '10.1017/s0033822200031635'),
    ('sapiens', 'Iceland (Landnám)', -21.9, 64.1, 1.05, 1.13, False, 'Vésteinsson & McGovern 2012, Norw. Archaeol. Rev.', '10.1080/00293652.2012.721792'),
    # older than 300 ka: species and sites not in Timmermann et al. 2022
    ('antecessor', 'Gran Dolina TD6, Atapuerca', -3.52, 42.35, 0.77, 0.95, False, 'Bermúdez de Castro et al. 1997, Science', '10.1126/science.276.5317.1392'),
    ('antecessor', 'Sima del Elefante, Atapuerca (Homo sp.)', -3.52, 42.36, 1.1, 1.3, True, 'Carbonell et al. 2008, Nature', '10.1038/nature06815'),
    ('erectus', 'Dmanisi', 44.34, 41.34, 1.77, 1.85, False, 'Lordkipanidze et al. 2013, Science', '10.1126/science.1238484'),
    ('erectus', 'Shangchen, Loess Plateau (artefacts)', 109.6, 34.1, 1.26, 2.12, True, 'Zhu et al. 2018, Nature', '10.1038/s41586-018-0299-4'),
    ('floresiensis', 'Mata Menge, Flores', 121.1, -8.6, 0.65, 0.75, False, 'van den Bergh et al. 2016, Nature', '10.1038/nature17999'),
    ('paranthropus', 'Olduvai Gorge (OH 5)', 35.35, -2.99, 1.75, 1.85, False, 'Leakey 1959, Nature', '10.1038/184491a0'),
    ('paranthropus', 'Koobi Fora', 36.3, 3.95, 1.4, 2.0, False, 'Wood & Constantino 2007, Am. J. Phys. Anthropol.', '10.1002/ajpa.20732'),
    ('paranthropus', 'Omo Shungura', 36.0, 5.0, 1.4, 2.3, False, 'Wood & Constantino 2007, Am. J. Phys. Anthropol.', '10.1002/ajpa.20732'),
    ('paranthropus', 'Konso', 37.4, 5.3, 1.4, 1.45, False, 'Wood & Constantino 2007, Am. J. Phys. Anthropol.', '10.1002/ajpa.20732'),
    ('paranthropus', 'Peninj', 35.9, -2.4, 1.3, 1.5, False, 'Wood & Constantino 2007, Am. J. Phys. Anthropol.', '10.1002/ajpa.20732'),
    ('paranthropus', 'Drimolen', 27.75, -25.97, 1.95, 2.04, False, 'Herries et al. 2020, Science', '10.1126/science.aaw7293'),
    ('paranthropus', 'Swartkrans', 27.72, -26.02, 1.0, 2.0, False, 'Herries et al. 2020, Science', '10.1126/science.aaw7293'),
    ('sediba', 'Malapa', 27.8, -25.89, 1.97, 1.98, False, 'Pickering et al. 2011, Science', '10.1126/science.1203697'),
    ('denisovan', 'Denisova Cave', 84.68, 51.4, 50, 200, False, 'Slon et al. 2018, Nature', '10.1038/s41586-018-0455-x'),
    ('denisovan', 'Baishiya Karst Cave', 102.57, 35.45, 45, 190, False, 'Chen et al. 2019, Nature', '10.1038/s41586-019-1139-x'),
    ('denisovan', 'Harbin', 126.6, 45.8, 138, 170, True, 'Ji et al. 2021, The Innovation', '10.1016/j.xinn.2021.100132'),
    ('denisovan', 'Tam Ngu Hao 2 (Cobra Cave)', 103.0, 20.2, 131, 164, True, 'Demeter et al. 2022, Nat. Commun.', '10.1038/s41467-022-29923-z'),
    ('floresiensis', 'Liang Bua', 120.46, -8.53, 50, 100, False, 'Sutikna et al. 2016, Nature', '10.1038/nature17179'),
    ('luzonensis', 'Callao Cave', 121.82, 17.7, 50, 67, False, 'Détroit et al. 2019, Nature', '10.1038/s41586-019-1067-9'),
    ('naledi', 'Rising Star Cave', 27.73, -26.02, 236, 335, False, 'Dirks et al. 2017, eLife', '10.7554/eLife.24231'),
    ('erectus', 'Ngandong', 111.33, -7.37, 108, 117, False, 'Rizal et al. 2019, Nature', '10.1038/s41586-019-1863-2'),
]
for sp, name, lon, lat, a0, a1, disp, label, doi in CURATED:
    lab = f'{label} — {name}'
    src = next((i for i, s in enumerate(SOURCES) if s['label'] == lab), None)
    if src is None:
        SOURCES.append({'label': lab, 'url': 'https://doi.org/' + doi}); src = len(SOURCES) - 1
    add(sp, lon, lat, a0, a1, disp, src)

recs = sorted(sites.values(), key=lambda r: (r[0], -r[4]))
out = {
    'note': 'Dated sites attributed to a human species. Each record: [species index, lon, lat, min age ka, max age ka, '
            'disputed (attribution or date debated), source index]. Built by tools/build_sites.py. Contains records derived '
            'from ROAD (CC BY-SA 4.0), so this file is released under CC BY-SA 4.0.',
    'license': 'CC BY-SA 4.0', 'species': SPECIES, 'sources': SOURCES, 'sites': recs,
}
json.dump(out, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
from collections import Counter
print(len(recs), 'sites', {SPECIES[k]: v for k, v in Counter(r[0] for r in recs).items()}, 'disputed', sum(r[5] for r in recs))
