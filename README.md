# Raqamli Tadqiqot

Sayt: **Raqamli Tadqiqot — AI dalillarini o'lchaydigan talabalar tashabbusi** (TDIU).

Bu repo https://raqamli-tadqiqot-v2.pages.dev/ saytining to'liq kloni (front-end).

## Tuzilma

```
.
├── index.html          # butun sayt: bitta sahifa, CSS va JS ichida (inline)
├── favicon.svg
├── apple-touch-icon.png
├── og.png              # ijtimoiy tarmoqlar uchun ulashilma rasm (1200×630)
├── robots.txt
├── sitemap.xml
└── fonts/              # Inter shrifti (5 xil og'irlik, woff2)
    ├── inter-regular.woff2
    ├── inter-medium.woff2
    ├── inter-semibold.woff2
    ├── inter-bold.woff2
    └── inter-extrabold.woff2
```

## Sahifa bo'limlari (anchor'lar)

| Anchor      | Bo'lim                          |
|-------------|---------------------------------|
| `#top`      | Bosh qism (hero)                |
| `#qanday`   | Qanday ishlaydi                 |
| `#hisobla`  | Kalkulyator                     |
| `#pilot`    | Pilot natijalari                |
| `#faq`      | Savol-javoblar                  |
| `#klub`     | Klub                            |
| `#yol`      | Yo'l xaritasi (roadmap)         |
| `#qoshil`   | Qo'shilish                      |
| `#sinov`    | Sinov o'yini (mini-o'yin)       |

## Mahalliy ishga tushirish

```bash
python3 -m http.server 8080
# brauzerda: http://localhost:8080
```

## Tashqi bog'liqliklar

- **Login/API:** `RT_API = https://aiindeksi-bot.onrender.com` → `POST /api/auth`
  (admin panelga kirish modali). `admin.html` sahifasi ushbu saytda mavjud emas.
- **Telegram:** `https://t.me/Raqamli_tadqiqot`, `https://t.me/aiindeksi_bot`

## Deploy

Cloudflare Pages: ushbu repo'ni ulang, build sozlamasi kerak emas
(Build command: bo'sh, Output directory: `/`).
