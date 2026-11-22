#!/usr/bin/env python3
"""« Tu ne sais pas quoi poster cette semaine ? / vole ces 5 hooks pour ta semaine : » — her weekly hooks reel
(src/ref.mov) rebuilt on a new B-roll, layout and timing measured on her video: title block on screen from frame 0,
the pill types itself 0-0.8 s, the five days (white boxes, her brown italic Poppins) land together at 1.0 s.

PY build.py      writes index.html (assets/v1.mp4)
"""
import json

DUR = 5.16
DARK = '#523301'
PILL = 'vole ces 5 hooks pour ta semaine :'
# this week's hooks (fill-in templates, like hers)
DAYS = [      # this week's hooks — generic fill-in templates any creator can use in HER OWN niche (her rule, 22 Nov:
    # not about Instagram / views / clients, she is the Instagram coach, her audience works in every kind of métier)
    ('LUNDI :', 46, 770, ['Tu fais sûrement cette erreur', 'quand tu [action du quotidien].']),
    ('MARDI :', 46, 945, ['Le mythe sur [sujet] que tout', 'le monde croit encore.']),
    ('MERCREDI :', 34, 1110, ['Ce que je ne ferai plus jamais', 'après [X] ans en tant que [métier].']),
    ('JEUDI :', 40, 1290, ['Si tu veux [résultat], commence', 'par arrêter de [mauvaise habitude].']),
    ('VENDREDI :', 34, 1475, ['La question qu’on me pose', 'tous les jours : [question].']),
]


def build():
    H, T = [], []
    H.append(f'<div class="hk"><div class="blk"><span>TU NE SAIS PAS QUOI POSTER</span><br/><span>CETTE SEMAINE ?</span></div>'
             f'<div class="pill"><span class="gh">{PILL}</span><span id="tx"></span></div></div>')
    T += ["tl.set('#tx',{textContent:''},0);"]
    T += [f"tl.set('#tx',{{textContent:{json.dumps(PILL[:i])}}},{.05 + .75 * i / len(PILL):.3f});" for i in range(1, len(PILL) + 1)]
    for k, (day, fs, y, lines) in enumerate(DAYS):
        H.append(f'<div id="d{k}" class="day" style="top:{y}px"><div class="lab" style="font-size:{fs}px">{day}</div>'
                 f'<div class="txt">{"<br/>".join(f"<span>{l}</span>" for l in lines)}</div></div>')
        T += [f"gsap.set('#d{k}',{{autoAlpha:0}});", f"tl.set('#d{k}',{{autoAlpha:1}},1.0);"]
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
.hk{{position:absolute;left:0;right:0;top:335px;z-index:20;text-align:center}}
.blk{{line-height:0}}
.blk span{{display:inline-block;background:{DARK};color:#fff;font:400 74px/1.28 Anton;letter-spacing:.06em;padding:0 26px}}
.pill{{position:relative;display:inline-block;margin-top:2px;height:70px;border-radius:35px;background:#fff;padding:0 26px;
  font:italic 800 44px/70px Poppins;letter-spacing:-.05em;color:{DARK};white-space:nowrap}}
.gh{{visibility:hidden}}
#tx{{position:absolute;left:26px;top:0}}
.day{{position:absolute;left:0;right:0;z-index:20}}
.lab{{position:absolute;left:80px;width:190px;text-align:center;background:#fff;color:{DARK};font-family:Poppins;font-style:italic;font-weight:800;
  letter-spacing:-.04em;line-height:70px;height:70px;top:10px}}
.txt{{position:absolute;left:310px;line-height:0}}
.txt span{{display:inline-block;background:#fff;color:{DARK};font:italic 800 34px/46px Poppins;letter-spacing:-.04em;padding:0 14px;white-space:nowrap}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="amb" src="assets/ref_audio.m4a" data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/v1.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
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
    print('wrote index.html')
