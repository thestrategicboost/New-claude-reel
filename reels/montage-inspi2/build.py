#!/usr/bin/env python3
"""Reel "réels vs carrousels vs stories", edited after the "Reels get followers, carousels get engagement" inspiration:
a fixed row of the inspiration's three icons on top (Reels / carousel / Story, "vs" between them), the one she names
popping on the word itself, and under it one card per clause in her caption style (Poppins white, black shadow): a
small lead line that builds word by word, the key word landing huge on its spoken word, sometimes a small line under it. Lilac look, alternate punch-ins hide the jump cuts.

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
SEGS = json.load(open('work/segs.json'))
TOP = 250


def ct(t):
    """raw time -> edit time"""
    out = 0.0
    for a, b in SEGS:
        if t >= b:
            out += b - a
        else:
            return out + max(0.0, t - a)
    return out


# (raw start of the card, active format, lead line, big word, raw time the big word is said, small line, its raw time)
CARDS = [
    (112.12, 'reels', 'les réels sont montrés à', 'TES ABONNÉS', 113.28, '', 0),
    (114.04, 'reels', 'mais surtout à tes', 'NON-ABONNÉS', 114.68, '', 0),
    (115.44, 'reels', "n'oublie pas l'option", "RÉEL D'ESSAI", 116.72, "c'est un banger", 117.54),
    (118.48, 'reels', 'pour pousser tes réels vers des', 'NON-ABONNÉS', 120.30, '', 0),
    (121.16, 'carrousel', 'les carrousels sont montrés à', 'TES ABONNÉS', 122.42, '+ quelques non-abonnés', 123.18),
    (124.14, 'story', 'et les stories uniquement à', 'TES ABONNÉS', 125.42, '', 0),
    (129.10, 'reels', 'les réels génèrent des', 'ABONNEMENTS', 130.30, '', 0),
    (131.08, 'carrousel', "les carrousels génèrent de l'", 'ENREGISTREMENT', 132.26, '', 0),
    (132.98, 'story', "et les stories de l'", 'ENGAGEMENT', 134.34, '', 0),
    (138.82, 'reels', "les réels te permettent d'être", 'VISIBLE', 140.34, '', 0),
    (141.12, 'carrousel', "les carrousels te permettent d'", 'ÉDUQUER', 142.18, '', 0),
    (143.08, 'story', 'et les stories te permettent de', 'VENDRE', 144.20, '', 0),
    (144.64, 'story', '', 'MONEY, MONEY, MONEY !', 144.64, '', 0),
    (150.36, 'reels', 'pour les réels, publie', '4 À 7 FOIS', 151.44, 'par semaine', 153.74),
    (154.56, 'carrousel', 'pour les carrousels', '1 À 2 FOIS', 155.26, 'par semaine', 155.74),
    (156.18, 'carrousel', 'ou alors', 'PAS DU TOUT', 156.60, '', 0),
    (157.34, 'story', 'et les stories', '1 À 2 FOIS', 158.06, 'par jour', 158.44),
    (160.30, None, 'commente', 'CHIRAC', 160.84, 'pour avoir mon kit du créateur au complet', 161.10),
]

# the three icons of the inspiration, redrawn as vectors: Instagram's gradient Reels icon, the neon carousel, the
# white Story disc in its gradient ring
IGG = ('<defs><linearGradient id="gr" x1="0" y1="0" x2=".35" y2="1"><stop offset="0" stop-color="#C72A9C"/>'
       '<stop offset=".5" stop-color="#F0335C"/><stop offset="1" stop-color="#FA8F2C"/></linearGradient>'
       '<linearGradient id="gs" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FBB13C"/><stop offset=".45" stop-color="#F2365E"/>'
       '<stop offset="1" stop-color="#9B33C9"/></linearGradient></defs>')
ICONS = {
    'reels': '<svg viewBox="0 0 48 48">' + IGG + '<g fill="none" stroke="url(#gr)" stroke-width="3.8" stroke-linejoin="round" stroke-linecap="round">'
             '<rect x="4.5" y="4.5" width="39" height="39" rx="11"/><path d="M5 16h38M16.5 5l6 11M28.5 5l6 11"/></g>'
             '<path d="M19.5 22.5v13l11-6.5z" fill="#F0353B" stroke="#F0353B" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    'carrousel': '<svg viewBox="0 0 76 48"><g fill="none" stroke-linejoin="miter"><path id="cb" d="M24 6H16V42H24M16 10H9V38H16M52 6H60V42H52M60 10H67V38H60" stroke="#D4FF3A" stroke-width="4.4"/>'
                 '<path d="M24 6H16V42H24M16 10H9V38H16M52 6H60V42H52M60 10H67V38H60" stroke="#fff" stroke-width="1.6"/></g>'
                 '<rect x="25" y="3" width="26" height="42" fill="#fff"/></svg>',
    'story': '<svg viewBox="0 0 48 48">' + IGG + '<circle cx="24" cy="24" r="20.5" fill="none" stroke="url(#gs)" stroke-width="3.2"/>'
             '<circle cx="24" cy="24" r="18" fill="#fff"/></svg>',
}
NAMES = {'reels': 'RÉELS', 'carrousel': 'CARROUSEL', 'story': 'STORY'}


def scenes():
    H, T, S = [], [], []
    # format row: the one she names pops (as in the inspiration), its label at full white
    H.append('<div id="row" class="row">' + ''.join(
        ('<b class="vs">vs</b>' if j else '') + f'<div id="ic-{k}" class="ic"><div class="ig">{ICONS[k]}</div><span>{NAMES[k]}</span></div>'
        for j, k in enumerate(ICONS)) + '</div>')
    T += ["gsap.set('.ic',{scale:1});", "gsap.set('.ic span',{opacity:.6});"]
    raw = json.load(open('work/take3_words.json'))
    key = {'reels': 'réel', 'carrousel': 'carousel', 'story': 'stor'}
    last = None
    for i, (t, fmt, *_rest) in enumerate(CARDS):
        if fmt is None or fmt == last:
            continue
        hit = next((w['s'] for w in raw if w['s'] >= t - .05 and key[fmt] in w['w'].lower()), t)
        a = ct(hit)
        for k in ICONS:
            if k == fmt:      # one frame squeezed, then pops a bit bigger and settles
                T += [f"tl.set('#ic-{k}',{{scale:.86}},{a:.3f});",
                      f"tl.to('#ic-{k}',{{scale:1.3,duration:.08,ease:'power2.out'}},{a + .034:.3f});",
                      f"tl.to('#ic-{k}',{{scale:1.22,duration:.2,ease:'power1.out'}},{a + .12:.3f});",
                      f"tl.set('#ic-{k} span',{{opacity:1}},{a + .034:.3f});"]
                S.append(('pop', a, .5))
            elif k == last:
                T += [f"tl.to('#ic-{k}',{{scale:1,duration:.12,ease:'power2.out'}},{a:.3f});",
                      f"tl.set('#ic-{k} span',{{opacity:.6}},{a:.3f});"]
        last = fmt
    T += [f"tl.to('#row',{{autoAlpha:0,y:-30,duration:.25}},{ct(160.30) - .1:.3f});"]

    # captions: her usual one word at a time (Poppins white, black shadow, lowercase); the key words of each clause
    # land together, huge, and stay until the next clause; the words said after them show one at a time under them
    raw = []
    for w in json.load(open('work/take3_words.json')):
        t = w['w'].strip()
        if (t.startswith("'") or t.startswith('-')) and raw:
            raw[-1]['w'] += t
            raw[-1]['e'] = w['e']
        else:
            raw.append(dict(w, w=t))
    n = 0
    for i, (t, fmt, lead, big, tb, small, ts) in enumerate(CARDS):
        t_next = CARDS[i + 1][0] if i + 1 < len(CARDS) else 1e9
        ws = [w for w in raw if t - .05 <= w['s'] < t_next - .05]
        kb = next(k for k, w in enumerate(ws) if w['s'] >= tb - .05)
        nb = len(big.replace(',', '').replace('!', '').split())
        card_end = ct(t_next) - .02 if i + 1 < len(CARDS) else DUR + .1
        a_big = ct(ws[kb]['s'])
        if fmt is None:
            # the CTA as an Instagram comment bar above her head: it slides in on "commente", CHIRAC types itself on the
            # word, the send button is tapped, the bar pulses
            send = ('<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" '
                    'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
            H.append(f'<div id="cb" class="cb"><img class="cav" src="assets/avatar.png"/><div class="cw"><span id="cph" class="cph">Ajouter un commentaire…</span>'
                     f'<span id="cty" class="cty"></span><i id="ccr" class="ccr"></i></div><div id="csd" class="csd">{send}</div></div>')
            a_in = ct(t)
            T += ["gsap.set('#cb',{autoAlpha:0});",
                  f"tl.fromTo('#cb',{{autoAlpha:0,y:-50,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:false}},{a_in:.3f});",
                  "gsap.set('#cty',{textContent:''});", "gsap.set('#cph',{display:'inline'});",
                  f"tl.set('#cty',{{textContent:''}},{a_in:.3f});", f"tl.set('#cph',{{display:'inline'}},{a_in:.3f});",
                  f"tl.set('#cph',{{display:'none'}},{a_big:.3f});"]
            T += [f"tl.set('#cty',{{textContent:{json.dumps(big[:q])}}},{a_big + (q - 1) * .07:.3f});" for q in range(1, len(big) + 1)]
            ts_ = a_big + len(big) * .07 + .15
            T += ["gsap.set('#ccr',{opacity:1});"] + [f"tl.set('#ccr',{{opacity:{q % 2}}},{a_in + .3 + q * .25:.3f});" for q in range(int((DUR - a_in) / .25))]
            T += [f"tl.to('#csd',{{scale:.78,duration:.07,yoyo:true,repeat:1}},{ts_:.3f});",
                  f"tl.to('#cb',{{boxShadow:'0 0 0 7px #573307, 0 16px 36px rgba(0,0,0,.3)',scale:1.05,duration:.18,yoyo:true,repeat:1}},{ts_ + .1:.3f});"]
            S += [('pop', a_in, .45), ('click', ts_, .6)]
            singles = [(w, False) for w in ws[:kb]] + [(w, False) for w in ws[kb + nb:]]
        else:
            H.append(f'<div id="b{i}" class="big{" s" if len(big) > 14 else ""}">{big}</div>')
            T += [f"gsap.set('#b{i}',{{autoAlpha:0}});",
                  f"tl.fromTo('#b{i}',{{autoAlpha:0,scale:1.35,y:10}},{{autoAlpha:1,scale:1,y:0,duration:.16,ease:'back.out(2.2)',immediateRender:false}},{a_big:.3f});",
                  f"tl.set('#b{i}',{{autoAlpha:0}},{card_end:.3f});"]
            singles = [(w, False) for w in ws[:kb]] + [(w, True) for w in ws[kb + nb:]]
        for k, (w, under) in enumerate(singles):
            txt = re.sub(r'[,.!?…]', '', w['w']).lower().replace('carousel', 'carrousel')
            if not txt:
                continue
            a = ct(w['s'])
            nxt = singles[k + 1][0]['s'] if k + 1 < len(singles) and singles[k + 1][1] == under else None
            end = ct(nxt) if nxt is not None and nxt - w['e'] < .5 else ct(w['e']) + .3
            end = min(end, a_big if w['s'] < ws[kb]['s'] else card_end, card_end)
            if end <= a:
                continue
            H.append(f'<div id="w{n}" class="cap{" un" if under else ""}">{txt}</div>')
            T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{a:.3f});",
                  f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - a):.3f},ease:'back.out(2.5)',immediateRender:false}},{a:.3f});",
                  f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
            n += 1

    # alternate punch-ins hide the jump cuts between the kept pieces
    edge = 0.0
    for k, (sa, sb) in enumerate(SEGS):
        T.append(f"tl.set('#cam',{{scale:{1.0 if k % 2 == 0 else 1.14}}},{edge:.3f});")
        edge += sb - sa
    return H, T, S


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 42%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.row{{position:absolute;left:24px;right:24px;top:{TOP}px;z-index:20;display:flex;justify-content:space-between;align-items:flex-start}}
.ic{{width:300px;text-align:center;transform-origin:50% 0%}}
.ig{{height:176px;display:flex;justify-content:center;filter:drop-shadow(0 0 5px rgba(240,255,170,.5)) drop-shadow(0 3px 8px rgba(0,0,0,.25))}}
.ig svg{{height:176px;width:auto}}
.ic span{{display:block;margin-top:10px;font:800 50px/1 Poppins;letter-spacing:.01em;color:#fff;text-shadow:0 3px 0 rgba(0,0,0,.6)}}
.vs{{margin-top:66px;font:800 40px/1 Poppins;color:#fff;text-shadow:0 2px 0 rgba(0,0,0,.6)}}
.cap{{position:absolute;left:40px;right:40px;top:1270px;z-index:25;text-align:center;font:700 66px/1 Poppins;letter-spacing:-.01em;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.cap.un{{top:1370px;font-size:52px}}
.big{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1235px;z-index:26;font:800 108px/1.05 Poppins;color:#fff;white-space:nowrap;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.big.s{{font-size:78px;top:1262px}}
.cb{{position:absolute;left:90px;right:90px;top:470px;z-index:30;height:118px;border-radius:59px;background:#fff;display:flex;align-items:center;gap:20px;
  padding:0 18px 0 18px;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.cav{{width:80px;height:80px;border-radius:50%;object-fit:cover;flex:none;border:3px solid #573307}}
.cw{{flex:1;display:flex;align-items:center;min-width:0}}
.cph{{font:500 36px/1 Poppins;color:#9A9087}}
.cty{{font:400 66px/1 Anton;letter-spacing:.06em;color:#2A1A10}}
.ccr{{width:4px;height:56px;background:#573307;margin-left:6px}}
.csd{{width:84px;height:84px;border-radius:50%;background:#573307;display:flex;align-items:center;justify-content:center;flex:none}}
'''


def build():
    H, T, S = scenes()
    nl = '\n'
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
  <audio id="voice" src="assets/voice.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration=".7" data-track-index="{10 + k % 2}" data-volume="{v:.2f}"></audio>' for k, (n, t, v) in enumerate(S))}
  <div id="cam"><video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video></div>
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
    print(f'wrote index.html {DUR:.3f}s')
