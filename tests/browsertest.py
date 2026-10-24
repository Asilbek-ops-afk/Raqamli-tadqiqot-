#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real brauzer (Chromium/Playwright) runtime testi.
Ishlatish:  URL=http://127.0.0.1:8080/ python3 tests/browsertest.py
Kerak:      pip install playwright && python3 -m playwright install chromium"""
import os
from playwright.sync_api import sync_playwright

URL = os.environ.get('URL', 'http://127.0.0.1:8080/')
FAIL, WARN = [], []
def ok(cond, msg):
    print(("  [OK]   " if cond else "  [FAIL] ") + msg)
    if not cond: FAIL.append(msg)
def warn(cond, msg):
    if not cond:
        print("  [WARN] " + msg); WARN.append(msg)

with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 1440, 'height': 960},
                         device_scale_factor=2, locale='uz')
    pg = ctx.new_page()
    errs, reqfail, console = [], [], []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: console.append((m.type, m.text)) if m.type in ('error','warning') else None)
    pg.on('requestfailed', lambda r: reqfail.append(f"{r.url} :: {r.failure}"))

    print("=" * 74); print("1. SAHIFA YUKLANISHI"); print("=" * 74)
    resp = pg.goto(URL, wait_until='networkidle', timeout=30000)
    ok(resp.status == 200, f"HTTP {resp.status}")
    ok(not errs, f"JavaScript xatolari yo'q: {errs if errs else 'toza'}")
    ok(not reqfail, f"Muvaffaqiyatsiz so'rovlar yo'q: {reqfail if reqfail else 'toza'}")
    for t, m in console[:8]:
        print(f"    console.{t}: {m[:120]}")
    ok(pg.title().startswith('Raqamli Tadqiqot'), f"<title>: {pg.title()[:60]}")

    print(); print("=" * 74); print("2. LOGOTIP (base64 o'rniga tashqi WebP)"); print("=" * 74)
    logos = pg.locator('img.brandlogo')
    ok(logos.count() == 2, f"2 ta logotip <img> (header + footer): {logos.count()}")
    for i in range(logos.count()):
        el = logos.nth(i)
        box = el.bounding_box()
        nat = el.evaluate('e => [e.naturalWidth, e.naturalHeight, e.complete]')
        ok(nat[2] and nat[0] > 0, f"  logo[{i}] yuklandi: natural={nat[0]}x{nat[1]}, complete={nat[2]}")
        ok(box and 28 <= box['width'] <= 40, f"  logo[{i}] render o'lchami: {box['width']:.1f}x{box['height']:.1f} (kutilgan ~34)")
    ok(pg.evaluate("document.querySelectorAll('svg image').length") == 0, "eski base64 <svg><image> yo'q")

    print(); print("=" * 74); print("3. STATIK FAQ / ROADMAP (SEO)"); print("=" * 74)
    ok(pg.locator('#faqL .fq').count() == 9, f"FAQ: {pg.locator('#faqL .fq').count()}/9 ta")
    ok(pg.locator('#road .ms').count() == 8, f"Roadmap: {pg.locator('#road .ms').count()}/8 ta band")
    ok('32,6' not in pg.content(), "'32,6' render qilingan DOM'da yo'q")
    q1 = pg.locator('#faqL .fq button').first.inner_text()
    ok('Qamrov va indeks' in q1, f"FAQ[0] yangilangan: {q1[:44]!r}")
    # akkordeon ishlashi
    pg.locator('#faqL .fq button').first.click()
    pg.wait_for_timeout(450)
    ok(pg.locator('#faqL .fq').first.get_attribute('class').find('open') >= 0, "FAQ akkordeon ochiladi")
    ok(pg.locator('#faqL .fq button').first.get_attribute('aria-expanded') == 'true', "aria-expanded=true bo'ldi")
    vis = pg.locator('#fa0 p').is_visible()
    ok(vis, "FAQ javobi ko'rinadi")
    ok('dalil topilgani' in pg.locator('#fa0 p').inner_text(), "FAQ javobi yangi matn (qamrov izohi)")
    pg.locator('#faqL .fq button').nth(2).click(); pg.wait_for_timeout(400)
    ok(pg.locator('#faqL .fq.open').count() == 1, "faqat bitta FAQ ochiq (akkordeon xatti-harakati)")

    print(); print("=" * 74); print("4. PILOT MATRITSA (d.ev)"); print("=" * 74)
    cells = pg.locator('#hg .c')
    ok(cells.count() == 60, f"matritsa kataklari: {cells.count()}/60")
    filled = pg.locator('#hg .c.f').count()
    ok(filled == 30, f"to'ldirilgan: {filled}/30")
    mb = pg.locator('#mb button')
    ok(mb.count() == 6, f"o'lchov tugmalari: {mb.count()}/6")
    ok(mb.first.inner_text().find('/10') > 0, f"mb tugma matni 'N/10' formatida: {mb.first.inner_text()!r}")
    # onReveal (exSet(1)) poyga holatini oldini olish: avval bo'limga scroll + kutish
    pg.evaluate("document.getElementById('pilot').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(1600)
    mb.nth(5).click(); pg.wait_for_timeout(500)
    exv = pg.locator('#exVal').inner_text()
    ok(exv == '8', f"#exVal D6 uchun = 8 (ev): {exv!r}")
    ok('Oshkoralik' in pg.locator('#exT').inner_text(), f"#exT: {pg.locator('#exT').inner_text()!r}")
    sel = pg.evaluate("[...document.querySelectorAll('#mb button')].findIndex(b=>b.classList.contains('sel'))")
    ok(sel == 5, f".sel indeksi = 5 (D6): {sel}")
    # hero tooltip
    cells.first.hover(); pg.wait_for_timeout(300)
    tip = pg.locator('#tip')
    tt = tip.inner_text()
    ok('dalil' in tt and 'ball qo' not in tt, f"tooltip yangi terminologiya: {tt[:60]!r}")

    print(); print("=" * 74); print("5. KALKULYATOR"); print("=" * 74)
    pg.locator('.pre button[data-p="lead"]').click(); pg.wait_for_timeout(350)
    v = pg.locator('#cVal').inner_text()
    # PRE.lead = [3,2,3,2,2,3], w=[15,15,30,15,15,10]
    exp = round(sum(w*x for w, x in zip([15,15,30,15,15,10],[3,2,3,2,2,3])) / 300 * 1000) / 10
    exp_s = f"{exp:.1f}" if exp % 1 else str(int(exp))   # sayt butun sonlarda '.0' ni tashlaydi
    ok(v == exp_s, f"'lider' namunasi = {exp_s} (ko'rsatilgan: {v})")
    pg.locator('.pre button[data-p="mid"]').click(); pg.wait_for_timeout(400)
    v2 = pg.locator('#cVal').inner_text()
    exp2 = round((15*2+30*2+15*1+15*1+10*2)/(3*85)*1000)/10
    ok(v2 == f"{exp2}", f"'o'rtacha' namunasi = {exp2} (ko'rsatilgan: {v2}) - null maxrajdan chiqarildi")
    ok('Kengroq qamrov' in pg.locator('#cBadge').inner_text(), f"badge: {pg.locator('#cBadge').inner_text()!r}")
    pg.locator('.pre button[data-p="clr"]').click(); pg.wait_for_timeout(300)
    ok(pg.locator('#cVal').inner_text() == '—', "tozalashdan keyin '—'")
    ok("Ball qo'ying" in pg.locator('#cBadge').inner_text(), "bo'sh holat badge'i")
    # bitta o'lchov -> cheklangan qamrov
    pg.locator('.pick').first.locator('button', has_text='2').click(); pg.wait_for_timeout(300)
    ok('Cheklangan qamrov' in pg.locator('#cBadge').inner_text(), f"1 o'lchov: {pg.locator('#cBadge').inner_text()!r}")

    print(); print("=" * 74); print("6. MAVZU (THEME) ALMASHINUVI"); print("=" * 74)
    ok(pg.evaluate("document.documentElement.getAttribute('data-theme')") == 'light', "boshlang'ich: light")
    pg.locator('#tgl').click(); pg.wait_for_timeout(700)
    ok(pg.evaluate("document.documentElement.getAttribute('data-theme')") == 'dark', "bosildi -> dark")
    ok(pg.evaluate("localStorage.getItem('theme')") == 'dark', "localStorage'ga saqlandi")
    pass
    ok(pg.evaluate("document.getElementById('metaTheme').content") in ('#080E18','#0B1320'),
       f"meta theme-color yangilandi: {pg.evaluate('document.getElementById(chr(39)+chr(39))') if False else pg.evaluate('document.getElementById(\"metaTheme\").content')}")
    ok(pg.evaluate("getComputedStyle(document.documentElement).colorScheme") == 'dark', "CSS color-scheme: dark")
    # dark kontrast: --pri
    pri = pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--pri').trim()")
    ok(pri == '#2C62C4', f"dark --pri = {pri} (kutilgan #2C62C4, oldin #3D7EEA)")
    pg.screenshot(path=os.environ.get('SHOTS', 'shots') + '/dark-hero.png', clip={'x':0,'y':0,'width':1440,'height':900})
    pg.locator('#tgl').click(); pg.wait_for_timeout(700)
    ok(pg.evaluate("document.documentElement.getAttribute('data-theme')") == 'light', "qayta -> light")

    print(); print("=" * 74); print("7. SKIP-LINK VA FOKUS"); print("=" * 74)
    pg.goto(URL, wait_until='networkidle')
    ok(pg.evaluate("document.activeElement.tagName") == 'BODY', "yangi sahifada fokus BODY'da")
    pg.keyboard.press('Tab'); pg.wait_for_timeout(250)
    f = pg.evaluate("document.activeElement.className + ' | ' + document.activeElement.textContent.trim()")
    ok('skip' in f, f"1-Tab = skip-link: {f!r}")
    pg.keyboard.press('Tab'); pg.wait_for_timeout(200)
    f2 = pg.evaluate("document.activeElement.className")
    ok('brand' in f2, f"2-Tab = brend havolasi: {f2!r}")
    vis = pg.evaluate("""() => {const e=document.activeElement,r=e.getBoundingClientRect();
        return r.top>=0 && r.top<200 && getComputedStyle(e).transform}""")
    ok('matrix' in str(vis) or 'none' in str(vis), f"skip-link fokusda ko'rinadi (transform: {vis})")

    print(); print("=" * 74); print("8. KIRISH MODALI (404 yo'q)"); print("=" * 74)
    pg.locator('#kirBtn').click(); pg.wait_for_timeout(400)
    ok(pg.locator('#kirModal').is_visible(), "modal ochildi (openKirish() orqali)")
    ok(pg.locator('#kirModal').get_attribute('role') == 'dialog', "role=dialog")
    ok(pg.locator('#kirModal').get_attribute('aria-modal') == 'true', "aria-modal=true")
    act = pg.evaluate("document.activeElement.id")
    ok(act == 'kirU', f"fokus birinchi maydonda: #{act}")
    ok(pg.locator('#kirModal label.sr').count() == 2, "2 ta screen-reader label")
    ok('holanmagan' in pg.locator('#kirModal').inner_text().lower() or 'ulanmagan' in pg.locator('#kirModal').inner_text(),
       "panel holati haqida halol xabar ko'rinadi")
    # Tab trap
    for _ in range(8): pg.keyboard.press('Tab')
    inside = pg.evaluate("document.getElementById('kirModal').contains(document.activeElement)")
    ok(inside, f"fokus qopqoni ishlaydi (8x Tab keyin modal ichida: {inside})")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok(not pg.locator('#kirModal').is_visible(), "Escape bilan yopildi")
    # RT_ADMIN_URL bo'sh -> /admin.html ga o'tmaydi
    ok(pg.evaluate("typeof RT_ADMIN_URL !== 'undefined' && RT_ADMIN_URL === ''"), "RT_ADMIN_URL='' (sozlanadigan)")
    ok('/admin.html' not in pg.content(), "DOM'da /admin.html yo'q")

    print(); print("=" * 74); print("9. O'YIN (canvas)"); print("=" * 74)
    pg.locator('#sinov').scroll_into_view_if_needed(); pg.wait_for_timeout(500)
    cv = pg.locator('#gmCanvas')
    ok(cv.count() == 1, "canvas mavjud")
    fb = cv.inner_text()
    ok(len(fb) > 30, f"canvas fallback matni: {fb[:50]!r}")
    ok(pg.locator('#gmStart').is_visible(), "o'yin boshlash tugmasi ko'rinadi")
    pg.locator('#gmStart').click(); pg.wait_for_timeout(500)
    ok(pg.locator('#gmModal').is_visible(), "ro'yxatdan o'tish modali ochildi (o'yin hisob talab qiladi)")
    pg.locator('#gmClose').click(); pg.wait_for_timeout(300)

    print(); print("=" * 74); print("10. NAVIGATSIYA IZCHILLIGI"); print("=" * 74)
    nav = [a.inner_text() for a in pg.locator('.links a').all()]
    print(f"    desktop nav: {nav}")
    pg.set_viewport_size({'width': 420, 'height': 860}); pg.wait_for_timeout(500)
    pg.locator('#burger').click(); pg.wait_for_timeout(500)
    mm = [a.inner_text() for a in pg.locator('#mm a').all() if a.inner_text().strip()][:7]
    print(f"    mobil menyu: {mm}")
    ok(nav[:7] == mm, "desktop va mobil menyu nomlari BIR XIL")
    ok('#qoshil' in str(pg.evaluate("[...document.querySelectorAll('.links a')].map(a=>a.getAttribute('href'))")),
       "#qoshil navigatsiyaga qo'shildi")
    # mobil touch target
    ib = pg.evaluate("""() => {const e=document.querySelector('#tgl');
        const r=e.getBoundingClientRect(); return [r.width, r.height]}""")
    ok(ib[0] >= 44 and ib[1] >= 44, f"mobil .iconbtn = {ib[0]:.0f}x{ib[1]:.0f}px (>=44)")
    # menyuni yopish: overlay burger'ni to'sib qo'yadi -> Escape yoki force click
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    if pg.locator('#mm.on').count():
        pg.locator('#burger').click(force=True); pg.wait_for_timeout(300)
    warn(not pg.locator('#mm.on').count(), "mobil menyu yopildi")

    print(); print("=" * 74); print("11. RESPONSIVE SKRINSHOTLAR"); print("=" * 74)
    os.makedirs(os.environ.get('SHOTS', 'shots'), exist_ok=True)
    pg.set_viewport_size({'width': 1440, 'height': 960}); pg.wait_for_timeout(400)
    pg.screenshot(path=os.environ.get('SHOTS', 'shots') + '/desktop-light.png')
    pg.locator('#tgl').click(); pg.wait_for_timeout(700)
    pg.screenshot(path=os.environ.get('SHOTS', 'shots') + '/desktop-dark.png')
    pg.locator('#tgl').click(); pg.wait_for_timeout(600)
    pg.evaluate("document.getElementById('pilot').scrollIntoView()"); pg.wait_for_timeout(700)
    pg.screenshot(path=os.environ.get('SHOTS', 'shots') + '/desktop-pilot.png')
    pg.evaluate("document.getElementById('faq').scrollIntoView()"); pg.wait_for_timeout(700)
    pg.screenshot(path=os.environ.get('SHOTS', 'shots') + '/desktop-faq.png')
    pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(600)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(600)
    pg.screenshot(path=os.environ.get('SHOTS', 'shots') + '/mobile-light.png')
    pg.evaluate("document.getElementById('hisobla').scrollIntoView()"); pg.wait_for_timeout(700)
    pg.screenshot(path=os.environ.get('SHOTS', 'shots') + '/mobile-calc.png')
    # horizontal overflow tekshiruvi
    ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok(ov <= 1, f"mobil gorizontal overflow yo'q: {ov}px")
    pg.set_viewport_size({'width': 768, 'height': 1024}); pg.wait_for_timeout(500)
    ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok(ov <= 1, f"planshet gorizontal overflow yo'q: {ov}px")
    pg.set_viewport_size({'width': 1440, 'height': 960}); pg.wait_for_timeout(500)
    ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    ok(ov <= 1, f"desktop gorizontal overflow yo'q: {ov}px")

    print(); print("=" * 74); print("12. REDUCED MOTION"); print("=" * 74)
    ctx2 = br.new_context(viewport={'width': 1440, 'height': 960}, reduced_motion='reduce')
    pg2 = ctx2.new_page()
    e2 = []
    pg2.on('pageerror', lambda e: e2.append(str(e)))
    pg2.goto(URL, wait_until='networkidle')
    ok(not e2, f"reduced-motion rejimida JS xatosi yo'q: {e2 if e2 else 'toza'}")
    ok(pg2.locator('#faqL .fq').count() == 9, "reduced-motion'da ham FAQ 9 ta")
    rv = pg2.evaluate("getComputedStyle(document.querySelector('.rv')).opacity")
    ok(float(rv) > 0.9, f".rv elementlari ko'rinadi (opacity={rv}) - kontent yashirilmagan")
    ctx2.close()

    print(); print("=" * 74); print("13. JS'SIZ HOLAT (progressive enhancement)"); print("=" * 74)
    ctx3 = br.new_context(viewport={'width': 1440, 'height': 960}, java_script_enabled=False)
    pg3 = ctx3.new_page()
    pg3.goto(URL, wait_until='load')
    n3 = pg3.locator('#faqL .fq').count()
    r3 = pg3.locator('#road .ms').count()
    ok(n3 == 9, f"JS o'chirilgan: FAQ {n3}/9 ta ko'rinadi (oldin 0 ta edi)")
    ok(r3 == 8, f"JS o'chirilgan: roadmap {r3}/8 ta ko'rinadi (oldin 0 ta edi)")
    pg3.screenshot(path=os.environ.get('SHOTS', 'shots') + '/nojs.png')
    ctx3.close()

    br.close()

print(); print("=" * 74)
if FAIL:
    print(f"X {len(FAIL)} TA MUVAFFAQIYATSIZ:")
    for f in FAIL: print("   -", f)
else:
    print("BARCHA BRAUZER TESTLARI O'TDI")
if WARN:
    print(f"\n{len(WARN)} ta ogohlantirish:")
    for w in WARN: print("   -", w)
print("=" * 74)
sys.exit(1 if FAIL else 0)
