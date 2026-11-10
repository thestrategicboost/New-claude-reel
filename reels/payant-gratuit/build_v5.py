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
P = [1.74, 4.03, 6.56, 8.77, 11.71]      # dead air between topics cut (work/aroll_full.mp4 -> 5 pieces, her ask)
G = [2.22, 4.55, 7.04, 9.37, 12.25]
# her own voice reading each topic (cut from her first edit, assets/vo/t*.wav), placed in the pause before 'payant'
VO = [(0.34, 1.3), (2.77, 1.18), (5.3, 1.18), (7.63, 1.06), (10.13, 1.5)]
# topic, (paid tool, monogram, tile colours), (free tool, monogram, tile colours)
ROUNDS = [   # topic as she says it, paid (name, logo, show name?), free (name, logo(s), show name?) - exactly as in her first edit
    ('Trouver tes idées de contenu', ('AnswerThePublic', 'answerthepublic', False), ('Google Trends', 'googletrends', False)),
    ('Faire ton montage vidéo', ('Premiere Pro', 'premiere', True), ('Edits · CapCut', ('edits', 'capcut'), False)),
    ('Pour programmer ton contenu', ('Metricool', 'metricool', False), ('Meta Business Suite', 'meta', False)),
    ('Pour créer tes visuels', ('Photoshop', 'photoshop', True), ('Canva', 'canva', False)),
    ('Pour étudier ta concurrence', ('Sort Feed', 'sortfeed', False), ('Social Blade', 'socialblade', False)),
]
LEFT, RIGHT = 300, 780      # card centres
CX = [70, 750]                # column left edges (260 px wide, inside the margins, beside her face)
ROW0, ROWH = 460, 122         # first logo row, row step


def starts():
    """topic k shows from here: at once for the first, then a beat after the previous 'gratuit'"""
    return [v[0] for v in VO]


def tile(name, logo):
    if isinstance(logo, tuple):      # two free tools stacked
        return '<div class="logo two">' + ''.join(f'<img src="assets/logos/{l}.png"/>' for l in logo) + '</div>'
    return f'<div class="logo"><img src="assets/logos/{logo}.png"/></div>'


def board():
    """v5 (her ask): TWO COLUMNS, always on screen. PAYANT (red) on the left, GRATUIT (green) on the right, both headers
    there from the first frame; each round adds its logo tile in its column on her word and it STAYS to the end, the
    newest row lit, so there is always something on screen. The topic changes in her dark-brown block on top."""
    html, tw = [], []
    st = starts()
    html.append(f'<div class="col p" style="left:{CX[0]}px"><div class="hd p">PAYANT</div></div>'
                f'<div class="col g" style="left:{CX[1]}px"><div class="hd g">GRATUIT</div></div>')
    for k, (topic, paid, free) in enumerate(ROUNDS):
        a = 0 if k == 0 else st[k]
        b = st[k + 1] if k + 1 < len(ROUNDS) else DUR
        html.append(f'<div id="t{k}" class="topic"><span class="tb">{topic}</span></div>')
        tw += [f"gsap.set('#t{k}',{{autoAlpha:{1 if k == 0 else 0}}});"]
        if k:
            tw += [f"tl.fromTo('#t{k}',{{autoAlpha:0,scale:.85}},{{autoAlpha:1,scale:1,duration:.2,ease:'back.out(2)',immediateRender:false}},{a:.3f});"]
        if b < DUR - .01:
            tw += [f"tl.set('#t{k}',{{autoAlpha:0}},{b:.3f});"]
        y = ROW0 + k * ROWH
        for c, (side, (name, logo, show_name), t) in enumerate((('p', paid, P[k]), ('g', free, G[k]))):
            cid = f'r{side}{k}'
            html.append(f'<div id="{cid}" class="row {side}" style="left:{CX[c]}px;top:{y}px">{tile(name, logo)}</div>')
            tw += [f"gsap.set('#{cid}',{{autoAlpha:0}});",
                   f"tl.fromTo('#{cid}',{{autoAlpha:0,scale:.3}},{{autoAlpha:1,scale:1.08,duration:.22,ease:'back.out(2.4)',immediateRender:false}},{t - .04:.3f});",
                   f"tl.to('#{cid}',{{scale:1,duration:.2}},{t + .3:.3f});"]
    return html, tw


def sfx_list():
    out = []
    for k, a in enumerate(starts()):
        out.append(('whoosh-short', a, .12))
        out.append(('pop', P[k] - .04, .22))
        out.append(('pop', G[k] - .04, .22))
    return out


SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click-soft': .36}


def audio():
    out, lanes = [f'<audio id="vo{k}" src="assets/vo/t{k}.wav" data-start="{t:.3f}" data-duration="{d:.3f}" data-track-index="{30 + k}" data-volume="0.9"></audio>'
                  for k, (t, d) in enumerate(VO)], []
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
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.topic{{position:absolute;left:0;right:0;top:250px;z-index:12;text-align:center}}
.tb{{display:inline-block;max-width:860px;background:{BLOCK};color:#fff;font:400 58px/1.08 Anton;letter-spacing:.03em;text-transform:uppercase;padding:10px 24px 6px;white-space:nowrap}}
.col{{position:absolute;top:350px;width:260px;z-index:11}}
.hd{{height:84px;border-radius:20px;font:400 56px/84px Anton;letter-spacing:.05em;color:#fff;text-align:center;box-shadow:0 10px 24px rgba(0,0,0,.3)}}
.hd.p{{background:{RED}}} .hd.g{{background:{GREEN}}}
.row{{position:absolute;width:260px;height:106px;z-index:11;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center;
  box-shadow:0 10px 22px rgba(0,0,0,.25)}}
.row.p{{border:4px solid {RED}}} .row.g{{border:4px solid {GREEN}}}
.logo{{max-width:220px;height:84px;display:flex;align-items:center;justify-content:center}}
.logo.two{{flex-direction:row;gap:10px}}
.logo.two img{{max-height:70px!important;max-width:100px!important}}
.logo img{{max-width:220px;max-height:84px;object-fit:contain;border-radius:12px;display:block}}
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
