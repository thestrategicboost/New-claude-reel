#!/usr/bin/env python3
"""Short text-hook reel, cloned from her best performer (src/ref.mp4): B-roll of her, a brown Anton block with the
hook, a white rounded pill under it where the second line types itself letter by letter, then "Lis la description"
in small white italic. Same ambient sound as the original, a soft keyboard sound while the line types, a pop on the
block and on "Lis la description". Four variants, each with its own B-roll and its own angle on the same topic.

PY build.py <1-4>      writes index.html
"""
import json
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DUR = 5.3
DARK = '#573307'
HOOKS = {
    1: ('COMMENT FORCER INSTA', 'à montrer tes réels à des non abonnés'),
    2: ('TES RÉELS BLOQUENT À 200 VUES ?', 'voici comment toucher des non abonnés'),
    3: ("L'OPTION CACHÉE D'INSTAGRAM", 'pour montrer tes réels à des non abonnés'),
    4: ('ARRÊTE DE PUBLIER POUR TES ABONNÉS', 'fais voir tes réels à des inconnus'),
}
TYPE_A, TYPE_B, DESC = .15, 1.95, 2.05       # same rhythm as the original


def build():
    big, line = HOOKS[N]
    n = len(line)
    T = ["gsap.set('#blk',{autoAlpha:0});", "tl.fromTo('#blk',{autoAlpha:0,scale:.8},{autoAlpha:1,scale:1,duration:.22,ease:'back.out(2)',immediateRender:true},0.02);",
         "gsap.set('#pl',{autoAlpha:0});", "tl.fromTo('#pl',{autoAlpha:0,scaleX:.3},{autoAlpha:1,scaleX:1,duration:.18,ease:'power3.out',immediateRender:false},.08);",
         "tl.set('#tx',{textContent:''},0);"]
    T += [f"tl.set('#tx',{{textContent:{json.dumps(line[:i])}}},{TYPE_A + (TYPE_B - TYPE_A) * i / n:.3f});" for i in range(1, n + 1)]
    T += ["gsap.set('#ds',{autoAlpha:0});", f"tl.fromTo('#ds',{{autoAlpha:0,y:12}},{{autoAlpha:1,y:0,duration:.2,ease:'power2.out',immediateRender:false}},{DESC:.3f});"]
    sfx = [('pop', .02, .5, .72), ('typing', TYPE_A, .55, 1.9), ('pop', DESC, .4, .72)]
    audio = '\n'.join(f'<audio id="s{k}" src="assets/sfx/{s}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" data-track-index="{10 + k}" data-volume="{v}"></audio>'
                      for k, (s, t, v, d) in enumerate(sfx))
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
.hk{{position:absolute;left:0;right:0;top:300px;z-index:20;text-align:center}}
#blk{{display:inline-block;max-width:820px;background:{DARK};color:#fff;font:400 76px/1.08 Anton;letter-spacing:.03em;padding:10px 26px 6px}}
#pl{{position:relative;display:inline-block;max-width:820px;height:62px;margin-top:-4px;border-radius:31px;background:#fff;padding:0 30px;transform-origin:50% 50%}}
.gh{{visibility:hidden}}
#tx,.gh{{font:italic 800 38px/62px Poppins;letter-spacing:-.02em;color:{DARK};white-space:nowrap}}
#tx{{position:absolute;left:30px;top:0}}
#ds{{margin-top:16px;font:italic 700 34px/1 Poppins;color:#fff;text-shadow:0 2px 2px rgba(0,0,0,.35),0 4px 14px rgba(0,0,0,.45)}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="amb" src="assets/ref_audio.m4a" data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
{audio}
  <video id="bgv" class="full" src="assets/v{N}.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
  <div class="hk"><div id="blk">{big}</div><br/><div id="pl"><span class="gh">{line}</span><span id="tx"></span></div><div id="ds">Lis la description</div></div>
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
