#!/usr/bin/env python3
"""Reel "réels vs carrousels vs stories", edited after the "Reels get followers, carousels get engagement" inspiration:
a fixed row of the three Instagram formats on top (Réels / Carrousel / Story) where the one she talks about lights
up in gold, and under it one card per clause: a small lead line that builds word by word, the key word landing huge
(Anton, gold) on its spoken word, sometimes a small line under it. Lilac look, alternate punch-ins hide the jump cuts.

PY build.py    writes index.html
"""
import json
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
SEGS = json.load(open('work/segs.json'))
PILL = 'linear-gradient(135deg,#F3DFB2 0%,#D6AE66 50%,#A97A3E 100%)'
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
    (124.14, 'story', 'et les stories uniquement à', 'TES ABONNÉS', 125.30, '', 0),
    (129.10, 'reels', 'les réels génèrent des', 'ABONNEMENTS', 129.86, '', 0),
    (131.08, 'carrousel', "les carrousels génèrent de l'", 'ENREGISTREMENT', 132.26, '', 0),
    (132.98, 'story', "et les stories de l'", 'ENGAGEMENT', 134.22, '', 0),
    (138.82, 'reels', "les réels te permettent d'être", 'VISIBLE', 140.34, '', 0),
    (141.12, 'carrousel', "les carrousels te permettent d'", 'ÉDUQUER', 142.18, '', 0),
    (143.08, 'story', 'et les stories te permettent de', 'VENDRE', 144.00, '', 0),
    (144.64, 'story', '', 'MONEY, MONEY, MONEY !', 144.64, '', 0),
    (150.36, 'reels', 'pour les réels, publie', '4 À 7 FOIS', 151.44, 'par semaine', 153.74),
    (154.56, 'carrousel', 'pour les carrousels', '1 À 2 FOIS', 155.26, 'par semaine', 155.74),
    (156.18, 'carrousel', 'ou alors', 'PAS DU TOUT', 156.60, '', 0),
    (157.34, 'story', 'et les stories', '1 À 2 FOIS', 158.06, 'par jour', 158.44),
    (160.30, None, 'commente', 'CHIRAC', 160.84, 'pour avoir mon kit du créateur au complet', 161.10),
]

ICONS = {
    'reels': '<svg viewBox="0 0 48 48"><rect x="5" y="5" width="38" height="38" rx="11"/><path d="M5 16h38M17 5l6 11M29 5l6 11"/>'
             '<path d="M20 22.5v12l10-6z" class="f"/></svg>',
    'carrousel': '<svg viewBox="0 0 48 48"><rect x="12" y="7" width="24" height="34" rx="4"/><path d="M7 12v24M41 12v24"/></svg>',
    'story': '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="18" stroke-dasharray="6 4.5"/><circle cx="24" cy="24" r="11"/></svg>',
}
NAMES = {'reels': 'RÉELS', 'carrousel': 'CARROUSEL', 'story': 'STORY'}


def scenes():
    H, T, S = [], [], []
    # format row: the active one in gold, the others white and dimmed
    H.append('<div id="row" class="row">' + ''.join(
        f'<div id="ic-{k}" class="ic"><div class="ig">{ICONS[k]}</div><span>{NAMES[k]}</span></div>' for k in ICONS) + '</div>')
    T += ["gsap.set('.ic',{opacity:.55,scale:.9,color:'#FFFFFF'});"]
    last = None
    for i, (t, fmt, *_rest) in enumerate(CARDS):
        if fmt == last:
            continue
        a = ct(t) - .04
        for k in ICONS:
            on = k == fmt
            col = '#EBCB8B' if on else '#FFFFFF'
            T.append(f"tl.to('#ic-{k}',{{opacity:{1 if on else .55},scale:{1.12 if on else .9},color:'{col}',duration:.18,ease:'power2.out'}},{a:.3f});")
        last = fmt
    T += [f"tl.to('#row',{{autoAlpha:0,y:-30,duration:.25}},{ct(160.30) - .1:.3f});"]

    # one card per clause
    for i, (t, fmt, lead, big, tb, small, ts) in enumerate(CARDS):
        a = ct(t)
        b = ct(CARDS[i + 1][0]) - .02 if i + 1 < len(CARDS) else DUR + .1
        words = lead.split()
        spans = ''.join(f'<span id="c{i}w{j}">{w}</span> ' for j, w in enumerate(words))
        H.append(f'<div id="c{i}" class="card"><div class="ld">{spans}</div><div id="c{i}b" class="big{' s' if len(big) > 14 else ''}">{big}</div>'
                 + (f'<div id="c{i}s" class="sm">{small}</div>' if small else '') + '</div>')
        T += [f"gsap.set('#c{i}',{{autoAlpha:0}});", f"tl.set('#c{i}',{{autoAlpha:1}},{a:.3f});", f"tl.set('#c{i}',{{autoAlpha:0}},{b:.3f});"]
        tb_ = max(a, ct(tb))
        step = (tb_ - a) / max(1, len(words))
        for j in range(len(words)):
            T += [f"gsap.set('#c{i}w{j}',{{opacity:0}});", f"tl.set('#c{i}w{j}',{{opacity:1}},{a + j * step:.3f});"]
        T += [f"gsap.set('#c{i}b',{{autoAlpha:0}});",
              f"tl.fromTo('#c{i}b',{{autoAlpha:0,scale:1.35,y:10}},{{autoAlpha:1,scale:1,y:0,duration:.16,ease:'back.out(2.2)',immediateRender:false}},{tb_:.3f});"]
        if small:
            T += [f"gsap.set('#c{i}s',{{autoAlpha:0}});",
                  f"tl.fromTo('#c{i}s',{{autoAlpha:0,y:12}},{{autoAlpha:1,y:0,duration:.18,ease:'power2.out',immediateRender:false}},{max(tb_ + .1, ct(ts)):.3f});"]

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
.row{{position:absolute;left:150px;right:150px;top:{TOP}px;z-index:20;display:flex;justify-content:space-between}}
.ic{{width:200px;text-align:center;transform-origin:50% 40%}}
.ig{{width:96px;height:96px;margin:0 auto;filter:drop-shadow(0 4px 10px rgba(0,0,0,.35))}}
.ic{{color:#fff}}
.ig svg{{width:100%;height:100%;fill:none;stroke:currentColor;stroke-width:3.4;stroke-linecap:round;stroke-linejoin:round}}
.ig svg .f{{fill:currentColor;stroke:none}}
.ic span{{display:block;margin-top:8px;font:800 28px/1 Poppins;letter-spacing:.06em;color:inherit;text-shadow:0 2px 6px rgba(0,0,0,.45)}}
.card{{position:absolute;left:60px;right:60px;top:1250px;z-index:25;text-align:center}}
.ld{{font:700 42px/1.2 Poppins;color:#fff;text-shadow:0 3px 0 rgba(0,0,0,.55),0 0 16px rgba(0,0,0,.35)}}
.big{{display:inline-block;margin-top:4px;font:400 124px/1 Anton;letter-spacing:.01em;background:{PILL};-webkit-background-clip:text;
  background-clip:text;color:transparent;filter:drop-shadow(0 5px 0 rgba(60,30,5,.75)) drop-shadow(0 0 18px rgba(0,0,0,.3));white-space:nowrap}}
.big.s{{font-size:96px}}
.sm{{margin-top:6px;font:italic 600 36px/1.2 Poppins;color:#fff;text-shadow:0 3px 0 rgba(0,0,0,.55)}}
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
