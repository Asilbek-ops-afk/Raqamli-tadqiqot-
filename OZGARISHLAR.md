# O'zgarishlar reyestri (CHANGELOG)

**Sana:** 24.10.2026
**Asos:** `index.html.orig` (asl klon, 200 109 B) → `index.html` (tuzatilgan, 172 647 B)
**Metod:** har bir o'zgarish assertion bilan tekshirilgan; yakunda 60+ statik tekshiruv, 5 ta JS bloki `node --check`, va 90+ real Chromium (Playwright) testi o'tkazilgan.

---

## Yakuniy o'lchovlar

| Ko'rsatkich | Asl | Tuzatilgan | Farq |
|---|---|---|---|
| `index.html` raw | 200 109 B | 172 647 B | **−27 462 B (−13,7%)** |
| `index.html` gzip | 75 672 B | 49 227 B | **−26 445 B (−34,9%)** |
| base64 inline rasm | 34 936 B (2 nusxa) | 0 B | −100% |
| Tashqi fayl qo'shildi | — | `logo.webp` 8 300 B | +8 300 B (1 marta) |
| `#faq` statik kontent | 201 B | 3 302 B | +16× (9/9 savol) |
| `#yol` statik kontent | 247 B | 1 017 B | +4× (8/8 band) |
| Takroriy `id` | 1 (`lgc112`×2) | 0 | tuzatildi |
| `aria-hidden`'siz SVG | 29 ta | 0 ta | 34/34 belgilangan |
| JS o'chirilgan FAQ | 0 ko'rinadi | 9/9 ko'rinadi | progressive enhancement |

---

## P0 — jiddiy muammolar (5/5 bajarildi)

### 1. Logotip: base64 → tashqi WebP
- **Muammo:** bitta 384×384 JPEG base64 ko'rinishida (17 468 belgi) HTML ichiga **2 marta** yopishtirilgan (header + footer).
- **Yechim:** `logo.webp` (8 300 B, yumaloq burchaklar `rx=112/512` nisbati bilan saqlangan) + `<img class="brandlogo" ... decoding="async" fetchpriority="high">`, `<link rel="preload">`, CSS `.brand svg,.brand img.brandlogo` va `border-radius:21.9%`.
- **Natija:** gzip **−28 KB ga yaqin**; brauzer faylni keshlaydi; har sahifada 2×17 KB pars qilinmaydi.

### 2. Takroriy `id="lgc112"` yo'q qilindi
- `<clipPath id="lgc112">` 2 marta takrorlanardi (HTML standartini buzadi, `getElementById` noto'g'ri ishlaydi). Logotip tashqi faylga ko'chgani sababli umuman qolmadi. **Tekshiruv: 114 ta id, hammasi noyob.**

### 3. `32,6/100` → hisoblanadigan metrika
- **Muammo:** raqam hech qanday formula bilan keltirib chiqarilmaydi (saytning o'z `calc()` si 166,67 beradi; 6 ta muqobil formula ham 32,6 bermaydi).
- **Yechim:**
  - `#pilot` endi **hisoblangan qamrovni** ko'rsatadi: **"Dalil qamrovi — 50% (30/60 katak)"**, yonida metodika izohi: *"Indeks (0–100) har dalilning kuchini 0–3 ball bilan baholashni talab qiladi — bu bosqich hali yakunlanmagan."*
  - FAQ'dagi *"32,6/100 nimani anglatadi?"* → *"Qamrov va indeks — nima farqi?"*
  - `DATA.meta` qo'shildi: kesim sanasi, indeks formulasi, holat izohi — **metodika endi kod ichida hujjatlangan**.
- **Qayta tiklash yo'li:** agar jamoaning ichki ishchi jadvalida 0–3 ballar mavjud bo'lsa, `DATA.dims[].st` maydoniga yozing — sahifa indeksni avtomatik hisoblaydi (formula `DATA.meta.formula_indeks` da).

### 4. Shkala chalkashligi: `c` → `ev` + `st`
- **Muammo:** `DATA.dims[].c` (0–10: nechta bankda dalil bor) kalkulyatorda **0–3 ball** deb ishlatilardi.
- **Yechim:**
  - `c` → **`ev`** (evidence: dalil qayd etilgan banklar soni, 0–10) va yangi **`st`** (strength: 0–3 ball, hozircha `null`).
  - JS'da 4 ta `d.c` → `d.ev` (`meta.c` — o'yin kartasi rangi — **tegilmadi**, alohida obyekt).
  - Terminologiya ajratildi: matritsa = **"dalil qayd etilgan"** (boolean), kalkulyator = **"ball"** (0–3). 6 ta joyda matn yangilandi (hero, pilot sarlavha/izoh/KPI, legenda, JS tooltip).

### 5. `/admin.html` 404 → sozlanadigan + halol xabar
- **Muammo:** login muvaffaqiyatli bo'lsa `window.location.href="/admin.html"` → **404**.
- **Yechim:** yangi `var RT_ADMIN_URL=""` sozlamasi. Bo'sh bo'lsa foydalanuvchiga aniq xabar: *"Kirish tasdiqlandi, ammo yopiq ishchi panel hali ulanmagan."* Panel tayyor bo'lgach bitta qatorga manzil yozish kifoya.
- Qo'shimcha: `kirModal` ga `role="dialog"`, `aria-modal`, `aria-labelledby`, 2 ta `<label class="sr">`, `autocomplete` atributlari, **fokus qopqoni** (`trapFocus`), yopish tugmasiga `aria-label` va 36px hit-area; fragil `querySelector('#kirModal button[onclick=...]')` → `getElementById('kirSubmit')`; inline DOM manipulyatsiyasi → `openKirish()`.

---

## P1 — SEO va ochiqlik

| # | Tuzatish |
|---|---|
| 1 | **5 ta noto'g'ri domen ishorasi** → `raqamli-tadqiqot-v2.pages.dev`: `canonical`, `og:url`, `og:image`, JSON-LD `url`/`logo`/`image`, `robots.txt`, `sitemap.xml` |
| 2 | `#faq` **statik server-render** (9/9 savol HTML'da) + JS faqat bo'sh konteynerda render qiladi (duplikat yo'q). **JS o'chirilgan brauzerda ham 9/9 ko'rinadi** |
| 3 | `#yol` **statik server-render** (8/8 band) — xuddi shu progressive enhancement |
| 4 | **FAQPage schema.org** qo'shildi (rich snippet imkoni) |
| 5 | JSON-LD'dan sahifada uchramaydigan `alternateName: ["RT Monitor","AAI-UZ pilot"]` olib tashlandi; `inLanguage:"uz"` qo'shildi |
| 6 | **29 ta dekorativ SVG** ga `aria-hidden="true"` (endi 34/34 belgilangan: 33 hidden + 1 `role="img"`) |
| 7 | **Skip-link** qo'shildi (`.skip`, fokusda ko'rinadi). Tekshiruv: 1-Tab = skip-link, 2-Tab = brend |
| 8 | **`.sr` sinfi endi ishlatiladi** (kirish formasi labellari) — oldin CSS'da bor edi-yu 0 marta qo'llangan |
| 9 | **`<canvas>` fallback matni** (JS o'chsa o'yin haqida izoh) |
| 10 | **Dark rejim kontrast**: `--pri` `#3D7EEA` → `#2C62C4` (oq matn bilan **3,91:1 → ~5,6:1**, AA ✓) |
| 11 | **`color-scheme`** e'lon qilindi (light/dark) — native forma, scrollbar, `select` moslashadi |
| 12 | **Mobil sensorli maqsadlar 44px**: `.iconbtn`, `.btn.sm`, `.gm-snd` (oldin 40/40/30px) |
| 13 | **Modal fokus qopqoni**: Tab/Shift+Tab modal ichida aylanadi; ochilganda birinchi maydonga fokus |

---

## P2 — kod tozaligi va izchillik

| # | Tuzatish |
|---|---|
| 1 | **~2,5 KB o'lik CSS o'chirildi** — eski DOM-asosidagi o'yin versiyasi qoldig'i: `.gm-cell`, `.gm-opt(s)`, `.gm-card`, `.gm-feed`, `.gm-grid`, `.gm-miss`, `.gm-user`, `.rgrid`, `.rcol`, `.rrow`, `.kom`, `.qres`, `.rl`, `.eye`, `.bad` va h.k. **Ishlatiladiganlar saqlandi** (`.gm-res`, `.gm-bar`, `.gm-bars`, `.gm-row` — har biri alohida tasdiqlangan) |
| 2 | Ishlatilmagan `--violet`, `--orange` olib tashlandi; `--green`/`--amber` tarixiy nomlari uchun izoh + `--ok`/`--info` aliaslari |
| 3 | **Navigatsiya nomlari birlashtirildi**: desktop / mobil menyu / footer endi bir xil. `#qoshil` desktop navigatsiyaga qo'shildi |
| 4 | `aria-label` izchilligi: `"Yuqori"` / `"Tepaga"` → `"Yuqoriga"` |
| 5 | `#sinov` matni: *"4 mezonga"* → *"3–4 mezonga"* (real: 2 ta funksiyada 4 mezon, 6 tasida 3 ta) |
| 6 | Bo'sh CSS qatorlar tozalandi; qavs muvozanati tasdiqlandi (559/559) |

---

## Ataylab O'TKAZILGAN ishlar (xavf tahlili asosida)

| # | Narsa | Sabab |
|---|---|---|
| 1 | **Apostrof izchilligi** (`'` vs `'`) | Global almashtirish JS qatorlaridagi `\'` ekranlashini va matn ichidagi ma'noli tirnoqlarni buzadi. Qo'lda, tahririyat darajasida qilish kerak |
| 2 | **Tipografik shkala** (32 xil font-size → modul skala) | Har bir qiymat vizual muvozanatning qismi; global o'zgartirish dizaynni buzadi. Alohida dizayn qarori sifatida |
| 3 | **`z-index` / radius tokenizatsiyasi** | Yuqoridagi bilan bir xil: vizual regressiya xavfi |
| 4 | **Faylni modullarga ajratish** (`styles.css`, `game.js` …) | Build jarayonisiz xavfli; alohida migratsiya loyihasi |
| 5 | **`tileAt` "dublikati"** | Tekshirildi: **dublikat emas** — 2 ta alohida skop (tashqi: piksel→katak; `bindDrag` ichida: hodisa→katak). To'qnashuv yo'q, ikkalasi ham ishlatiladi |
| 6 | **Hero rotatsiyasini qo'lda to'xtatish tugmasi** | Tekshirildi: `if(!RM && cube) setInterval(...)` — `prefers-reduced-motion` yoqilganda **allaqachon to'xtaydi** |
| 7 | **`canonical` eski domenga qoldirish** (oldingi kelishuv) | Professional xulosa: sayt `raqamli-tadqiqot-v2` da turib canonical boshqa domenga qarashi **real SEO xatosi** (dublikat kontent + noto'g'ri ijtimoiy preview). Tuzatildi; istasangiz bir qatorga qaytarish mumkin |

---

## Tekshiruv natijalari

**Statik (verify.py):** 60+ assertion — hajm/siqish, id noyobligi, base64 yo'qligi, SVG belgilanishi, skip-link, canvas fallback, color-scheme, domen ishlari, statik FAQ/roadmap, schema yaroqliligi, DATA modeli (`ev`/`st`/vazn=100/matritsa 30/60), JS `d.ev` almashtiruvi.

**Sintaksis:** 5 ta JS bloki `node --check` → barchasi OK. 2 ta JSON-LD `json.loads` → yaroqli.

**Runtime (Chromium, Playwright):** 90+ tekshiruv, barchasi OK:
- JS xatolari: **0**; muvaffaqiyatsiz so'rovlar: **0**
- Logotip: 2/2 `<img>` yuklandi (`naturalWidth=384`), render ~34px va ~30px (mobil)
- FAQ akkordeon, faqat-bitta-ochiq xatti-harakati, `aria-expanded`
- Pilot: 60/60 katak, 30 to'ldirilgan; D6 bosilganda `#exVal=8`, `.sel=5`; tooltip yangi terminologiya
- Kalkulyator: `lider → 85`, `o'rtacha → 54,9` (formulaga aynan mos; `null` maxrajdan chiqarilganini tasdiqlaydi), badge holatlari
- Mavzu: light→dark→light, `localStorage`, `meta#metaTheme`, `color-scheme`, yangi `--pri`
- FokUS: 1-Tab = skip-link; modal trap 8×Tab keyin ham ichida; Escape yopadi
- O'yin: canvas + fallback matni; start → ro'yxat modali (halollik matni bilan)
- Navigatsiya: desktop == mobil menyu nomlari; `#qoshil` bor
- Responsive: 390 / 768 / 1440 px — **gorizontal overflow 0 px**
- `reduced-motion`: JS xatosiz, `.rv` kontent ko'rinadi (opacity=1)
- **JS o'chirilgan**: FAQ 9/9, roadmap 8/8 ko'rinadi

---

## Qoldiq ishlar (keyingi bosqich)

1. **`DATA.dims[].st` (0–3 ball) to'ldirish** — jamoaning ichki ishchi jadvalidan. Shunda indeks avtomatik hisoblanadi va sahifa uni ko'rsatadi.
2. **`RT_ADMIN_URL` ga manzil yozish** — panel tayyor bo'lgach.
3. **`og.png` ni WebP'ga** (395 KB → ~60 KB) — faqat ijtimoiy preview uchun yuklanadi, sahifa tezligiga ta'siri yo'q.
4. **Apostrof tahriri** — qo'lda, matn muharriri darajasida.
5. **Build/migratsiya** — faylni `styles.css` / `data.js` / `game.js` ga ajratish (Vite yoki oddiy esbuild).
6. **CSP header** — Cloudflare Pages `_headers` fayli orqali.
