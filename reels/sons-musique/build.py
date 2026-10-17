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
WAVE = '#D9AF88'      # caramel waveform on the brown clip
HEAD = '#5C3A25'      # darker header band
# (song, vibe, start, end) on the music clock (cut from the inspi's audio)
SOUNDS = [('Now or Never', 'Motivant', 0.0, 4.3), ('Good Man With a<br/>Broken Heart', 'Cinématique', 4.3, 7.9),
          ('Runaway', 'Dramatique', 7.9, 11.9), ('Timeless', 'Puissant', 11.9, DUR)]
PX = 175          # timeline pixels per second
PLAY_X = 390      # fixed playhead
STRIP_Y = 770
CLIP_H = 92
HEAD_H = 26
GAP = 14
ENV = json.load(open('work/env60.json'))   # 60 loudness values per second


def clip(k, name, vibe, a, b):
    """an editing-app audio clip: dark header band with the note / fx marks, dense filled waveform, fade handles"""
    x, w = a * PX, (b - a) * PX - GAP
    hh, wh = HEAD_H, CLIP_H - HEAD_H
    n = int((b - a) * 60)
    pts = [(0, wh)]
    for i in range(n):
        v = ENV[min(int(a * 60) + i, len(ENV) - 1)]
        pts.append((round(i * w / n, 1), round(wh - max(.06, v) * (wh - 6), 1)))
    pts += [(w, pts[-1][1]), (w, wh)]
    path = 'M' + ' L'.join(f'{px} {py}' for px, py in pts) + ' Z'
    two = ' two' if '<br/>' in name else ''
    return (f'<div class="lab{two}" style="left:{x}px;width:{w}px"><div class="nm">{name}</div><div class="vb">{vibe}</div></div>'
            f'<div class="clip" style="left:{x}px;width:{w}px"><div class="hb"><span class="note">♫</span><span class="fx">fx</span></div>'
            f'<svg class="wv" width="{w}" height="{wh}" viewBox="0 0 {w} {wh}" preserveAspectRatio="none"><path d="{path}" fill="{WAVE}"/></svg>'
            f'<span class="fh l"></span><span class="fh r"></span></div>')


def build():
    strip = ''.join(clip(k, *s) for k, s in enumerate(SOUNDS))
    css = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#shade{{position:absolute;left:0;right:0;top:0;height:1000px;z-index:5;
  background:linear-gradient(180deg,rgba(25,14,6,.35) 0%,rgba(25,14,6,.4) 60%,rgba(25,14,6,0) 100%)}}
#strip{{position:absolute;left:0;top:{STRIP_Y - 112}px;height:{CLIP_H + 112}px;z-index:10;will-change:transform}}
.clip{{position:absolute;top:112px;height:{CLIP_H}px;border-radius:5px;background:{BROWN};overflow:hidden;
  box-shadow:0 8px 22px rgba(0,0,0,.35),inset 0 0 0 1px rgba(255,255,255,.14)}}
.hb{{position:absolute;left:0;right:0;top:0;height:{HEAD_H}px;background:{HEAD}}}
.note{{position:absolute;right:46px;top:1px;font:700 21px/24px Poppins;color:#F3E2CF}}
.fx{{position:absolute;right:12px;top:1px;font:italic 400 19px/24px Georgia,serif;color:rgba(243,226,207,.45)}}
.wv{{position:absolute;left:0;bottom:0}}
.fh{{position:absolute;bottom:8px;width:22px;height:22px;border-radius:4px;background:rgba(60,36,20,.55);border:1.5px solid rgba(255,255,255,.55)}}
.fh.l{{left:8px}}
.fh.r{{right:8px}}
.fh:after{{content:'';position:absolute;inset:4px;background:rgba(255,255,255,.75)}}
.fh.l:after{{clip-path:polygon(100% 0,100% 100%,0 100%)}}
.fh.r:after{{clip-path:polygon(0 0,100% 100%,0 100%)}}
.lab{{position:absolute;top:22px;text-align:center;overflow:hidden;white-space:nowrap;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.6)}}
.lab.two{{top:-14px}}
.nm{{font:700 34px/1.08 Poppins;letter-spacing:-.01em;padding:0 10px}}
.lab.two .nm{{font-size:31px}}
.vb{{font:italic 400 28px/1.2 Inter,Poppins;opacity:.92;margin-top:4px}}
#ph{{position:absolute;left:{PLAY_X - 3}px;top:{STRIP_Y - 8}px;width:6px;height:{CLIP_H + 30}px;background:#fff;z-index:12;border-radius:3px;
  box-shadow:0 0 12px rgba(0,0,0,.45)}}
#ph:before{{content:'';position:absolute;left:-11px;top:-14px;border-left:14px solid transparent;border-right:14px solid transparent;
  border-top:18px solid #fff}}
'''
    # zooms on her (origin on her face): slow push / punch-in on each new sound / zoom out
    zoom = [(0.0, 1.0, 1.12, 4.25, 'sine.inOut'), (4.3, 1.28, 1.28, .01, 'none'), (4.32, 1.28, 1.05, 3.5, 'power2.out'),
            (7.9, 1.05, 1.0, .01, 'none'), (7.92, 1.0, 1.18, 3.9, 'sine.inOut'), (11.9, 1.34, 1.34, .01, 'none'),
            (11.92, 1.34, 1.0, DUR - 11.92, 'power1.inOut')]
    tw = ["gsap.set('#bgv',{transformOrigin:'42% 34%'});"]
    tw += [f"tl.fromTo('#bgv',{{scale:{a}}},{{scale:{b},duration:{d:.2f},ease:'{e}',immediateRender:{'true' if t == 0 else 'false'}}},{t:.2f});"
           for t, a, b, d, e in zoom]
    tw += [          f"tl.fromTo('#strip',{{x:{PLAY_X}}},{{x:{PLAY_X - DUR * PX:.1f},duration:{DUR:.3f},ease:'none',immediateRender:true}},0);",
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
