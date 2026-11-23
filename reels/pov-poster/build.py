#!/usr/bin/env python3
"""« POV : Tu commences à poster sur les réseaux » — her own video (src/pov.mp4), only the first title changed to her
charter: the old burned-in text is covered by a feathered wall patch (work/clean.mp4, ffmpeg), then rewritten here:
« POV : » in her brown block (Anton, white), the line in her white pill (Poppins italic 800, brown), same place, same
time (0 -> 2.43 s, until her cut). Everything else untouched.     PY build.py"""
DUR, T_END, DARK = 7.33, 2.433, '#523301'
html = f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#t{{position:absolute;left:0;right:0;top:450px;z-index:20;text-align:center}}
.blk{{display:inline-block;background:{DARK};color:#fff;font:400 96px/1.1 Anton;letter-spacing:.05em;padding:8px 40px 2px}}
.pw{{line-height:0;margin-top:-6px}}
.pw span{{display:inline-block;background:#fff;color:{DARK};font:italic 800 50px/1.45 Poppins;letter-spacing:-.04em;padding:0 30px;border-radius:40px;margin:-4px 0}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="aud" src="assets/audio.m4a" data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/clean.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
  <div id="t"><div class="blk">POV :</div><div class="pw"><span>Tu commences à poster</span><br/><span>sur les réseaux</span></div></div>
</div>
<script>const tl = gsap.timeline({{ paused: true }});
tl.set('#t',{{autoAlpha:0}},{T_END});
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;</script></body></html>
'''
open('index.html', 'w', encoding='utf-8').write(html)
print('ok')
