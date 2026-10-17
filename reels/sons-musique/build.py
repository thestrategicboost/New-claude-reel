#!/usr/bin/env python3
"""Reel "mes sons viraux classés par vibe": Maé's b-roll with a music timeline scrolling under a fixed playhead,
each clip named with its vibe and playing as the playhead crosses it (inspi: "My most used viral sounds
categorized by vibe", same first four sounds, clips in her brown instead of green).

PY build.py    writes index.html
"""
import json
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/music.m4a'], capture_output=True, text=True).stdout.strip())
BROWN, DARK = '#8C5C41', '#573307'
WAVE = '#EBD5BC'
# (song, vibe, start, end) on the music clock (cut from the inspi's audio)
SOUNDS = [('Now or Never', 'Motivant', 0.0, 4.3), ('Good Man With a<br/>Broken Heart', 'Cinématique', 4.3, 7.9),
          ('Runaway', 'Dramatique', 7.9, 11.9), ('Timeless', 'Puissant', 11.9, DUR)]
PX = 175          # timeline pixels per second
PLAY_X = 390      # fixed playhead
STRIP_Y = 600
CLIP_H = 104
GAP = 14
ENV = json.load(open('work/env.json'))     # 20 loudness values per second


def clip(k, name, vibe, a, b):
    x, w = a * PX, (b - a) * PX - GAP
    bars, n = [], int((b - a) * 20)
    for i in range(n):
        v = ENV[min(int(a * 20) + i, len(ENV) - 1)]
        h = max(6, v * (CLIP_H - 30))
        bars.append(f'<rect x="{i * PX / 20 + 2:.1f}" y="{(CLIP_H - 6 - h):.1f}" width="{PX / 20 - 2.6:.1f}" height="{h:.1f}" rx="1.5"/>')
    two = ' two' if '<br/>' in name else ''
    return (f'<div class="lab{two}" style="left:{x}px;width:{w}px"><div class="nm">{name}</div><div class="vb">{vibe}</div></div>'
            f'<div class="clip" style="left:{x}px;width:{w}px"><span class="note">♪</span>'
            f'<svg width="{w}" height="{CLIP_H}" viewBox="0 0 {w} {CLIP_H}"><g fill="{WAVE}">{"".join(bars)}</g></svg></div>')


def build():
    strip = ''.join(clip(k, *s) for k, s in enumerate(SOUNDS))
    css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#shade{{position:absolute;left:0;right:0;top:0;height:900px;z-index:5;
  background:linear-gradient(180deg,rgba(25,14,6,.62) 0%,rgba(25,14,6,.42) 55%,rgba(25,14,6,0) 100%)}}
#title{{position:absolute;left:80px;right:80px;top:262px;z-index:10;text-align:center;color:#fff;font:800 56px/1.12 Poppins;
  letter-spacing:-.01em;text-shadow:0 3px 14px rgba(0,0,0,.55)}}
#strip{{position:absolute;left:0;top:{STRIP_Y - 112}px;height:{CLIP_H + 112}px;z-index:10;will-change:transform}}
.clip{{position:absolute;top:112px;height:{CLIP_H}px;border-radius:12px;background:{BROWN};border:2px solid {DARK};overflow:hidden;
  box-shadow:0 10px 26px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.18)}}
.clip svg{{position:absolute;left:0;top:0}}
.note{{position:absolute;right:10px;top:4px;font:700 22px/1 Poppins;color:{WAVE}}}
.lab{{position:absolute;top:22px;text-align:center;overflow:hidden;white-space:nowrap;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.6)}}
.lab.two{{top:-14px}}
.nm{{font:700 34px/1.08 Poppins;padding:0 10px}}
.lab.two .nm{{font-size:31px}}
.vb{{font:600 italic 27px/1.2 Poppins;opacity:.88;margin-top:4px}}
#ph{{position:absolute;left:{PLAY_X - 3}px;top:{STRIP_Y - 8}px;width:6px;height:{CLIP_H + 30}px;background:#fff;z-index:12;border-radius:3px;
  box-shadow:0 0 12px rgba(0,0,0,.45)}}
#ph:before{{content:'';position:absolute;left:-11px;top:-14px;border-left:14px solid transparent;border-right:14px solid transparent;
  border-top:18px solid #fff}}
'''
    tw = ["tl.fromTo('#title',{autoAlpha:0,y:-20},{autoAlpha:1,y:0,duration:.35,ease:'power3.out',immediateRender:true},0);",
          f"tl.fromTo('#strip',{{x:{PLAY_X}}},{{x:{PLAY_X - DUR * PX:.1f},duration:{DUR:.3f},ease:'none',immediateRender:true}},0);",
          "tl.fromTo('#ph',{scaleY:0,transformOrigin:'50% 0%'},{scaleY:1,duration:.3,ease:'power2.out',immediateRender:true},0);"]
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="assets/vendor/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="music" src="assets/music.m4a" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/broll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
  <div id="shade"></div>
  <div id="title">Mes sons viraux les plus utilisés,<br/>classés par « vibe »</div>
  <div id="strip">{strip}</div>
  <div id="ph"></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tw)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s')
