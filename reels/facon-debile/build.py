#!/usr/bin/env python3
"""« La façon la plus débile de passer de ça… à ça… » — her reel that worked (src/ref.mp4), rebuilt EXACTLY on other B-rolls:
same texts, same positions and timings (measured on her video), her real view-count screenshots (assets/crops, cut from her
video), her original sound (assets/ref_audio.m4a).

PY build.py <n>      writes index.html for assets/v<n>.mp4
"""
import json
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DUR = 6.267
DARK = '#573307'
P1 = 'de passer de ça…'
# (id, image, x, y, w, h, time) — positions and appearance times measured on her reel
BEFORE = [('b0', 'v261', 185, 510, 177, 79, .50), ('b1', 'v337', 426, 515, 227, 79, .77), ('b2', 'v409', 713, 511, 185, 73, 1.03)]
AFTER = [('a0', 'v290k', 162, 759, 231, 77, 2.30), ('a1', 'v352k', 443, 752, 194, 82, 2.67), ('a2', 'v629k', 695, 747, 223, 97, 3.03)]


def build():
    T, H = [], []
    H.append('<div class="hk"><div class="blk">LA FAÇON LA PLUS DÉBILE</div><br/>'
             f'<div id="p1" class="pill"><span class="gh">{P1}</span><span id="tx"></span></div></div>')
    T += ["gsap.set('#p1',{autoAlpha:1});", "tl.set('#tx',{textContent:''},0);"]
    T += [f"tl.set('#tx',{{textContent:{json.dumps(P1[:i])}}},{.05 + .22 * i / len(P1):.3f});" for i in range(1, len(P1) + 1)]
    for i, img, x, y, w, h, t in BEFORE + AFTER:
        H.append(f'<img id="{i}" class="crop" src="assets/crops/{img}.png" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"/>')
        T += [f"gsap.set('#{i}',{{autoAlpha:0}});",
              f"tl.fromTo('#{i}',{{autoAlpha:0,scale:.5}},{{autoAlpha:1,scale:1,duration:.18,ease:'back.out(2.2)',immediateRender:false}},{t:.3f});"]
    for i, txt, y, t in (('p2', 'à ça…', 640, 1.77), ('p3', 'lis la description', 900, 4.27)):
        H.append(f'<div id="{i}" class="pw" style="top:{y}px"><span class="pill">{txt}</span></div>')
        T += [f"gsap.set('#{i}',{{autoAlpha:0}});",
              f"tl.fromTo('#{i}',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.18,ease:'back.out(2)',immediateRender:false}},{t:.3f});"]
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
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.hk{{position:absolute;left:0;right:0;top:277px;z-index:20;text-align:center}}
.blk{{display:inline-block;background:{DARK};color:#fff;font:400 80px/1.22 Anton;letter-spacing:.05em;padding:4px 26px 0}}
.pill{{position:relative;display:inline-block;height:72px;margin-top:-8px;border-radius:36px;background:#fff;padding:0 26px;
  font:italic 800 46px/72px Poppins;letter-spacing:-.04em;color:{DARK};white-space:nowrap}}
.gh{{visibility:hidden}}
#tx{{position:absolute;left:26px;top:0}}
.pw{{position:absolute;left:0;right:0;z-index:20;text-align:center}}
.pw .pill{{margin:0}}
.crop{{position:absolute;z-index:19;object-fit:cover}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="amb" src="assets/ref_audio.m4a" data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/v{N}.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
{chr(10).join(H)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(T)}
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


if __name__ == '__main__':
    with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
        _f.write(build())
    print(f'wrote index.html (variante {N})')
