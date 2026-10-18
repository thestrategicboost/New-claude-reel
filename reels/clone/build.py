#!/usr/bin/env python3
"""Clone reel "l'entrepreneuse qui floppe vs celle qui réussit": two Maé in one shot (assemble.py builds the
dialogue, the success Maé is cut out and laid over the flop track, brightened grade). On top: a tag over each
head (the one speaking lights up), one-word captions under the speaker.

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
GOLD = 'linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)'
X = {'f': 300, 's': 830}   # the success Maé is laid 130px further right (more space between them)
IG_AT = 37.50              # 'parce que je suis Maé de The Strategic Boost': her Instagram card over their heads          # centre of each Maé (tags + captions)
CAP_Y = 1180


def tags():
    html = [f'<div id="tf" class="tag" style="left:{X["f"] - 200}px"><div class="tl">L\'entrepreneuse</div><div class="tb f">QUI FLOPPE</div></div>',
            f'<div id="ts" class="tag" style="left:{X["s"] - 200}px"><div class="tl">L\'entrepreneuse</div><div class="tb s">QUI RÉUSSIT</div></div>']
    tw = ["tl.fromTo('#tf',{autoAlpha:0,y:-30},{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.7)',immediateRender:true},0);",
          "tl.fromTo('#ts',{autoAlpha:0,y:-30},{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.7)',immediateRender:true},.12);"]
    for p in PLAN:
        on, off = ('#tf', '#ts') if p['who'] == 'f' else ('#ts', '#tf')
        tw += [f"tl.to('{on}',{{opacity:1,scale:1.06,duration:.2,ease:'power2.out'}},{max(p['start'], .4):.2f});",
               f"tl.to('{off}',{{opacity:.5,scale:.94,duration:.2,ease:'power2.out'}},{max(p['start'], .4):.2f});"]
    tw.append("tl.to('#tf',{autoAlpha:0,y:-20,duration:.4},35.6);")   # she walks out after 'j'abandonne'
    # her Instagram card above the heads, the follow button gets tapped
    # her real Instagram profile (her screenshot) above the heads
    html.append('<div id="fol"><img src="assets/profil.png"/></div>')
    tw += ["gsap.set('#fol',{autoAlpha:0});",
           f"tl.to('#ts',{{autoAlpha:0,y:-20,duration:.2}},{IG_AT - .2:.2f});",
           f"tl.fromTo('#fol',{{autoAlpha:0,y:-40,scale:.85}},{{autoAlpha:1,y:0,scale:1,duration:.4,ease:'back.out(1.7)',immediateRender:false}},{IG_AT:.2f});",
           f"tl.to('#fol',{{scale:1.03,duration:.5,ease:'sine.inOut',yoyo:true,repeat:1}},{IG_AT + .6:.2f});"]
    return html, tw


def captions():
    html, tw = [], []
    for k, w in enumerate(WORDS):
        end = WORDS[k + 1]['s'] if k + 1 < len(WORDS) and WORDS[k + 1]['s'] - w['e'] < .5 else w['e'] + .25
        end = min(end, DUR)
        html.append(f'<div id="w{k}" class="cap" style="left:{X[w["who"]] - 300}px">{w["w"]}</div>')
        tw += [f"gsap.set('#w{k}',{{autoAlpha:0}});",
               f"tl.fromTo('#w{k}',{{autoAlpha:1,scale:.82}},{{autoAlpha:1,scale:1,duration:.12,ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
               f"tl.set('#w{k}',{{autoAlpha:0}},{end:.3f});"]
    return html, tw


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.tag{{position:absolute;top:300px;width:400px;text-align:center;z-index:10;transform-origin:50% 100%}}
.tl{{font:600 32px/1 Poppins;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.55);margin-bottom:10px}}
.tb{{display:inline-block;font:400 54px/1 Anton;letter-spacing:.03em;color:#fff;padding:12px 26px 10px;border-radius:14px;
  box-shadow:0 12px 28px rgba(0,0,0,.3)}}
.tb.f{{background:{DARK}}}
.tb.s{{background:{GOLD};text-shadow:0 2px 6px rgba(80,45,10,.45)}}
#fol{{position:absolute;z-index:15;left:190px;top:236px;width:700px;border-radius:30px;overflow:hidden;background:#fff;
  box-shadow:0 18px 44px rgba(0,0,0,.3)}}
#fol img{{width:100%;display:block}}
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
