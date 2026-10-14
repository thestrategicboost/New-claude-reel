#!/usr/bin/env python3
"""Reel "payant vs gratuit": six creator needs, for each one a paid tool and a free one. Maé only says "payant,
gratuit" six times (the topic is read on screen in the pause before), so each round is: the topic lands in a
dark-brown block, then a paid tool card flips in on "payant" and a free one on "gratuit", under a fixed
PAYANT / GRATUIT header whose active side lights up. Her lilac look, frosted cards, app-style monogram tiles.

PY build.py    writes index.html
"""
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
BLOCK = '#573307'
RED, GREEN = '#E5262B', '#22B83A'      # payant / gratuit: red and green catch the eye (as in her first edit)
GOLD = 'linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)'

# when she says "payant" / "gratuit" (raw trimmed from 3.3 s)
P = [1.75, 5.21, 8.35, 11.82, 16.39, 21.07]
G = [2.26, 5.78, 9.16, 12.44, 16.96, 21.58]
# topic, (paid tool, monogram, tile colours), (free tool, monogram, tile colours)
ROUNDS = [   # topic, paid (name, logo file cropped from Maé's own first edit, show name?), free (same)
    ('Trouver tes idées', ('AnswerThePublic', 'answerthepublic', False), ('Google Trends', 'googletrends', False)),
    ('Monter tes vidéos', ('Premiere Pro', 'premiere', True), ('Edits', 'edits', False)),
    ('Programmer ton contenu', ('Metricool', 'metricool', False), ('Meta Business Suite', 'meta', False)),
    ('Créer tes visuels', ('Photoshop', 'photoshop', True), ('Canva', 'canva', False)),
    ('Étudier ta concurrence', ('Sort Feed', 'sortfeed', False), ('Social Blade', 'socialblade', False)),
    ('Ajouter tes sous-titres', ('Submagic', None, True), ('CapCut', 'capcut', False)),
]
LEFT, RIGHT = 300, 780      # card centres


def starts():
    """topic k shows from here: at once for the first, then a beat after the previous 'gratuit'"""
    return [0.0] + [g + .85 for g in G[:-1]]


def tile(name, logo):
    if logo is None:     # no logo in her edit: a plain monogram tile
        return '<div class="tile" style="background:#111;color:#C6FF3D;font-size:64px">S</div>'
    return f'<div class="logo"><img src="assets/logos/{logo}.png"/></div>'


def board():
    html, tw = [], []
    html.append('<div id="hdr"><div class="hc" style="left:' + str(LEFT - 200) + 'px"><span id="hP" class="hb pay">PAYANT</span></div>'
                '<div class="hc" style="left:' + str(RIGHT - 200) + 'px"><span id="hG" class="hb free">GRATUIT</span></div></div>')
    tw += ["gsap.set('#hdr',{autoAlpha:1});", "tl.fromTo('#hdr',{y:-40},{y:0,duration:.35,ease:'power3.out',immediateRender:true},0);",
           "gsap.set('#hP, #hG',{opacity:.6});"]
    st = starts()
    for k, (topic, paid, free) in enumerate(ROUNDS):
        a = st[k]
        b = st[k + 1] if k + 1 < len(ROUNDS) else DUR
        first = 'true' if a == 0 else 'false'
        html.append(f'<div id="t{k}" class="topic"><span class="tb">{topic}</span></div>')
        tw += [f"gsap.set('#t{k}',{{autoAlpha:0}});",
               f"tl.fromTo('#t{k}',{{autoAlpha:0,y:-24,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:{first}}},{a:.3f});"]
        for side, (name, logo, show_name), t, cx, tag in (('p', paid, P[k], LEFT, '€'), ('g', free, G[k], RIGHT, '0 €')):
            cid = f'c{side}{k}'
            html.append(f'<div id="{cid}" class="card {side}" style="left:{cx - 170}px">{tile(name, logo)}{f'<div class="nm">{name}</div>' if show_name else ''}'
                        f'<div class="tag {side}">{tag}</div></div>')
            tw += [f"gsap.set('#{cid}',{{autoAlpha:0}});",
                   f"tl.fromTo('#{cid}',{{autoAlpha:0,rotationY:-90,scale:.8}},{{autoAlpha:1,rotationY:0,scale:1,duration:.35,ease:'back.out(1.6)',immediateRender:false}},{t - .04:.3f});",
                   f"tl.fromTo('#{cid} .tag',{{scale:0}},{{scale:1,duration:.25,ease:'back.out(3)',immediateRender:false}},{t + .2:.3f});"]
            hid = '#hP' if side == 'p' else '#hG'
            tw += [f"tl.to('{hid}',{{opacity:1,scale:1.1,duration:.15}},{t - .04:.3f});", f"tl.to('{hid}',{{opacity:.6,scale:1,duration:.2}},{t + .45:.3f});"]
            if b < DUR - .01:
                tw += [f"tl.to('#{cid}',{{autoAlpha:0,rotationY:90,duration:.18}},{b - .18:.3f});", f"tl.set('#{cid}',{{autoAlpha:0}},{b:.3f});"]
        if b < DUR - .01:
            tw += [f"tl.to('#t{k}',{{autoAlpha:0,y:-16,duration:.15}},{b - .15:.3f});", f"tl.set('#t{k}',{{autoAlpha:0}},{b:.3f});"]
    return html, tw


def sfx_list():
    out = []
    for k, a in enumerate(starts()):
        out.append(('whoosh-short', a, .22))
        out.append(('pop', P[k] - .04, .22))
        out.append(('pop', G[k] - .04, .22))
        out.append(('click-soft', G[k] + .2, .3))
    return out


SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click-soft': .36}


def audio():
    out, lanes = [], []
    for k, (name, t, vol) in enumerate(sorted(sfx_list(), key=lambda x: x[1])):
        d = min(SFX_LEN[name], DUR - t)
        lane = next((i for i, end in enumerate(lanes) if end <= t), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{name}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{vol:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000;perspective:1400px}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.topic{{position:absolute;left:0;right:0;top:250px;z-index:12;text-align:center}}
.tb{{display:inline-block;font:400 76px/1 Anton;letter-spacing:.02em;color:#fff;text-transform:uppercase;
  text-shadow:0 4px 0 {BLOCK},0 0 22px rgba(87,51,7,.85),0 6px 18px rgba(40,20,5,.7)}}
#hdr{{position:absolute;left:0;right:0;top:352px;z-index:12}}
.hc{{position:absolute;width:400px;text-align:center}}
.hb{{display:inline-block;font:400 54px/1 Anton;letter-spacing:.04em;padding:8px 26px 6px;transform-origin:50% 50%;color:#fff;box-shadow:0 10px 24px rgba(0,0,0,.3)}}
.hb.pay{{background:{RED}}}
.hb.free{{background:{GREEN}}}
.card.p{{border-color:{RED}!important;box-shadow:0 22px 50px rgba(0,0,0,.35),0 0 0 3px {RED},0 0 34px rgba(229,38,43,.45)!important}}
.card.g{{border-color:{GREEN}!important;box-shadow:0 22px 50px rgba(0,0,0,.35),0 0 0 3px {GREEN},0 0 34px rgba(34,184,58,.45)!important}}
.card{{position:absolute;z-index:11;top:448px;width:340px;height:200px;border-radius:36px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:12px;background:rgba(58,38,26,.55);-webkit-backdrop-filter:blur(22px) saturate(1.2);backdrop-filter:blur(22px) saturate(1.2);
  border:1.5px solid rgba(255,255,255,.35);box-shadow:0 22px 50px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.25);color:#fff;transform-style:preserve-3d}}
.tile{{width:104px;height:104px;border-radius:28px;display:flex;align-items:center;justify-content:center;font-family:Poppins;font-weight:800;
  letter-spacing:-.03em;box-shadow:0 10px 22px rgba(0,0,0,.3),inset 0 0 0 2px rgba(255,255,255,.18)}}
.logo{{max-width:290px;height:130px;display:flex;align-items:center;justify-content:center}}
.logo img{{max-width:290px;max-height:130px;object-fit:contain;border-radius:16px;display:block;box-shadow:0 8px 20px rgba(0,0,0,.3)}}
.nm{{font:700 28px/1.1 Poppins;text-align:center;padding:0 14px;white-space:nowrap}}
.tag{{position:absolute;top:-18px;right:-14px;min-width:84px;height:56px;padding:0 14px;border-radius:28px;font:800 28px/56px Poppins;text-align:center;
  box-shadow:0 8px 18px rgba(0,0,0,.3)}}
.tag.p{{background:{RED};color:#fff;border:2px solid #fff}}
.tag.g{{background:{GREEN};color:#fff;border:2px solid #fff}}
'''


def build():
    h, tw = board()
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
{nl.join(h)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tw)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s')
