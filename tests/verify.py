#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tuzatilgan sayt uchun qat'iy statik verifikatsiya.
Ishlatish:  python3 tests/verify.py [tuzatilgan_index.html] [asl_index.html]
Ikkinchi argument ixtiyoriy (asl nusxa bilan hajm solishtiruvi uchun)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'index.html')
ORIG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', '..', 'site', 'index.html')
if not os.path.exists(ORIG): ORIG = None
import re, gzip, json, os, subprocess
from collections import Counter

h = open(SRC, encoding='utf-8').read()
orig = open(ORIG, encoding='utf-8').read() if ORIG else None
FAIL = []
def chk(ok, msg):
    print(("  [OK]   " if ok else "  [FAIL] ") + msg)
    if not ok: FAIL.append(msg)

print("=" * 74); print("A. HAJM VA SIQISH"); print("=" * 74)
r2, g2 = len(h.encode()), len(gzip.compress(h.encode(), 9))
print(f"  TUZATILGAN  raw {r2:>7} B   gzip {g2:>6} B")
if orig:
    r1, g1 = len(orig.encode()), len(gzip.compress(orig.encode(), 9))
    print(f"  ASL         raw {r1:>7} B   gzip {g1:>6} B")
    print(f"  TEJASH      raw {r1-r2:>7} B ({(r1-r2)/r1*100:.1f}%)   gzip {g1-g2:>6} B ({(g1-g2)/g1*100:.1f}%)")
    chk(g2 < g1, f"gzip hajmi kamaydi: {g1} -> {g2}")
else:
    print("  (asl nusxa ko'rsatilmagan - solishtiruv o'tkazildi)")

print(); print("=" * 74); print("B. HTML YAXLITLIGI"); print("=" * 74)
ids = re.findall(r'\bid="([^"]+)"', h)
dup = {k: v for k, v in Counter(ids).items() if v > 1}
chk(not dup, f"takrorlanuvchi id yo'q (jami {len(ids)}, duplikat: {dup})")
chk(len(re.findall(r'data:image/[a-z]+;base64', h)) == 0, "base64 data-uri yo'q")
svgs = re.findall(r'<svg[^>]*>', h)
hid = len([s for s in svgs if 'aria-hidden' in s]); rol = len([s for s in svgs if 'role=' in s])
chk(hid + rol == len(svgs), f"barcha SVG belgilangan: {hid} aria-hidden + {rol} role=img = {len(svgs)}")
chk(h.count('class="sr"') >= 2, f".sr sinfi ishlatilgan: {h.count('class=\"sr\"')} marta")
chk('class="skip"' in h, "skip-link bor")
chk(bool(re.search(r'<canvas[^>]*>[^<]{20,}', h)), "canvas fallback matni bor")
chk(h.count('color-scheme') >= 2, f"color-scheme: {h.count('color-scheme')}")
chk(h.count('32,6') == 0, "32,6 butunlay olib tashlandi")
chk(h.count('raqamlitadqiqot.pages.dev') == 0, "eski domen olib tashlandi")
chk(h.count('raqamli-tadqiqot-v2.pages.dev') >= 5, f"yangi domen: {h.count('raqamli-tadqiqot-v2.pages.dev')} joy")
chk(h.count('"/admin.html"') == 0, "/admin.html redirect olib tashlandi")
chk('RT_ADMIN_URL' in h, "RT_ADMIN_URL sozlamasi bor")
chk('3–4 mezonga' in h, "'3–4 mezonga' tuzatildi")
chk(h.count('<label') >= 2, f"label: {h.count('<label')}")
chk('role="dialog"' in h and 'aria-labelledby="kirTitle"' in h, "kirModal ARIA to'liq")
chk('trapFocus' in h, "modal focus trap bor")

# teglar muvozanati
for t in ['div', 'section', 'button', 'span', 'a', 'p', 'h2', 'h3', 'script', 'style', 'header', 'footer', 'main', 'nav', 'label']:
    o = len(re.findall(r'<' + t + r'[\s>]', h)); c = len(re.findall(r'</' + t + r'>', h))
    if o != c:
        chk(False, f"<{t}> muvozanatsiz: {o} ochilish / {c} yopilish")
print("  [OK]   barcha asosiy teglar muvozanati tekshirildi")

print(); print("=" * 74); print("C. STATIK KONTENT (SEO)"); print("=" * 74)
i = h.find('<section id="faq"'); j = h.find('<!-- FINAL -->')
faq_sz = j - i; faq_btn = h[i:j].count('<button')
chk(faq_btn == 9, f"#faq statik: {faq_sz} B (oldin 201 B), {faq_btn}/9 savol HTML'da")
i = h.find('<section id="yol"'); j = h.find('<!-- JOIN -->')
road_sz = j - i; road_ms = h[i:j].count('class="ms')
chk(road_ms == 8, f"#yol statik: {road_sz} B (oldin 247 B), {road_ms}/8 band HTML'da")
chk('FAQPage' in h, "FAQPage schema.org qo'shildi")
ld = json.loads(re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema.org","@type":"Project".*?)</script>', h, re.S).group(1))
chk('alternateName' not in ld, "sahifada yo'q alternateName olib tashlandi")
chk(ld['url'].endswith('raqamli-tadqiqot-v2.pages.dev/'), f"JSON-LD url: {ld['url']}")
chk(os.path.exists(os.path.join(os.path.dirname(SRC), 'logo.webp')), "logo.webp fayli mavjud")
chk(open(os.path.join(os.path.dirname(SRC), 'robots.txt')).read().find('raqamli-tadqiqot-v2') > 0, "robots.txt to'g'ri domen")
chk(open(os.path.join(os.path.dirname(SRC), 'sitemap.xml')).read().find('raqamli-tadqiqot-v2') > 0, "sitemap.xml to'g'ri domen")

print(); print("=" * 74); print("D. DATA MODELI"); print("=" * 74)
i = h.find('var DATA = ') + len('var DATA = '); d = 0; j = i
while j < len(h):
    if h[j] == '{': d += 1
    elif h[j] == '}':
        d -= 1
        if d == 0: j += 1; break
    j += 1
DATA = json.loads(h[i:j])
chk('meta' in DATA, "DATA.meta qo'shildi")
chk(all('ev' in x and 'st' in x and 'c' not in x for x in DATA['dims']), "dims: 'c' -> 'ev' + 'st'")
chk(sum(x['w'] for x in DATA['dims']) == 100, f"vaznlar yig'indisi = {sum(x['w'] for x in DATA['dims'])}")
chk(sum(DATA['flat']) == 30 and len(DATA['flat']) == 60, "matritsa 30/60")
chk([c for r in DATA['rows'] for c in r] == DATA['flat'], "rows -> flat mosligi saqlandi")
chk(all(x['ev'] == sum(r[k] for r in DATA['rows']) for k, x in enumerate(DATA['dims'])),
    "ev qiymatlari matritsa bilan mos (har o'lchov ustuni yig'indisi)")
chk('d.ev/DATA.nb' in h and h.count('d.c/') == 0, "JS: d.c -> d.ev almashtirildi")
chk('meta.c' in h, "meta.c (o'yin kartasi rangi) saqlandi")

print(); print("=" * 74); print("E. JAVASCRIPT SINTAKSISI (node --check)"); print("=" * 74)
blocks = re.findall(r'<script(?![^>]*ld\+json)[^>]*>(.*?)</script>', h, re.S)
print(f"  {len(blocks)} ta JS blok topildi")
ok_all = True
for n, b in enumerate(blocks, 1):
    fn = f'/tmp/js{n}.js'
    open(fn, 'w', encoding='utf-8').write(b)
    r = subprocess.run(['node', '--check', fn], capture_output=True, text=True)
    st = "OK" if r.returncode == 0 else "FAIL"
    print(f"  [{st}]  JS-{n}  ({len(b)} B)")
    if r.returncode != 0:
        ok_all = False
        print("        " + (r.stderr.strip().split('\n')[0:6] and '\n        '.join(r.stderr.strip().split('\n')[:6])))
        FAIL.append(f"JS-{n} sintaksis xatosi")
chk(ok_all, "barcha JS bloklari sintaktik to'g'ri")

# JSON-LD bloklari
for n, m in enumerate(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S), 1):
    try:
        json.loads(m.group(1)); print(f"  [OK]   JSON-LD #{n} yaroqli")
    except Exception as e:
        print(f"  [FAIL] JSON-LD #{n}: {e}"); FAIL.append(f"JSON-LD #{n}")

print(); print("=" * 74)
if FAIL:
    print(f"❌ {len(FAIL)} TA MUAMMO:")
    for f in FAIL: print("   -", f)
else:
    print("✅ BARCHA TEKSHIRUVLAR MUVAFFAQIYATLI O'TDI")
print("=" * 74)
