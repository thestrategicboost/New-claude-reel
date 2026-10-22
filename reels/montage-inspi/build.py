#!/usr/bin/env python3
"""Reel "Utilise cette transition avec ce son", edited after the "Use this transition with this sound" inspiration:
two fixed labels on top ("avec ce son" / "cette transition"), on each line a sound player pill slides in on the left
and a transition tile (her own frame with the effect) pops in on the right, then the transition plays on the cut
with its sound: Brush Glitch (baked into assets/aroll.mp4 by ffmpeg), Slide Left (whip blur), Shake & Flash, Hand
Click. CTA in her gold pill, her usual one-word captions, lilac look.

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
INK, CREAM = '#2A1A10', '#F4EEE6'
PILL = 'linear-gradient(135deg,#EBCB8B 0%,#C99A55 55%,#A97A3E 100%)'
TOP = 250
L = [0.0, 2.44, 4.98, 7.50]          # line starts (edit clock)
J = [2.44, 4.98, 7.50, 9.70]         # the cut that ends each line, where its transition plays
LINES = [('glitch', 'Brush Glitch', 'son glitch qui matche', '00:01'), ('slide', 'Slide Left', 'deep woosh', '00:02'),
         ('flash', 'Shake & Flash', 'flash appareil photo', '00:01'), ('click', 'Hand Click', 'clic de souris', '00:01')]
NOTE = ('<svg viewBox="0 0 24 24" width="30" height="30"><path d="M9 17.5V6l10-2v11.5" stroke="#fff" stroke-width="2" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round"/><circle cx="6.5" cy="17.5" r="2.5" fill="#fff"/><circle cx="16.5" cy="15.5" r="2.5" fill="#fff"/></svg>')


def show(sel, a, b, frm, d=.3, ease='back.out(1.7)'):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,x:0,y:0,scale:1,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,duration:.15}},{b - .15:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def captions():
    ws = json.load(open('work/words.json'))
    out, html, tw = [], [], []
    for w in ws:
        t = re.sub(r'[,.!?…]', '', w['w']).lower().strip()
        if not t:
            continue
        if t.startswith('-') and out:
            out[-1]['w'] += t
            out[-1]['e'] = w['e']
            continue
        out.append(dict(w, w=t.replace('tchüss', 'tchüss')))
    out[0]['s'] = max(out[0]['s'], .08)
    for k, w in enumerate(out):
        nxt = out[k + 1]['s'] if k + 1 < len(out) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        html.append(f'<div id="w{k}" class="cap">{w["w"]}</div>')
        tw += [f"gsap.set('#w{k}',{{autoAlpha:0}});", f"tl.set('#w{k}',{{autoAlpha:1}},{w['s']:.3f});",
               f"tl.fromTo('#w{k}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
               f"tl.set('#w{k}',{{autoAlpha:0}},{end:.3f});"]
    return html, tw


def scenes():
    H, T, S = [], [], []
    T.append("gsap.set('#cam',{scale:1.12});")
    # the two labels stay on the whole tutorial part
    H.append('<div id="hd" class="hd"><span>avec ce son</span><span>cette transition</span></div>')
    T += show('#hd', .05, J[3], "{autoAlpha:0,y:-20}", .25, 'power3.out')
    for k, (key, tile, sound, dur) in enumerate(LINES):
        a, b = L[k] + .18, J[k] + .02
        H.append(f'<div id="sp{k}" class="sp"><i class="ic">{NOTE}</i><div class="st"><b>{sound}</b><small>{dur} · CapCut</small>'
                 f'<div class="pr"><i id="pb{k}"></i></div></div><span class="ac">♡</span><span class="ac">＋</span></div>')
        H.append(f'<div id="tt{k}" class="tt"><div class="ti"><img src="assets/tiles/{key}.jpg"/><em>✦</em></div><span>{tile}</span></div>')
        T += show(f'#tt{k}', a, b, "{autoAlpha:0,scale:.6,y:-10}", .3, 'back.out(2)')
        T += show(f'#sp{k}', a + .45, b, "{autoAlpha:0,x:-60}", .3, 'power3.out')
        T += [f"gsap.set('#pb{k}',{{scaleX:0,transformOrigin:'0 50%'}});",
              f"tl.to('#pb{k}',{{scaleX:1,duration:{b - a - .5:.2f},ease:'none'}},{a + .5:.3f});"]
    # 1. Brush Glitch: baked in the footage (2.26-2.62)
    S.append(('glitch2', J[0] - .16, .55))
    # 2. Slide Left: whip out to the left with motion blur, the next shot whips in from the right
    j = J[1]
    T += [f"tl.to('#cam',{{x:-260,scale:1.55,filter:'blur(26px)',duration:.16,ease:'power2.in'}},{j - .16:.3f});",
          f"tl.fromTo('#cam',{{x:260,scale:1.55,filter:'blur(26px)'}},{{x:0,scale:1.12,filter:'blur(0px)',duration:.22,ease:'power2.out',immediateRender:false}},{j:.3f});"]
    S.append(('whoosh-short', j - .2, .6))
    # 3. Shake & Flash: white flash on the cut and a camera shake
    j = J[2]
    H.append('<div id="fl" class="fl"></div>')
    T += ["gsap.set('#fl',{autoAlpha:0});", f"tl.fromTo('#fl',{{autoAlpha:.95}},{{autoAlpha:0,duration:.3,ease:'power2.out',immediateRender:false}},{j:.3f});"]
    for i, (dx, dy, r) in enumerate([(-34, 18, -2), (28, -22, 1.6), (-20, 14, -1.2), (16, -10, .8), (-8, 6, -.4), (0, 0, 0)]):
        T.append(f"tl.set('#cam',{{x:{dx},y:{dy},rotation:{r}}},{j + i * .045:.3f});")
    S.append(('shutter', j - .02, .7))
    # 4. Hand Click: white click strokes burst next to her and a quick punch-in
    j = J[3]
    H.append('<svg id="ck" class="ck" viewBox="-60 -60 120 120">' +
             ''.join(f'<path d="M0 -20 L0 -48" transform="rotate({a})"/>' for a in (-60, -20, 20, 60, 100)) + '</svg>')
    T += ["gsap.set('#ck',{autoAlpha:0});",
          f"tl.fromTo('#ck',{{autoAlpha:1,scale:.4}},{{autoAlpha:1,scale:1.15,duration:.22,ease:'power3.out',immediateRender:false}},{j - .06:.3f});",
          f"tl.to('#ck',{{autoAlpha:0,duration:.12}},{j + .16:.3f});",
          f"tl.fromTo('#cam',{{scale:1.12}},{{scale:1.24,duration:.08,ease:'power2.out',immediateRender:false}},{j - .02:.3f});",
          f"tl.to('#cam',{{scale:1.12,duration:.25,ease:'power2.inOut'}},{j + .08:.3f});"]
    S.append(('click', j - .06, .7))
    # CTA: her gold pill "abonne-toi"
    H.append('<div id="cta" class="pill">abonne-toi pour plus de conseils</div>')
    T += show('#cta', J[3] + .32, DUR + .2, "{autoAlpha:0,scale:.6,y:20}", .3, 'back.out(2)')
    S.append(('pop', J[3] + .32, .35))
    return H, T, S


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.hd{{position:absolute;left:70px;right:70px;top:{TOP}px;z-index:20;display:flex;justify-content:space-between;
  font:800 50px/1 Poppins;white-space:nowrap;color:#fff;text-shadow:0 4px 0 rgba(0,0,0,.55),0 0 24px rgba(0,0,0,.25)}}
.hd span:last-child{{width:420px;text-align:center}}
.hd span:first-child{{width:420px;text-align:center}}
.tt{{position:absolute;right:120px;top:{TOP + 92}px;z-index:20;width:230px;padding:10px 10px 8px;border-radius:22px;
  background:rgba(42,26,16,.82);border:1.5px solid rgba(233,201,143,.65);box-shadow:0 16px 36px rgba(0,0,0,.35);text-align:center}}
.ti{{position:relative;width:210px;height:210px;border-radius:14px;overflow:hidden}}
.ti img{{width:100%;height:100%;object-fit:cover;display:block}}
.ti em{{position:absolute;left:8px;top:6px;font:700 22px/1 Poppins;color:#EBCB8B;font-style:normal;text-shadow:0 1px 3px rgba(0,0,0,.6)}}
.tt span{{display:block;margin-top:8px;font:600 26px/1.1 Poppins;color:{CREAM}}}
.sp{{position:absolute;left:70px;top:{TOP + 150}px;z-index:20;width:500px;height:104px;padding:0 20px;border-radius:26px;display:flex;align-items:center;gap:16px;
  background:rgba(42,26,16,.82);border:1.5px solid rgba(233,201,143,.4);box-shadow:0 16px 36px rgba(0,0,0,.35)}}
.ic{{width:62px;height:62px;flex:none;border-radius:50%;background:{PILL};display:flex;align-items:center;justify-content:center}}
.st{{flex:1;min-width:0}}
.st b{{display:block;font:600 28px/1.15 Poppins;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.st small{{display:block;font:500 20px/1.2 Poppins;color:rgba(244,238,230,.6);margin-top:2px}}
.pr{{height:5px;border-radius:3px;background:rgba(244,238,230,.18);margin-top:8px;overflow:hidden}}
.pr i{{display:block;height:100%;background:#E9C98F}}
.ac{{font:500 30px/1 Poppins;color:rgba(244,238,230,.8)}}
.fl{{position:absolute;inset:0;z-index:40;background:#fff}}
.ck{{position:absolute;left:740px;top:820px;width:200px;height:200px;z-index:21;overflow:visible}}
.ck path{{stroke:#fff;stroke-width:9;stroke-linecap:round;fill:none;filter:drop-shadow(0 2px 4px rgba(0,0,0,.4))}}
.pill{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP + 40}px;z-index:22;padding:16px 46px 20px;border-radius:999px;
  background:{PILL};font:italic 700 54px/1 Poppins;color:#fff;text-shadow:0 3px 0 rgba(70,35,5,.7)}}
.cap{{position:absolute;left:80px;right:80px;top:1250px;z-index:25;text-align:center;font:700 66px/1 Poppins;color:#fff;
  text-shadow:0 4px 0 #000,0 0 18px rgba(0,0,0,.45)}}
'''

SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click': .36, 'glitch2': .8, 'shutter': .4}


def build():
    H, T, S = scenes()
    ch, ct_ = captions()
    nl = '\n'
    sfx = [f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(SFX_LEN[n], DUR - t):.3f}" '
           f'data-track-index="{10 + k % 2}" data-volume="{v * .8:.3f}"></audio>' for k, (n, t, v) in enumerate(sorted(S, key=lambda x: x[1]))]
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
{nl.join(sfx)}
  <div id="cam"><video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video></div>
{nl.join(H)}
{nl.join(ch)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(T + ct_)}
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
