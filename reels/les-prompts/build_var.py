#!/usr/bin/env python3
"""Variants of « Les prompts » on her other B-rolls (assets/v<n>.mp4, retouched, not darkened): same texts, same
timing as her validated version.   PY build_var.py <n>
(original doc:) « Les prompts » — her own video (src/v.mp4); only the text changed to her charter: the burned-in white text is
removed by inpaint.py (work/clean.mp4) and rewritten here, same place, whole video: the first sentence in her brown block
(Anton, white), the rest in her white pills (Poppins italic 800, brown); « Utilise ces prompts… » lands 0.8 s after the title (her ask).      PY build.py"""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DUR, DARK = 7.59, '#523301'
html = f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#t{{position:absolute;left:0;right:0;top:360px;z-index:20;text-align:center;filter:drop-shadow(0 10px 22px rgba(0,0,0,.28))}}
.blk{{line-height:0}}
.blk span{{display:inline-block;background:{DARK};color:#fff;font:400 64px/1.24 Anton;letter-spacing:.04em;padding:0 26px}}
.pw{{line-height:0;margin-top:-2px}}
.pw span{{display:inline-block;background:#fff;color:{DARK};font:italic 800 42px/1.5 Poppins;letter-spacing:-.04em;padding:0 28px;border-radius:36px;margin:-3px 0}}
.gap{{height:22px}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="aud" src="assets/audio.m4a" data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/v{N}.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
  <div id="t"><div class="blk"><span>ARRÊTE DE COPIER-COLLER</span><br/><span>LES RÉPONSES DE CHATGPT !</span></div>
  <div class="pw"><span>On voit que c’est pas toi qui as écrit…</span></div><div class="gap"></div>
  <div id="p2" class="pw"><span>Utilise ces prompts à la place</span><br/><span>pour humaniser ton compte.</span></div></div>
</div>
<script>const tl = gsap.timeline({{ paused: true }});
gsap.set('#p2',{{autoAlpha:0}});
tl.fromTo('#p2',{{autoAlpha:0,y:12}},{{autoAlpha:1,y:0,duration:.25,ease:'power2.out',immediateRender:false}},0.8);
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;</script></body></html>
'''
open('index.html', 'w', encoding='utf-8').write(html)
print('ok', N)
