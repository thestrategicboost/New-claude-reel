#!/usr/bin/env python3
"""Reel "vues-classement": live ranking of 6 Instagram tips on a 100 / 10K / 100K VUES scale.

Edit idea from the reel Maé sent (a scale at the top, a handwritten title per tip, an icon that pops beside her and
flies into the column it earns, short capital captions), dressed in HER branding: Anton white capitals, gold gradient,
Poppins captions (white, key ones gold), Caveat for the handwritten title. No yellow.

PY build.py            writes index.html
PY build.py --safe     same + red Instagram safe-zone guide (snapshots only)
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
with open('segments.json', encoding='utf-8') as _f:
    SEG = {s['id']: s['frame'] / 30 for s in json.load(_f)}
GOLD = '#D8B26E'
GRAD = 'linear-gradient(135deg,#9C7232 0%,#D2AE66 45%,#EBD39A 60%,#B4873F 100%)'

COLS = [('100', 200), ('10K', 540), ('100K', 880)]   # label, centre x
NUM_TOP, SLOT_Y, SLOT, BIG = 282, 432, 100, 190     # board layout; icon size in its slot / when it pops
POP_X, POP_Y = 900, 760                              # where an icon first appears (on the wall, right of her head)

# tips: (title, title in, icon, icon in, rating time, column)
TIPS = [
    ('Poster à une heure précise', 0.00, 'clock', 0.10, 2.26, 0),
    ('Vidéos courtes (5s)', SEG['t2'], 'short', 2.90, 5.22, 2),
    ('Vidéos éducatives longues', SEG['t3'], 'long', 10.64, 12.38, 1),
    ('Reprendre des reels viraux', SEG['t4'], 'viral', 13.24, 15.06, 2),
    ('Audio tendance', SEG['t5'], 'music', 18.46, 20.26, 0),
    ('Ajouter ManyChat', SEG['t6'], 'dm', 23.88, 26.00, 2),
    ('Commente AVOCADO', SEG['cta'], None, None, None, None),
]

# captions: (time, text); a leading * makes the chunk gold
CAPS = [(0.00, 'POSTER À UNE'), (0.80, 'HEURE PRÉCISE'), (2.26, '*100 VUES'),
        (2.90, 'VIDÉO COURTE'), (3.50, 'DE 5 SECONDES'), (5.22, '*100 000 VUES'), (5.92, 'À CONDITION'), (6.56, 'D’AVOIR UN'),
        (7.08, '*HOOK TEXTUEL'), (7.92, 'BANGER'), (8.48, 'ET DE REDIRIGER'), (9.40, 'DIRECTEMENT'), (9.84, 'EN LÉGENDE'),
        (10.64, 'VIDÉO ÉDUCATIVE'), (11.60, 'LONGUE'), (12.38, '*10 000 VUES'),
        (13.24, 'REPRENDRE DES'), (13.88, 'REELS VIRAUX'), (15.06, '*100 000 VUES'), (16.02, 'OF COURSE'), (16.58, 'TU REPRENDS'),
        (17.22, 'QUELQUE CHOSE'), (17.52, 'QUI MARCHE DÉJÀ'),
        (18.46, 'AUDIO TENDANCE'), (19.76, 'FRANCHEMENT'), (20.26, '*100 VUES'), (20.74, 'ON PEUT S’EN PASSER'),
        (21.34, 'EN FAIT C’EST JUSTE'), (21.80, 'QU’IL FAUT QUE'), (22.08, 'LA MUSIQUE COLLE'), (22.80, 'AVEC CE QUE'),
        (23.22, 'TU MONTRES'),
        (23.88, 'AJOUTEZ MANYCHAT'), (25.38, 'ÇA C’EST'), (26.00, '*100 000 VUES'), (26.86, 'C’EST JUSTE UN'),
        (27.54, '*NON NÉGOCIABLE'), (28.28, 'POUR ENVOYER'), (28.84, 'TOUTES TES RESSOURCES'), (29.38, 'GRATUITES'),
        (30.12, 'ET COMMENTE'), (30.72, '*AVOCADO'), (31.16, 'POUR AVOIR'), (31.58, 'UN RÉCAP'), (32.02, 'DE TOUS LES'),
        (32.74, 'CONTENUS'), (33.00, 'QUE TU DOIS FAIRE'), (33.54, 'POUR CRÉER'), (33.96, 'TA STRATÉGIE'),
        (35.00, '*TCHÜSS !')]

ICONS = {   # white line icons on the gold card, 100x100 viewBox
    'clock': '<circle cx="50" cy="54" r="30"/><path d="M50 54V36M50 54l13 9M42 16h16M50 16v8"/>',
    'short': '<rect x="30" y="14" width="40" height="72" rx="8"/><text x="50" y="60" text-anchor="middle" '
             'font-family="Anton" font-size="26" fill="#fff" stroke="none">5s</text>',
    'long': '<rect x="12" y="24" width="76" height="48" rx="8"/><path d="M44 38v20l16-10z" fill="#fff"/><path d="M12 84h76"/>'
            '<path d="M12 84h60" stroke-width="9"/>',
    'viral': '<path d="M50 20a30 30 0 1 1-27 17"/><path d="M14 30l9 8 9-9"/><path d="M44 38v24l19-12z" fill="#fff"/>',
    'music': '<path d="M40 70V24l34-8v46"/><circle cx="31" cy="70" r="10" fill="#fff"/><circle cx="65" cy="62" r="10" fill="#fff"/>',
    'dm': '<path d="M16 22h68v44H46L30 80V66H16z"/><path d="M54 30l-12 18h12l-6 14 14-20H50z" fill="#fff" stroke-width="2"/>',
}


def show(sel, a, b):
    tw = [f"gsap.set('{sel}',{{autoAlpha:0}});", f"tl.set('{sel}',{{autoAlpha:1}},{a:.3f});"]
    if b < DUR - .01:
        tw.append(f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});")
    return tw


def board():
    html = ['<div id="board">']
    for k, (label, cx) in enumerate(COLS):
        html.append(f'<div id="col{k}" class="col" style="left:{cx - 160}px;top:{NUM_TOP}px"><div class="num">{label}</div>'
                    f'<div class="vues">VUES</div></div>')
    html.append('</div>')
    tw = ["gsap.set('#board',{autoAlpha:0});", "tl.fromTo('#board',{autoAlpha:0,y:-30},{autoAlpha:1,y:0,duration:.35,ease:'power3.out',immediateRender:false},0);"]
    return html, tw


def titles():
    html, tw = [], []
    for k, (title, a, *_r) in enumerate(TIPS):
        b = TIPS[k + 1][1] if k + 1 < len(TIPS) else DUR
        html.append(f'<div id="tt{k}" class="title">{title}</div>')
        tw += show(f'#tt{k}', a, b)
        tw.append(f"tl.fromTo('#tt{k}',{{y:14,opacity:0}},{{y:0,opacity:1,duration:.3,ease:'power2.out',immediateRender:false}},{a:.3f});")
    return html, tw


def icons():
    html, tw = [], []
    count = {c: sum(1 for t in TIPS if t[5] == c) for c in range(3)}
    seen = {c: 0 for c in range(3)}
    for k, (title, _, icon, t_in, t_rate, col) in enumerate(TIPS):
        if icon is None:
            continue
        n, i = count[col], seen[col]
        seen[col] += 1
        sx = COLS[col][1] + (i - (n - 1) / 2) * (SLOT + 12)     # final slot centre
        html.append(f'<div id="ic{k}" class="icon"><svg viewBox="0 0 100 100">{ICONS[icon]}</svg></div>')
        tw += [f"gsap.set('#ic{k}',{{autoAlpha:0,x:{POP_X - BIG / 2},y:{POP_Y - BIG / 2},width:{BIG},height:{BIG}}});",
               f"tl.fromTo('#ic{k}',{{autoAlpha:0,scale:.3,rotation:-12}},{{autoAlpha:1,scale:1,rotation:0,duration:.35,ease:'back.out(2)',immediateRender:false}},{t_in:.3f});",
               # it earns its column: fly up into the slot and shrink
               f"tl.to('#ic{k}',{{x:{sx - SLOT / 2:.0f},y:{SLOT_Y},width:{SLOT},height:{SLOT},duration:.45,ease:'power3.inOut'}},{t_rate:.3f});",
               # the column it lands in lights up gold for a beat
               f"tl.to('#col{col} .num',{{color:'{GOLD}',scale:1.14,duration:.15,ease:'power2.out'}},{t_rate + .4:.3f});",
               f"tl.to('#col{col} .num',{{color:'#ffffff',scale:1,duration:.4,ease:'power2.inOut'}},{t_rate + .75:.3f});"]
    return html, tw


def comment():
    a = 30.30
    html = [f'<div id="cm"><div class="cmav"><img src="assets/avatar.png"/></div><div class="cmbar"><span id="cmtext"></span>'
            f'<span id="cmcaret" class="caret"></span></div><div id="cmsend" class="cmsend"><svg viewBox="0 0 24 24" width="40" height="40">'
            f'<path d="M12 19V6M6 11l6-6 6 6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>']
    tw = show('#cm', a, SEG['bye'])
    tw.append(f"tl.fromTo('#cm',{{y:40,scale:.92}},{{y:0,scale:1,duration:.3,ease:'back.out(1.7)',immediateRender:false}},{a:.3f});")
    word = 'AVOCADO'
    for i in range(1, len(word) + 1):
        tw.append(f"tl.set('#cmtext',{{textContent:'{word[:i]}'}},{30.72 + (i - 1) * .07:.3f});")
    tw.append("gsap.set('#cmtext',{textContent:''});")
    tw.append(f"tl.to('#cmsend',{{scale:.82,duration:.07,yoyo:true,repeat:1}},{31.35:.3f});")
    return html, tw


def captions():
    html, tw = [], []
    for k, (t, txt) in enumerate(CAPS):
        b = CAPS[k + 1][0] if k + 1 < len(CAPS) else DUR
        b = min(b, t + 1.4)
        gold = txt.startswith('*')
        html.append(f'<div id="cp{k}" class="cap{" gold" if gold else ""}">{txt.lstrip("*")}</div>')
        tw += show(f'#cp{k}', max(0, t - .03), b - .03)
        tw.append(f"tl.fromTo('#cp{k}',{{scale:1.15}},{{scale:1,duration:.12,ease:'power2.out',immediateRender:false}},{max(0, t - .03):.3f});")
    return html, tw


def sfx_list():
    out = []
    for k, (title, a, icon, t_in, t_rate, col) in enumerate(TIPS):
        if k:
            out.append(('click-soft', a, .4))                 # new tip title
        if icon:
            out += [('pop', t_in, .3), ('whoosh-short', t_rate, .25), ('pop', t_rate + .4, .22)]
    out.append(('pop', 30.30, .3))
    out += [('click-soft', 30.72 + i * .07, .22) for i in range(7)]   # typing AVOCADO
    out += [('click', 31.35, .5), ('sparkle', 31.40, .15), ('pop', 35.00, .28)]
    return out


SFX_LEN = {'whoosh-short': .57, 'pop': .72, 'sparkle': 1.8, 'click': .36, 'click-soft': .36}
SFX_GAIN = 0.75


def audio():
    out, lanes = [], []
    for k, (name, t, vol) in enumerate(sorted(sfx_list(), key=lambda x: x[1])):
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
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#bgv{{z-index:0;filter:contrast(1.05) saturate(1.04) brightness(1.02)}}
#shade{{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(20,14,8,.42) 0%,rgba(20,14,8,0) 30%,rgba(20,14,8,0) 62%,rgba(20,14,8,.25) 100%)}}
.col{{position:absolute;z-index:5;width:320px;text-align:center;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.45)}}
.num{{font:400 116px/1 Anton;letter-spacing:.01em;display:inline-block;transform-origin:50% 60%}}
.vues{{font:700 30px/1 Poppins;letter-spacing:.24em;margin-top:2px;padding-left:.24em}}
.title{{position:absolute;left:0;right:0;top:226px;z-index:6;text-align:center;font:600 56px/1 Caveat;color:#fff;
  text-shadow:0 3px 14px rgba(0,0,0,.5)}}
.icon{{position:absolute;left:0;top:0;z-index:7;border-radius:26%;background:{GRAD};border:4px solid #fff;
  box-shadow:0 14px 34px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center}}
.icon svg{{width:74%;height:74%;fill:none;stroke:#fff;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;
  filter:drop-shadow(0 2px 3px rgba(80,50,10,.45))}}
.cap{{position:absolute;left:0;right:0;top:1392px;z-index:9;text-align:center;color:#fff;font:800 66px/1 Poppins;
  letter-spacing:-.01em;white-space:nowrap;text-shadow:0 0 20px rgba(0,0,0,.55),0 3px 8px rgba(0,0,0,.5);transform-origin:50% 50%}}
.cap.gold{{color:{GOLD};text-shadow:0 0 3px rgba(45,28,10,.95),0 0 6px rgba(45,28,10,.8),0 0 22px rgba(0,0,0,.6)}}
#cm{{position:absolute;left:70px;right:70px;top:1100px;z-index:8;height:116px;display:flex;align-items:center;gap:18px}}
.cmav{{width:104px;height:104px;border-radius:50%;padding:5px;background:{GRAD};flex:none}}
.cmav img{{width:100%;height:100%;border-radius:50%;border:4px solid #fff;object-fit:cover;display:block}}
.cmbar{{flex:1;height:96px;border-radius:48px;background:rgba(30,22,16,.62);border:2px solid rgba(255,255,255,.35);
  display:flex;align-items:center;padding:0 34px;font:700 50px/1 Poppins;color:#fff;letter-spacing:.02em}}
.caret{{display:inline-block;width:4px;height:52px;background:{GOLD};margin-left:6px}}
.cmsend{{position:absolute;right:16px;width:76px;height:76px;border-radius:50%;background:{GRAD};display:flex;align-items:center;justify-content:center}}
'''

SAFE_GUIDE = ('<div style="position:absolute;inset:0;z-index:99;pointer-events:none">'
              '<div style="position:absolute;left:0;right:0;top:0;height:220px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;right:0;top:1470px;bottom:0;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:100px;top:1155px;height:315px;background:rgba(255,0,0,.28)"></div></div>')


def build():
    b_html, b_tw = board()
    t_html, t_tw = titles()
    i_html, i_tw = icons()
    c_html, c_tw = comment()
    cap_html, cap_tw = captions()
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
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
  <div id="shade"></div>
{nl.join(b_html)}
{nl.join(t_html)}
{nl.join(i_html)}
{nl.join(c_html)}
{nl.join(cap_html)}
{SAFE_GUIDE if SAFE else ''}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(b_tw + t_tw + i_tw + c_tw + cap_tw)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s')
