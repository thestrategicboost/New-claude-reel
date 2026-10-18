#!/usr/bin/env python3
"""Clone reel "entrepreneuse à 100 followers vs à 100 000 followers": two Maé in one shot (assemble.py builds the
dialogue; both Maé are cut out and laid on an empty-wall plate, the 100 one 90px left, the 100 000 one 40px right,
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
DARK = '#573307'
RED, GREEN = '#E5262B', '#22B83A'   # 100 followers / 100 000 followers
GOLD = 'linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)'
X = {'f': 230, 's': 770}   # centre of each Maé (tags + captions)
ZOOM_AT = 35.35            # the 100-followers Maé is out of frame: the other slides to the centre and we push in
ZOOM = (1.45, 0, 250)      # scale, x, y of the a-roll (she is centred in the plate by then)
BLOCK = (28.45, 30.24)     # pop-up shows on 'juge', 'Bloquer' is tapped on 'bloque'
IG_AT = 37.50              # 'parce que je suis Maé de The Strategic Boost': her Instagram profile over her head
CAP_Y = 1180


def tags():
    html = [f'<div id="tf" class="tag" style="left:{X["f"] - 210}px"><div class="tl">Entrepreneuse à</div><div class="tb f">100 FOLLOWERS</div></div>',
            f'<div id="ts" class="tag" style="left:{X["s"] - 210}px"><div class="tl">Entrepreneuse à</div><div class="tb s">100 000 FOLLOWERS</div></div>']
    tw = ["tl.fromTo('#tf',{autoAlpha:0,y:-30},{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.7)',immediateRender:true},0);",
          "tl.fromTo('#ts',{autoAlpha:0,y:-30},{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.7)',immediateRender:true},.12);"]
    for p in PLAN:
        on, off = ('#tf', '#ts') if p['who'] == 'f' else ('#ts', '#tf')
        tw += [f"tl.to('{on}',{{opacity:1,scale:1.06,duration:.2,ease:'power2.out'}},{max(p['start'], .4):.2f});",
               f"tl.to('{off}',{{opacity:.5,scale:.94,duration:.2,ease:'power2.out'}},{max(p['start'], .4):.2f});"]
    tw.append("tl.to('#tf',{autoAlpha:0,y:-20,duration:.35},35.0);")   # she walks out after 'j'abandonne'
    # her Instagram card above the heads, the follow button gets tapped
    tw.append(f"tl.fromTo('#bgv',{{scale:1,x:0,y:0}},{{scale:{ZOOM[0]},x:{ZOOM[1]},y:{ZOOM[2]},duration:.9,ease:'power2.inOut',immediateRender:false}},{ZOOM_AT:.2f});")
    # "je bloque": an Instagram block pop-up, 'Bloquer' gets tapped
    html.append('<div id="blk"><div class="bt">Bloquer ce compte ?</div><div class="bs">Cette personne ne pourra plus voir ton profil '
                'ni te contacter.</div><div id="bb" class="bb">Bloquer</div><div id="bd" class="bb done">Compte bloqué</div>'
                '<div class="bc">Annuler</div></div>')
    a, b = BLOCK
    tw += ["gsap.set('#blk, #bd',{autoAlpha:0});",
           f"tl.fromTo('#blk',{{autoAlpha:0,scale:.8}},{{autoAlpha:1,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:false}},{a:.2f});",
           f"tl.to('#bb',{{scale:.9,duration:.08,yoyo:true,repeat:1}},{b:.2f});",
           f"tl.set('#bb',{{autoAlpha:0}},{b + .16:.2f});", f"tl.set('#bd',{{autoAlpha:1}},{b + .16:.2f});",
           f"tl.to('#blk',{{autoAlpha:0,scale:.9,duration:.25}},{b + 1.3:.2f});"]
    # her real Instagram profile (her screenshot) above the heads
    html.append('<div id="fol"><img src="assets/profil.png"/></div>')
    tw += ["gsap.set('#fol',{autoAlpha:0});",
           f"tl.to('#ts',{{autoAlpha:0,y:-20,duration:.2}},{IG_AT - .2:.2f});",
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


SFX = [('whoosh-short', 0.0, .3), ('pop', BLOCK[0], .45), ('click', BLOCK[1], .6), ('impact-bass-1', BLOCK[1] + .1, .35),
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
.tb{{display:inline-block;white-space:nowrap;font:400 44px/1 Anton;letter-spacing:.03em;color:#fff;padding:12px 26px 10px;border-radius:14px;
  box-shadow:0 12px 28px rgba(0,0,0,.3)}}
.tb.f{{background:{RED}}}
.tb.s{{background:{GREEN}}}
#fol{{position:absolute;z-index:15;left:190px;top:236px;width:700px;border-radius:30px;overflow:hidden;background:#fff;
  box-shadow:0 18px 44px rgba(0,0,0,.3)}}
#fol img{{width:100%;display:block}}
.tag{{width:420px}}
#blk{{position:absolute;z-index:16;left:200px;top:270px;width:680px;padding:34px 34px 18px;border-radius:30px;background:#fff;text-align:center;
  box-shadow:0 24px 60px rgba(0,0,0,.35)}}
.bt{{font:700 40px/1.2 Poppins;color:#111}}
.bs{{font:500 26px/1.35 Poppins;color:#777;margin-top:12px}}
.bb{{margin-top:26px;height:84px;border-radius:18px;background:#ED4956;color:#fff;font:700 32px/84px Poppins}}
.bb.done{{position:absolute;left:34px;right:34px;top:auto;margin-top:0;transform:translateY(-84px);background:#EFEFEF;color:#111}}
.bc{{margin-top:12px;height:64px;font:600 28px/64px Poppins;color:#111}}
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
