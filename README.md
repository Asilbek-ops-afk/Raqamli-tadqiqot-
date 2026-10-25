# Raqamli Tadqiqot — tuzatilgan versiya

**Joriy versiya: `v2.2.0`** (`<html data-version>` da ham belgilangan)

| Tag | Commit | Tarkibi |
|---|---|---|
| `v1.0.0` | `dc9d855` | Asl klon (`raqamli-tadqiqot-v2.pages.dev`, o'zgartirilmagan) — `asl-klon-v1` branch |
| `v2.0.0` | `90f671d` | P0–P2 tuzatishlar: logo, DATA modeli, SEO, a11y, o'lik CSS |
| `v2.1.0` | `d209550` | Dizayn tizimi: tip/radius/oraliq shkalalari, zebra, roadmap, bento, footer |
| `v2.2.0` | joriy | Reliz paketi: og.webp (−90%), Twitter Card, `_headers` CSP, cache siyosati |

Sayt: **Raqamli Tadqiqot — AI dalillarini o'lchaydigan talabalar tashabbusi** (TDIU).
Bu papka `https://raqamli-tadqiqot-v2.pages.dev/` saytining **professional darajada qayta ishlangan** kloni.

- Asl klon: `../site/` (o'zgartirilmagan, solishtirish uchun)
- O'zgarishlar ro'yxati: [`OZGARISHLAR.md`](OZGARISHLAR.md)
- To'liq UI tahlili: [`../UI-TAHLIL.md`](../UI-TAHLIL.md)

---

## Nima o'zgardi (qisqa)

| Muammo (aslda) | Holat (tuzatilganda) |
|---|---|
| Logotip 2× base64 HTML ichida (34 936 B) | Tashqi `logo.webp` (8 300 B), preload bilan |
| Takroriy `id="lgc112"` | Yo'q (114 id, hammasi noyob) |
| `32,6/100` — keltirib chiqarib bo'lmaydigan raqam | Hisoblangan **"Dalil qamrovi — 50% (30/60)"** + metodika izohi; indeks formulasi `DATA.meta` da hujjatlangan |
| Shkala chalkash (`c` = bank soni, ball deb ishlatilgan) | `ev` (dalil soni 0–10) + `st` (ball 0–3, hozir `null`); terminologiya: matritsa = "dalil", kalkulyator = "ball" |
| Login → `/admin.html` → **404** | `RT_ADMIN_URL` sozlamasi; bo'sh bo'lsa halol xabar |
| FAQ/roadmap faqat JS'da (SEO = 0, JS'siz bo'sh) | Statik server-render + JS faqat bo'sh konteynerda (progressive enhancement) |
| 5 ta canonical/OG noto'g'ri domenga | Barchasi `raqamli-tadqiqot-v2.pages.dev` + FAQPage schema |
| 29 ta SVG `aria-hidden`'siz, skip-link yo'q, `.sr` ishlatilmagan, canvas fallback yo'q, dark tugma 3,91:1, mobil tugmalar 40px | Hammasi tuzatildi (WCAG 2.1 AA) |
| ~2,5 KB o'lik CSS (eski DOM-o'yin qoldig'i) | O'chirildi, ishlatiladiganlar saqlandi |
| 3 xil navigatsiya nomlash | Birlashtirildi; `#qoshil` qo'shildi |
| Dizayn tizimi yo'q (30+ shrift, 24 radius, 12+ tugma kombini) | Shkalalar: tip `12–52` (12 qiymat), radius 6 token, oraliq 4px-grid; `--fs-*`, `--r-*`, `--shadowBtn*` tokenlari |
| Zebra notekis, eyebrow ikki xil, roadmap kesilgan, footer «yopmaydi» | Zebra `NANANANAN`, yagona `.kick`, scroll fade+scrollbar, navy footer-qatlam |

**Hajm:** 200 109 B → **174 697 B** raw (−12,7%) · gzip 75 672 B → **49 404 B** (−34,7%)

---

## Tuzilma

```
.
├── index.html          # butun sayt: HTML + CSS + JS (inline), statik FAQ/roadmap bilan
├── logo.webp           # 384×384, yumaloq burchakli logotip (base64 o'rniga)
├── favicon.svg
├── apple-touch-icon.png
├── og.png              # ijtimoiy tarmoq rasm (1200×630)
├── robots.txt          # to'g'ri domenga
├── sitemap.xml         # to'g'ri domenga
├── fonts/              # Inter, 5 og'irlik (woff2, self-hosted)
├── OZGARISHLAR.md      # to'liq changelog + tekshiruv natijalari
└── README.md
```

## Sahifa bo'limlari (anchor'lar)

| Anchor | Bo'lim | Kontent holati |
|---|---|---|
| `#top` | Hero | statik + JS matritsa |
| `#qanday` | Qanday ishlaydi | statik |
| `#qizil` | Qizil jamoa | statik |
| `#pilot` | Pilot natijasi | statik sarlavha + JS matritsa/segmentlar |
| `#hisobla` | Kalkulyator | JS (interaktiv) |
| `#klub` | Klub (bento) | statik |
| `#yol` | Yo'l xaritasi | **statik (8/8)** + JS enhancement |
| `#sinov` | Sinov o'yini | JS (canvas) + fallback matn |
| `#qoshil` | Qo'shilish | statik + QR |
| `#faq` | Savol-javob | **statik (9/9)** + JS akkordeon |

## Mahalliy ishga tushirish

```bash
python3 -m http.server 8080        # yoki istalgan statik server
```

## Sozlamalar (index.html ichida)

```js
var RT_API      = "https://aiindeksi-bot.onrender.com";  // login tekshiruvi backend'i
var RT_ADMIN_URL = "";   // ← yopiq panel manzili. Bo'sh = halol "ulanmagan" xabari.
                         //   Panel tayyor bo'lgach shu yerga yozing (masalan "/admin.html")
```

## Indeks qanday hisoblanadi (hujjatlangan metodika)

```
Qamrov  = to'ldirilgan katak / jami katak          = 30/60 = 50%   (sahifada ko'rinadi)
Indeks  = Σ(vazn × ball) / (3 × Σvazn) × 100        ball ∈ 0–3      (DATA.meta.formula_indeks)
```

Indeks hisoblash uchun har o'lchovga **0–3 kuchi balli** kerak — `DATA.dims[].st` maydoni
(hozircha `null`). Qiymatlarni to'ldirsangiz kalkulyator va metodika bir xil formulada ishlaydi.

## Deploy

Cloudflare Pages: repo'ni ulang, **Build command: bo'sh**, **Output directory: `/`**.
Statik sayt — build talab qilinmaydi.

## Tekshiruvlar

- 60+ statik assertion (`verify.py`) — barchasi OK
- 5/5 JS bloki `node --check` — sintaksis toza
- 90+ Chromium (Playwright) runtime testi — barchasi OK, shu jumladan:
  JS'siz holat (FAQ 9/9, roadmap 8/8), reduced-motion, fokus tartibi, modal trap,
  390/768/1440 px overflow=0, mavzu almashinuvi, kalkulyator formulasi
