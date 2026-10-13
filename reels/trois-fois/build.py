#!/usr/bin/env python3
"""Reel "3 fois": "une fois par jour, une fois par semaine, une fois par mois", said three times. Each time she says a
frequency, ONE habit appears as a small motion-design scene on a frosted card (story ring filling, reels fanning out,
a month filling up, DMs arriving, stats climbing, an arrow hitting a target, notes writing themselves, clips stacking,
a profile ticking), under a dark-brown Anton header that spells the frequency out. Maé's branding: brown / gold /
white, Instagram-style touches.

PY build.py    writes index.html
"""
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
BLOCK = '#573307'
GOLD = 'linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)'
IG = 'linear-gradient(225deg,#4F5BD5 0%,#962FBF 28%,#D62976 55%,#FA7E1E 80%,#FEDA75 100%)'
import os
THEME = os.environ.get('THEME', 'brown')        # card colour: 'brown' or 'gold'
FREQ = {'j': 'UNE FOIS PAR JOUR', 's': 'UNE FOIS PAR SEMAINE', 'm': 'UNE FOIS PAR MOIS'}

# (start, frequency, scene, label) - when she says "une fois par ..." (round 3 from the silences: whisper skipped it)
MOMENTS = [(0.00, 'j', 'story', 'Poster une story'), (1.54, 's', 'script', 'Écrire tes scripts'), (2.66, 'm', 'month', 'Planifier ton mois'),
           (3.50, 'j', 'dm', 'Répondre à tes DM'), (4.90, 's', 'stats', 'Analyser tes stats'), (6.04, 'm', 'goal', 'Fixer tes objectifs'),
           (7.33, 'j', 'ideas', 'Noter tes idées'), (8.49, 's', 'batch', 'Filmer en batch'), (9.64, 'm', 'audit', 'Auditer ton profil')]


def scene(k, kind, t):
    """inner html of the card + its animation, all relative to the moment start t"""
    s = f'#c{k}'
    a = t + .12
    if kind == 'story':
        bars = ''.join(f'<div class="sbar"><i></i></div>' for _ in range(3))
        h = (f'<div class="phone"><div class="sbars">{bars}</div><div class="ring"><div class="ringin"><img src="assets/img/avatar.png"/></div></div>'
             f'<div class="plus">+</div></div>')
        w = [f"tl.fromTo('{s} .ring',{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:.4,ease:'back.out(1.7)',immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .sbar i',{{scaleX:0}},{{scaleX:1,duration:.3,stagger:.3,ease:'none',immediateRender:false}},{a + .1:.3f});",
             f"tl.fromTo('{s} .plus',{{scale:0}},{{scale:1,duration:.25,ease:'back.out(3)',immediateRender:false}},{a + .35:.3f});"]
    elif kind == 'script':
        lines = ''.join(f'<div class="sl"><b>{h}</b><i style="width:{w}%"></i></div>' for h, w in (('HOOK', 70), ('VALEUR', 82), ('CTA', 55)))
        h = (f'<div class="script"><div class="sth">SCRIPT · RÉEL</div>{lines}</div>'
             '<svg class="pen" viewBox="0 0 24 24" width="74" height="74"><path d="M4 20l1-4L16 5l3 3L8 19z" fill="#fff" stroke="#3a261a" stroke-width="1.2" stroke-linejoin="round"/></svg>')
        w = [f"tl.fromTo('{s} .sl',{{autoAlpha:0,x:-16}},{{autoAlpha:1,x:0,duration:.15,stagger:.18,immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .sl i',{{scaleX:0}},{{scaleX:1,duration:.22,stagger:.18,ease:'power1.out',immediateRender:false}},{a + .06:.3f});",
             f"tl.fromTo('{s} .pen',{{x:-150,y:-60,rotation:-8}},{{x:30,y:40,rotation:6,duration:.7,ease:'none',immediateRender:false}},{a:.3f});"]
    elif kind == 'reels':
        cards = ''.join(f'<div class="rc" style="--r:{r}deg"><img src="assets/img/r{n}.jpg"/><div class="play">▶</div></div>'
                        for r, n in ((-14, 1), (0, 3), (14, 5)))
        h = f'<div class="fan">{cards}</div>'
        w = [f"tl.fromTo('{s} .rc',{{rotation:0,y:60,autoAlpha:0}},{{rotation:(i,el)=>[-14,0,14][i],y:0,autoAlpha:1,duration:.35,stagger:.1,ease:'back.out(1.6)',immediateRender:false}},{a:.3f});"]
    elif kind == 'month':
        cells = ''.join(f'<div class="mc{" on" if d % 7 in (0, 2, 4) else ""}"><span>{d + 1}</span></div>' for d in range(28))
        h = f'<div class="mhd">OCTOBRE</div><div class="mgrid">{cells}</div>'
        w = [f"tl.fromTo('{s} .mc',{{autoAlpha:0,scale:.5}},{{autoAlpha:1,scale:1,duration:.15,stagger:.012,immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .mc.on',{{background:'rgba(255,255,255,.12)'}},{{background:'#D6AE66',duration:.12,stagger:.035,immediateRender:false}},{a + .3:.3f});"]
    elif kind == 'dm':
        h = ('<div class="chat"><div class="bub l">Hello ! Ton offre m’intéresse</div><div class="bub r">Avec plaisir, je t’explique</div>'
             '<div class="bub l typing"><i></i><i></i><i></i></div></div>')
        w = [f"tl.fromTo('{s} .bub',{{autoAlpha:0,y:24,scale:.8}},{{autoAlpha:1,y:0,scale:1,duration:.25,stagger:.25,ease:'back.out(2)',immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .typing i',{{y:0}},{{y:-8,duration:.15,stagger:.08,yoyo:true,repeat:5,immediateRender:false}},{a + .55:.3f});"]
    elif kind == 'stats':
        bars = ''.join(f'<div class="bar" style="height:{v}px"></div>' for v in (60, 90, 80, 130, 175))
        h = f'<div class="chart">{bars}<svg class="trend" viewBox="0 0 400 200"><path d="M10 170 L100 130 L190 140 L280 80 L390 25" /></svg></div><div class="kpi">+38 %</div>'
        w = [f"tl.fromTo('{s} .bar',{{scaleY:0}},{{scaleY:1,duration:.3,stagger:.07,ease:'power3.out',immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .trend path',{{strokeDashoffset:520}},{{strokeDashoffset:0,duration:.5,ease:'power2.out',immediateRender:false}},{a + .15:.3f});",
             f"tl.fromTo('{s} .kpi',{{scale:0}},{{scale:1,duration:.3,ease:'back.out(2.5)',immediateRender:false}},{a + .45:.3f});"]
    elif kind == 'goal':
        h = ('<div class="target"><i class="t1"></i><i class="t2"></i><i class="t3"></i></div>'
             '<svg class="arrow" viewBox="0 0 200 40"><path d="M0 20H170M150 6l24 14-24 14" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
        w = [f"tl.fromTo('{s} .target i',{{scale:0}},{{scale:1,duration:.3,stagger:.06,ease:'back.out(2)',immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .arrow',{{x:-320,autoAlpha:0}},{{x:0,autoAlpha:1,duration:.3,ease:'power3.in',immediateRender:false}},{a + .25:.3f});",
             f"tl.fromTo('{s} .target',{{x:0}},{{x:8,duration:.05,yoyo:true,repeat:3,immediateRender:false}},{a + .55:.3f});"]
    elif kind == 'ideas':
        h = ('<div class="note"><div class="nl" style="width:78%"></div><div class="nl" style="width:62%"></div><div class="nl" style="width:70%"></div>'
             '<div class="nl" style="width:45%"></div></div><div class="bulb"><svg viewBox="0 0 24 24" width="70" height="70"><path d="M12 3a6 6 0 0 0-3.6 10.8c.8.6 1.1 1.3 1.1 2.2h5c0-.9.3-1.6 1.1-2.2A6 6 0 0 0 12 3z" fill="#fff"/><path d="M9.5 19.5h5M10.5 22h3" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg></div>')
        w = [f"tl.fromTo('{s} .nl',{{scaleX:0}},{{scaleX:1,duration:.22,stagger:.12,ease:'power2.out',immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .bulb',{{scale:0,rotation:-20}},{{scale:1,rotation:0,duration:.35,ease:'back.out(2.5)',immediateRender:false}},{a + .35:.3f});",
             f"tl.fromTo('{s} .bulb',{{boxShadow:'0 0 0 rgba(243,223,178,0)'}},{{boxShadow:'0 0 60px rgba(243,223,178,.9)',duration:.3,yoyo:true,repeat:1,immediateRender:false}},{a + .6:.3f});"]
    elif kind == 'batch':
        clips = ''.join(f'<div class="clip" style="--i:{i}"><b>Vidéo {i + 1}</b><span>0:{15 + i * 7:02d}</span></div>' for i in range(4))
        h = f'<div class="rec"><i></i>REC</div><div class="clips">{clips}</div>'
        w = [f"tl.fromTo('{s} .clip',{{x:260,autoAlpha:0}},{{x:0,autoAlpha:1,duration:.25,stagger:.12,ease:'power3.out',immediateRender:false}},{a + .05:.3f});",
             f"tl.fromTo('{s} .rec i',{{opacity:1}},{{opacity:.2,duration:.2,yoyo:true,repeat:5,immediateRender:false}},{a:.3f});"]
    else:   # audit
        rows = ''.join(f'<div class="ar"><i class="ck">✓</i><span>{x}</span></div>' for x in ('Photo de profil', 'Bio claire', 'Lien en bio'))
        h = (f'<div class="prof"><div class="pav"><img src="assets/img/avatar.png"/></div><div class="pnm">@thestrategicboost.fr'
             f'<div class="pst">Stratégie Instagram</div></div></div><div class="audit">{rows}</div>')
        w = [f"tl.fromTo('{s} .prof',{{y:30,autoAlpha:0}},{{y:0,autoAlpha:1,duration:.25,ease:'power3.out',immediateRender:false}},{a:.3f});",
             f"tl.fromTo('{s} .ar',{{autoAlpha:0,x:-20}},{{autoAlpha:1,x:0,duration:.18,stagger:.14,immediateRender:false}},{a + .18:.3f});",
             f"tl.fromTo('{s} .ck',{{scale:0}},{{scale:1,duration:.2,stagger:.14,ease:'back.out(3)',immediateRender:false}},{a + .25:.3f});"]
    return h, w


COLS = {'j': 190, 's': 540, 'm': 890}          # the three frequencies on one line, left to right as she points


COLS = {'j': 190, 's': 540, 'm': 890}          # the three frequencies on one line, left to right as she points


def board():
    html, tw = [], []
    # one fixed line of three titles; the one she is saying lights up
    for f, cx in COLS.items():
        word = FREQ[f].split(' PAR ')[1]
        html.append(f'<div id="hd{f}" class="hcol" style="left:{cx - 170}px"><span class="hb"><small>UNE FOIS</small>PAR {word}</span></div>')
        tw.append(f"gsap.set('#hd{f}',{{autoAlpha:.45}});")
    for k, (t, f, kind, label) in enumerate(MOMENTS):
        same = [m[0] for m in MOMENTS[k + 1:] if m[1] == f]
        b = same[0] if same else DUR                      # a card stays until the next card of its column
        nxt = MOMENTS[k + 1][0] if k + 1 < len(MOMENTS) else DUR
        inner, anim = scene(k, kind, t)
        cx = COLS[f]
        html.append(f'<div id="c{k}" class="card" style="left:{cx - 165}px"><div class="scaler"><div class="stagebox">{inner}</div></div>'
                    f'<div class="lbl">{label}</div></div>')
        first = 'true' if t == 0 else 'false'
        tw += [f"gsap.set('#c{k}',{{autoAlpha:0}});",
               f"tl.fromTo('#c{k}',{{autoAlpha:0,scale:.7,y:-30}},{{autoAlpha:1,scale:1,y:0,duration:.3,ease:'back.out(1.6)',immediateRender:{first}}},{t + .02:.3f});",
               f"tl.to('#hd{f}',{{autoAlpha:1,scale:1.08,duration:.15}},{t:.3f});",
               f"tl.to('#hd{f}',{{autoAlpha:.45,scale:1,duration:.15}},{nxt - .05:.3f});"]
        tw += anim
        if b < DUR - .01:
            tw += [f"tl.to('#c{k}',{{autoAlpha:0,scale:.85,duration:.12}},{b - .12:.3f});", f"tl.set('#c{k}',{{autoAlpha:0}},{b:.3f});"]
    tw.append(f"tl.set('#hd{MOMENTS[0][1]}',{{autoAlpha:1,scale:1.08}},0);")
    return html, tw


def sfx_list():
    out = []
    for t, _f, kind, _l in MOMENTS:
        out.append(('whoosh-short', max(0.0, t - .02), .22))
        out.append(('pop', t + .3, .2))
    return out


SFX_LEN = {'pop': .72, 'whoosh-short': .57}


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


CARD_BG = 'linear-gradient(160deg,#9A6A4A 0%,#7A4E33 55%,#5E3A24 100%)' if THEME == 'brown' else GOLD
CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.hcol{{position:absolute;top:236px;width:340px;z-index:12;text-align:center;transform-origin:50% 50%}}
.hb{{display:inline-block;font:400 50px/1 Anton;letter-spacing:.02em;color:#fff;background:{BLOCK};padding:8px 20px 6px;box-shadow:0 10px 24px rgba(0,0,0,.28)}}
.hb small{{display:block;font-size:28px;letter-spacing:.08em;opacity:.85;margin-bottom:2px}}
.card{{position:absolute;z-index:11;top:372px;width:330px;height:262px;border-radius:32px;overflow:hidden;
  background:{CARD_BG};-webkit-backdrop-filter:blur(22px) saturate(1.2);backdrop-filter:blur(22px) saturate(1.2);
  border:1.5px solid rgba(255,255,255,.35);box-shadow:0 22px 50px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.25);color:#fff}}
.scaler{{position:absolute;left:0;top:0;width:580px;height:320px;transform:scale(.569);transform-origin:0 0}}
.scaler{{position:absolute;left:0;top:0;width:580px;height:320px;transform:scale(.569);transform-origin:0 0}}\n.stagebox{{position:absolute;left:0;right:0;top:0;height:320px;display:flex;align-items:center;justify-content:center}}
.lbl{{position:absolute;left:0;right:0;bottom:22px;text-align:center;font:700 26px/1 Poppins;letter-spacing:-.01em;color:{'#fff' if THEME == 'brown' else '#3a261a'}}}
/* script */
.script{{position:relative;width:360px;height:250px;border-radius:22px;background:#FFF8EC;padding:24px 26px;box-shadow:0 14px 30px rgba(0,0,0,.3);color:#3a261a}}
.sth{{font:700 20px/1 Poppins;letter-spacing:.14em;color:#B88A4E;margin-bottom:22px}}
.sl{{display:flex;align-items:center;gap:14px;margin-bottom:22px}}
.sl b{{width:92px;font:800 22px/1 Poppins}}
.sl i{{display:block;height:13px;border-radius:7px;background:#B88A4E;transform-origin:0 50%}}
.pen{{position:absolute;left:330px;top:120px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.35))}}
/* story */
.phone{{position:relative;width:160px;height:280px;border:5px solid #fff;border-radius:32px;margin-top:14px}}
.sbars{{position:absolute;left:14px;right:14px;top:14px;display:flex;gap:6px}}
.sbar{{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,.3);overflow:hidden}}
.sbar i{{display:block;height:100%;background:#fff;transform-origin:0 50%}}
.ring{{position:absolute;left:23px;top:70px;width:104px;height:104px;border-radius:50%;padding:6px;background:{IG}}}
.ringin{{width:100%;height:100%;border-radius:50%;border:4px solid #3a261a;overflow:hidden}}
.ringin img,.pav img{{width:100%;height:100%;object-fit:cover;display:block}}
.plus{{position:absolute;left:95px;top:148px;width:40px;height:40px;border-radius:50%;background:#0095F6;border:3px solid #fff;
  font:800 30px/32px Poppins;text-align:center;color:#fff}}
/* reels */
.fan{{position:relative;width:420px;height:290px;margin-top:20px}}
.rc{{position:absolute;left:135px;top:0;width:150px;height:260px;border-radius:20px;overflow:hidden;border:4px solid #fff;
  box-shadow:0 14px 30px rgba(0,0,0,.35);transform-origin:50% 120%}}
.rc:nth-child(1){{left:40px}} .rc:nth-child(3){{left:230px}}
.rc img{{width:100%;height:100%;object-fit:cover;display:block}}
.play{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:44px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.5)}}
/* month */
.mhd{{position:absolute;top:24px;left:0;right:0;text-align:center;font:600 22px/1 Poppins;letter-spacing:.18em;color:#E2BF77}}
.mgrid{{display:grid;grid-template-columns:repeat(7,58px);gap:8px;margin-top:40px}}
.mc{{height:52px;border-radius:14px;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;font:600 20px/1 Poppins}}
/* dm */
.chat{{width:470px;display:flex;flex-direction:column;gap:14px;margin-top:6px}}
.bub{{max-width:360px;padding:16px 22px;border-radius:26px;font:600 24px/1.2 Poppins}}
.bub.l{{align-self:flex-start;background:rgba(255,255,255,.2);border-bottom-left-radius:8px}}
.bub.r{{align-self:flex-end;background:{GOLD};color:#3a261a;border-bottom-right-radius:8px}}
.typing{{display:flex;gap:8px;padding:20px 24px}}
.typing i{{width:12px;height:12px;border-radius:50%;background:#fff;display:block}}
/* stats */
.chart{{position:relative;width:420px;height:200px;display:flex;align-items:flex-end;gap:26px;padding:0 20px;margin-top:30px}}
.bar{{flex:1;border-radius:12px 12px 4px 4px;background:{GOLD};transform-origin:50% 100%}}
.trend{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.trend path{{fill:none;stroke:#fff;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:520}}
.kpi{{position:absolute;right:46px;top:30px;font:800 40px/1 Poppins;color:#fff;background:rgba(255,255,255,.18);border:1.5px solid rgba(255,255,255,.4);
  border-radius:20px;padding:8px 16px}}
/* goal */
.target{{position:relative;width:230px;height:230px}}
.target i{{position:absolute;border-radius:50%;display:block}}
.t1{{inset:0;background:rgba(255,255,255,.18);border:6px solid #fff}}
.t2{{inset:44px;background:{GOLD}}}
.t3{{inset:88px;background:#fff}}
.arrow{{position:absolute;left:150px;top:132px;width:200px;height:40px}}
/* ideas */
.note{{width:320px;height:230px;border-radius:22px;background:#FFF8EC;padding:34px 30px;display:flex;flex-direction:column;gap:22px;transform:rotate(-3deg);
  box-shadow:0 14px 30px rgba(0,0,0,.3)}}
.nl{{height:14px;border-radius:7px;background:#B88A4E;transform-origin:0 50%}}
.bulb{{position:absolute;right:92px;top:30px;width:110px;height:110px;border-radius:32px;background:{GOLD};display:flex;align-items:center;justify-content:center}}
/* batch */
.rec{{position:absolute;top:26px;left:40px;display:flex;align-items:center;gap:10px;font:700 24px/1 Poppins}}
.rec i{{width:18px;height:18px;border-radius:50%;background:#FF3B30;display:block}}
.clips{{display:flex;flex-direction:column;gap:12px;width:440px;margin-top:40px}}
.clip{{display:flex;justify-content:space-between;align-items:center;height:52px;border-radius:16px;padding:0 22px;
  background:rgba(255,255,255,.16);border:1.5px solid rgba(255,255,255,.3);font:600 24px/1 Poppins}}
.clip b{{font-weight:700}}
.clip span{{opacity:.8}}
/* audit */
.prof{{position:absolute;top:30px;left:40px;right:40px;display:flex;align-items:center;gap:18px}}
.pav{{width:96px;height:96px;border-radius:50%;padding:4px;background:{IG};flex:none;overflow:hidden}}
.pav img{{border-radius:50%;border:3px solid #3a261a}}
.pnm{{font:700 28px/1.2 Poppins}}
.pst{{font:500 22px/1.3 Poppins;opacity:.85}}
.audit{{position:absolute;top:150px;left:60px;display:flex;flex-direction:column;gap:12px}}
.ar{{display:flex;align-items:center;gap:14px;font:600 28px/1 Poppins}}
.ck{{width:40px;height:40px;border-radius:50%;background:#34C759;font:800 26px/40px Poppins;text-align:center;font-style:normal;display:block}}
'''


def build():
    h, tw = board()
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
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(h)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tw)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s')
