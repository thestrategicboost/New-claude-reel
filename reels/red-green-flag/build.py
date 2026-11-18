#!/usr/bin/env python3
"""« Red flag / Green flag » — her own edit kept as is (src/brut.mov: flags, captions, texts already burned in), plus
small extras: face retouch; on every spoken « red flag » / « green flag » the matching flag (cut from her own frame, edges
feathered) pops and waves with a soft sound (red: low thud, green: sparkle). Her edit already has its own follow banner at
the end, so nothing is added there. No zoom on her face, nothing over her face.
PY build.py      writes index.html"""
import json
import re

W = json.load(open('work/words.json'))
DUR = 59.7
DARK = '#523301'
BOX = {'red': (95, 190, 340, 320), 'green': (620, 195, 320, 310)}     # x, y, w, h around each burned-in flag
V = []
for a, b in zip(W, W[1:]):
    k = re.sub(r'[^a-z]', '', a['w'].lower())
    if k in ('red', 'green') and re.sub(r'[^a-z]', '', b['w'].lower()) == 'flag':
        V.append((k, a['s']))
T_AB = next(w['s'] for w in W if w['s'] > 56 and 'abonne' in w['w'].lower())
T_TAP = T_AB + .75


def build():
    H, T, S = [], [], []
    for c, (x, y, w, h) in BOX.items():
        H.append(f'<div id="fl{c}" class="fl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                 f'<video id="v{c}" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" '
                 f'data-track-index="{1 if c == "red" else 4}" style="left:-{x}px;top:-{y}px"></video></div>')
        T.append(f"gsap.set('#fl{c}',{{autoAlpha:0}});")
    for c, t in V:
        s = f'#fl{c}'
        T += [f"tl.set('{s}',{{autoAlpha:1,scale:1,rotation:0}},{t:.3f});",
              f"tl.to('{s}',{{scale:1.24,duration:.18,ease:'back.out(2.4)'}},{t:.3f});",
              f"tl.to('{s}',{{rotation:-5,duration:.09,yoyo:true,repeat:3,ease:'sine.inOut'}},{t + .12:.3f});",
              f"tl.to('{s}',{{scale:1,rotation:0,duration:.22,ease:'power2.inOut'}},{t + .5:.3f});",
              f"tl.set('{s}',{{autoAlpha:0}},{t + .74:.3f});"]
        S.append(('sparkle', t, .3, 1.0) if c == 'green' else ('impact-bass-1', t, .32, .8))
    sfx = [f'<audio id="s{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(d, DUR - t):.3f}" data-track-index="{10 + k % 3}" '
           f'data-volume="{v}"></audio>' for k, (n, t, v, d) in enumerate(S)]
    nl = '\n'
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.fl{{position:absolute;z-index:10;overflow:hidden;-webkit-mask-image:radial-gradient(ellipse closest-side,#000 72%,transparent 100%);
  mask-image:radial-gradient(ellipse closest-side,#000 72%,transparent 100%)}}
.fl video{{position:absolute;width:1080px;height:1920px}}
.fb{{position:absolute;left:150px;width:780px;top:1500px;z-index:20;height:124px;border-radius:62px;background:#fff;display:flex;align-items:center;gap:18px;
  padding:0 18px;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.fb img{{width:88px;height:88px;border-radius:50%;object-fit:cover;border:3px solid {DARK}}}
.nm{{flex:1;display:flex;flex-direction:column;font-family:Poppins;color:#2A1A10}} .nm b{{font:700 34px/1.15 Poppins}} .nm span{{font:500 26px/1.2 Poppins;color:#8a7d72}}
.bt{{background:{DARK};color:#fff;font:700 32px/1 Poppins;padding:22px 34px;border-radius:40px}}
.bt.done{{background:#EFEAE4;color:#2A1A10}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="voice" src="assets/voice.m4a" data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
{nl.join(sfx)}
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
{nl.join(H)}
</div>
<script>const tl = gsap.timeline({{ paused: true }});
{nl.join(T)}
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;</script></body></html>
'''


if __name__ == '__main__':
    open('index.html', 'w', encoding='utf-8').write(build())
    print('verdicts', [(c, round(t, 2)) for c, t in V], 'abonne', round(T_AB, 2))
