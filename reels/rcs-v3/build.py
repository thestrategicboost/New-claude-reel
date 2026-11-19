#!/usr/bin/env python3
"""« Réels vs carrousels vs stories » — a new kind of edit (v3): a live comparison TABLE in the empty wall above her head.
Fixed header row (three brown blocks RÉELS / CARROUSELS / STORIES), above it a white pill that types the round's question
with her keyboard sound (her signature), under it one white card per column that lands on the word she says.
4 rounds: who sees it (reach gauges), what it brings, what it lets you do, how often to post. CTA: her Instagram comment
bar, CHIRAC types itself. One-word captions (Poppins white, soft shadow, key words bigger). Lilac look + retouch, no zoom.

PY build.py      writes index.html
"""
import json
import re
import subprocess

DUR = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'assets/aroll.mp4'],
                           capture_output=True, text=True).stdout)
SEGS = json.load(open('work/segs.json'))
DARK, GOLD = '#523301', '#C9A15B'


def ct(t):
    out = 0.0
    for a, b in SEGS:
        if a - .05 <= t <= b + .05:
            return out + max(0.0, t - a)
        out += b - a
    return None


# rounds: (raw start, question, [(column, raw time it lands, big text, small text, gauge 0-1 or icon)])
ICON = {
    'follow': '<path d="M15 19c0-2.8-2.7-5-6-5s-6 2.2-6 5M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M19 8v6M16 11h6"/>',
    'save': '<path d="M6 3h12v18l-6-4-6 4z"/>',
    'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    'eye': '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    'book': '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 19V5"/>',
    'cash': '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/>',
}
ROUNDS = [
    (112.05, 'Qui voit ton contenu ?', [
        (0, 113.40, 'TOUT LE MONDE', 'abonnés + non-abonnés', 1.0),
        (1, 122.60, 'TES ABONNÉS', '+ quelques non-abonnés', .55),
        (2, 125.30, 'TES ABONNÉS', 'uniquement', .22)]),
    (129.03, 'Ce que ça génère', [
        (0, 130.30, 'ABONNEMENTS', '', 'follow'),
        (1, 132.40, 'ENREGISTREMENTS', '', 'save'),
        (2, 134.40, 'ENGAGEMENT', '', 'heart')]),
    (138.75, 'Ce que ça te permet', [
        (0, 140.30, 'ÊTRE VISIBLE', '', 'eye'),
        (1, 142.40, 'ÉDUQUER', '', 'book'),
        (2, 144.20, 'VENDRE', '', 'cash')]),
    (152.20, 'Combien de fois publier ?', [
        (0, 153.30, '4 à 7 fois', 'par semaine', None),
        (1, 155.30, '1 à 2 fois', 'par semaine (ou pas)', None),
        (2, 158.00, '1 à 2 fois', 'par jour', None)]),
]
NAMES = [(112.60, 0), (121.30, 1), (124.50, 2), (129.30, 0), (131.20, 1), (133.50, 2), (139.20, 0), (141.30, 1), (143.30, 2),
         (152.64, 0), (154.90, 1), (157.60, 2)]                  # raw times she names a column -> it pops
T_TRIAL = 116.70                                                  # « l'option réels d'essai »
T_MONEY = 144.66
T_CTA, T_CHIRAC = 160.30, 160.84
COLX = [130, 410, 690]
# captions
RAW = [w for w in json.load(open('work/words.json')) if not (149 < w['s'] < 154.3)]
RAW += [{'w': w, 's': s, 'e': e} for w, s, e in [('pour', 152.20, 152.46), ('les', 152.48, 152.62), ('réels', 152.64, 152.82),
                                                  ('publie', 152.84, 153.25), ('4', 153.30, 153.30), ('à', 153.30, 153.42),
                                                  ('7', 153.44, 153.6), ('fois', 153.62, 153.72), ('par', 153.74, 153.9),
                                                  ('semaine', 153.92, 154.2)]]
RAW.sort(key=lambda w: w['s'])
FIX = {'carousels': 'carrousels', 'dc': 'd’essai', 'binger': 'banger', 'chirac': 'CHIRAC', 'tchuss': 'tchus', "n'oublie": 'n’oublie',
       "d'utiliser": 'd’utiliser', "l'option": 'l’option', "c'est": 'c’est', "l'enregistrement": 'l’enregistrement',
       "l'engagement": 'l’engagement', "d'être": 'd’être', "d'éduquer": 'd’éduquer'}
KEY = {'réels', 'carrousels', 'stories', 'non-abonnés', 'abonnements', 'l’enregistrement', 'l’engagement', 'visible', 'd’éduquer',
       'vendre', 'money', 'CHIRAC', 'banger'}


def build():
    H, T, S = [], [], []
    # question pill (typed) + header row + cards
    H.append('<div id="qp" class="qp"><span id="qgh" class="gh"></span><span id="qtx"></span></div>')
    T += ["gsap.set('#qp',{autoAlpha:0});"]
    for k, n in enumerate(['RÉELS', 'CARROUSELS', 'STORIES']):
        H.append(f'<div id="h{k}" class="hd" style="left:{COLX[k]}px">{n}<i id="u{k}"></i></div>')
        T += [f"gsap.set('#h{k}',{{autoAlpha:0}});", f"gsap.set('#u{k}',{{scaleX:0}});"]
    t0 = ct(ROUNDS[0][0])
    T += [f"tl.fromTo('#h{k}',{{autoAlpha:0,y:-20}},{{autoAlpha:1,y:0,duration:.25,ease:'back.out(2)',immediateRender:false}},{t0 + .05 * k:.3f});"
          for k in range(3)]
    for r, (rs, q, cells) in enumerate(ROUNDS):
        a = ct(rs)
        b = ct(ROUNDS[r + 1][0]) if r + 1 < len(ROUNDS) else ct(T_CTA) - .05
        # the question types itself (keyboard sound)
        T += [f"tl.set('#qp',{{autoAlpha:1}},{a:.3f});", f"tl.set('#qgh',{{textContent:{json.dumps(q)}}},{a:.3f});",
              f"tl.set('#qtx',{{textContent:''}},{a:.3f});"]
        T += [f"tl.set('#qtx',{{textContent:{json.dumps(q[:i])}}},{a + .05 + .6 * i / len(q):.3f});" for i in range(1, len(q) + 1)]
        S.append(('typing', a + .05, .5, .65))
        for col, tl_, big, small, extra in cells:
            cid = f'c{r}{col}'
            inner = f'<b>{big}</b>'
            if isinstance(extra, float):
                inner += f'<span>{small}</span><div class="g"><i id="g{cid}"></i></div>'
            elif isinstance(extra, str):
                inner = (f'<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="{DARK}" stroke-width="2.2" '
                         f'stroke-linecap="round" stroke-linejoin="round">{ICON[extra]}</svg>') + inner
            elif small:
                inner += f'<span>{small}</span>'
            fs = 25 if len(big) > 13 else 29 if len(big) > 10 else 36
            H.append(f'<div id="{cid}" class="cd" style="left:{COLX[col]}px;font-size:{fs}px">{inner}</div>')
            t = ct(tl_)
            T += [f"gsap.set('#{cid}',{{autoAlpha:0}});",
                  f"tl.fromTo('#{cid}',{{autoAlpha:0,y:-24,scale:.85}},{{autoAlpha:1,y:0,scale:1,duration:.26,ease:'back.out(2)',immediateRender:false}},{t:.3f});",
                  f"tl.to('#{cid}',{{autoAlpha:0,duration:.15}},{b - .15:.3f});", f"tl.set('#{cid}',{{autoAlpha:0}},{b:.3f});"]
            if isinstance(extra, float):
                T += [f"gsap.set('#g{cid}',{{width:'0%'}});",
                      f"tl.to('#g{cid}',{{width:'{extra * 100:.0f}%',duration:.6,ease:'power2.out'}},{t + .15:.3f});"]
            S.append(('click-soft', t, .28, .36))
    # the column she names pops, gold underline
    for raw, k in NAMES:
        t = ct(raw)
        T += [f"tl.fromTo('#h{k}',{{scale:1}},{{scale:1.1,duration:.12,yoyo:true,repeat:1,immediateRender:false}},{t:.3f});",
              f"tl.to('#u{k}',{{scaleX:1,duration:.2}},{t:.3f});", f"tl.to('#u{k}',{{scaleX:0,duration:.2}},{t + 1.4:.3f});"]
    # réels d'essai tag under the réels card
    H.append('<div id="trial" class="tag">+ option réels d’essai</div>')
    tt = ct(T_TRIAL)
    T += ["gsap.set('#trial',{autoAlpha:0});",
          f"tl.fromTo('#trial',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.22,ease:'back.out(2.4)',immediateRender:false}},{tt:.3f});",
          f"tl.to('#trial',{{autoAlpha:0,duration:.15}},{ct(121.2):.3f});"]
    # money money money: the VENDRE card shakes
    tm = ct(T_MONEY)
    T.append(f"tl.to('#c22',{{rotation:4,duration:.08,yoyo:true,repeat:9,ease:'sine.inOut'}},{tm:.3f});")
    # table leaves before the CTA
    tc = ct(T_CTA)
    T += [f"tl.to(['#qp','#h0','#h1','#h2'],{{autoAlpha:0,duration:.2}},{tc - .25:.3f});"]
    # CTA: her comment bar, CHIRAC types itself, send tapped
    send = ('<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" '
            'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    H.append(f'<div id="cb" class="cb"><img class="cav" src="assets/avatar.png"/><div class="cw"><span id="cph" class="cph">Ajouter un commentaire…</span>'
             f'<span id="cty" class="cty"></span><i class="ccr"></i></div><div id="csd" class="csd">{send}</div></div>')
    H.append('<div id="kit" class="kit">pour recevoir mon kit du créateur</div>')
    word, tw = 'CHIRAC', ct(T_CHIRAC)
    T += ["gsap.set(['#cb','#kit'],{autoAlpha:0});", "gsap.set('#cty',{textContent:''});",
          f"tl.fromTo('#cb',{{autoAlpha:0,y:-40,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:false}},{tc:.3f});",
          f"tl.set('#cph',{{display:'none'}},{tw:.3f});"]
    T += [f"tl.set('#cty',{{textContent:{json.dumps(word[:q])}}},{tw + (q - 1) * .06:.3f});" for q in range(1, len(word) + 1)]
    ts = tw + len(word) * .06 + .15
    T += [f"tl.to('#csd',{{scale:.78,duration:.07,yoyo:true,repeat:1}},{ts:.3f});",
          f"tl.fromTo('#kit',{{autoAlpha:0,y:10}},{{autoAlpha:1,y:0,duration:.2,immediateRender:false}},{ts + .1:.3f});"]
    S += [('click', ts, .45, .36)]
    # one-word captions
    ws = []
    for w in RAW:
        t = w['w'].strip()
        if (t.startswith("'") or t.startswith('-')) and ws:
            ws[-1]['t'] += t
            ws[-1]['e'] = w['e']
            continue
        k = re.sub(r'[,.!?…]', '', t).lower()
        s = ct(w['s'])
        if k and s is not None:
            ws.append({'t': k, 's': s, 'e': ct(min(w['e'], w['s'] + 1.0)) or s + .3})
    for n, w in enumerate(ws):
        txt = FIX.get(w['t'], w['t'])
        if w['s'] >= tw - .05 and txt == 'CHIRAC':
            continue
        nxt = ws[n + 1]['s'] if n + 1 < len(ws) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        if end - w['s'] < .05:
            continue
        H.append(f'<div id="w{n}" class="{"cap key" if txt in KEY else "cap"}">{txt}</div>')
        T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
              f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
              f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
    sfx = [f'<audio id="s{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(d, DUR - t):.3f}" data-track-index="{10 + k % 3}" '
           f'data-volume="{v}"></audio>' for k, (n, t, v, d) in enumerate(sorted(S, key=lambda x: x[1]))]
    nl = '\n'
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.qp{{position:absolute;left:50%;top:345px;transform:translateX(-50%);z-index:20;height:66px;border-radius:33px;background:#fff;padding:0 30px;
  font:italic 800 40px/66px Poppins;letter-spacing:-.04em;color:{DARK};white-space:nowrap;box-shadow:0 8px 20px rgba(0,0,0,.15)}}
.gh{{visibility:hidden}} #qtx{{position:absolute;left:30px;top:0}}
.hd{{position:absolute;top:428px;width:260px;height:64px;z-index:20;background:{DARK};color:#fff;font:400 40px/68px Anton;letter-spacing:.05em;text-align:center}}
.hd i{{position:absolute;left:18px;right:18px;bottom:-9px;height:6px;border-radius:3px;background:{GOLD};transform-origin:50% 50%}}
.cd{{position:absolute;top:508px;width:260px;height:124px;z-index:20;background:#fff;border-radius:22px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:4px;color:{DARK};text-align:center;box-shadow:0 10px 24px rgba(0,0,0,.18);padding:0 10px}}
.cd b{{font:italic 800 1em/1.05 Poppins;letter-spacing:-.04em}}
.cd span{{font:600 23px/1.12 Poppins;color:#7a6a5c}}
.g{{width:190px;height:12px;border-radius:6px;background:#EFE6DC;overflow:hidden;margin-top:4px}} .g i{{display:block;height:100%;background:{DARK};border-radius:6px}}
.tag{{position:absolute;left:{COLX[0] + 20}px;top:616px;z-index:21;background:{GOLD};color:#fff;font:700 22px/1 Poppins;padding:9px 16px;border-radius:20px;
  box-shadow:0 6px 14px rgba(0,0,0,.2)}}
.cb{{position:absolute;left:130px;width:820px;top:380px;z-index:30;height:118px;border-radius:59px;background:#fff;display:flex;align-items:center;gap:20px;
  padding:0 18px;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.cav{{width:80px;height:80px;border-radius:50%;object-fit:cover;flex:none;border:3px solid {DARK}}}
.cw{{flex:1;display:flex;align-items:center;min-width:0}} .cph{{font:500 36px/1 Poppins;color:#9A9087}}
.cty{{font:400 66px/1 Anton;letter-spacing:.06em;color:#2A1A10}} .ccr{{width:4px;height:56px;background:{DARK};margin-left:6px}}
.csd{{width:84px;height:84px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center;flex:none}}
.kit{{position:absolute;left:0;right:0;top:518px;z-index:30;text-align:center;font:italic 800 38px/1 Poppins;letter-spacing:-.04em;color:#fff;
  text-shadow:0 3px 3px rgba(0,0,0,.3),0 6px 16px rgba(0,0,0,.35)}}
.cap{{position:absolute;left:40px;right:40px;top:1330px;z-index:25;text-align:center;font:700 64px/1 Poppins;letter-spacing:-.03em;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.cap.key{{font-size:84px;font-weight:800}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="voice" src="assets/voice.m4a" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(sfx)}
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(H)}
</div>
<script>const tl = gsap.timeline({{ paused: true }});
{nl.join(T)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;</script></body></html>
'''


if __name__ == '__main__':
    open('index.html', 'w', encoding='utf-8').write(build())
    print(f'wrote index.html {DUR:.2f}s')
