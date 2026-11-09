#!/usr/bin/env python3
"""Reel "vues-classement" v4 (her ask): the three numbers 100 (red) / 10 000 (yellow) / 100 000 (green) stay on screen
side by side from the first frame as a visual hook; on each verdict its number grows and lights up, the others fade
back (100 wobbles, 100 000 flashes with turning rays). The next title waits until the verdict has been seen.
v3 (v2 gauge was too small to read): each verdict lands as a HUGE number above her head
(Anton 176px on a plate: dark for 100, brown for 10K, gold with turning rays + white flash for 100K), counting up.
Rest as v2.
v2: a different edit of the same cut (the first one was a ranking board with icons):
a VIEWS GAUGE. Each tip lands in her dark-brown block (Anton, white) on top; under it a semicircle meter (100 / 10K /
100K) whose needle searches, then swings to the verdict on her word, while the white pill under the title rolls the
number up (39 Odometer). Tip 2's two conditions pop as chips (56 Chip row), "non négociable" slams in as a stamp
(01 Kinetic hook), the CTA is her Instagram comment banner with AVOCADO typing itself. Her one-word captions
(Poppins white, key words bigger), her retouch (assets/aroll_r.mp4), no zoom on her face. Sounds only where something
appears: a soft "nope" on 100 views, a ding on 10K, a cash register on 100K.

PY build_v2.py      writes index.html
"""
import json
import os
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
if os.environ.get('TEST'):
    DUR = min(DUR, float(os.environ['TEST']))
SEG = {s['id']: s['frame'] / 30 for s in json.load(open('segments.json', encoding='utf-8'))}
DARK, BROWN, GOLD, CREAM = '#573307', '#8C5C41', '#C99A55', '#F4EEE6'

# tips: (title, title in, verdict time, zone 0=100 / 1=10K / 2=100K)
TIPS = [
    ('POSTER À UNE HEURE PRÉCISE', 0.00, 2.26, 0),
    ('VIDÉOS COURTES (5 S)', SEG['t2'], 5.22, 2),
    ('VIDÉOS ÉDUCATIVES LONGUES', SEG['t3'], 12.38, 1),
    ('REPRENDRE DES REELS VIRAUX', SEG['t4'], 15.06, 2),
    ('AUDIO TENDANCE', SEG['t5'], 20.26, 0),
    ('AJOUTER MANYCHAT', SEG['t6'], 26.00, 2),
]
CTA = 30.12
ZONES = [('100', -58, '100 vues'), ('10K', 0, '10 000 vues'), ('100K', 58, '100 000 vues')]
ZSFX = ['fail', 'ding', 'kaching']      # 100 views: her own "son négatif" buzzer (Drive pour Claude)
CHIPS = [(7.08, 'hook textuel banger'), (9.04, 'redirection en légende')]
STAMP = 27.54
GX, GY, GR = 540, 588, 122          # gauge centre and radius (sits above her head)


def show(sel, a, b, frm='{autoAlpha:0,y:-24,scale:.92}', d=.28, ease='back.out(1.8)'):
    d = min(d, max(.08, b - a - .2))
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,y:0,x:0,scale:1,rotation:0,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def arc(a0, a1, r):
    """svg arc path between two angles (degrees, 0 = straight up, clockwise positive)"""
    import math
    p = lambda a: (GX + r * math.sin(math.radians(a)), GY - r * math.cos(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    return f'M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}'


def gauge():
    import math
    segs = [(-90, -31, DARK), (-29, 29, BROWN), (31, 90, GOLD)]
    svg = ['<svg id="gsvg" class="full" viewBox="0 0 1080 1920">',
           f'<path d="{arc(-90, 90, GR)}" fill="none" stroke="rgba(30,18,10,.35)" stroke-width="42" stroke-linecap="round"/>']
    for k, (a0, a1, c) in enumerate(segs):
        svg.append(f'<path id="gz{k}" d="{arc(a0, a1, GR)}" fill="none" stroke="{c}" stroke-width="32" stroke-linecap="butt"/>')
    for k, (lab, ang, _) in enumerate(ZONES):
        x, y = GX + (GR + 50) * math.sin(math.radians(ang)), GY - (GR + 50) * math.cos(math.radians(ang))
        svg.append(f'<text id="gl{k}" x="{x:.0f}" y="{y + 14:.0f}" text-anchor="middle" font-family="Anton" font-size="34" fill="#fff" '
                   f'style="paint-order:stroke" stroke="rgba(40,24,12,.55)" stroke-width="6">{lab}</text>')
    svg.append(f'<g id="needle"><path d="M{GX - 9} {GY} L{GX} {GY - GR + 22} L{GX + 9} {GY} Z" fill="#fff" stroke="{DARK}" stroke-width="3"/>'
               f'<circle cx="{GX}" cy="{GY}" r="16" fill="{DARK}" stroke="#fff" stroke-width="4"/></g></svg>')
    return ''.join(svg)


def scenes():
    H, T, S = [], [], []
    # the three numbers stay on screen the whole time (visual hook): 100 red, 10 000 yellow, 100 000 green
    rays = ('<svg class="rays" viewBox="-100 -100 200 200">' + ''.join(
        f'<path d="M0 0 L-9 -100 L9 -100Z" transform="rotate({q * 30})" fill="rgba(255,255,255,.4)"/>' for q in range(12)) + '</svg>')
    H.append('<div id="row" class="row">' + ''.join(
        f'<div id="pl{z}" class="plate t{z}"><b>{lab}</b><small>vues</small></div>'
        for z, lab in enumerate(('100', '10 000', '100 000'))) + '</div>')
    T += [      # no entrance (her ask): the three numbers are there from the very first frame
          f"tl.to('#row',{{autoAlpha:0,duration:.2}},{CTA - .2:.3f});", f"tl.set('#row',{{autoAlpha:0}},{CTA:.3f});"]
    # each verdict is held at least .9 s; the next title waits for it, so a lit number never sits under the wrong tip
    ENDS = [min(max(TIPS[k + 1][1] if k + 1 < len(TIPS) else CTA, tv + .9), TIPS[k + 1][2] - .25 if k + 1 < len(TIPS) else CTA)
            for k, (_, _, tv, _) in enumerate(TIPS)]
    for k, (title, a, tv, z) in enumerate(TIPS):
        b = ENDS[k]
        a = max(a, ENDS[k - 1]) if k else a
        H.append(f'<div id="tp{k}" class="top"><div class="blk"><span class="no">{k + 1}</span>{title}</div></div>')
        if k == 0:        # the first title is there at once too
            T += [f"tl.to('#tp0',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('#tp0',{{autoAlpha:0}},{b:.3f});"]
        else:
            T += show(f'#tp{k}', a + .02, b, '{autoAlpha:0,x:-120}', .26, 'power3.out')
        if k:
            S.append(('whoosh-short', a + .02, .3))
        # THE VERDICT: its number grows and lights up, the two others fade back
        others = ', '.join(f'#pl{q}' for q in range(3) if q != z)
        T += [f"tl.to('#pl{z}',{{scale:1.3,duration:.24,ease:'back.out(2.6)'}},{tv - .02:.3f});",
              f"tl.to('{others}',{{opacity:.28,scale:.9,duration:.18}},{tv - .02:.3f});",
              f"tl.to('#row .plate',{{opacity:1,scale:1,duration:.2,ease:'power2.out'}},{b - .2:.3f});"]
        if z == 2:     # 100 000: a green glow pulses around the plate only (no rays / flash over her face, her ask)
            T += [f"tl.fromTo('#pl2',{{boxShadow:'0 0 0 0px rgba(35,169,75,.0), 0 12px 28px rgba(0,0,0,.3)'}},{{boxShadow:'0 0 0 12px rgba(35,169,75,.45), 0 12px 28px rgba(0,0,0,.3)',duration:.2,yoyo:true,repeat:3,ease:'sine.inOut',immediateRender:false}},{tv + .25:.3f});"]
        elif z == 0:   # 100: a little "dud" wobble
            T.append(f"tl.to('#pl0 b',{{rotation:-6,duration:.07,yoyo:true,repeat:3,ease:'sine.inOut'}},{tv + .3:.3f});")
        S += [('whoosh-short', tv - .05, .2), (ZSFX[z], tv + .25, [.55, .45, .5][z])]
    # 56 Chip row: the two conditions of tip 2
    for k, (t, txt) in enumerate(CHIPS):
        H.append(f'<div id="ch{k}" class="chip" style="top:{1150 + k * 92}px"><b>✓</b>{txt}</div>')
        T += show(f'#ch{k}', t, TIPS[2][1], '{autoAlpha:0,scale:.3,y:34}', .26, 'back.out(2.2)')
        S.append(('click-soft', t, .45))
    # "non négociable": a stamp slams in
    H.append('<div id="stamp" class="stamp">NON NÉGOCIABLE</div>')
    T += ["gsap.set('#stamp',{autoAlpha:0});",
          f"tl.fromTo('#stamp',{{autoAlpha:0,scale:2.2,rotation:-20}},{{autoAlpha:1,scale:1,rotation:-7,duration:.22,ease:'expo.out',immediateRender:false}},{STAMP:.3f});",
          f"tl.to('#stamp',{{autoAlpha:0,duration:.15}},{CTA - .15:.3f});", f"tl.set('#stamp',{{autoAlpha:0}},{CTA:.3f});"]
    S.append(('stamp', STAMP, .7))          # a rubber-stamp thud (her ask: not the bass impact)
    # CTA: her comment banner, AVOCADO types itself, send is tapped
    a_in, tb, word = CTA + .1, 30.72, 'AVOCADO'
    send = ('<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" '
            'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    H.append(f'<div id="cb" class="cb"><img class="cav" src="assets/avatar.png"/><div class="cw"><span id="cph" class="cph">Ajouter un commentaire…</span>'
             f'<span id="cty" class="cty"></span><i id="ccr" class="ccr"></i></div><div id="csd" class="csd">{send}</div></div>')
    T += ["gsap.set('#cb',{autoAlpha:0});",
          f"tl.fromTo('#cb',{{autoAlpha:0,y:-50,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:false}},{a_in:.3f});",
          "gsap.set('#cty',{textContent:''});", "gsap.set('#cph',{display:'inline'});",
          f"tl.set('#cty',{{textContent:''}},{a_in:.3f});", f"tl.set('#cph',{{display:'inline'}},{a_in:.3f});", f"tl.set('#cph',{{display:'none'}},{tb:.3f});"]
    T += [f"tl.set('#cty',{{textContent:'{word[:q]}'}},{tb + (q - 1) * .07:.3f});" for q in range(1, len(word) + 1)]
    ts = tb + len(word) * .07 + .2
    T += ["gsap.set('#ccr',{opacity:1});"] + [f"tl.set('#ccr',{{opacity:{q % 2}}},{a_in + .3 + q * .25:.3f});" for q in range(int((DUR - a_in) / .25))]
    T += [f"tl.to('#csd',{{scale:.78,duration:.07,yoyo:true,repeat:1}},{ts:.3f});",
          f"tl.to('#cb',{{boxShadow:'0 0 0 7px {DARK}, 0 16px 36px rgba(0,0,0,.3)',scale:1.05,duration:.18,yoyo:true,repeat:1}},{ts + .1:.3f});"]
    S += [('pop', a_in, .45), ('click', ts, .6)]
    # her one-word captions (lowercase; numbers, banger, négociable, avocado bigger)
    H_, T_ = captions()
    return H + H_, T + T_, S


KEY = {'100', '10 000', '100 000', 'banger', 'négociable', 'avocado', 'viraux', 'manychat', 'tchus'}


def captions():
    raw = json.load(open('words.json', encoding='utf-8'))
    ws = []
    for w in raw:
        t = w['text'].strip()
        if (t.startswith("'") or t.startswith('-')) and ws:
            ws[-1]['t'] += t
            ws[-1]['e'] = w['end']
            continue
        k = re.sub(r'[,.!?…]', '', t).lower()
        if ws and ws[-1]['t'] in ('100', '10') and k == '000':       # "100 000", "10 000" as one caption
            ws[-1]['t'] += ' 000'
            ws[-1]['e'] = w['end']
            continue
        k = {'off': 'of'}.get(k, k)
        ws.append({'t': k, 's': w['start'], 'e': w['end']})
    ws.append({'t': 'tchus', 's': SEG['bye'] + .81, 'e': SEG['bye'] + 1.4})   # after her finger kiss (kept: her signature)       # her signature
    H, T = [], []
    for n, w in enumerate(ws):
        nxt = ws[n + 1]['s'] if n + 1 < len(ws) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        if end - w['s'] < .05:
            continue
        if w['t'] in ('100', '10 000', '100 000', 'vues') and any(tv - .15 <= w['s'] <= tv + 1.0 for _, _, tv, _ in TIPS):
            continue      # the huge verdict number already says it
        cls = 'cap key' if w['t'] in KEY else 'cap'
        H.append(f'<div id="w{n}" class="{cls}">{w["t"]}</div>')
        T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
              f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
              f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
    return H, T


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.layer{{position:absolute;inset:0;z-index:15}}
.top{{position:absolute;left:0;right:0;top:250px;z-index:20;text-align:center}}
.blk{{display:inline-flex;align-items:center;gap:16px;max-width:860px;background:{DARK};color:#fff;font:400 58px/1.08 Anton;letter-spacing:.03em;
  padding:10px 26px 6px 14px;white-space:nowrap}}
.no{{display:inline-block;width:56px;height:56px;border-radius:50%;background:#fff;color:{DARK};font:400 38px/58px Anton;text-align:center;flex:none}}
.bigw{{position:absolute;left:0;right:0;top:372px;height:230px;z-index:19;display:flex;align-items:center;justify-content:center}}
.big{{position:relative;display:inline-flex;align-items:baseline;gap:18px;padding:6px 34px 0;border-radius:22px;color:#fff;font:400 176px/1 Anton;
  letter-spacing:.01em;text-shadow:0 6px 0 rgba(40,22,6,.45);box-shadow:0 18px 40px rgba(0,0,0,.35);white-space:nowrap}}
.big small{{font:400 66px/1 Anton;letter-spacing:.04em}}
.big.t0{{background:#E0322C}} .big.t1{{background:#F7C51E;color:#2A1A10;text-shadow:0 5px 0 rgba(255,255,255,.35)}} .big.t2{{background:#23A94B}}   /* her ask for this reel: red / yellow / green */
.rays{{position:absolute;width:760px;height:760px;left:50%;top:50%;margin:-380px 0 0 -380px;z-index:-1}}
.row{{position:absolute;left:0;right:0;top:350px;z-index:19;display:flex;justify-content:center;align-items:flex-start;gap:16px}}
.plate{{position:relative;display:flex;flex-direction:column;align-items:center;padding:8px 18px 6px;border-radius:18px;color:#fff;
  box-shadow:0 12px 28px rgba(0,0,0,.3);transform-origin:50% 0%}}
.plate b{{display:block;font:400 92px/1 Anton;letter-spacing:.01em;white-space:nowrap;text-shadow:0 4px 0 rgba(0,0,0,.25)}}
.plate small{{font:800 26px/1.1 Poppins;letter-spacing:.06em;text-transform:uppercase}}
.plate.t0{{background:#E0322C}} .plate.t1{{background:#F7C51E;color:#2A1A10}} .plate.t1 b{{text-shadow:0 4px 0 rgba(255,255,255,.35)}} .plate.t2{{background:#23A94B}}
.plate .rays{{position:absolute;width:640px;height:640px;left:50%;top:50%;margin:-320px 0 0 -320px;z-index:-1}}
.pill{{display:inline-flex;align-items:center;gap:12px;margin-top:-4px;padding:6px 30px 6px 22px;border-radius:40px;background:#fff;color:{DARK};
  font:italic 800 44px/1.2 Poppins;letter-spacing:-.02em;box-shadow:0 4px 16px rgba(0,0,0,.22);transform-origin:50% 50%}}
.chip{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;z-index:21;display:flex;align-items:center;gap:14px;padding:10px 30px 12px 20px;
  border-radius:999px;background:#fff;color:{DARK};font:italic 800 42px/1.1 Poppins;letter-spacing:-.02em;box-shadow:0 6px 18px rgba(0,0,0,.25)}}
.chip b{{display:inline-block;width:46px;height:46px;border-radius:50%;background:{DARK};color:#fff;font:700 28px/46px Poppins;text-align:center;font-style:normal}}
.stamp{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1140px;z-index:22;padding:14px 34px 8px;border:8px solid #fff;border-radius:18px;
  background:rgba(87,51,7,.92);color:#fff;font:400 92px/1 Anton;letter-spacing:.04em;box-shadow:0 14px 34px rgba(0,0,0,.35)}}
.cb{{position:absolute;left:130px;width:820px;top:300px;z-index:30;height:118px;border-radius:59px;background:#fff;display:flex;align-items:center;gap:20px;
  padding:0 18px;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.cav{{width:80px;height:80px;border-radius:50%;object-fit:cover;flex:none;border:3px solid {DARK}}}
.cw{{flex:1;display:flex;align-items:center;min-width:0}}
.cph{{font:500 36px/1 Poppins;color:#9A9087}}
.cty{{font:400 66px/1 Anton;letter-spacing:.06em;color:#2A1A10}}
.ccr{{width:4px;height:56px;background:{DARK};margin-left:6px}}
.csd{{width:84px;height:84px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center;flex:none}}
.cap{{position:absolute;left:40px;right:40px;top:1400px;z-index:25;text-align:center;font:700 66px/1 Poppins;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.cap.key{{font-size:88px;font-weight:800}}
'''
SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click': .36, 'click-soft': .36, 'ding': 1.2, 'nope': .8, 'kaching': 1.2, 'impact-bass-1': 2.1, 'stamp': .45, 'fail': .45}


def build():
    H, T, S = scenes()
    nl = '\n'
    sfx, lanes = [], []
    for k, (n, t, v) in enumerate(sorted(S, key=lambda x: x[1])):
        d = min(SFX_LEN[n], DUR - t)
        lane = next((i for i, e in enumerate(lanes) if e <= t), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = t + d
        sfx.append(f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" data-track-index="{10 + lane}" data-volume="{v:.2f}"></audio>')
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="assets/vendor/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(sfx)}
  <video id="bgv" class="full" src="assets/aroll_r.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(H)}
  <div id="flash" style="position:absolute;inset:0;z-index:40;background:#fff;opacity:0;pointer-events:none"></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(T)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


if __name__ == '__main__':
    with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
        _f.write(build())
    print(f'wrote index.html {DUR:.3f}s')
