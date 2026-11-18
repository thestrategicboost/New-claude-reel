#!/usr/bin/env python3
"""« 10 ans de marketing résumés en 30 secondes » — her charter: brown block (Anton, white) + white pill (Poppins italic,
brown), one-word captions (Poppins white, soft shadow, key words bigger), lilac look + retouch, no zoom on her face,
everything below the « Reels d'essai » band.
An iPhone stopwatch (black card, thin white digits, round Tour / Arrêter buttons) sits on top: it shows 00:00,00 during
the hook, starts on « Let's go », takes a lap (« Tour n ») on each lesson while the lesson lands in a white pill, stops
after the last lesson; the CTA is her Instagram comment banner (LEVEL UP types itself).

PY build.py      writes index.html
"""
import json
import re

SEG = json.load(open('work/segs.json'))
SEGS, DURS = SEG['segs'], SEG['durs']
DUR = round(sum(DURS), 3)
EDGES, _e = [], 0.0
for _d in DURS:
    EDGES.append(_e)
    _e += _d
DARK = '#523301'
RAW = json.load(open('work/words.json'))


def ct(t):
    for (a, b), e in zip(SEGS, EDGES):
        if a - .05 <= t <= b + .05:
            return e + max(0.0, t - a)
    return None


def first(word, after=0.0):
    for w in RAW:
        if w['s'] >= after and re.sub(r'[^\w’\']', '', w['w'].lower()).startswith(word):
            return ct(w['s'])
    raise ValueError(word)


T_GO = first('go', 4.0)                       # « Let's go ! »: the stopwatch starts
LESSONS = [                                   # (raw time of its first word, pill text)
    (5.68, 'On achète une transformation'),
    (11.08, 'Le marketing répond à un problème'),
    (15.48, 'La clarté bat la créativité'),
    (20.62, 'Tu ne peux pas vendre à tout le monde'),
    (25.04, 'La preuve sociale déclenche l’achat'),
    (29.14, 'Sans stratégie, c’est épuisant'),
    (34.54, 'Le marketing ne sauve pas une offre'),
]
T_STOP = first('girl', 39.0) + .35            # after « Pas le marketing, ma girl »
T_CTA = first('commente', 40.0)
T_LVL = first('level', 40.0)
KEY = {'transformation', 'bénéfice', 'problème', 'clarté', 'créativité', 'cible', 'preuve', 'sociale', 'stratégie', 'offre', 'résultats'}
FIX = {'etats-unis': 'États-Unis', 'états-unis': 'États-Unis', 'france': 'France', 'tchüss': 'tchus', 'tchuss': 'tchus', "let's": "let’s"}


def show(sel, a, b, frm='{autoAlpha:0,y:-18,scale:.9}', d=.24, ease='back.out(1.9)'):
    d = min(d, max(.08, b - a - .2))
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,y:0,scale:1,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def build():
    H, T, S = [], [], []
    # hook: title + typed pill (0 -> « Let's go »)
    pill = 'résumés en 30 secondes'
    H.append(f'<div id="hk" class="hk"><div class="blk">10 ANS DE MARKETING</div><br/><div class="pill"><span class="gh">{pill}</span><span id="tx"></span></div></div>')
    T += [f"tl.to('#hk',{{autoAlpha:0,duration:.15}},{T_GO - .1:.3f});", f"tl.set('#hk',{{autoAlpha:0}},{T_GO + .05:.3f});",
          "tl.set('#tx',{textContent:''},0);"]
    t0, t1 = first('résumé', 0) - .05, first('secondes', 0) + .35
    T += [f"tl.set('#tx',{{textContent:{json.dumps(pill[:i])}}},{t0 + (t1 - t0) * i / len(pill):.3f});" for i in range(1, len(pill) + 1)]
    S += [('typing', t0, .55, t1 - t0 + .1)]
    # the two flags on « États-Unis » and « France »
    US = ('<svg viewBox="0 0 190 100" width="190" height="100"><rect width="190" height="100" fill="#B22234"/>'
          + ''.join(f'<rect y="{i * 100 / 13 * 2 + 100 / 13:.2f}" width="190" height="{100 / 13:.2f}" fill="#fff"/>' for i in range(6))
          + '<rect width="76" height="53.85" fill="#3C3B6E"/>'
          + ''.join(f'<circle cx="{8 + c * 12 + (6 if r % 2 else 0)}" cy="{6 + r * 10.5}" r="2.2" fill="#fff"/>' for r in range(5) for c in range(6 if r % 2 == 0 else 5))
          + '</svg>')
    FR = '<svg viewBox="0 0 150 100" width="150" height="100"><rect width="50" height="100" fill="#0055A4"/><rect x="50" width="50" height="100" fill="#fff"/><rect x="100" width="50" height="100" fill="#EF4135"/></svg>'
    for fid, svg, raw, x, rot in (('fus', US, 4.16, 110, -8), ('ffr', FR, 4.90, 800, 8)):
        a = ct(raw)
        H.append(f'<div id="{fid}" class="flag" style="left:{x}px">{svg}</div>')
        T += [f"gsap.set('#{fid}',{{autoAlpha:0}});",
              f"tl.fromTo('#{fid}',{{autoAlpha:0,scale:.3,rotation:{rot * 3}}},{{autoAlpha:1,scale:1,rotation:{rot},duration:.3,ease:'back.out(2.2)',immediateRender:false}},{a - .05:.3f});",
              f"tl.to('#{fid}',{{autoAlpha:0,scale:.8,duration:.15}},{T_GO + .25:.3f});", f"tl.set('#{fid}',{{autoAlpha:0}},{T_GO + .4:.3f});"]
        S.append(('pop', a - .05, .4))
    # the iPhone stopwatch
    H.append('<div id="sw" class="sw"><div id="dig" class="dig">00:00,00</div><div class="btns"><span id="bt" class="b tour">Tour</span>'
             '<span id="lap" class="lap">Tour 1</span><span id="bs" class="b go">Démarrer</span></div></div>')
    T += ["gsap.set('#sw',{autoAlpha:0});", "gsap.set('#lap',{autoAlpha:0});",
          f"tl.fromTo('#sw',{{autoAlpha:0,scale:.85}},{{autoAlpha:1,scale:1,duration:.25,ease:'back.out(1.8)',immediateRender:false}},{T_GO - .12:.3f});",
          "const ck={v:0}; const fmt=v=>{const m=Math.floor(v/60),s=Math.floor(v%60),c=Math.floor((v*100)%100);return String(m).padStart(2,'0')+':'+String(s).padStart(2,'0')+','+String(c).padStart(2,'0')};",
          f"tl.fromTo(ck,{{v:0}},{{v:{T_STOP - T_GO:.3f},duration:{T_STOP - T_GO:.3f},ease:'none',immediateRender:false,onUpdate:()=>{{document.getElementById('dig').textContent=fmt(ck.v)}}}},{T_GO:.3f});",
          f"tl.set('#bs',{{textContent:'Arrêter',className:'b stop'}},{T_GO:.3f});",
          f"tl.fromTo('#bs',{{scale:.8}},{{scale:1,duration:.15,immediateRender:false}},{T_GO:.3f});",
          f"tl.set('#bs',{{textContent:'Démarrer',className:'b go'}},{T_STOP:.3f});",
          f"tl.fromTo('#bs',{{scale:.8}},{{scale:1,duration:.15,immediateRender:false}},{T_STOP:.3f});",
          f"tl.fromTo('#dig',{{opacity:1}},{{opacity:.35,duration:.12,yoyo:true,repeat:3,immediateRender:false}},{T_STOP + .05:.3f});",
          f"tl.to('#sw',{{autoAlpha:0,duration:.2}},{T_CTA - .25:.3f});", f"tl.set('#sw',{{autoAlpha:0}},{T_CTA - .05:.3f});"]
    S += [('click', T_STOP, .6)]      # no click at the start (her ask)
    # each lesson: a lap on the stopwatch + the lesson in a white pill under it
    for k, (raw, txt) in enumerate(LESSONS):
        a = ct(raw)
        b = ct(LESSONS[k + 1][0]) if k + 1 < len(LESSONS) else T_STOP + .6
        H.append(f'<div id="ls{k}" class="ls"><span class="n">{k + 1}</span><span class="lt">{txt}</span></div>')
        T += show(f'#ls{k}', a, b)
        T += [f"tl.set('#lap',{{textContent:'Tour {k + 1}'}},{a:.3f});", f"tl.fromTo('#bt',{{scale:.82}},{{scale:1,duration:.14,immediateRender:false}},{a:.3f});",
              f"tl.fromTo('#lap',{{autoAlpha:0}},{{autoAlpha:1,duration:.12,immediateRender:false}},{a:.3f});"]
        S.append(('click-soft', a, .5))
    # CTA: her Instagram comment banner, LEVEL UP types itself, send is tapped
    # a wall of her e-book « LEVEL UP TON BIZ » pages pops in BEHIND her (her ask, like a reel wall): her cut-out (subject_cta.webm,
    # cut from aroll frame 1230 = 41.0 s) on top of it, captions and banner above
    PAGES = [1, 3, 4, 2, 6, 7, 5, 13, 10, 15, 19, 20]      # cover top-left (never behind her head)
    ROT = [-3, 2, -2, 3, 2, -3, 3, -2, -2, 3, -3, 2]
    for k, (pg, r) in enumerate(zip(PAGES, ROT)):
        ry = (18, 9, -9, -18)[k % 4]                       # 3D: the pages turn toward her, like a curved wall
        H.append(f'<div id="wt{k}" class="wt" style="left:{40 + (k % 4) * 260}px;top:{515 + (k // 4) * 350}px">'
                 f'<img src="assets/wall/p{pg:02d}.jpg"/></div>')
        T.append(f"gsap.set('#wt{k}',{{transformPerspective:900,rotationY:{ry},rotationX:{6 - (k // 4) * 6},rotation:{r * .6:.1f}}});")
    T += ["gsap.set('.wt',{autoAlpha:0});",
          f"tl.fromTo('.wt',{{autoAlpha:0,scale:.4}},{{autoAlpha:1,scale:1,duration:.28,ease:'back.out(1.8)',stagger:{{each:.06,from:'center'}},immediateRender:false}},{T_CTA + .1:.3f});"]
    S.append(('whoosh-short', T_CTA + .15, .35))
    word = 'LEVEL UP'
    send = ('<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" '
            'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    H.append(f'<div id="cb" class="cb"><img class="cav" src="assets/avatar.png"/><div class="cw"><span id="cph" class="cph">Ajouter un commentaire…</span>'
             f'<span id="cty" class="cty"></span><i id="ccr" class="ccr"></i></div><div id="csd" class="csd">{send}</div></div>')
    T += ["gsap.set('#cb',{autoAlpha:0});",
          f"tl.fromTo('#cb',{{autoAlpha:0,y:-50,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:false}},{T_CTA - .05:.3f});",
          "gsap.set('#cty',{textContent:''});", "gsap.set('#cph',{display:'inline'});",
          f"tl.set('#cph',{{display:'none'}},{T_LVL:.3f});"]
    T += [f"tl.set('#cty',{{textContent:{json.dumps(word[:q])}}},{T_LVL + (q - 1) * .07:.3f});" for q in range(1, len(word) + 1)]
    ts = T_LVL + len(word) * .07 + .2
    T += [f"tl.to('#csd',{{scale:.78,duration:.07,yoyo:true,repeat:1}},{ts:.3f});",
          f"tl.to('#cb',{{boxShadow:'0 0 0 7px {DARK}, 0 16px 36px rgba(0,0,0,.3)',scale:1.05,duration:.18,yoyo:true,repeat:1}},{ts + .1:.3f});"]
    S += [('pop', T_CTA - .05, .45), ('click', ts, .5)]
    # one-word captions
    ws = []
    for w in RAW:
        t = w['w'].strip()
        if (t.startswith("'") or t.startswith('-')) and ws:
            ws[-1]['t'] += t
            ws[-1]['e'] = w['e']
            continue
        k = re.sub(r'[,.!?…]', '', t).lower()
        k = FIX.get(k, k)
        s = ct(w['s'])
        if k and s is not None:
            ws.append({'t': k, 's': s, 'e': ct(min(w['e'], w['s'] + 1.2)) or s + .3})
    for n, w in enumerate(ws):
        if w['s'] >= T_CTA - .05 and w['t'] in ('level', 'up'):
            continue
        nxt = ws[n + 1]['s'] if n + 1 < len(ws) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        if end - w['s'] < .05:
            continue
        cls = 'cap key' if w['t'] in KEY else 'cap'
        H.append(f'<div id="w{n}" class="{cls}">{FIX.get(w["t"].lower(), w["t"])}</div>')
        T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
              f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
              f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
    SL = {'whoosh-short': .57, 'pop': .72, 'click': .36, 'click-soft': .36, 'typing': 1.8}
    sfx = []
    for k, (n, t, v, *d) in enumerate(sorted(S, key=lambda x: x[1])):
        sfx.append(f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(d[0] if d else SL[n], DUR - t):.3f}" '
                   f'data-track-index="{10 + k % 3}" data-volume="{v:.2f}"></audio>')
    nl = '\n'
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.hk{{position:absolute;left:0;right:0;top:350px;z-index:20;text-align:center}}
.blk{{display:inline-block;background:{DARK};color:#fff;font:400 78px/1.12 Anton;letter-spacing:.05em;padding:12px 40px 24px}}
.pill{{position:relative;display:inline-block;margin-top:-22px;height:70px;border-radius:35px;background:#fff;padding:0 32px;
  font:italic 800 44px/70px Poppins;letter-spacing:-.04em;color:{DARK};white-space:nowrap}}
.gh{{visibility:hidden}} #tx{{position:absolute;left:32px;top:0}}
.cd{{position:absolute;left:440px;top:1500px;width:200px;height:200px;z-index:22;border-radius:50%;background:{DARK};color:#fff;
  font:400 130px/206px Anton;text-align:center;box-shadow:0 0 0 8px #fff,0 18px 40px rgba(0,0,0,.3)}}
.flag{{position:absolute;top:1170px;z-index:22;padding:8px;background:#fff;border-radius:12px;box-shadow:0 12px 28px rgba(0,0,0,.3);line-height:0}}
.sw{{position:absolute;left:190px;width:700px;top:345px;z-index:21;border-radius:44px;background:rgba(0,0,0,.88);padding:22px 34px 26px;
  box-shadow:0 20px 50px rgba(0,0,0,.35);text-align:center}}
.dig{{font:500 128px/1 Inter;color:#fff;letter-spacing:-.02em;font-variant-numeric:tabular-nums}}
.btns{{display:flex;align-items:center;justify-content:space-between;margin-top:18px}}
.b{{width:116px;height:116px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:600 24px/1 Inter;
  box-shadow:0 0 0 4px #000,0 0 0 6px currentColor}}
.tour{{background:#3a3a3c;color:#fff}}
.go{{background:#0d3b1a;color:#34C759}} .stop{{background:#4a1310;color:#FF453A}}
.lap{{font:500 32px/1 Inter;color:#8e8e93}}
.ls{{position:absolute;left:0;right:0;top:618px;z-index:23;text-align:center}}
.ls .n{{display:inline-block;width:62px;height:62px;border-radius:50%;background:{DARK};color:#fff;font:400 38px/62px Anton;vertical-align:middle;margin-right:-14px;position:relative;z-index:2;box-shadow:0 0 0 4px #fff}}
.ls .lt{{display:inline-block;vertical-align:middle;background:#fff;color:{DARK};font:italic 800 40px/1.25 Poppins;letter-spacing:-.04em;padding:8px 30px 10px 34px;border-radius:40px;
  white-space:nowrap;box-shadow:0 6px 16px rgba(0,0,0,.2)}}
.wt{{position:absolute;transform-style:preserve-3d;width:230px;z-index:23;border-radius:6px;overflow:hidden;box-shadow:0 24px 40px rgba(0,0,0,.38),0 6px 12px rgba(0,0,0,.25);line-height:0}}
.wt::after{{content:'';position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.28),rgba(255,255,255,0) 42%,rgba(0,0,0,.14))}}
.wt img{{width:100%;display:block}}
#subj{{z-index:24}}
.cb{{position:absolute;left:130px;width:820px;top:380px;z-index:30;height:118px;border-radius:59px;background:#fff;display:flex;align-items:center;gap:20px;
  padding:0 18px;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.cav{{width:80px;height:80px;border-radius:50%;object-fit:cover;flex:none;border:3px solid {DARK}}}
.cw{{flex:1;display:flex;align-items:center;min-width:0}}
.cph{{font:500 36px/1 Poppins;color:#9A9087}}
.cty{{font:400 66px/1 Anton;letter-spacing:.06em;color:#2A1A10}}
.ccr{{width:4px;height:56px;background:{DARK};margin-left:6px}}
.csd{{width:84px;height:84px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center;flex:none}}
.cap{{position:absolute;left:40px;right:40px;top:1400px;z-index:25;text-align:center;font:700 66px/1 Poppins;letter-spacing:-.03em;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.cap.key{{font-size:86px;font-weight:800}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="voice" src="assets/voice.m4a" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(sfx)}
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
  <video id="subj" class="full" src="assets/subject_cta.webm" muted playsinline data-start="41.000" data-media-start="0" data-duration="{DUR - 41.0:.3f}" data-track-index="1"></video>
{nl.join(H)}
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
    print(f'wrote index.html {DUR:.3f}s  go {T_GO:.2f} stop {T_STOP:.2f} -> chrono {T_STOP - T_GO:.2f}s')
