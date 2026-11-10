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


def starts():
    """topic k shows from here: at once for the first, then a beat after the previous 'gratuit'"""
    return [v[0] for v in VO]


def tile(name, logo):
    if isinstance(logo, tuple):      # two free tools stacked
        return '<div class="logo two">' + ''.join(f'<img src="assets/logos/{l}.png"/>' for l in logo) + '</div>'
    return f'<div class="logo"><img src="assets/logos/{logo}.png"/></div>'


def board():
    """v4 layout (her ask: another layout): a DUEL. The topic in her dark-brown block; under it two white cards slide in
    from the screen edges, each with its own coloured band (PAYANT red / GRATUIT green), a brown VS badge pops between them."""
    html, tw = [], []
    st = starts()
    html.append('<div id="vs" class="vs">VS</div>')
    tw += ["gsap.set('#vs',{autoAlpha:0});"]
    for k, (topic, paid, free) in enumerate(ROUNDS):
        a = st[k]
        b = st[k + 1] if k + 1 < len(ROUNDS) else DUR
        first = 'true' if a == 0 else 'false'
        html.append(f'<div id="t{k}" class="topic"><span class="tb">{topic}</span></div>')
        tw += [f"gsap.set('#t{k}',{{autoAlpha:0}});",
               f"tl.fromTo('#t{k}',{{autoAlpha:0,scale:.85}},{{autoAlpha:1,scale:1,duration:.24,ease:'back.out(2)',immediateRender:{first}}},{a:.3f});"]
        for side, (name, logo, show_name), t, x, dx, lab in (('p', paid, P[k], 130, -520, 'PAYANT'), ('g', free, G[k], 570, 520, 'GRATUIT')):
            cid = f'c{side}{k}'
            html.append(f'<div id="{cid}" class="duel {side}" style="left:{x}px"><div class="band {side}">{lab}</div>'
                        f'<div class="body">{tile(name, logo)}{f"<div class=nm>{name}</div>" if show_name else ""}</div></div>')
            tw += [f"gsap.set('#{cid}',{{autoAlpha:0}});",
                   f"tl.fromTo('#{cid}',{{autoAlpha:0,x:{dx},rotation:{-8 if side == 'p' else 8}}},{{autoAlpha:1,x:0,rotation:0,duration:.32,ease:'back.out(1.5)',immediateRender:false}},{t - .06:.3f});"]
            if b < DUR - .01:
                tw += [f"tl.to('#{cid}',{{autoAlpha:0,x:{dx // 3},duration:.14}},{b - .14:.3f});", f"tl.set('#{cid}',{{autoAlpha:0}},{b:.3f});"]
        # VS pops between them when the free one lands
        tw += [f"tl.fromTo('#vs',{{autoAlpha:0,scale:2.2,rotation:-20}},{{autoAlpha:1,scale:1,rotation:0,duration:.22,ease:'expo.out',immediateRender:false}},{G[k] + .1:.3f});"]
        if b < DUR - .01:
            tw += [f"tl.to('#t{k}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('#t{k}',{{autoAlpha:0}},{b:.3f});",
                   f"tl.to('#vs',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('#vs',{{autoAlpha:0}},{b:.3f});"]
    return html, tw


def sfx_list():
    out = []
    for k, a in enumerate(starts()):
        out.append(('whoosh-short', a, .12))
        out.append(('pop', P[k] - .04, .22))
        out.append(('pop', G[k] - .04, .22))
        out.append(('click-soft', G[k] + .1, .3))      # VS badge
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
.tb{{display:inline-block;max-width:860px;background:{BLOCK};color:#fff;font:400 62px/1.08 Anton;letter-spacing:.03em;text-transform:uppercase;padding:10px 26px 6px;white-space:nowrap}}
.duel{{position:absolute;top:372px;width:380px;height:250px;z-index:11;border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 18px 40px rgba(0,0,0,.3)}}
.band{{height:66px;font:400 44px/66px Anton;letter-spacing:.06em;color:#fff;text-align:center}}
.band.p{{background:{RED}}} .band.g{{background:{GREEN}}}
.body{{height:184px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}}
.logo{{max-width:300px;height:120px;display:flex;align-items:center;justify-content:center}}
.logo.two{{flex-direction:row;gap:14px}}
.logo.two img{{max-height:100px!important;max-width:130px!important}}
.logo img{{max-width:300px;max-height:120px;object-fit:contain;border-radius:16px;display:block}}
.nm{{font:700 26px/1.1 Poppins;color:#2A1A10;white-space:nowrap}}
.vs{{position:absolute;left:490px;top:447px;width:100px;height:100px;z-index:13;border-radius:50%;background:{BLOCK};color:#fff;border:5px solid #fff;
  font:400 46px/90px Anton;text-align:center;box-shadow:0 10px 24px rgba(0,0,0,.35)}}
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
