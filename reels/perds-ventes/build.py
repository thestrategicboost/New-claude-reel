#!/usr/bin/env python3
"""« Tu perds des ventes à cause de ta bio » on her B-rolls: her brown block on screen from frame 0, the white pill types
itself with her keyboard sound (her signature), then « Lis la description » with her cling. B-roll muted.  PY build.py <n>"""
import json, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DUR, DARK = 6.0, '#523301'
PILL = 'à cause de ta bio'
TA, TB, DESC = .15, 1.05, 1.75
T = ["tl.set('#tx',{textContent:''},0);"] + [f"tl.set('#tx',{{textContent:{json.dumps(PILL[:i])}}},{TA + (TB - TA) * i / len(PILL):.3f});" for i in range(1, len(PILL) + 1)]
T += ["gsap.set('#ds',{autoAlpha:0});", f"tl.fromTo('#ds',{{autoAlpha:0,y:12}},{{autoAlpha:1,y:0,duration:.2,ease:'power2.out',immediateRender:false}},{DESC});"]
html = f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#w{{position:absolute;left:0;right:0;top:360px;z-index:20;text-align:center}}
.blk{{display:inline-block;background:{DARK};color:#fff;font:400 76px/1.2 Anton;letter-spacing:.06em;padding:10px 30px 4px}}
.pill{{position:relative;z-index:3;display:inline-block;margin-top:-14px;background:#fff;border-radius:44px;padding:4px 40px 10px;
 font:italic 800 56px/1.25 Poppins;letter-spacing:-.05em;color:{DARK};white-space:nowrap}}
.gh{{visibility:hidden}} #tx{{position:absolute;left:40px;top:4px}}
#ds{{margin-top:44px;font:italic 800 40px/1 Poppins;letter-spacing:-.05em;color:#fff;text-shadow:0 3px 3px rgba(0,0,0,.3),0 6px 16px rgba(0,0,0,.35)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="cling" src="assets/sfx/cling.mp3" data-start="{DESC - .03:.3f}" data-duration="1.0" data-track-index="3" data-volume="1"></audio>
  <audio id="typ" src="assets/sfx/typing.mp3" data-start="{TA}" data-duration="0.95" data-track-index="2" data-volume="0.6"></audio>
  <video id="bgv" class="full" src="assets/v{N}.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
  <div id="w"><div class="blk">TU PERDS DES VENTES</div><br/>
  <div class="pill"><span class="gh">{PILL}</span><span id="tx"></span></div><div id="ds">Lis la description</div></div>
</div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(T)}
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;</script></body></html>
'''
open('index.html', 'w', encoding='utf-8').write(html)
print('ok', N)
