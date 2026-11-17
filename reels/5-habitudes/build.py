#!/usr/bin/env python3
"""« 5 habitudes pour forcer Insta » on other B-rolls: big white 5 + her brown block on screen from frame 0, the white pill
« à montrer tes réels à des non-abonnés » types itself letter by letter with her keyboard sound (her signature), then
« Lis la description ». No other sound (B-roll muted).   PY build.py <n>"""
import json, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DUR, DARK = 6.0, '#523301'
PILL = 'à montrer tes réels à des non-abonnés'
TA, TB, DESC = .15, 1.95, 2.6      # « Lis la description » a beat after the pill (her ask)
T = ["tl.set('#tx',{textContent:''},0);"] + [f"tl.set('#tx',{{textContent:{json.dumps(PILL[:i])}}},{TA + (TB - TA) * i / len(PILL):.3f});" for i in range(1, len(PILL) + 1)]
T += ["gsap.set('#ds',{autoAlpha:0});", f"tl.fromTo('#ds',{{autoAlpha:0,y:12}},{{autoAlpha:1,y:0,duration:.2,ease:'power2.out',immediateRender:false}},{DESC});"]
html = f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#w{{position:absolute;left:0;right:0;top:340px;z-index:20;text-align:center}}
.row{{display:inline-flex;align-items:flex-end}}
.five{{font:400 380px/.78 Anton;color:#fff;margin-right:-30px;position:relative;z-index:2;text-shadow:0 6px 24px rgba(0,0,0,.18)}}
.blk{{background:{DARK};color:#fff;font:400 74px/1.14 Anton;letter-spacing:.05em;padding:14px 26px 8px 50px;text-align:left;margin-bottom:6px}}
.pill{{position:relative;z-index:3;display:inline-block;margin-top:-26px;background:#fff;border-radius:44px;padding:4px 34px 10px;
 font:italic 800 46px/1.25 Poppins;letter-spacing:-.05em;color:{DARK};white-space:nowrap}}
.gh{{visibility:hidden}} #tx{{position:absolute;left:34px;top:4px}}
#ds{{margin-top:44px;font:italic 800 40px/1 Poppins;letter-spacing:-.05em;color:#fff;text-shadow:0 3px 3px rgba(0,0,0,.3),0 6px 16px rgba(0,0,0,.35)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="typ" src="assets/sfx/typing.mp3" data-start="{TA}" data-duration="1.8" data-track-index="2" data-volume="0.6"></audio>
  <video id="bgv" class="full" src="assets/v{N}.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
  <div id="w"><div class="row"><span class="five">5</span><div class="blk">HABITUDES POUR<br/>FORCER INSTA</div></div><br/>
  <div class="pill"><span class="gh">{PILL}</span><span id="tx"></span></div><div id="ds">Lis la description</div></div>
</div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(T)}
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;</script></body></html>
'''
open('index.html', 'w', encoding='utf-8').write(html)
print('ok', N)
