#!/usr/bin/env python3
"""Reel "tofu mofu bofu" (@thestrategicboost.fr), bold look throughout.

Built from the /video-edit template: same machinery (bold words, grade, cut punches, SFX lanes, safe guide),
content rewritten for this French script. Word times are cut times, measured on words.json (medium) and, for the
first two shots, on the ingest transcript (medium dropped the opening words).

PY build.py            writes index.html
PY build.py --safe     same + red Instagram safe-zone guide (snapshots only, never render with it)
"""
import json
import os
import shutil
import subprocess
import sys

SAFE = '--safe' in sys.argv or bool(os.environ.get('SAFE'))
DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=duration', '-of', 'csv=p=0', 'assets/aroll.mp4'],
                           capture_output=True, encoding='utf-8', errors='replace').stdout.strip().split(',')[0])
YEL = '#D8B26E'   # brand gold (Maé: brown, gold or white, never yellow)
with open('segments.json', encoding='utf-8') as _f:
    SEG = {s['id']: s for s in json.load(_f)}
# cut times = exact first frame of each segment, nudged 2ms early so a tl.set lands ON that frame
T = {k: s['frame'] / 30 - .002 if s['frame'] else 0.0 for k, s in SEG.items()}
CUTS = [T[k] for k in sorted(T) if T[k] > 0]

BOLD_F = 'contrast(1.07) saturate(.9) brightness(.97)'

# head top per segment (y in the 1080x1920 frame), from headpos.py when available, else measured by eye
HEAD = {'s01': 400, 's02': 700, 's03': 420, 's04': 480, 's05': 480, 's06': 480, 's07': 480, 's08': 420,
        's09': 480, 's10': 450, 's11': 420, 's12': 450}
if os.path.exists('headpos.json'):
    with open('headpos.json', encoding='utf-8') as _f:
        HEAD.update({k: v for k, v in json.load(_f).items() if k in HEAD})
SIZE = {'xl': 220, 'lg': 180, 'md': 150}


def BT(seg, cls='xl'):
    """top for a behind-head word: baseline ~30% of the x-height below the head top (layout.md)"""
    s = SIZE[cls]
    return C + f'top:{max(225, round(HEAD[seg] - 0.57 * s))}px'


C = 'left:0;right:0;text-align:center;'
# lead-in lines centred below the chin: wide shots (chin ~1000-1120) and punch-ins (chin ~1160-1200)
L1, L2, LP = C + 'top:1200px', C + 'top:1290px', C + 'top:1290px'
Z1, Z2, ZP = C + 'top:1250px', C + 'top:1340px', C + 'top:1330px'
W3 = 'width:330px;text-align:center;top:520px;'   # wide shot: one word above each of the three Maé

GROUPS = [  # (start, end, [(t, text, classes, style)])
    # s01 hook: tofu mofu bofu
    (0.00, T['s02'], [(0.00, 'tofu', 'mds y', 'left:60px;width:320px;text-align:center;top:1150px'),
                      (0.30, 'mofu', 'mds y', 'left:380px;width:320px;text-align:center;top:1150px'),
                      (0.60, 'bofu', 'mds y', 'left:680px;width:300px;text-align:center;top:1150px')]),
    # s02 wide shot, three Maé
    (T['s02'], 2.70, [(1.10, 'il y a', 'sm', C + 'top:290px'), (1.22, '3 types', 'big y', C + 'top:370px'),
                      (1.76, 'de contenus que tu dois publier', 'sm2', C + 'top:600px')]),
    (2.70, T['s03'], [(2.80, 'tofu', 'mdm y', 'left:35px;' + W3), (3.30, 'mofu', 'mdm y', 'left:375px;' + W3),
                      (3.70, 'bofu', 'mdm y', 'left:705px;' + W3)]),
    # s03
    (T['s03'], 5.30, [(4.24, 'premièrement,', 'sm', L1), (4.54, 'dans ta stratégie', 'sm', L2)]),
    (5.30, 6.85, [(5.36, 'tu dois créer du contenu', 'sm2', L1), (6.40, 'tofu', 'xl back y', BT('s03'))]),
    (6.85, T['s04'], [(6.92, 'le', 'sm', L1), (7.10, 'top of funnel', 'mdm y', LP)]),
    # s04 (punch-in)
    (T['s04'], 9.80, [(7.90, 'ça, c’est du contenu', 'sm', Z1), (8.54, 'large', 'xl back y', BT('s04'))]),
    (9.80, 11.71, [(9.86, 'du coup tu vas toucher', 'sm2', C + 'top:1230px'), (10.86, 'beaucoup plus', 'sm', C + 'top:1280px'),
                   (11.44, 'de personnes', 'sm', C + 'top:1365px')]),
    (11.71, T['s05'], [(11.66, 'et avoir plus de', 'sm', Z1), (12.38, 'visibilité.', 'mdm y', ZP)]),
    # s05 the tofu list
    (T['s05'], 14.20, [(12.84, 'les contenus', 'sm', L1), (13.40, 'tofu', 'xl back y', BT('s05')), (13.70, 'qui marchent', 'sm', L2)]),
    (14.20, T['s06'], [(14.74, '1. classement', 'sm3', C + 'top:1130px'), (15.42, '2. notation', 'sm3', C + 'top:1195px'),
                       (16.76, '3. liste', 'sm3', C + 'top:1260px'), (17.18, '4. questions-réponses', 'sm3', C + 'top:1325px'),
                       (18.18, '5. storytelling', 'sm3 y', C + 'top:1390px')]),
    # s06 (punch-in) mofu
    (T['s06'], 20.45, [(19.00, 'après, on a le contenu', 'sm2', Z1), (20.08, 'mofu', 'xl back y', BT('s06'))]),
    (20.45, 21.62, [(20.52, 'ce type de contenu est bien,', 'sm2', Z1)]),
    (21.62, 22.91, [(21.66, 'c’est déjà une base d’abonnés', 'sm2', Z1), (22.64, 'solides', 'mdm y', ZP)]),
    (22.91, 23.80, [(22.84, 'et une bonne', 'sm', Z1), (23.16, 'portée.', 'mdm y', ZP)]),
    (23.80, 25.90, [(23.88, 'tu vas créer un lien', 'sm', Z1), (25.16, 'avec ton audience', 'sm', Z2)]),
    (25.90, T['s07'], [(25.94, 'et aussi asseoir ton', 'sm2', Z1), (26.94, 'autorité', 'lg back y', BT('s06', 'lg'))]),
    # s07
    (T['s07'], 28.55, [(27.52, 'là, le contenu que tu vas faire,', 'sm2', L1)]),
    (28.55, 30.25, [(28.60, 'ça va être du contenu', 'sm', L1), (29.22, 'éducatif', 'lg back y', BT('s07', 'lg')),
                    (29.64, 'approfondi', 'sm', L2)]),
    (30.25, 31.25, [(30.28, 'des tutoriels', 'sm', L1), (30.76, 'pas à pas', 'mdm y', LP)]),
    (31.25, 32.50, [(31.28, 'des vidéos', 'sm', L1), (31.84, 'storytelling', 'mdm y', LP)]),
    (32.50, T['s08'], [(32.58, 'tes réussites,', 'sm', C + 'top:1180px'), (33.38, 'tes échecs,', 'sm', C + 'top:1265px'),
                       (33.98, 'tes expériences personnelles', 'sm2', C + 'top:1360px')]),
    # s08 (punch-in) bofu
    (T['s08'], 36.28, [(35.05, 'et enfin, si tu as', 'sm', Z1), (35.86, 'une forte connexion', 'sm', Z2)]),
    (36.28, 38.10, [(36.32, 'avec ton audience', 'sm', Z1), (37.06, 'et une vraie autorité,', 'sm', Z2)]),
    (38.10, 40.40, [(38.18, 'à ce moment-là, tu vas créer', 'sm2', Z1), (39.96, 'bofu', 'xl back y', BT('s08'))]),
    (40.40, T['s09'], [(40.46, 'le', 'sm', Z1), (40.84, 'bottom of funnel', 'mds y', ZP)]),
    # s09
    (T['s09'], 43.70, [(41.54, 'tu vas venir publier des', 'sm2', L1), (42.48, 'transformations', 'sm', C + 'top:1255px'),
                       (43.02, 'avant-après', 'mdm y', C + 'top:1330px')]),
    (43.70, 46.10, [(43.72, 'que ce soit des transformations', 'sm2', L1), (44.66, 'personnelles', 'sm', C + 'top:1270px'),
                    (45.18, 'ou bien celles de tes', 'sm2', C + 'top:1365px'), (45.74, 'clients', 'xl back y', BT('s09'))]),
    (46.10, T['s10'], [(46.12, 'tu vas aussi faire des', 'sm2', L1), (46.66, 'études de cas', 'sm', C + 'top:1255px'),
                       (47.12, 'fictives', 'mdm y', C + 'top:1330px')]),
    # s10 (punch-in)
    (T['s10'], 49.55, [(47.68, 'par exemple,', 'sm', Z1), (48.14, 'qu’est-ce que je ferais pour', 'sm2', Z2),
                       (49.06, 'une célébrité', 'lg back y', BT('s10', 'lg'))]),
    (49.55, 50.55, [(49.60, 'ou bien pour une grande', 'sm2', Z1), (50.20, 'marque', 'xl back y', BT('s10'))]),
    (50.55, 52.40, [(50.64, 'et tu peux faire des vidéos du type', 'sm2', Z1)]),
    (52.40, T['s11'], [(52.48, '« voici ce que je ferais', 'sm', Z1), (53.04, 'dans telle situation »', 'sm', Z2)]),
    # s11
    (T['s11'], 54.70, [(54.02, 'ton', 'sm', L1), (54.06, 'objectif', 'xl back y', BT('s11'))]),
    (54.70, 56.90, [(54.74, 'va déterminer le type', 'sm', L1), (55.90, 'de contenu que tu vas créer', 'sm2', C + 'top:1300px')]),
    (56.90, 59.20, [(56.92, 'mais dans la majorité des cas', 'sm2', L1), (58.30, 'la plupart des créateurs', 'sm', C + 'top:1280px')]),
    (59.20, T['s12'], [(59.26, 'font un', 'sm', L1), (59.58, 'mix des trois', 'mdm y', LP)]),
    # s12 (punch-in) call to action
    (T['s12'], DUR, [(60.40, 'à toi de jouer !', 'sm', Z1), (61.56, 'abonne-toi', 'md back y', BT('s12', 'md')),
                     (61.80, 'pour plus de conseils', 'sm', Z2)]),
]


def words():
    html, tw = [], []
    for g, (a, b, ws) in enumerate(GROUPS):
        for k, (t, txt, cls, st) in enumerate(ws):
            wid = f'w{g}-{k}'
            html.append(f'<div id="{wid}" class="dw {cls}" style="{st}">{txt}</div>')
            tw.append(f"gsap.set('#{wid}',{{autoAlpha:0}});")
            tw.append(f"tl.fromTo('#{wid}',{{autoAlpha:0,scale:1.22,filter:'blur(22px)'}},{{autoAlpha:1,scale:1,filter:'blur(0px)',"
                      f"duration:.2,ease:'power3.out',immediateRender:false}},{max(a, t - .05):.3f});")
            if b < DUR - .01:
                tw.append(f"tl.to('#{wid}',{{autoAlpha:0,scale:.96,filter:'blur(16px)',duration:.12,ease:'power2.in'}},{b - .12:.3f});")
                tw.append(f"tl.set('#{wid}',{{autoAlpha:0}},{b:.3f});")
    return html, tw


def grades():
    tw = [f"gsap.set('.g',{{filter:'{BOLD_F}'}});"]
    for t in CUTS:
        tw.append(f"tl.fromTo('#stage',{{scale:1.05}},{{scale:1,duration:.32,ease:'power2.out',immediateRender:false}},{t:.3f});")
    return tw


SFX = [('whoosh-short', .02, .22), ('pop', 1.22, .16), ('sparkle', 2.80, .2)]
SFX += [('whoosh-short', t, .2) for t in (T['s05'], T['s06'], T['s08'], T['s11'], T['s12'])]
SFX += [('pop', t, .14) for t in (6.40, 13.40, 20.08, 39.96, 61.56)]
SFX += [('click-soft', t, .35) for t in (14.74, 15.42, 16.76, 17.18, 18.18)]
SFX_LEN = {'whoosh-short': .57, 'pop': .72, 'sparkle': 1.8, 'click': .3, 'click-soft': .37}
SFX_GAIN = 0.75   # sounds sit 25% under the original levels: subtle, never louder than the voice


def audio():
    out, lanes = [], []
    for k, (name, t, vol) in enumerate(sorted(SFX, key=lambda x: x[1])):
        d = min(SFX_LEN[name], DUR - t)
        lane = next((i for i, end in enumerate(lanes) if end <= t), None)
        if lane is None:
            lanes.append(0); lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{name}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{vol * SFX_GAIN:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;inset:0;transform-origin:50% 45%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#bgv{{z-index:0}}
.dw.back{{z-index:3}}
#cutwrap{{position:absolute;inset:0;z-index:4}}
.fx{{position:absolute;inset:0;pointer-events:none}}
#dtone{{z-index:7;background:linear-gradient(180deg,rgba(20,55,75,.16),rgba(60,40,20,.08));mix-blend-mode:soft-light}}
#dvig{{z-index:7;background:radial-gradient(95% 62% at 50% 46%,rgba(0,0,0,0) 55%,rgba(0,0,0,.42) 100%)}}
#dgrad{{z-index:7;background:linear-gradient(180deg,rgba(0,0,0,.34) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 58%,rgba(0,0,0,.30) 100%)}}
.dw{{position:absolute;z-index:8;color:#fff;font-family:'Inter Tight';font-weight:900;letter-spacing:-.05em;line-height:.9;
  text-shadow:0 10px 40px rgba(0,0,0,.55),0 2px 8px rgba(0,0,0,.35);transform-origin:50% 60%;white-space:nowrap}}
.sm{{font-size:84px;font-weight:800;letter-spacing:-.04em}}
.sm2{{font-size:56px;font-weight:800;letter-spacing:-.03em}}
.sm3{{font-size:62px;font-weight:800;letter-spacing:-.03em}}
.mds{{font-size:110px}}
.mdm{{font-size:130px}}
.md{{font-size:150px}}
.lg{{font-size:180px}}
.big{{font-size:236px}}
.xl{{font-size:220px}}
.y{{color:{YEL}}}
'''

SAFE_GUIDE = ('<div style="position:absolute;inset:0;z-index:99;pointer-events:none">'
              '<div style="position:absolute;left:0;right:0;top:0;height:220px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;right:0;top:1470px;bottom:0;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;width:35px;top:220px;height:1250px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:35px;top:220px;height:935px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:100px;top:1155px;height:315px;background:rgba(255,0,0,.28)"></div></div>')


def build():
    w_html, w_tw = words()
    back = [h for h in w_html if 'back' in h.split('class="')[1].split('"')[0]]
    front = [h for h in w_html if h not in back]
    tweens = grades() + w_tw
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
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(audio())}
  <div id="stage">
    <video id="bgv" class="full g" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(back)}
    <div id="cutwrap"><video id="cut" class="full g" src="assets/subject.webm" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="1"></video></div>
  </div>
  <div id="dtone" class="fx"></div><div id="dvig" class="fx"></div><div id="dgrad" class="fx"></div>
{nl.join(front)}
{SAFE_GUIDE if SAFE else ''}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tweens)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s  cuts {[round(c, 3) for c in CUTS]}')
