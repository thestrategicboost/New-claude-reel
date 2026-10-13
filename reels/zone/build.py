#!/usr/bin/env python3
"""Reel "zone": where to put things in an Instagram reel (safe zone, zones to avoid, eye line, captions, text hook,
wide shot for zooms), edited like the "Zone Brian" reference: green / red translucent zones drawn over the speaker
as she points at them, in Maé's branding (dark-brown Anton label blocks, white Poppins word-by-word captions).

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
EYE_Y = 772                     # her eye line in the frame
CAP_Y = 1065                    # captions sit just under her mouth (the advice of the video)
GREEN, GREEN_B = 'rgba(70,205,110,.30)', 'rgba(140,255,170,.95)'
RED = 'rgba(235,55,55,.36)'
BLOCK = '#573307'               # her dark-brown title blocks

with open('work/src/raw_words.json', encoding='utf-8') as _f:
    RAW = json.load(_f)
FIX = {'hoop': 'hook', 'cheat.': 'texte.', 'Tchuss': 'Tchus'}


def words():
    out = []
    for w in RAW:
        t = w['text']
        if out and t[:1] in "'’-" and len(t) > 1:
            out[-1]['text'] += t
            out[-1]['end'] = w['end']
            continue
        out.append(dict(w))
    res = []
    for w in out:
        t = FIX.get(w['text'], w['text'])
        t = re.sub(r'[.,!?;:]', '', t).replace("'", '’').strip()
        if t:
            res.append({'text': t, 'start': w['start'], 'end': w['end']})
    for i, w in enumerate(res):                      # "ton hook de texte" -> "ton hook texte"
        if w['text'] == 'de' and i and res[i - 1]['text'] == 'hook':
            w['text'] = ''
    return [w for w in res if w['text']]


def show(sel, a, b):
    tw = [f"gsap.set('{sel}',{{autoAlpha:0}});", f"tl.set('{sel}',{{autoAlpha:1}},{a:.3f});"]
    if b < DUR - .01:
        tw.append(f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});")
    return tw


def pop(sel, t, d=.3, s=.6):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{{autoAlpha:0,scale:{s}}},{{autoAlpha:1,scale:1,duration:{d},ease:'back.out(1.8)',immediateRender:false}},{t:.3f});"]


def fade(sel, a, b, d=.25):
    """zone overlays: quick fade in, fade out"""
    tw = [f"gsap.set('{sel}',{{autoAlpha:0}});",
          f"tl.fromTo('{sel}',{{autoAlpha:0}},{{autoAlpha:1,duration:{d},immediateRender:false}},{a:.3f});"]
    if b < DUR - .01:
        tw.append(f"tl.to('{sel}',{{autoAlpha:0,duration:.2}},{b - .2:.3f});")
    return tw


def label(lid, text, x, y, t, b, size=56):
    html = [f'<div id="{lid}" class="lbl" style="left:{x}px;top:{y}px;font-size:{size}px">{text}</div>']
    return html, pop(f'#{lid}', t, .28, .5) + [f"tl.set('#{lid}',{{autoAlpha:0}},{b:.3f});"]


# ------------------------------------------------------------------ the zones, in the order she points at them
def zones():
    html, tw = [], []
    # 1. strategic (safe) zone
    html.append('<div id="zSafe" class="zone g" style="left:70px;top:230px;width:850px;height:1230px"></div>')
    tw += [f"tl.fromTo('#zSafe',{{scale:1.08}},{{scale:1,duration:.4,ease:'power3.out',immediateRender:true}},0);",
           "gsap.set('#zSafe',{autoAlpha:1});", "tl.to('#zSafe',{autoAlpha:0,duration:.2},3.0);", "tl.set('#zSafe',{autoAlpha:0},3.2);"]
    h, t = label('lSafe', 'ZONE STRATÉGIQUE', 110, 270, 0.0, 3.2)
    html += h
    tw += t + ["tl.set('#lSafe',{autoAlpha:1,scale:1},0);"]
    # 2. zones to avoid (top, bottom, Instagram buttons column)
    html.append('<div id="zRed">'
                '<div class="zone r" style="left:0;top:0;width:1080px;height:220px"></div>'
                '<div class="zone r" style="left:0;top:1470px;width:1080px;height:450px"></div>'
                '<div id="zRight" class="zone r" style="left:940px;top:220px;width:140px;height:1250px"></div></div>')
    tw += fade('#zRed', 3.22, 8.25)
    tw.append("tl.fromTo('#zRight',{backgroundColor:'rgba(235,55,55,.36)'},{backgroundColor:'rgba(235,55,55,.62)',duration:.25,yoyo:true,repeat:3,immediateRender:false},5.50);")
    h, t = label('lRed', 'ZONE À ÉVITER', 300, 80, 3.30, 8.25)
    html += h
    tw += t
    # fake Instagram buttons + a text that hides under them
    icons = ''.join(f'<div class="igi">{s}</div>' for s in IG_ICONS)
    html.append(f'<div id="igcol">{icons}</div>')
    tw += pop('#igcol', 5.55, .3, .7) + ["tl.set('#igcol',{autoAlpha:0},8.25);"]
    tw += ["gsap.set('#igcol .igi',{autoAlpha:0});",
           "tl.fromTo('#igcol .igi',{autoAlpha:0,x:30},{autoAlpha:1,x:0,duration:.18,stagger:.07,immediateRender:false},5.60);"]
    html.append('<div id="badTxt">Mon super texte ici</div>')
    tw += pop('#badTxt', 6.55, .25, .7) + ["tl.set('#badTxt',{autoAlpha:0},8.25);"]
    html.append('<div id="badX"><svg viewBox="0 0 100 100" width="150" height="150"><circle cx="50" cy="50" r="44" fill="#E53935"/>'
                '<path d="M32 32l36 36M68 32L32 68" stroke="#fff" stroke-width="11" stroke-linecap="round"/></svg></div>')
    tw += pop('#badX', 7.40, .3, .3) + ["tl.set('#badX',{autoAlpha:0},8.25);"]
    # 3. eye line, stays put while the picture zooms in and out
    html.append(f'<div id="zEye" class="zone g" style="left:110px;top:{EYE_Y - 55}px;width:830px;height:110px"></div>'
                f'<div id="eyeLine" style="top:{EYE_Y}px"></div>')
    tw += fade('#zEye', 8.70, 13.85) + fade('#eyeLine', 8.70, 13.85)
    tw.append("tl.fromTo('#eyeLine',{scaleX:0},{scaleX:1,duration:.4,ease:'power2.out',immediateRender:false},8.70);")
    h, t = label('lEye', 'LIGNE DES YEUX', 110, EYE_Y - 150, 8.75, 13.85, 48)
    html += h
    tw += t
    # 4. captions zone, the real captions sit inside it
    html.append(f'<div id="zCap" class="zone g" style="left:120px;top:{CAP_Y - 70}px;width:840px;height:140px"></div>')
    tw += fade('#zCap', 14.24, 17.60)
    h, t = label('lCap', 'SOUS-TITRES', 120, CAP_Y - 165, 14.30, 17.60, 48)
    html += h
    tw += t
    # 5. text hook at the top of the safe zone
    html.append('<div id="zHook" class="zone g" style="left:120px;top:240px;width:840px;height:170px"></div>')
    tw += fade('#zHook', 18.24, 19.55)
    html.append('<div id="hookDemo" class="lbl" style="left:0;right:0;top:270px;margin:0 auto;width:max-content;font-size:84px">TON HOOK ICI</div>')
    tw += pop('#hookDemo', 18.80, .3, .5) + ["tl.set('#hookDemo',{autoAlpha:0},19.55);"]
    # 6. wide shot: frame marks, then a zoom in and a zoom out
    html.append('<div id="marks">' + ''.join(f'<i class="mk {c}"></i>' for c in ('tl', 'tr', 'bl', 'br')) + '</div>')
    tw += fade('#marks', 21.20, 23.95)
    tw.append("tl.fromTo('#marks',{scale:1.12},{scale:1,duration:.4,ease:'power3.out',immediateRender:false},21.20);")
    h, t = label('lWide', 'PLAN LARGE', 330, 270, 21.30, 23.95)
    html += h
    tw += t
    # zooms on the picture (the eye-line demo zooms around her eyes so they stay on the line)
    tw += [f"tl.to('#stage',{{scale:1.22,duration:.35,ease:'power2.out'}},10.70);",
           f"tl.to('#stage',{{scale:1,duration:.35,ease:'power2.out'}},11.38);",
           "tl.set('#stage',{transformOrigin:'50% 50%'},21.0);",
           "tl.to('#stage',{scale:1.2,duration:.3,ease:'power2.out'},22.62);",
           "tl.to('#stage',{scale:1,duration:.3,ease:'power2.out'},23.36);"]
    return html, tw


IG_ICONS = [   # white Instagram-style side buttons
    '<svg viewBox="0 0 24 24" width="62" height="62"><path d="M12 21s-7.5-4.6-9.5-9.2C1 8.4 3.2 5 6.6 5c2.1 0 3.4 1.2 4.4 2.5C12 6.2 13.3 5 15.4 5 18.8 5 21 8.4 19.5 11.8 17.5 16.4 12 21 12 21z" fill="none" stroke="#fff" stroke-width="2"/></svg>',
    '<svg viewBox="0 0 24 24" width="62" height="62"><path d="M20.5 11.5a8.5 8.5 0 1 1-3.4-6.8 8.4 8.4 0 0 1 3.4 6.8zM20.5 20.5l-2-4" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>',
    '<svg viewBox="0 0 24 24" width="62" height="62"><path d="M21 3L3 10l7 3 3 7z M10 13L21 3" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></svg>',
    '<svg viewBox="0 0 24 24" width="62" height="62"><circle cx="5" cy="12" r="2" fill="#fff"/><circle cx="12" cy="12" r="2" fill="#fff"/><circle cx="19" cy="12" r="2" fill="#fff"/></svg>',
]


# ------------------------------------------------------------------ captions: one word at a time
def captions():
    html, tw = [], []
    ws = words()
    for k, w in enumerate(ws):
        a = max(0.0, w['start'] - .03)
        b = ws[k + 1]['start'] - .03 if k + 1 < len(ws) else DUR
        b = min(b, a + 1.2)
        if b - a < .06:
            continue
        html.append(f'<div id="cp{k}" class="cap">{w["text"]}</div>')
        tw += show(f'#cp{k}', a, b)
        tw.append(f"tl.fromTo('#cp{k}',{{scale:1.3,y:10}},{{scale:1,y:0,duration:.14,ease:'back.out(2.2)',immediateRender:false}},{a:.3f});")
    return html, tw


# ------------------------------------------------------------------ follow card
def follow():
    html = ['<div id="fol"><div class="fav"><img src="assets/avatar.png"/></div><div class="fnm">thestrategicboost.fr'
            '<div class="fsub">Stratégie Instagram</div></div><div id="fbtn" class="fbtn">S’abonner</div>'
            '<div id="fbtn2" class="fbtn on">Abonné</div></div>']
    tw = pop('#fol', 24.30, .35, .7) + show('#fbtn2', 25.35, DUR) + [
        "tl.to('#fbtn',{scale:.85,duration:.08,yoyo:true,repeat:1},25.20);", "tl.set('#fbtn',{autoAlpha:0},25.35);"]
    return html, tw


def sfx_list():
    out = [('pop', 0.0, .22), ('whoosh-short', 3.22, .24), ('pop', 3.30, .2), ('click-soft', 5.55, .3), ('pop', 6.55, .2),
           ('impact-bass-1', 7.40, .22), ('whoosh-short', 8.70, .22), ('pop', 8.75, .2), ('whoosh-short', 10.70, .2),
           ('whoosh-short', 11.38, .18), ('pop', 14.30, .22), ('pop', 18.80, .24), ('pop', 21.30, .2),
           ('whoosh-short', 22.62, .2), ('whoosh-short', 23.36, .18), ('pop', 24.30, .24), ('click', 25.20, .4),
           ('sparkle', 25.35, .14)]
    return out


SFX_LEN = {'whoosh-short': .57, 'pop': .72, 'sparkle': 1.8, 'click': .36, 'click-soft': .36, 'impact-bass-1': 1.2}


def audio():
    out, lanes = [], []
    for k, (name, t, vol) in enumerate(sorted(sfx_list(), key=lambda x: x[1])):
        d = min(SFX_LEN[name], DUR - t)
        lane = next((i for i, end in enumerate(lanes) if end <= t), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{name}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{vol * .75:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;inset:0;transform-origin:50% {EYE_Y}px}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.zone{{position:absolute;z-index:5;border-radius:26px}}
.zone.g{{background:{GREEN};border:4px solid {GREEN_B};box-shadow:0 0 40px rgba(70,205,110,.35)}}
.zone.r{{background:{RED};border-radius:0}}
#zRed{{position:absolute;inset:0;z-index:5}}
.lbl{{position:absolute;z-index:12;font-family:Anton;letter-spacing:.02em;color:#fff;background:{BLOCK};padding:6px 22px 4px;
  box-shadow:0 10px 26px rgba(0,0,0,.3)}}
#igcol{{position:absolute;z-index:9;left:968px;top:1130px;display:flex;flex-direction:column;gap:38px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5))}}
#badTxt{{position:absolute;z-index:8;left:520px;top:1300px;font:800 64px/1.05 Poppins;color:#fff;width:520px;
  text-shadow:0 0 18px rgba(0,0,0,.6),0 3px 8px rgba(0,0,0,.5)}}
#badX{{position:absolute;z-index:11;left:690px;top:1270px}}
#eyeLine{{position:absolute;z-index:6;left:40px;right:40px;height:0;border-top:5px dashed #fff;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5))}}
#marks{{position:absolute;inset:0;z-index:6}}
.mk{{position:absolute;width:120px;height:120px;border:0 solid #fff;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5))}}
.mk.tl{{left:70px;top:230px;border-top-width:10px;border-left-width:10px}}
.mk.tr{{right:140px;top:230px;border-top-width:10px;border-right-width:10px}}
.mk.bl{{left:70px;top:1340px;border-bottom-width:10px;border-left-width:10px}}
.mk.br{{right:140px;top:1340px;border-bottom-width:10px;border-right-width:10px}}
.cap{{position:absolute;left:0;right:0;top:{CAP_Y - 52}px;z-index:20;text-align:center;font:700 84px/1.1 Poppins;color:#fff;letter-spacing:-.03em;
  text-shadow:0 0 24px rgba(0,0,0,.6),0 4px 12px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.5);white-space:nowrap;transform-origin:50% 50%}}
#fol{{position:absolute;z-index:15;left:110px;top:1240px;width:830px;height:150px;background:#fff;border-radius:28px;display:flex;align-items:center;
  gap:22px;padding:0 26px;box-shadow:0 18px 50px rgba(0,0,0,.3)}}
.fav{{width:100px;height:100px;border-radius:50%;padding:4px;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.fav img{{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid #fff;display:block}}
.fnm{{flex:1;font:700 34px/1.2 Poppins;color:#111}}
.fsub{{font:500 26px/1.2 Poppins;color:#777}}
.fbtn{{position:absolute;right:26px;width:220px;height:74px;border-radius:16px;background:#0095F6;color:#fff;font:700 30px/74px Poppins;text-align:center}}
.fbtn.on{{background:#EFEFEF;color:#111}}
'''


def build():
    parts = [zones(), captions(), follow()]
    html = '\n'.join('\n'.join(h) for h, _ in parts)
    tw = '\n'.join('\n'.join(t) for _, t in parts)
    nl = '\n'
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="assets/vendor/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(audio())}
  <div id="stage"><video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video></div>
{html}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{tw}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s, {len(words())} words')
