#!/usr/bin/env python3
"""Clone reel "0 followers vs 10K followers": two Maé in one shot (assemble.py builds the
dialogue; both Maé are cut out and laid on an empty-wall plate, the 0-followers one 90px left, the 10K one 40px right; the 0 one is sharpened (softer focus), all sped up 1.12x,
then centred once she is alone; brightened grade + her lilac look, lilac.py). On top: a tag over each head (the one
speaking lights up), one-word captions under the speaker, an Instagram "block" pop-up on "je bloque", her real
Instagram profile at the end, a few sound effects.

PY build.py    writes index.html
"""
import json
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
PLAN = json.load(open('work/plan.json'))
WORDS = json.load(open('work/words_tl.json'))
SPEED = 1.12   # the composite is sped up 1.12x (more punch): every time written on the dialogue clock is divided by it
for _p in PLAN:
    _p['start'], _p['end'] = _p['start'] / SPEED, _p['end'] / SPEED
for _w in WORDS:
    _w['s'], _w['e'] = _w['s'] / SPEED, _w['e'] / SPEED
DARK = '#573307'
RED, GREEN = '#E03E31', '#4CB73F'   # 0 followers / 10K followers (her reference capture)
GOLD = 'linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)'
X = {'f': 230, 's': 770}   # centre of each Maé (tags + captions)
ZOOM_AT = 35.35 / SPEED           # the 100-followers Maé is out of frame: the other slides to the centre and we push in
ZOOM = (1.45, 0, 250)      # scale, x, y of the a-roll (she is centred in the plate by then)
BLOCK = (21.25 / SPEED, 30.24 / SPEED)    # block dialog panel from the 'juge' exchange, 'Bloquer' is tapped on 'bloque'
IG_AT = 37.50 / SPEED             # 'parce que je suis Maé de The Strategic Boost': her Instagram profile over her head
CAP_Y = 1180


CAM = ('<svg viewBox="0 0 24 24" width="74" height="74" fill="none" stroke="#111" stroke-width="1.4"><circle cx="12" cy="12" r="11"/>'
       '<rect x="6" y="8.5" width="12" height="8.5" rx="1.6"/><circle cx="12" cy="12.7" r="2.6"/><path d="M9.5 8.5l1-1.6h3l1 1.6"/></svg>')
# one pair of panels over their heads per exchange (inspired by her "Clone inspi" reel): 0 followers left, 10K right
PANELS = [
    ('<img src="assets/photos/camescope.jpg"/>', '<img src="assets/photos/telephone.jpg"/>'),                 # caméra / mon téléphone
    ('<div class="vw"><div class="vl">Vues de la vidéo</div><div class="vn">500</div></div>',
     '<img src="assets/photos/public.jpg"/>'),                                                                # 500 vues / 500 personnes
    ('<img src="assets/photos/stress.jpg"/>', '<img src="assets/photos/tournage.jpg"/>'),                     # pas le temps / je trouve le temps
    (f'<div class="ep">{CAM}<div>Aucune publication</div></div>',
     '<div class="bk"><div class="bt">Bloquer ce compte ?</div><div class="bs">Cette personne ne pourra plus te contacter.</div>'
     '<div id="bb" class="bb">Bloquer</div><div id="bd" class="bb done">Compte bloqué</div></div>'),          # peur d'être jugée / je bloque
]
PX = {'f': 280, 's': 800}  # panel + tag centres (inside the 80px side margins)


def tags():
    html = [f'<div id="tf" class="tag" style="left:{PX["f"] - 210}px"><div class="tb f">0 FOLLOWERS</div></div>',
            f'<div id="ts" class="tag" style="left:{PX["s"] - 210}px"><div class="tb s">10K FOLLOWERS</div></div>']
    tw = ["tl.fromTo('#tf',{autoAlpha:0,y:-30},{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.7)',immediateRender:true},0);",
          "tl.fromTo('#ts',{autoAlpha:0,y:-30},{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.7)',immediateRender:true},.12);"]
    for p in PLAN:
        on, off = ('#tf', '#ts') if p['who'] == 'f' else ('#ts', '#tf')
        tw += [f"tl.to('{on}',{{opacity:1,scale:1.06,duration:.2,ease:'power2.out'}},{max(p['start'], .4):.2f});",
               f"tl.to('{off}',{{opacity:.5,scale:.94,duration:.2,ease:'power2.out'}},{max(p['start'], .4):.2f});"]
    tw.append("gsap.set('.pn.s .dim',{opacity:.55});")
    for p in PLAN:   # the panel of the one listening is darkened too
        on, off = ('.pn.f .dim', '.pn.s .dim') if p['who'] == 'f' else ('.pn.s .dim', '.pn.f .dim')
        tw += [f"tl.to('{on}',{{opacity:0,duration:.2}},{max(p['start'], .4):.2f});",
               f"tl.to('{off}',{{opacity:.55,duration:.2}},{max(p['start'], .4):.2f});"]
    tw.append(f"tl.to('#tf',{{autoAlpha:0,y:-20,duration:.35}},{35.0 / SPEED:.2f});")   # she walks out after 'j'abandonne'
    # the panels, swapped at each new exchange
    for k, (left, right) in enumerate(PANELS):
        a, b = PLAN[2 * k]['start'], PLAN[2 * k + 1]['end']
        for side, inner, d in (('f', left, 0), ('s', right, .08)):
            pid = f'p{side}{k}'
            html.append(f'<div id="{pid}" class="pn {side}" style="left:{PX[side] - 200}px">{inner}<div class="dim"></div></div>')
            tw += [f"gsap.set('#{pid}',{{autoAlpha:0}});",
                   f"tl.fromTo('#{pid}',{{autoAlpha:0,scale:.85,y:-20}},{{autoAlpha:1,scale:1,y:0,duration:.3,ease:'back.out(1.7)',immediateRender:{'true' if a + d == 0 else 'false'}}},{a + d:.2f});",
                   f"tl.to('#{pid}',{{autoAlpha:0,scale:.92,duration:.15}},{b - .15:.2f});", f"tl.set('#{pid}',{{autoAlpha:0}},{b:.2f});"]
    tw += ["gsap.set('#bd',{autoAlpha:0});", f"tl.to('#bb',{{scale:.9,duration:.08,yoyo:true,repeat:1}},{BLOCK[1]:.2f});",
           f"tl.set('#bb',{{autoAlpha:0}},{BLOCK[1] + .16:.2f});", f"tl.set('#bd',{{autoAlpha:1}},{BLOCK[1] + .16:.2f});"]
    tw.append(f"tl.to('#ts',{{autoAlpha:0,y:-20,duration:.25}},{ZOOM_AT:.2f});")   # alone and centred: no more tag
    tw.append(f"tl.fromTo('#bgv',{{scale:1,x:0,y:0}},{{scale:{ZOOM[0]},x:{ZOOM[1]},y:{ZOOM[2]},duration:.9,ease:'power2.inOut',immediateRender:false}},{ZOOM_AT:.2f});")
    # her real Instagram profile (her screenshot) above the heads
    html.append('<div id="fol"><img src="assets/profil.png"/></div>')
    tw += ["gsap.set('#fol',{autoAlpha:0});",
           f"tl.fromTo('#fol',{{autoAlpha:0,y:-40,scale:.85}},{{autoAlpha:1,y:0,scale:1,duration:.4,ease:'back.out(1.7)',immediateRender:false}},{IG_AT:.2f});",
           f"tl.to('#fol',{{scale:1.03,duration:.5,ease:'sine.inOut',yoyo:true,repeat:1}},{IG_AT + .6:.2f});"]
    return html, tw


def captions():
    """one word at a time; a word shorter than 0.14 s is shown together with the next one (never two on screen)"""
    groups = []
    for w in WORDS:
        if groups and groups[-1]['who'] == w['who'] and w['s'] - groups[-1]['s'] < .14:
            groups[-1]['w'] += ' ' + w['w']
            groups[-1]['e'] = w['e']
        else:
            groups.append(dict(w))
    html, tw = [], []
    for k, w in enumerate(groups):
        nxt = groups[k + 1]['s'] if k + 1 < len(groups) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .25, nxt, DUR)
        cx = 540 if w['s'] >= ZOOM_AT + .4 else X[w['who']]
        html.append(f'<div id="w{k}" class="cap" style="left:{cx - 300}px">{w["w"]}</div>')
        tw += [f"gsap.set('#w{k}',{{autoAlpha:0}});",
               f"tl.set('#w{k}',{{autoAlpha:1}},{w['s']:.3f});",
               f"tl.fromTo('#w{k}',{{scale:.82}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
               f"tl.set('#w{k}',{{autoAlpha:0}},{end:.3f});"]
    return html, tw


SFX = [('whoosh-short', 0.0, .3)] + [('pop', PLAN[2 * k]['start'], .3) for k in range(1, len(PANELS))] + [('click', BLOCK[1], .6), ('impact-bass-1', BLOCK[1] + .1, .35),
       ('whoosh-short', ZOOM_AT, .4), ('pop', IG_AT, .45), ('sparkle', IG_AT + .3, .22)]
SFX_LEN = {'whoosh-short': .57, 'pop': .72, 'click': .36, 'impact-bass-1': 2.1, 'sparkle': 1.8}


def audio():
    return [f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(SFX_LEN[n], DUR - t):.3f}" '
            f'data-track-index="{10 + k}" data-volume="{v}"></audio>' for k, (n, t, v) in enumerate(SFX)]


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.tag{{position:absolute;top:300px;width:400px;text-align:center;z-index:10;transform-origin:50% 100%}}
.tl{{font:600 32px/1 Poppins;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.55);margin-bottom:10px}}
.tb{{display:inline-block;white-space:nowrap;font:400 54px/1 Anton;letter-spacing:.07em;color:#fff;padding:14px 30px 12px;border-radius:0;
  box-shadow:0 12px 28px rgba(0,0,0,.3)}}
.tb.f{{background:{RED}}}
.tb.s{{background:{GREEN}}}
#fol{{position:absolute;z-index:15;left:190px;top:236px;width:700px;border-radius:30px;overflow:hidden;background:#fff;
  box-shadow:0 18px 44px rgba(0,0,0,.3)}}
#fol img{{width:100%;display:block}}
.tag{{width:420px;top:490px}}
.pn{{position:absolute;z-index:12;top:236px;width:400px;height:236px;border-radius:0;overflow:hidden;background:#fff;border:4px solid #fff;
  box-shadow:0 16px 40px rgba(0,0,0,.3)}}
.dim{{position:absolute;inset:0;background:#000;opacity:0}}
.pn img{{width:100%;height:100%;object-fit:cover;display:block}}
.vw{{padding:38px 34px}}
.vl{{font:600 30px/1 Poppins;color:#555}}
.vn{{font:800 104px/1.1 Poppins;color:#111;letter-spacing:-.02em;margin-top:10px}}
.ep{{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;font:600 30px/1 Poppins;color:#111}}
.bk{{padding:22px 24px;text-align:center;position:relative;height:100%}}
.bt{{font:700 30px/1.2 Poppins;color:#111}}
.bs{{font:500 21px/1.3 Poppins;color:#777;margin-top:8px}}
.bb{{margin-top:18px;height:66px;border-radius:14px;background:#ED4956;color:#fff;font:700 28px/66px Poppins}}
.bb.done{{position:absolute;left:24px;right:24px;bottom:22px;margin:0;background:#EFEFEF;color:#111}}
.cap{{position:absolute;top:{CAP_Y}px;width:600px;text-align:center;z-index:11;font:700 70px/1 Poppins;color:#fff;
  text-shadow:0 4px 0 rgba(0,0,0,.85),0 0 18px rgba(0,0,0,.6);white-space:nowrap}}
'''


def build():
    th, tt = tags()
    ch, ct = captions()
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
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(audio())}
{nl.join(th)}
{nl.join(ch)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tt + ct)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s')
