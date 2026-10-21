#!/usr/bin/env python3
"""Test reel for the effects library (33-59): Maé's A-roll plays once, each effect gets an equal slot with its
number and name in a chip at the bottom. Effects live in fxa.py / fxb.py / fxc.py as EFFECTS = [(num, name, fn)],
fn(a, b, k) -> dict(front=[html], behind=[html], tw=[gsap lines], css='') where k is the id prefix to use.

PY build.py            all effects
ONLY=fxb PY build.py   one module only (slots restart at 0)
"""
import importlib
import json
import os
import shutil
import subprocess

FF = shutil.which('ffmpeg') or 'ffmpeg'
DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
BROWN, DARK, INK, CREAM = '#8C5C41', '#573307', '#2A1A10', '#F4EEE6'
PILL = 'linear-gradient(135deg,#EBCB8B 0%,#C99A55 55%,#A97A3E 100%)'
TOP = 262        # inserts start under the Instagram top band
MODS = ['fxa', 'fxb', 'fxc']


# ------------------------------------------------------------------ helpers shared by the effect modules
def show(sel, a, b, frm="{autoAlpha:0,y:-30,scale:.92}", d=.3, ease='back.out(1.7)'):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,y:0,x:0,scale:1,rotation:0,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,duration:.15}},{b - .15:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def typing(sel, text, a, b):
    n = len(text)
    return [f"tl.set('{sel}',{{textContent:''}},{a - .01:.3f});"] + \
        [f"tl.set('{sel}',{{textContent:{json.dumps(text[:i])}}},{a + (b - a) * i / n:.3f});" for i in range(1, n + 1)]


def frame(t):
    """still of the A-roll at t (for freezes) -> assets/frames/f<t>.jpg"""
    os.makedirs('assets/frames', exist_ok=True)
    out = f'assets/frames/f{t:.2f}.jpg'
    if not os.path.exists(out):
        subprocess.run([FF, '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', 'assets/aroll.mp4', '-frames:v', '1', '-q:v', '2', out], check=True)
    return out


def cutframe(t):
    """still of her cut-out (transparent PNG) at t -> assets/frames/c<t>.png"""
    os.makedirs('assets/frames', exist_ok=True)
    out = f'assets/frames/c{t:.2f}.png'
    if not os.path.exists(out):
        subprocess.run([FF, '-v', 'error', '-y', '-c:v', 'libvpx-vp9', '-ss', f'{t:.3f}', '-i', 'assets/cut.webm', '-frames:v', '1', out], check=True)
    return out


# ------------------------------------------------------------------ page
def build():
    only = os.environ.get('ONLY')
    effects = []
    for m in MODS:
        if only and m != only:
            continue
        if os.path.exists(f'{m}.py'):
            effects += importlib.import_module(m).EFFECTS
    slot = DUR / max(1, len(effects))
    front, behind, tw, css = [], [], [], ''
    for i, (num, name, fn) in enumerate(effects):
        a, b = i * slot, (i + 1) * slot
        r = fn(a + .05, b - .05, f'e{num}')
        front += r.get('front', [])
        behind += r.get('behind', [])
        tw += r.get('tw', [])
        css += r.get('css', '')
        front.append(f'<div id="lab{num}" class="lab"><b>{num}</b>{name}</div>')
        tw += [f"gsap.set('#lab{num}',{{autoAlpha:0}});", f"tl.set('#lab{num}',{{autoAlpha:1}},{a:.3f});", f"tl.set('#lab{num}',{{autoAlpha:0}},{b:.3f});"]
    nl = '\n'
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#cutv{{z-index:5}}
.lab{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1580px;z-index:90;padding:10px 28px 8px;border-radius:999px;background:rgba(42,26,16,.88);
  font:400 44px/1 Anton;color:#fff;letter-spacing:.04em}}
.lab b{{font-weight:400;color:#E9C98F;margin-right:14px}}
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="voice" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
  <div id="cam">
    <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(behind)}
    <video id="cutv" class="full" src="assets/cut.webm" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="1"></video>
  </div>
{nl.join(front)}
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


if __name__ == '__main__':
    with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
        _f.write(build())
    print(f'wrote index.html {DUR:.3f}s')
