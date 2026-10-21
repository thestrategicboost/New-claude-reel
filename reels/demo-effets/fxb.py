#!/usr/bin/env python3
"""Effects 42-50 (set B). Each fn(a, b, k) -> dict(front, behind, tw, css). Every effect is built to read in a 1.3 s slot:
in during the first .3 s, hold, gone at b. Longer slots stretch the hold / secondary phases proportionally."""
import html
import os
import random
import subprocess

from build import BROWN, CREAM, DARK, FF, INK, PILL, frame, typing

GOLD, GOLDL, EMBER = '#C99A55', '#E9C98F', '#D9803A'


def hid(*sels):
    return [f"gsap.set('{s}',{{autoAlpha:0}});" for s in sels]


def off(b, *sels):
    return [f"tl.set('{s}',{{autoAlpha:0}},{b:.3f});" for s in sels]


def on(t, *sels):
    return [f"tl.set('{s}',{{autoAlpha:1}},{t:.3f});" for s in sels]


def pts(p):
    return 'polygon(' + ','.join(f'{x:.1f}px {y:.1f}px' for x, y in p) + ')'


# ====================================================================== 42 TIMELINE BURN
def fx42(a, b, k):
    L = b - a
    s = a + max(.55, .45 * L)          # catches fire
    e = b - max(.1, .08 * L)           # fully burnt
    W, Hh, X0, Y0 = 940, 344, 70, 300
    rnd = random.Random(42)
    # --- tracks
    tx0, tx1 = 92, 916                  # clip area inside the card
    v2 = [(0, 190, 'TITRE'), (204, 300, 'SOUS-TITRES'), (518, 150, 'ZOOM'), (682, 142, 'CTA')]
    v1 = [(0, 236, 't0'), (244, 190, 't2'), (442, 214, 't4'), (664, 160, 't1')]
    bars = ''.join(f'<i style="height:{rnd.randint(8, 40)}px"></i>' for _ in range(74))
    clips = ''
    for x, w, t in v2:
        clips += f'<div class="{k}-c {k}-tx" style="left:{tx0 + x}px;top:96px;width:{w}px">{t}</div>'
    for x, w, t in v1:
        clips += f'<div class="{k}-c {k}-th" style="left:{tx0 + x}px;top:164px;width:{w}px;background-image:url(assets/thumbs/{t}.jpg)"></div>'
    clips += f'<div class="{k}-c {k}-au" style="left:{tx0}px;top:264px;width:{tx1 - tx0}px">{bars}</div>'
    labs = ''.join(f'<span class="{k}-tl" style="top:{y}px">{n}</span>' for n, y in (('V2', 112), ('V1', 192), ('A1', 280)))

    # --- burn line (jagged, tilted), as px polygons relative to the card
    ys = [-24 + i * (Hh + 48) / 13 for i in range(14)]
    jag = [rnd.uniform(-16, 16) for _ in ys]
    jag2 = [rnd.uniform(-16, 16) for _ in ys]
    slope = .38

    def line(X, j):
        return [(X - slope * (y - Hh / 2) + jj, y) for y, jj in zip(ys, j)]

    XA = -slope * Hh / 2 - 90
    XB = W + slope * Hh / 2 + 90

    def card_poly(X, j):
        ln = line(X, j)
        return pts(ln + [(W + 60, Hh + 24), (W + 60, -24)])

    def band(X, j, bw):
        ln = line(X, j)
        return pts(ln + [(x + bw, y) for x, y in reversed(ln)])

    layers = [('char', 74, 'rgba(14,7,2,.82)', 9), ('glow', 40, EMBER, 9), ('hot', 11, '#FFE3C2', 2)]
    edge = ''.join(f'<div class="{k}-bw" id="{k}-bw{n}" style="filter:blur({bl}px)"><div id="{k}-{n}" class="{k}-band" style="background:{c}"></div></div>'
                   for n, bw, c, bl in layers)
    embers = ''
    tw = hid(f'#{k}-w') + [f"gsap.set('#{k}-card',{{clipPath:'{card_poly(XA, jag)}'}});"]
    tw += [f"gsap.set('#{k}-{n}',{{clipPath:'{band(XA, jag, bw)}'}});" for n, bw, _, _ in layers]
    # build in
    tw += [f"tl.fromTo('#{k}-w',{{autoAlpha:0,y:46,scale:.94}},{{autoAlpha:1,y:0,scale:1,duration:.28,ease:'power3.out',immediateRender:false}},{a:.3f});",
           f"tl.fromTo('#{k}-card .{k}-c',{{scaleX:0}},{{scaleX:1,transformOrigin:'0% 50%',duration:.2,ease:'power2.out',stagger:.018,immediateRender:false}},{a + .06:.3f});",
           f"tl.fromTo('#{k}-ph',{{x:0}},{{x:{tx1 - tx0 - 40},duration:{e - a - .05:.3f},ease:'none',immediateRender:false}},{a + .05:.3f});",
           f"tl.fromTo('#{k}-heat',{{autoAlpha:0}},{{autoAlpha:1,duration:{min(.25, s - a - .3):.3f},ease:'power1.in',immediateRender:false}},{s - min(.25, s - a - .3):.3f});"]
    # burn: card clip and the three edge bands move together
    bd = e - s
    tw += [f"tl.fromTo('#{k}-card',{{clipPath:'{card_poly(XA, jag)}'}},{{clipPath:'{card_poly(XB, jag2)}',duration:{bd:.3f},ease:'power1.in',immediateRender:false}},{s:.3f});"]
    for n, bw, _, _ in layers:
        tw += [f"tl.fromTo('#{k}-{n}',{{clipPath:'{band(XA, jag, bw)}'}},{{clipPath:'{band(XB, jag2, bw)}',duration:{bd:.3f},ease:'power1.in',immediateRender:false}},{s:.3f});"]
    nfl = max(2, int(bd / .07))
    tw += [f"tl.fromTo('#{k}-bwglow',{{opacity:1}},{{opacity:.55,duration:.035,repeat:{nfl},yoyo:true,ease:'steps(2)',immediateRender:false}},{s:.3f});",
           f"tl.fromTo('#{k}-bwhot',{{opacity:1}},{{opacity:.7,duration:.05,repeat:{max(2, int(bd / .1))},yoyo:true,ease:'none',immediateRender:false}},{s + .02:.3f});"]
    # embers spawn on the moving edge (power1.in progress = p^2)
    for j in range(14):
        f = (j + .5) / 14
        t = s + bd * f
        X = XA + (XB - XA) * f * f
        y = rnd.uniform(20, Hh - 20)
        x = X - slope * (y - Hh / 2) + 10
        if not (0 < x < W):
            continue
        sz = rnd.choice((6, 8, 10))
        embers += f'<i id="{k}-em{j}" class="{k}-em" style="left:{x:.0f}px;top:{y:.0f}px;width:{sz}px;height:{sz}px"></i>'
        tw += hid(f'#{k}-em{j}')
        tw += [f"tl.fromTo('#{k}-em{j}',{{autoAlpha:1,x:0,y:0,scale:1}},{{autoAlpha:0,x:{rnd.uniform(10, 50):.0f},y:{-rnd.uniform(90, 200):.0f},scale:.3,"
               f"duration:{min(.55, b - t):.3f},ease:'power1.out',immediateRender:false}},{t:.3f});"] + off(b, f'#{k}-em{j}')
    tw += off(b, f'#{k}-w')
    front = [f'''<div id="{k}-w" class="{k}-w">
  <div id="{k}-card" class="{k}-card">
    <div class="{k}-hd"><span class="{k}-rec"></span>MONTAGE · reel_claude.mp4<span class="{k}-tc">00:00:12:08</span></div>
    <div class="{k}-ru"></div>{labs}{clips}
    <div id="{k}-ph" class="{k}-ph"><b></b></div>
    <div id="{k}-heat" class="{k}-heat"></div>
  </div>{edge}{embers}
</div>''']
    css = f'''
.{k}-w{{position:absolute;left:{X0}px;top:{Y0}px;width:{W}px;height:{Hh}px;z-index:20}}
.{k}-card{{position:absolute;inset:0;border-radius:24px;background:rgba(42,26,16,.95);border:1.5px solid rgba(244,238,230,.14);overflow:hidden;
  box-shadow:0 30px 70px rgba(20,10,4,.45)}}
.{k}-hd{{position:absolute;left:24px;right:24px;top:18px;height:34px;font:500 21px/34px 'JetBrains Mono';color:rgba(244,238,230,.82);letter-spacing:.02em}}
.{k}-rec{{display:inline-block;width:12px;height:12px;border-radius:50%;background:{EMBER};margin-right:12px;vertical-align:1px;box-shadow:0 0 10px {EMBER}}}
.{k}-tc{{position:absolute;right:0;color:{GOLDL}}}
.{k}-ru{{position:absolute;left:{tx0}px;right:24px;top:62px;height:22px;
  background:repeating-linear-gradient(90deg,rgba(244,238,230,.4) 0 2px,transparent 2px 20.6px) bottom/100% 9px no-repeat,
  repeating-linear-gradient(90deg,rgba(244,238,230,.55) 0 2px,transparent 2px 103px) bottom/100% 18px no-repeat}}
.{k}-tl{{position:absolute;left:26px;font:500 20px/1 'JetBrains Mono';color:rgba(244,238,230,.5)}}
.{k}-c{{position:absolute;border-radius:10px}}
.{k}-tx{{height:56px;background:{BROWN};color:{CREAM};font:700 21px/56px Poppins;padding-left:16px;letter-spacing:.03em;border:1.5px solid rgba(244,238,230,.25)}}
.{k}-th{{height:86px;background-size:auto 100%;background-repeat:repeat-x;border:2px solid rgba(233,201,143,.85)}}
.{k}-au{{height:56px;background:rgba(201,154,85,.16);border:1.5px solid rgba(201,154,85,.5);display:flex;align-items:center;gap:5px;padding:0 10px;overflow:hidden}}
.{k}-au i{{flex:0 0 6px;border-radius:3px;background:{GOLD}}}
.{k}-ph{{position:absolute;left:{tx0}px;top:58px;bottom:12px;width:3px;background:{CREAM};box-shadow:0 0 12px rgba(244,238,230,.7)}}
.{k}-ph b{{position:absolute;left:-10px;top:-4px;width:23px;height:20px;background:{PILL};clip-path:polygon(0 0,100% 0,100% 55%,50% 100%,0 55%)}}
.{k}-heat{{position:absolute;inset:0;background:radial-gradient(120% 140% at 0% 100%,rgba(217,128,58,.55),rgba(140,92,65,.18) 45%,transparent 70%)}}
.{k}-bw{{position:absolute;inset:0;pointer-events:none}}
.{k}-band{{position:absolute;inset:0}}
.{k}-em{{position:absolute;border-radius:50%;background:#F2B979;box-shadow:0 0 10px 3px rgba(217,128,58,.85)}}
'''
    return dict(front=front, tw=tw, css=css)


# ====================================================================== 43 KNOCKOUT TILES (behind her)
def fx43(a, b, k):
    L = b - a
    tiles = [  # word, bg, fg, left, top, width, rot
        ('AFTER EFFECTS', DARK, CREAM, 85, 300, 540, -4),
        ('CAPCUT', CREAM, INK, 655, 296, 330, 3),
        ('PREMIERE', BROWN, CREAM, 120, 446, 390, 2.5),
        ('FINAL CUT', PILL, INK, 540, 440, 410, -3),
        ('DAVINCI', INK, GOLDL, 350, 590, 380, 1.5),
    ]
    front, tw = [], []
    for i, (w, bg, fg, x, y, wd, r) in enumerate(tiles):
        front.append(f'<div id="{k}-t{i}" class="{k}-t" style="left:{x}px;top:{y}px;width:{wd}px;background:{bg};color:{fg}">{w}</div>')
        tw += hid(f'#{k}-t{i}')
    s = a + max(.5, .4 * L)
    fd = min(.42, .28 * L)
    order = [1, 3, 0, 4, 2]
    gap = (b - .08 - s - .08 - fd) / (len(order) - 1)
    for i, (w, bg, fg, x, y, wd, r) in enumerate(tiles):
        t = a + .045 * i
        sel = f'#{k}-t{i}'
        tw += [f"tl.fromTo('{sel}',{{autoAlpha:0,scale:1.9,rotation:{r + (9 if i % 2 else -9)},x:0,y:0}},{{autoAlpha:1,scale:1,rotation:{r},duration:.15,ease:'power3.in',immediateRender:false}},{t:.3f});",
               f"tl.fromTo('{sel}',{{y:0}},{{y:7,duration:.045,yoyo:true,repeat:1,ease:'power1.out',immediateRender:false}},{t + .15:.3f});"]
    for j, i in enumerate(order):
        r = tiles[i][6]
        d = -1 if tiles[i][3] + tiles[i][5] / 2 < 540 else 1
        t = s + j * gap
        sel = f'#{k}-t{i}'
        tw += [f"tl.to('{sel}',{{y:-34,rotation:{r + d * 10},duration:.08,ease:'power2.out'}},{t:.3f});",
               f"tl.to('{sel}',{{x:{d * 520},y:1500,rotation:{r + d * 80},duration:{fd:.3f},ease:'power2.in'}},{t + .08:.3f});"]
    tw += off(b, *[f'#{k}-t{i}' for i in range(len(tiles))])
    css = f'''
.{k}-t{{position:absolute;height:118px;border-radius:20px;font:400 84px/118px Anton;text-align:center;letter-spacing:.02em;
  box-shadow:0 22px 44px rgba(42,26,16,.42),inset 0 0 0 2px rgba(244,238,230,.18)}}
'''
    return dict(behind=front, tw=tw, css=css)


# ====================================================================== 44 SHATTER 3D
def fx44(a, b, k):
    L = b - a
    img = frame(a)
    rnd = random.Random(44)
    C = (540, 930)
    n = 6
    import math
    ang = [math.radians(18 + i * 360 / n + rnd.uniform(-13, 13)) for i in range(n)]
    r1 = [rnd.uniform(300, 430) for _ in range(n)]

    def P(t, r):
        return (C[0] + r * math.cos(t), C[1] + r * math.sin(t))

    shards = []
    for i in range(n):
        j = (i + 1) % n
        tj = ang[j] + (2 * math.pi if j == 0 else 0)
        mid = (ang[i] + tj) / 2
        shards.append(([C, P(ang[i], r1[i]), P(tj, r1[j])], P(mid, r1[i] * .55), mid, 0))
        shards.append(([P(ang[i], r1[i]), P(ang[i], 2600), P(mid, 2600), P(tj, 2600), P(tj, r1[j])],
                       (min(1000, max(80, C[0] + 700 * math.cos(mid))), min(1800, max(120, C[1] + 800 * math.sin(mid)))), mid, 1))
    s = a + max(.45, .42 * L)
    fd = min(.7, .35 * L)
    st = min(.3, .12 * L)
    front, tw = [], []
    html_sh = ''
    for i, (poly, (ox, oy), mid, outer) in enumerate(shards):
        sid = f'{k}-s{i}'
        pp = ' '.join(f'{x:.1f},{y:.1f}' for x, y in poly)
        html_sh += (f'<div id="{sid}" class="{k}-sh" style="clip-path:{pts(poly)};transform-origin:{ox:.0f}px {oy:.0f}px">'
                    f'<div class="{k}-im"></div><svg class="{k}-ol" viewBox="0 0 1080 1920"><polygon points="{pp}"/></svg></div>')
        cx, cy = math.cos(mid), math.sin(mid)
        fl = 26 + 30 * outer
        tw += [f"tl.to('#{sid}',{{x:{cx * fl:.0f},y:{cy * fl:.0f},z:{rnd.uniform(15, 120):.0f},rotationX:{rnd.uniform(-1, 1) * (7 - 4 * outer):.1f},rotationY:{rnd.uniform(-1, 1) * (7 - 4 * outer):.1f},"
               f"rotation:{rnd.uniform(-1, 1) * (2.5 - outer):.1f},filter:'brightness({rnd.uniform(.95, 1.18):.2f})',duration:{s - a - .1:.3f},ease:'power2.out'}},{a + .1:.3f});"]
        rank = i // 2 + (n * outer) * 0  # inner shards first in each wedge pair
        delay = st * ((i % 2) * .5 + (i // 2) / (n - 1) * .5)
        tw += [f"tl.to('#{sid}',{{x:{cx * rnd.uniform(1100, 1500):.0f},y:{cy * 1200 + 500:.0f},z:{rnd.uniform(300, 700):.0f},rotationX:{rnd.uniform(-140, 140):.0f},"
               f"rotationY:{rnd.uniform(-140, 140):.0f},rotation:{rnd.uniform(-60, 60):.0f},autoAlpha:0,duration:{fd:.3f},ease:'power2.in'}},{s + delay:.3f});"]
        _ = rank
    front.append(f'<div id="{k}-g" class="{k}-g"><div id="{k}-dk" class="{k}-dk"></div>{html_sh}<div id="{k}-fl" class="{k}-fl"></div></div>')
    tw = hid(f'#{k}-g', f'#{k}-fl', f'.{k}-ol', f'#{k}-dk') + \
        [f"gsap.set('.{k}-sh',{{autoAlpha:1,x:0,y:0,z:0,rotationX:0,rotationY:0,rotation:0,filter:'brightness(1)'}});"] + \
        on(a, f'#{k}-g') + [f"tl.set('.{k}-sh',{{autoAlpha:1}},{a:.3f});"] + \
        [f"tl.fromTo('#{k}-fl',{{autoAlpha:.55}},{{autoAlpha:0,duration:.22,ease:'power2.out',immediateRender:false}},{a + .03:.3f});",
         f"tl.fromTo('.{k}-ol',{{autoAlpha:0}},{{autoAlpha:1,duration:.06,immediateRender:false}},{a + .04:.3f});",
         f"tl.fromTo('#{k}-dk',{{autoAlpha:0}},{{autoAlpha:1,duration:.12,immediateRender:false}},{a + .06:.3f});",
         f"tl.to('#{k}-dk',{{autoAlpha:0,duration:{fd + st:.3f},ease:'power1.in'}},{s:.3f});"] + tw + \
        off(b, f'#{k}-g', f'#{k}-fl', f'.{k}-ol', f'#{k}-dk')
    css = f'''
.{k}-g{{position:absolute;inset:0;z-index:20;perspective:1700px;perspective-origin:50% 48%;transform-style:preserve-3d}}
.{k}-sh{{position:absolute;inset:0;will-change:transform}}
.{k}-dk{{position:absolute;inset:0;transform:translateZ(-400px) scale(1.25);background:radial-gradient(70% 50% at 50% 48%,rgba(42,26,16,.35),rgba(20,10,4,.7))}}
.{k}-im{{position:absolute;inset:0;background:url({img}) center/cover}}
.{k}-ol{{position:absolute;inset:0;width:1080px;height:1920px}}
.{k}-ol polygon{{fill:rgba(255,255,255,.06);stroke:rgba(255,248,236,.95);stroke-width:7;stroke-linejoin:round}}
.{k}-fl{{position:absolute;inset:0;background:radial-gradient(60% 40% at 50% 48%,rgba(255,248,236,.9),rgba(244,238,230,.25) 60%,transparent)}}
'''
    return dict(front=front, tw=tw, css=css)


# ====================================================================== 45 CODE SCAN
CODE = ('const reel = await claude.monter({ rushs: "maé_brut.mp4", coupes: "auto", sous_titres: true, musique: "douce", effets: ["zoom","texte"] }); '
        'reel.export("thestrategicboost.fr"); // montage de réels avec Claude  if (silence > 0.4) couper(); for (const mot of script) caption(mot); ')


def ascii_layers(img, cols=112, rows=100):
    from PIL import Image
    import numpy as np
    im = Image.open(img).convert('L').resize((cols, rows), Image.BILINEAR)
    lum = np.asarray(im, np.float32)
    t1, t2 = np.percentile(lum, 38), np.percentile(lum, 80)
    gold, cream = [], []
    idx = 0
    for r in range(rows):
        g = c = ''
        for col in range(cols):
            ch = CODE[idx % len(CODE)]
            idx += 1
            v = lum[r, col]
            if v > t2:
                c += ch
                g += ' '
            elif v > t1:
                g += ch
                c += ' '
            else:
                g += ' '
                c += ' '
        gold.append(g)
        cream.append(c)
    return html.escape('\n'.join(gold)), html.escape('\n'.join(cream))


def fx45(a, b, k):
    L = b - a
    img = frame(a)
    g, c = ascii_layers(img)
    d1 = min(.6, max(.3, .17 * L))
    t2 = b - .04 - d1
    front = [f'''<div id="{k}-cd" class="{k}-cd"><img class="{k}-ti" src="{img}" alt="">
  <pre class="{k}-pre {k}-g">{g}</pre><pre class="{k}-pre {k}-c">{c}</pre><div class="{k}-crt"></div>
  <div class="{k}-chip"><b>$</b> claude --montage reel.mp4<i></i></div>
</div>
<div id="{k}-ln" class="{k}-ln"></div>''']
    tw = hid(f'#{k}-cd', f'#{k}-ln') + [
        f"tl.set('#{k}-cd',{{autoAlpha:1}},{a:.3f});",
        f"tl.fromTo('#{k}-cd',{{clipPath:'inset(0% 0% 100% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:{d1:.3f},ease:'power1.inOut',immediateRender:false}},{a:.3f});",
        f"tl.set('#{k}-ln',{{autoAlpha:1}},{a:.3f});",
        f"tl.fromTo('#{k}-ln',{{y:-60}},{{y:1920,duration:{d1:.3f},ease:'power1.inOut',immediateRender:false}},{a:.3f});",
        f"tl.set('#{k}-ln',{{autoAlpha:0}},{a + d1:.3f});",
        f"tl.fromTo('#{k}-cd .{k}-c',{{opacity:1}},{{opacity:.78,duration:.06,repeat:{max(1, int((t2 - a - d1) / .12))},yoyo:true,ease:'steps(1)',immediateRender:false}},{a + d1:.3f});",
        f"tl.set('#{k}-ln',{{autoAlpha:1}},{t2:.3f});",
        f"tl.fromTo('#{k}-ln',{{y:-60}},{{y:1920,duration:{d1:.3f},ease:'power1.inOut',immediateRender:false}},{t2:.3f});",
        f"tl.fromTo('#{k}-cd',{{clipPath:'inset(0% 0% 0% 0%)'}},{{clipPath:'inset(100% 0% 0% 0%)',duration:{d1:.3f},ease:'power1.inOut',immediateRender:false}},{t2:.3f});",
    ] + off(b, f'#{k}-cd', f'#{k}-ln')
    css = f'''
.{k}-cd{{position:absolute;inset:0;z-index:20;background:{INK};overflow:hidden}}
.{k}-ti{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) sepia(.9) brightness(.55) contrast(1.25);opacity:.7}}
.{k}-pre{{position:absolute;left:3px;top:0;margin:0;font:500 16px/19.2px 'JetBrains Mono';white-space:pre;letter-spacing:0}}
.{k}-g{{color:{GOLD};opacity:.85}}
.{k}-c{{color:{CREAM};text-shadow:0 0 6px rgba(244,238,230,.55)}}
.{k}-crt{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(42,26,16,.28) 0 2px,transparent 2px 5px)}}
.{k}-chip{{position:absolute;left:70px;top:300px;padding:16px 26px;border-radius:16px;background:rgba(42,26,16,.92);border:1.5px solid {GOLD};
  font:500 30px/1 'JetBrains Mono';color:{CREAM};box-shadow:0 12px 30px rgba(0,0,0,.4)}}
.{k}-chip b{{color:{GOLDL};font-weight:500;margin-right:10px}}
.{k}-chip i{{display:inline-block;width:15px;height:30px;background:{GOLDL};margin-left:8px;vertical-align:-5px}}
.{k}-ln{{position:absolute;left:0;top:0;width:1080px;height:60px;z-index:21;
  background:linear-gradient(180deg,transparent,rgba(233,201,143,.28) 80%,rgba(255,240,215,.95) 92%,{GOLD} 100%);
  box-shadow:0 4px 26px 4px rgba(201,154,85,.75)}}
'''
    return dict(front=front, tw=tw, css=css)


# ====================================================================== 46 WORD PILE
def fx46(a, b, k):
    base = 600
    bh, gap = 90, 8
    r1, r2, r3 = base - 6 - bh, base - 6 - 2 * bh - gap, base - 6 - 3 * bh - 2 * gap
    blocks = [  # word, bg, fg, left, top, width, rot
        ('SOUS-TITRES', CREAM, INK, 190, r1, 400, -1.5),
        ('MUSIQUE', BROWN, CREAM, 604, r1, 290, 2),
        ('COUPES', DARK, CREAM, 262, r2, 270, 2.5),
        ('EFFETS', PILL, INK, 546, r2, 262, -2.5),
        ('TRANSITIONS', INK, GOLDL, 345, r3, 400, 1.2),
    ]
    front = [f'<div id="{k}-sf" class="{k}-sf"></div>']
    tw = hid(f'#{k}-sf') + [f"tl.fromTo('#{k}-sf',{{autoAlpha:0,scaleX:0}},{{autoAlpha:1,scaleX:1,duration:.18,ease:'power3.out',immediateRender:false}},{a:.3f});"]
    sels = [f'#{k}-sf']
    for i, (w, bg, fg, x, y, wd, r) in enumerate(blocks):
        sel = f'#{k}-b{i}'
        sels.append(sel)
        front.append(f'<div id="{k}-b{i}" class="{k}-b" style="left:{x}px;top:{y}px;width:{wd}px;background:{bg};color:{fg}">{w}</div>')
        t = a + .04 + .065 * i
        tw += hid(sel) + [f"tl.set('{sel}',{{autoAlpha:1}},{t:.3f});",
                          f"tl.fromTo('{sel}',{{y:{-(y + 160)},rotation:{r * 5:.1f}}},{{y:0,rotation:{r},duration:.42,ease:'bounce.out',immediateRender:false}},{t:.3f});"]
    tw += [f"tl.to('{s_}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});" for s_ in sels] + off(b, *sels)
    css = f'''
.{k}-sf{{position:absolute;left:120px;top:{base}px;width:840px;height:9px;border-radius:5px;z-index:20;background:{PILL};
  box-shadow:0 10px 24px rgba(42,26,16,.35)}}
.{k}-b{{position:absolute;height:{bh}px;border-radius:16px;z-index:20;font:400 64px/{bh}px Anton;text-align:center;letter-spacing:.03em;
  box-shadow:0 14px 30px rgba(42,26,16,.38),inset 0 0 0 2px rgba(244,238,230,.16)}}
'''
    return dict(front=front, tw=tw, css=css)


# ====================================================================== 47 INSIDE OUT
RAW_M0 = 4.0   # rawclip.mp4 media offset used for both layers


def inside_clip(a, L):
    """rawclip.mp4 seen only through her silhouette (alpha of assets/cut.webm from a to a+L) -> webm with alpha."""
    os.makedirs('assets/fx47', exist_ok=True)
    out = f'assets/fx47/in_{a:.2f}_{L:.2f}.webm'
    if os.path.exists(out) or not os.path.exists('assets/cut.webm'):
        return out
    cmd = [FF, '-v', 'error', '-y', '-c:v', 'libvpx-vp9', '-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', 'assets/cut.webm',
           '-ss', f'{RAW_M0:.3f}', '-t', f'{L:.3f}', '-i', 'assets/rawclip.mp4', '-filter_complex',
           '[0:v]alphaextract,format=gray[m];'
           '[1:v]scale=1440:1920:flags=lanczos,crop=1080:1920,unsharp=5:5:0.6,eq=contrast=1.06:saturation=1.08,'
           'colorbalance=rs=.05:bs=-.05:rm=.04:bm=-.04,fps=30,setsar=1[c];'
           '[c][m]alphamerge,format=yuva420p[o]',
           '-map', '[o]', '-an', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '5M', '-auto-alt-ref', '0', '-t', f'{L:.3f}', out]
    subprocess.run(cmd, check=True)
    return out


def fx47(a, b, k):
    L = b - a
    src = inside_clip(a, L)
    s = a + max(.55, .45 * L)
    gd = min(.55, .2 * L + .25)
    cx, cy = 540, 960
    ti = 100 + 47 * 3
    front = [f'<video id="{k}-in" class="full {k}-in" src="{src}" muted playsinline data-start="{a:.3f}" data-media-start="0" data-duration="{L:.3f}" data-track-index="{ti}"></video>',
             f'<div id="{k}-rim" class="{k}-rim"></div>',
             f'<video id="{k}-fu" class="full {k}-fu" src="assets/rawclip.mp4" muted playsinline data-start="{s - .3:.3f}" data-media-start="{RAW_M0 + s - .3 - a:.3f}" '
             f'data-duration="{b - s + .3:.3f}" data-track-index="{ti + 1}"></video>',
             f'<div id="{k}-cap" class="{k}-cap">rushs bruts <b>→</b> réel monté</div>']
    tw = hid(f'#{k}-in', f'#{k}-rim', f'#{k}-fu', f'#{k}-cap') + [
        f"tl.set('#{k}-in',{{autoAlpha:1}},{a:.3f});",
        f"tl.fromTo('#{k}-in',{{clipPath:'circle(0px at {cx}px {cy + 200}px)'}},{{clipPath:'circle(1300px at {cx}px {cy + 200}px)',duration:.32,ease:'power2.in',immediateRender:false}},{a:.3f});",
        f"tl.fromTo('#{k}-cap',{{autoAlpha:0,y:20}},{{autoAlpha:1,y:0,duration:.22,ease:'power2.out',immediateRender:false}},{a + .12:.3f});",
        f"tl.set('#{k}-rim',{{autoAlpha:1}},{s + .04:.3f});", f"tl.set('#{k}-fu',{{autoAlpha:1}},{s:.3f});",
        f"tl.fromTo('#{k}-rim',{{clipPath:'circle(14px at {cx}px {cy}px)'}},{{clipPath:'circle(2214px at {cx}px {cy}px)',duration:{gd:.3f},ease:'power2.inOut',immediateRender:false}},{s:.3f});",
        f"tl.fromTo('#{k}-fu',{{clipPath:'circle(0px at {cx}px {cy}px)'}},{{clipPath:'circle(2200px at {cx}px {cy}px)',duration:{gd:.3f},ease:'power2.inOut',immediateRender:false}},{s:.3f});",
        f"tl.set('#{k}-in',{{autoAlpha:0}},{s + gd:.3f});",
        f"tl.set('#{k}-rim',{{autoAlpha:0}},{s + gd:.3f});",
    ] + off(b, f'#{k}-in', f'#{k}-rim', f'#{k}-fu', f'#{k}-cap')
    css = f'''
.{k}-in{{z-index:20;filter:drop-shadow(0 0 3px rgba(255,236,206,.95)) drop-shadow(0 0 16px rgba(201,154,85,.85))}}
.{k}-rim{{position:absolute;inset:0;z-index:21;background:{PILL};box-shadow:0 0 40px rgba(201,154,85,.8)}}
.{k}-fu{{z-index:22}}
.{k}-cap{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:300px;z-index:23;padding:16px 30px;border-radius:999px;
  background:rgba(42,26,16,.9);font:700 italic 38px/1 Poppins;color:{CREAM};box-shadow:0 12px 30px rgba(0,0,0,.35)}}
.{k}-cap b{{color:{GOLDL};font-weight:700;margin:0 6px}}
'''
    # rim sits under the full video: its circle is 50px wider so a gold ring leads the growing window
    return dict(front=front, tw=tw, css=css)


# ====================================================================== 48 SCENE TEXT (behind her)
def fx48(a, b, k):
    L = b - a
    line = 'montage de réels avec Claude — thestrategicboost.fr'
    td = min(.6, max(.28, .15 * L))
    w1, w2 = a + td + .02, a + td + .15
    behind = [f'<div id="{k}-ln" class="{k}-ln"><span id="{k}-tx"></span><i id="{k}-ca"></i></div>',
              f'<div id="{k}-w1" class="{k}-w {k}-w1">RÉELS</div>',
              f'<div id="{k}-w2" class="{k}-w {k}-w2">MONTÉS</div>',
              f'<div id="{k}-r1" class="{k}-ring" style="top:380px"></div><div id="{k}-r2" class="{k}-ring" style="top:600px"></div>']
    sels = [f'#{k}-ln', f'#{k}-w1', f'#{k}-w2', f'#{k}-r1', f'#{k}-r2']
    tw = hid(*sels) + on(a, f'#{k}-ln') + typing(f'#{k}-tx', line, a, a + td)
    tw += [f"tl.fromTo('#{k}-ca',{{opacity:1}},{{opacity:0,duration:.12,repeat:{int(L / .24)},yoyo:true,ease:'steps(1)',immediateRender:false}},{a:.3f});"]
    for sel, t in ((f'#{k}-w1', w1), (f'#{k}-w2', w2)):
        tw += [f"tl.fromTo('{sel}',{{autoAlpha:0,scale:1.75,y:-30}},{{autoAlpha:1,scale:1,y:0,duration:.15,ease:'power4.in',immediateRender:false}},{t:.3f});",
               f"tl.fromTo('{sel}',{{scaleY:1}},{{scaleY:.93,duration:.05,yoyo:true,repeat:1,ease:'power1.out',immediateRender:false}},{t + .15:.3f});"]
    for sel, t in ((f'#{k}-r1', w1), (f'#{k}-r2', w2)):
        tw += [f"tl.fromTo('{sel}',{{autoAlpha:.7,scale:.55}},{{autoAlpha:0,scale:1.35,duration:.45,ease:'power2.out',immediateRender:false}},{t + .14:.3f});"]
    tw += [f"tl.to('{s_}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});" for s_ in sels[:3]] + off(b, *sels)
    css = f'''
.{k}-ln{{position:absolute;left:127px;top:292px;font:500 27px/1 'JetBrains Mono';color:{CREAM};letter-spacing:.01em;white-space:pre;
  text-shadow:0 2px 12px rgba(42,26,16,.45)}}
.{k}-ln i{{display:inline-block;width:14px;height:30px;background:{GOLDL};margin-left:4px;vertical-align:-5px}}
.{k}-w{{position:absolute;left:0;right:0;text-align:center;font:400 250px/1 Anton;letter-spacing:.01em;filter:drop-shadow(0 16px 26px rgba(42,26,16,.42))}}
.{k}-w1{{top:345px;color:{CREAM}}}
.{k}-w2{{top:585px;background:{PILL};-webkit-background-clip:text;background-clip:text;color:transparent}}
.{k}-ring{{position:absolute;left:140px;width:800px;height:200px;border-radius:50%;border:3px solid rgba(244,238,230,.75)}}
'''
    return dict(behind=behind, tw=tw, css=css)


# ====================================================================== 49 NEON SIGN (behind her)
def fx49(a, b, k):
    L = b - a
    sw = '<svg class="{c}" viewBox="0 0 640 60"><path d="M10 38 C 140 8, 300 54, 420 30 S 600 18, 630 26"/></svg>'

    def sign(cls, lit):
        e = f'Claud<span id="{k}-e">e</span>' if lit else 'Claude'
        return (f'<div class="{k}-sg {cls}"><div class="{k}-l1">monté avec</div><div class="{k}-l2">{e}</div>'
                + sw.format(c=f'{k}-sw') + '</div>')
    behind = [f'<div id="{k}-glow" class="{k}-glow"></div>',
              f'<div id="{k}-off">{sign(k + "-off", False)}</div>',
              f'<div id="{k}-lit">{sign(k + "-lit", True)}</div>']
    sels = [f'#{k}-glow', f'#{k}-off', f'#{k}-lit']
    t0 = a + .06
    tw = hid(*sels, f'#{k}-e') + [f"tl.fromTo('#{k}-off',{{autoAlpha:0}},{{autoAlpha:1,duration:.08,immediateRender:false}},{a:.3f});"]
    steps = [(0, 1), (.035, 0), (.07, 1), (.1, .25), (.13, 1), (.19, .45), (.22, 1)]
    for dt, v in steps:
        tw += [f"tl.set('#{k}-lit',{{autoAlpha:{v}}},{t0 + dt:.3f});", f"tl.set('#{k}-glow',{{autoAlpha:{v * .9:.2f}}},{t0 + dt:.3f});"]
    # the last letter catches up a beat later, then a couple of mains hums during the hold
    for dt, v in [(.12, 1), (.17, 0), (.21, 1), (.27, 0), (.3, 1)]:
        tw += [f"tl.set('#{k}-e',{{autoAlpha:{v}}},{t0 + dt:.3f});"]
    for f in (.55, .8):
        t = a + f * L
        tw += [f"tl.set('#{k}-lit',{{autoAlpha:.72}},{t:.3f});", f"tl.set('#{k}-lit',{{autoAlpha:1}},{t + .04:.3f});"]
    tw += [f"tl.to('{s_}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});" for s_ in sels] + off(b, *sels, f'#{k}-e')
    neon = ('0 0 2px #fff,0 0 7px #FFF1DC,0 0 16px rgba(255,214,160,.95),0 0 32px rgba(233,170,95,.9),'
            '0 0 60px rgba(201,138,62,.85),0 0 110px rgba(168,106,46,.7)')
    css = f'''
.{k}-glow{{position:absolute;left:-60px;top:170px;width:1200px;height:680px;
  background:radial-gradient(50% 50% at 50% 48%,rgba(255,206,150,.42),rgba(201,138,62,.18) 45%,transparent 72%);mix-blend-mode:screen}}
.{k}-sg{{position:absolute;left:0;top:0;width:1080px;text-align:center;font-family:Caveat;font-weight:600}}
.{k}-l1{{position:absolute;left:0;right:0;top:268px;font-size:132px;line-height:1;transform:rotate(-4deg)}}
.{k}-l2{{position:absolute;left:0;right:0;top:372px;font-size:220px;line-height:1;transform:rotate(-4deg)}}
.{k}-sw{{position:absolute;left:250px;top:590px;width:600px;height:56px;transform:rotate(-4deg);overflow:visible}}
.{k}-sw path{{fill:none;stroke-width:7;stroke-linecap:round}}
.{k}-off{{color:rgba(244,238,230,.24);text-shadow:0 3px 0 rgba(42,26,16,.22)}}
.{k}-off .{k}-sw path{{stroke:rgba(244,238,230,.24)}}
.{k}-lit{{color:#FFF6EA;text-shadow:{neon}}}
.{k}-lit .{k}-sw path{{stroke:#FFF6EA;filter:drop-shadow(0 0 4px #FFE6C4) drop-shadow(0 0 14px rgba(233,170,95,.95)) drop-shadow(0 0 34px rgba(201,138,62,.85))}}
#{k}-e{{display:inline-block}}
'''
    return dict(behind=behind, tw=tw, css=css)


# ====================================================================== 50 SPATIAL GLASS
def fx50(a, b, k):
    L = b - a
    panels = [  # n, title, sub, left, top, w, h, rotX, rotY
        (1, 'Tes rushs', 'tu déposes tes clips bruts', 230, 292, 620, 196, 14, 0),
        (2, 'Claude monte', 'coupes, sous-titres, musique', 70, 720, 300, 262, 0, 26),
        (3, 'Tu publies', 'ton réel est prêt', 680, 1252, 330, 238, 0, -26),
    ]
    front, tw, sels = [], [], []
    inner = ''
    for i, (n, t, s, x, y, w, h, rx, ry) in enumerate(panels):
        wide = w > 400
        inner += (f'<div id="{k}-p{i}" class="{k}-bob" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                  f'<div id="{k}-q{i}" class="{k}-pn {k}-{"wide" if wide else "tall"}"><b id="{k}-n{i}">{n}</b>'
                  f'<div><h4>{t}</h4><p>{s}</p></div></div></div>')
        sels.append(f'#{k}-q{i}')
    front.append(f'<div id="{k}-sp" class="{k}-sp">{inner}</div>')
    tw += hid(f'#{k}-sp', *sels) + on(a, f'#{k}-sp')
    for i, (n, t, s, x, y, w, h, rx, ry) in enumerate(panels):
        q, p = f'#{k}-q{i}', f'#{k}-p{i}'
        t0 = a + .055 * i
        tw += [f"tl.fromTo('{q}',{{autoAlpha:0,z:-420,rotationX:{rx * 2.2:.0f},rotationY:{ry * 2.2 if ry else (30 if i % 2 else -30):.0f},y:50}},"
               f"{{autoAlpha:1,z:0,rotationX:{rx},rotationY:{ry},y:0,duration:.28,ease:'power3.out',immediateRender:false}},{t0:.3f});"]
        bob = .75 + .12 * i
        rep = max(0, int((b - t0 - .3) / bob) - 1)
        tw += [f"tl.fromTo('{p}',{{y:0,rotationZ:0}},{{y:{-14 if i % 2 else 12},rotationZ:{(.8 if i % 2 else -.8)},duration:{bob:.2f},yoyo:true,repeat:{rep},ease:'sine.inOut',immediateRender:false}},{t0 + .1:.3f});"]
        ts = a + .38 + i * max(.12, (L - .7) / 3)
        tw += [f"tl.fromTo('#{k}-n{i}',{{scale:1}},{{scale:1.22,duration:.12,yoyo:true,repeat:1,ease:'power2.out',immediateRender:false}},{ts:.3f});"]
    tw += [f"tl.to('{s_}',{{autoAlpha:0,duration:.13}},{b - .13:.3f});" for s_ in sels] + off(b, f'#{k}-sp', *sels)
    css = f'''
.{k}-sp{{position:absolute;inset:0;z-index:20;perspective:1300px;perspective-origin:50% 45%}}
.{k}-bob{{position:absolute}}
.{k}-pn{{position:absolute;inset:0;border-radius:34px;background:rgba(255,255,255,.15);-webkit-backdrop-filter:blur(20px) saturate(1.25);backdrop-filter:blur(20px) saturate(1.25);
  border:1.5px solid rgba(255,255,255,.5);box-shadow:0 30px 60px rgba(42,26,16,.28),inset 0 1px 0 rgba(255,255,255,.6),inset 0 -20px 40px rgba(255,255,255,.06);
  display:flex;gap:22px;padding:30px;color:#fff}}
.{k}-wide{{align-items:center;padding:30px 40px}}
.{k}-tall{{flex-direction:column;justify-content:center;padding:26px;gap:16px}}
.{k}-pn b{{flex:0 0 74px;width:74px;height:74px;border-radius:50%;background:{PILL};color:{INK};font:400 46px/74px Anton;text-align:center;
  box-shadow:0 8px 20px rgba(42,26,16,.3)}}
.{k}-pn h4{{font:700 40px/1.1 Poppins;letter-spacing:-.01em;text-shadow:0 2px 12px rgba(42,26,16,.35)}}
.{k}-tall h4{{font-size:34px}}
.{k}-pn p{{font:600 24px/1.25 Poppins;color:rgba(255,255,255,.92);margin-top:8px;text-shadow:0 2px 10px rgba(42,26,16,.35)}}
'''
    return dict(front=front, tw=tw, css=css)


EFFECTS = [
    (42, 'TIMELINE BURN', fx42),
    (43, 'KNOCKOUT TILES', fx43),
    (44, 'SHATTER 3D', fx44),
    (45, 'CODE SCAN', fx45),
    (46, 'WORD PILE', fx46),
    (47, 'INSIDE OUT', fx47),
    (48, 'SCENE TEXT', fx48),
    (49, 'NEON SIGN', fx49),
    (50, 'SPATIAL GLASS', fx50),
]
