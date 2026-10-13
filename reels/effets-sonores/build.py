#!/usr/bin/env python3
"""Reel "effets sonores": which sound effect to use for what, edited like the "Sound effect" reference (a fixed
"for this / use this" header, a category pill on the left, a sound card on the right) in Maé's branding, and every
sound is played AND shown at work (zoom, pop-ups, suspense push-in, photos with a flash, glitch, follow card).

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
BLOCK = '#573307'
CAP_Y = 1250

with open('work/src/raw_words.json', encoding='utf-8') as _f:
    RAW = json.load(_f)
FIX = {'Clique': 'Clic', 'Tchuss': 'Tchus'}

# (start, end, category, sound name, sound file, length shown)
SECTIONS = [
    (0.00, 2.55, 'Zooms', 'Whoosh', 'whoosh-short', '00:01'),
    (2.68, 5.55, 'Apparitions', 'Pop · Clic', 'pop', '00:01'),
    (5.68, 8.95, 'Suspense', 'Riser', 'riser', '00:03'),
    (9.04, 11.45, 'Photos', 'Camera shutter', 'shutter', '00:01'),
    (11.56, 13.90, 'Impact', 'Glitch', 'glitch', '00:01'),
]


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
        t = re.sub(r'[.,!?;:]', '', FIX.get(w['text'].strip('.,!'), w['text'])).replace("'", '’').strip()
        if t:
            res.append({'text': t, 'start': w['start'], 'end': w['end']})
    return res


def show(sel, a, b):
    tw = [f"gsap.set('{sel}',{{autoAlpha:0}});", f"tl.set('{sel}',{{autoAlpha:1}},{a:.3f});"]
    if b < DUR - .01:
        tw.append(f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});")
    return tw


def pop(sel, t, d=.3, s=.6):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{{autoAlpha:0,scale:{s}}},{{autoAlpha:1,scale:1,duration:{d},ease:'back.out(1.8)',immediateRender:false}},{t:.3f});"]


NOTE = ('<svg viewBox="0 0 24 24" width="40" height="40"><path d="M9 18V5l11-2v13" fill="none" stroke="#fff" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"/><circle cx="6.5" cy="18" r="2.6" fill="#fff"/><circle cx="17.5" cy="16" r="2.6" fill="#fff"/></svg>')


# ------------------------------------------------------------------ header + one pill / sound card per section
def header():
    html = ['<div id="hdr"><div class="hcol"><div class="hb">UTILISE ÇA</div></div><div class="hcol"><div class="hb">POUR ÇA</div></div></div>']
    tw = ["gsap.set('#hdr',{autoAlpha:1});", "tl.fromTo('#hdr',{y:-40},{y:0,duration:.35,ease:'power3.out',immediateRender:true},0);",
          "tl.to('#hdr',{autoAlpha:0,y:-20,duration:.2},13.80);", "tl.set('#hdr',{autoAlpha:0},14.0);"]   # the follow ask is not a sound tip
    for k, (a, b, cat, name, _f, ln) in enumerate(SECTIONS):
        b = b if b is not None else DUR
        bars = ''.join(f'<i style="animation-delay:-{(j * 0.13) % 1:.2f}s"></i>' for j in range(14))
        html.append(f'<div id="pl{k}" class="pill"><span class="pin">{cat}</span></div>')
        html.append(f'<div id="sc{k}" class="card"><div class="ctile">{NOTE}</div><div class="cbody"><div class="cname">{name}</div>'
                    f'<div class="cwave">{bars}</div><div class="cmeta">Effet sonore · {ln}</div></div></div>')
        tw += pop(f'#pl{k}', a + .02, .28, .6) + pop(f'#sc{k}', a + .12, .3, .6)
        if b < DUR - .01:
            tw += [f"tl.to('#pl{k}, #sc{k}',{{autoAlpha:0,y:-10,duration:.12}},{b - .12:.3f});", f"tl.set('#pl{k}, #sc{k}',{{autoAlpha:0}},{b:.3f});"]
        # the waveform bounces while the sound plays
        tw.append(f"tl.fromTo('#sc{k} .cwave i',{{scaleY:.25}},{{scaleY:1,duration:.12,stagger:{{each:.03,repeat:5,yoyo:true}},immediateRender:false}},{a + .2:.3f});")
    return html, tw


# ------------------------------------------------------------------ the sounds at work
def demos():
    html, tw = [], []
    # 1. whoosh: zoom in, zoom out
    tw += ["tl.to('#stage',{scale:1.25,duration:.25,ease:'power3.out'},1.30);",
           "tl.to('#stage',{scale:1,duration:.25,ease:'power3.out'},1.72);",
           "tl.fromTo('#stage',{filter:'blur(0px)'},{filter:'blur(6px)',duration:.12,yoyo:true,repeat:1,immediateRender:false},1.30);",
           "tl.fromTo('#stage',{filter:'blur(0px)'},{filter:'blur(6px)',duration:.12,yoyo:true,repeat:1,immediateRender:false},1.72);"]
    # 2. pop & clic: things appear on screen
    items = [('ap0', 90, 640, '<svg viewBox="0 0 24 24" width="70" height="70"><path d="M12 21s-7.5-4.6-9.5-9.2C1 8.4 3.2 5 6.6 5c2.1 0 3.4 1.2 4.4 2.5C12 6.2 13.3 5 15.4 5 18.8 5 21 8.4 19.5 11.8 17.5 16.4 12 21 12 21z" fill="#fff"/></svg>', 3.36),
             ('ap1', 820, 600, '<svg viewBox="0 0 24 24" width="70" height="70"><path d="M20.5 11.5a8.5 8.5 0 1 1-3.4-6.8 8.4 8.4 0 0 1 3.4 6.8zM20.5 20.5l-2-4" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>', 4.20),
             ('ap2', 830, 900, '<svg viewBox="0 0 24 24" width="70" height="70"><path d="M21 3L3 10l7 3 3 7z M10 13L21 3" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/></svg>', 4.66)]
    for aid, x, y, svg, t in items:
        html.append(f'<div id="{aid}" class="ig" style="left:{x}px;top:{y}px">{svg}</div>')
        tw += pop(f'#{aid}', t, .3, .3) + [f"tl.set('#{aid}',{{autoAlpha:0}},5.55);"]
    # 3. riser: slow push-in + the edges darken
    html.append('<div id="vig"></div>')
    tw += ["tl.to('#stage',{scale:1.18,duration:2.9,ease:'power1.in'},6.0);", "tl.set('#stage',{scale:1},8.95);",
           "gsap.set('#vig',{autoAlpha:0});", "tl.to('#vig',{autoAlpha:1,duration:2.9,ease:'power1.in'},6.0);", "tl.set('#vig',{autoAlpha:0},8.95);"]
    # 4. camera shutter: a white flash and a photo each time
    html.append('<div id="flash"></div>')
    tw.append("gsap.set('#flash',{autoAlpha:0});")
    shots = [('ph0', 60, 560, -8, 10.36, 'r2'), ('ph1', 760, 520, 7, 10.62, 'r4'), ('ph2', 70, 980, 5, 10.94, 'r6'), ('ph3', 770, 950, -6, 11.10, 'r8')]
    for pid, x, y, r, t, img in shots:
        html.append(f'<div id="{pid}" class="photo" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"><img src="assets/photos/{img}.jpg"/></div>')
        tw += pop(f'#{pid}', t, .25, 1.3) + [f"tl.set('#{pid}',{{autoAlpha:0}},11.45);"]
        tw.append(f"tl.fromTo('#flash',{{autoAlpha:.85}},{{autoAlpha:0,duration:.18,immediateRender:false}},{t:.3f});")
    # 5. glitch: the picture splits and shakes
    tw += ["tl.to('#stage',{x:-24,duration:.04,yoyo:true,repeat:5,ease:'none'},12.92);", "tl.set('#stage',{x:0},13.20);",
           "tl.fromTo('#stage',{filter:'hue-rotate(0deg) saturate(1)'},{filter:'hue-rotate(80deg) saturate(2.2)',duration:.05,yoyo:true,repeat:5,immediateRender:false},12.92);",
           "tl.set('#stage',{filter:'none'},13.25);"]
    html.append('<div id="glr" class="gl"></div><div id="glb" class="gl b"></div>')
    tw += ["gsap.set('#glr, #glb',{autoAlpha:0});",
           "tl.fromTo('#glr',{autoAlpha:.55,x:-30},{autoAlpha:0,x:30,duration:.3,ease:'steps(5)',immediateRender:false},12.92);",
           "tl.fromTo('#glb',{autoAlpha:.55,x:30},{autoAlpha:0,x:-30,duration:.3,ease:'steps(5)',immediateRender:false},12.95);"]
    # 6. follow card
    html.append('<div id="fol"><div class="fav"><img src="assets/avatar.png"/></div><div class="fnm">thestrategicboost.fr'
                '<div class="fsub">Stratégie Instagram</div></div><div id="fbtn" class="fbtn">S’abonner</div><div id="fbtn2" class="fbtn on">Abonné</div></div>')
    tw += pop('#fol', 14.20, .35, .7) + show('#fbtn2', 14.62, DUR) + ["tl.to('#fbtn',{scale:.85,duration:.08,yoyo:true,repeat:1},14.46);",
                                                                    "tl.set('#fbtn',{autoAlpha:0},14.62);"]
    return html, tw


# ------------------------------------------------------------------ captions: one word at a time, lowercase
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


def sfx_list():
    out = [('whoosh-short', 1.28, .5), ('whoosh-short', 1.70, .45), ('click', 3.36, .5), ('pop', 4.20, .45), ('pop', 4.66, .45),
           ('riser01-soft', 6.00, .32), ('shutter', 10.36, .6), ('shutter', 10.62, .55), ('shutter', 10.94, .55), ('shutter', 11.10, .5),
           ('glitch', 12.92, .55), ('pop', 14.20, .3), ('click', 14.46, .45)]
    for k, (a, *_r) in enumerate(SECTIONS):                 # soft tick when each new card lands
        if k:
            out.append(('click-soft', a + .12, .25))
    return out


SFX_LEN = {'whoosh-short': .57, 'pop': .72, 'sparkle': 1.8, 'click': .36, 'click-soft': .36, 'riser01-soft': 3.05, 'shutter': .35, 'glitch': .55}


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
                   f'data-track-index="{10 + lane}" data-volume="{vol:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;inset:0;transform-origin:50% 42%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#hdr{{position:absolute;left:40px;right:40px;top:250px;z-index:12;display:flex}}
.hcol{{flex:1;text-align:center}}
.hb{{display:inline-block;font:400 66px/1 Anton;letter-spacing:.02em;color:#fff;background:{BLOCK};padding:8px 26px 6px;box-shadow:0 10px 26px rgba(0,0,0,.3)}}
.pill{{position:absolute;z-index:12;left:540px;width:500px;top:372px;text-align:center}}
.pin{{display:inline-block;background:#fff;color:{BLOCK};font:700 40px/1 Poppins;padding:20px 34px;border-radius:40px;box-shadow:0 12px 28px rgba(0,0,0,.25)}}
.card{{position:absolute;z-index:12;left:70px;top:350px;width:440px;height:126px;border-radius:30px;display:flex;align-items:center;gap:16px;
  padding:0 20px;background:rgba(58,38,26,.55);-webkit-backdrop-filter:blur(22px) saturate(1.2);backdrop-filter:blur(22px) saturate(1.2);
  border:1.5px solid rgba(255,255,255,.35);box-shadow:0 18px 44px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.25);color:#fff}}
.ctile{{width:84px;height:84px;border-radius:22px;flex:none;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%);box-shadow:inset 0 2px 0 rgba(255,255,255,.6)}}
.cbody{{flex:1;min-width:0}}
.cname{{font:700 32px/1.05 Poppins;white-space:nowrap}}
.cwave{{display:flex;align-items:center;gap:4px;height:26px;margin:6px 0 4px}}
.cwave i{{display:block;width:6px;height:100%;border-radius:3px;background:#fff;opacity:.9;transform-origin:50% 50%}}
.cmeta{{font:500 19px/1 Poppins;opacity:.8}}
.ig{{position:absolute;z-index:11;width:130px;height:130px;border-radius:32px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(225deg,#4F5BD5 0%,#962FBF 28%,#D62976 55%,#FA7E1E 80%,#FEDA75 100%);box-shadow:0 14px 30px rgba(60,20,60,.35)}}
#vig{{position:absolute;inset:0;z-index:5;background:radial-gradient(90% 70% at 50% 42%,rgba(20,10,20,0) 45%,rgba(20,10,20,.65) 100%)}}
#flash{{position:absolute;inset:0;z-index:14;background:#fff}}
.photo{{position:absolute;z-index:11;width:260px;height:330px;background:#fff;padding:12px 12px 46px;box-shadow:0 18px 40px rgba(0,0,0,.35)}}
.photo img{{width:100%;height:100%;object-fit:cover;display:block}}
.gl{{position:absolute;inset:0;z-index:6;background:rgba(255,0,80,.35);mix-blend-mode:screen;clip-path:polygon(0 30%,100% 30%,100% 38%,0 38%,0 60%,100% 60%,100% 66%,0 66%)}}
.gl.b{{background:rgba(0,200,255,.35);clip-path:polygon(0 44%,100% 44%,100% 50%,0 50%,0 74%,100% 74%,100% 79%,0 79%)}}
.cap{{position:absolute;left:0;right:0;top:{CAP_Y - 52}px;z-index:20;text-align:center;text-transform:lowercase;font:700 84px/1.1 Poppins;color:#fff;
  letter-spacing:-.03em;text-shadow:0 0 24px rgba(0,0,0,.6),0 4px 12px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.5);white-space:nowrap;transform-origin:50% 50%}}
#fol{{position:absolute;z-index:15;left:110px;top:1400px;width:830px;height:150px;background:#fff;border-radius:28px;display:flex;align-items:center;
  gap:22px;padding:0 26px;box-shadow:0 18px 50px rgba(0,0,0,.3)}}
.fav{{width:100px;height:100px;border-radius:50%;padding:4px;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.fav img{{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid #fff;display:block}}
.fnm{{flex:1;font:700 34px/1.2 Poppins;color:#111}}
.fsub{{font:500 26px/1.2 Poppins;color:#777}}
.fbtn{{position:absolute;right:26px;width:220px;height:74px;border-radius:16px;background:#0095F6;color:#fff;font:700 30px/74px Poppins;text-align:center}}
.fbtn.on{{background:#EFEFEF;color:#111}}
'''

def build():
    parts = [header(), demos(), captions()]
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
