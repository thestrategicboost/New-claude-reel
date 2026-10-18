#!/usr/bin/env python3
"""Reel "cette vidéo, c'est Claude qui l'a montée": Maé's raw take (cut.py keeps the good takes), edited like the
"Drop Edit Below" inspiration, every effect landing on the word that announces it:
CapCut / Premiere struck out -> Claude; a prompt bar that types her requests; "un peu plus de rose, hop" = the natural
grade turns into her lilac look; "un mur de réels derrière moi, hop" = a wall of her real reels behind her (cut-out);
raw file dropped then "✓ réel monté"; "texte derrière" = giant word behind her head; "changer d'ambiance" = a warm film
look; "agrandir les sous-titres" = huge captions; "plan plus large / plus serré / des cuts" = zoom out, zoom in, hard
cuts; "en deux secondes" = a 2 s timer; her real guide + comment MONTAGE + DM at the end.

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll_nat.mp4'], capture_output=True, text=True).stdout.strip())
SEGS = json.load(open('work/segs.json'))
BROWN, DARK = '#8C5C41', '#573307'
GOLD = 'linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)'
TOP = 262        # top band for the inserts (Instagram UI above 240, her head from ~480)


def ct(t):
    """raw-clip time -> edit time"""
    out = 0.0
    for a, b in SEGS:
        if t >= b:
            out += b - a
        else:
            return out + max(0.0, t - a)
    return out


# ------------------------------------------------------------------ captions: one word at a time, lowercase
FIX = {'adios': 'tchuss', 'Adios': 'tchuss', 'bleu': 'bla', '-bleu': '-bla', '-bleu,': '-bla', 'à grandir': 'agrandir', 'grandir': 'agrandir'}


def words():
    raw = []
    for seg in json.load(open('work/raw_words.json')):
        for w in seg['words']:
            if any(a - .02 <= w['s'] and w['e'] <= b + .1 for a, b in SEGS):
                raw.append({'w': w['w'].strip(), 's': ct(w['s']), 'e': ct(min(w['e'], w['s'] + 1.2))})
    out = []
    for w in raw:
        t = w['w']
        if (t.startswith("'") or t.startswith('-')) and out:     # j 'ai -> j'ai, bleu -bleu -> bla-bla
            out[-1]['w'] += FIX.get(t, t)
            out[-1]['e'] = w['e']
            continue
        out.append(dict(w, w=FIX.get(t, t)))
    for w in out:
        w['w'] = re.sub(r'[.,!?…]', '', w['w']).lower().replace('dm', 'DM')
    out = [w for w in out if w['w']]
    for k, w in enumerate(out):                                  # "mais à grandir" -> "mais agrandir"
        if w['w'] == 'à' and k + 1 < len(out) and out[k + 1]['w'] == 'agrandir':
            w['w'] = ''
    return [w for w in out if w['w']]


BIG = (ct(52.84), ct(53.72))     # "agrandir les sous-titres": the captions get huge


def captions():
    ws = words()
    groups = []
    for w in ws:                 # a word shorter than 0.14 s rides with the next one (never two on screen)
        if groups and w['s'] - groups[-1]['s'] < .14:
            groups[-1]['w'] += ' ' + w['w']
            groups[-1]['e'] = w['e']
        else:
            groups.append(dict(w))
    html, tw = [], []
    for k, w in enumerate(groups):
        nxt = groups[k + 1]['s'] if k + 1 < len(groups) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        big = ' big' if BIG[0] <= w['s'] < BIG[1] else ''
        html.append(f'<div id="w{k}" class="cap{big}">{w["w"]}</div>')
        tw += [f"gsap.set('#w{k}',{{autoAlpha:0}});", f"tl.set('#w{k}',{{autoAlpha:1}},{w['s']:.3f});",
               f"tl.fromTo('#w{k}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
               f"tl.set('#w{k}',{{autoAlpha:0}},{end:.3f});"]
    return html, tw


# ------------------------------------------------------------------ helpers
def show(sel, a, b, frm="{autoAlpha:0,y:-30,scale:.9}", d=.3, ease='back.out(1.7)'):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,y:0,x:0,scale:1,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,y:-20,duration:.2}},{b - .2:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def typing(sel, text, a, b):
    """types `text` into `sel` between a and b (one tl.set per character)"""
    out = [f"tl.set('{sel}',{{textContent:''}},{a - .01:.3f});"]
    n = len(text)
    for i in range(1, n + 1):
        out.append(f"tl.set('{sel}',{{textContent:{json.dumps(text[:i])}}},{a + (b - a) * i / n:.3f});")
    return out


CLAUDE = ('<svg viewBox="0 0 100 100" width="120" height="120"><g fill="#D97757">' +
          ''.join(f'<rect x="46" y="6" width="8" height="44" rx="4" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 30)) +
          '</g></svg>')


def scenes():
    html, tw, sfx = [], [], []

    # 1. hook on a brown wall (she is cut out in front, like the green wall of the inspiration):
    #    "tu vois cette vidéo" -> CETTE VIDÉO behind her head; "c'est Claude qui l'a montée" -> MONTÉE behind her head
    html.append('<div id="bw1" class="bwall"></div>')
    html.append('<div id="hk1" class="bht"><div class="bs1">tu vois</div>CETTE<br/>VIDÉO</div>')
    html.append('<div id="hk2" class="bht"><div class="bs1">c\'est Claude qui l\'a</div>MONTÉE</div>')
    tw += ["gsap.set('#bw1',{autoAlpha:1});",
           f"tl.to('#bw1',{{clipPath:'inset(0 0 100% 0)',duration:.35,ease:'power3.inOut'}},{ct(7.50) - .35:.3f});",
           f"tl.set('#bw1',{{autoAlpha:0}},{ct(7.50):.3f});",
           "tl.fromTo('#hk1',{autoAlpha:0,scale:1.3},{autoAlpha:1,scale:1,duration:.3,ease:'expo.out',immediateRender:true},0);",
           f"tl.to('#hk1',{{autoAlpha:0,duration:.12}},{ct(2.86):.3f});",
           f"tl.fromTo('#hk2',{{autoAlpha:0,y:80}},{{autoAlpha:1,y:0,duration:.3,ease:'expo.out',immediateRender:false}},{ct(2.92):.3f});",
           f"tl.to('#hk2',{{autoAlpha:0,duration:.15}},{ct(4.40):.3f});"]
    sfx += [('whoosh-short', 0.0, .35), ('pop', ct(2.92), .35)]

    # 2. "pas de CapCut, pas de logiciel de montage" -> struck out; "juste Claude" -> Claude
    for k, (logo, name, at, hit) in enumerate((('capcut', 'CapCut', 4.48, 4.80), ('premiere', 'Logiciel de montage', 5.46, 5.98))):
        html.append(f'<div id="lg{k}" class="lg" style="left:{150 + 470 * k}px"><img src="assets/logos/{logo}.png"/><div class="ln">{name}</div>'
                    f'<svg class="strike" viewBox="0 0 200 200"><path d="M18 30 L182 170" /></svg></div>')
        tw += show(f'#lg{k}', ct(at), ct(6.62), "{autoAlpha:0,scale:.6}", .3)
        tw += [f"gsap.set('#lg{k} .strike path',{{strokeDasharray:240,strokeDashoffset:240}});",
               f"tl.to('#lg{k} .strike path',{{strokeDashoffset:0,duration:.22,ease:'power2.out'}},{ct(hit):.3f});",
               f"tl.to('#lg{k} img',{{opacity:.45,duration:.2}},{ct(hit):.3f});"]
        sfx += [('pop', ct(at), .3), ('click', ct(hit), .45)]
    html.append(f'<div id="cl" class="cl">{CLAUDE}</div>')
    html.append('<div id="cl2" class="bht gold">Claude.</div>')
    tw += [f"tl.fromTo('#cl2',{{autoAlpha:0,scale:1.25}},{{autoAlpha:1,scale:1,duration:.3,ease:'expo.out',immediateRender:false}},{ct(6.70):.3f});",
           f"tl.set('#cl2',{{autoAlpha:0}},{ct(7.50):.3f});"]
    tw += show('#cl', ct(6.70), ct(7.50) + .3, "{autoAlpha:0,scale:.5}", .35)
    tw += [f"tl.fromTo('#cl svg',{{rotation:-90}},{{rotation:0,duration:.6,ease:'power3.out',immediateRender:false}},{ct(6.70):.3f});"]
    sfx += [('sparkle', ct(6.70), .3)]

    # 3. the prompt bar: her requests typed, sent, done
    html.append('<div id="pb" class="pb"><div class="pl">PROMPT</div><div id="pt" class="pt"></div><div id="ps" class="ps">'
                '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" fill="none" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg></div><div id="pp" class="pp"></div></div>')
    tw += show('#pb', ct(15.76), ct(23.62), "{autoAlpha:0,y:-40}", .3)
    tw += ["gsap.set('#pp',{scaleX:0,transformOrigin:'0 50%'});"]
    for txt, a, b, send in (('Monte ma vidéo dans ma charte', 15.80, 16.60, 16.90),
                            ('Mets un peu plus de rose', 18.72, 19.95, 20.10),
                            ('Fais un mur de réels derrière moi', 21.40, 23.10, 23.40)):
        tw += typing('#pt', txt, ct(a), ct(b))
        tw += [f"tl.to('#ps',{{scale:.82,duration:.08,yoyo:true,repeat:1}},{ct(send):.3f});",
               f"tl.set('#pp',{{scaleX:0}},{ct(a):.3f});",
               f"tl.to('#pp',{{scaleX:1,duration:{max(.3, ct(send) + .9 - ct(send)):.2f},ease:'power1.inOut'}},{ct(send):.3f});"]
        sfx += [('click-soft', ct(send), .5)]
    # "toute la vidéo est montée": the bar confirms
    html.append('<div id="ok1" class="ok">✓ Vidéo montée</div>')
    tw += show('#ok1', ct(17.46), ct(18.66), "{autoAlpha:0,scale:.7}", .25)
    sfx += [('pop', ct(17.46), .3)]

    # 4. "un peu plus de rose, hop" -> the lilac look fades in (stays for the rest of the reel)
    tw += ["gsap.set('#bgl',{opacity:0});", f"tl.to('#bgl',{{opacity:1,duration:.3,ease:'power1.inOut'}},{ct(20.22):.3f});"]
    sfx += [('sparkle', ct(20.22), .3)]

    # 5. "(snap) hop, il met un mur de réel derrière moi" -> brown wall + her real reels in 3D, columns sliding up and down
    reels = [f'assets/reels/r{i}.jpg' for i in range(1, 17)]
    cols = ''
    for c in range(4):
        imgs = [reels[(c * 4 + j) % 16] for j in range(7)]
        cols += f'<div class="col c{c}">' + ''.join(f'<div class="rc"><img src="{r}"/></div>' for r in imgs) + '</div>'
    html.append(f'<div id="wall" class="wall"><div class="wallin">{cols}</div></div>')
    a, b = ct(25.85), ct(27.50)
    tw += ["gsap.set('#wall',{autoAlpha:0});", f"tl.set('#wall',{{autoAlpha:1}},{a:.3f});",
           f"tl.fromTo('#wall .wallin',{{rotationY:-70,scale:.7}},{{rotationY:-24,scale:1,duration:.55,ease:'power3.out',immediateRender:false}},{a:.3f});",
           f"tl.fromTo('#wall .rc',{{autoAlpha:0,z:-300}},{{autoAlpha:1,z:0,duration:.35,ease:'back.out(1.4)',stagger:{{each:.012,from:'random'}},immediateRender:false}},{a:.3f});"]
    for c in range(4):
        d = -1 if c % 2 == 0 else 1
        tw.append(f"tl.fromTo('#wall .c{c}',{{y:{-250 if d > 0 else 0}}},{{y:{0 if d > 0 else -250},duration:{b - a:.2f},ease:'none',immediateRender:false}},{a:.3f});")
    tw += [f"tl.to('#wall',{{autoAlpha:0,duration:.2}},{b - .2:.3f});", f"tl.set('#wall',{{autoAlpha:0}},{b:.3f});"]
    sfx += [('whoosh-short', a, .45), ('sparkle', a + .1, .25)]

    # 6. "la vidéo brute de décoffrage avec tous mes bugs ... et hop il me fait ça tout seul"
    html.append('<div id="fd" class="fd"><div class="fz">⇩ Dépose ta vidéo brute</div><div id="ff" class="ff"><div class="fth"></div>'
                '<div><div class="fn">IMG_4807.MOV</div><div class="fs">vidéo brute · 1:13</div></div></div>'
                '<div id="fok" class="fok">✓ Réel monté</div></div>')
    tw += show('#fd', ct(40.58), ct(45.52), "{autoAlpha:0,y:-40}", .3)
    tw += ["gsap.set('#ff',{autoAlpha:0});", "gsap.set('#fok',{autoAlpha:0});",
           f"tl.fromTo('#ff',{{autoAlpha:0,x:-380,y:-60,rotation:-14,scale:.7}},{{autoAlpha:1,x:0,y:0,rotation:0,scale:1,duration:.45,ease:'power3.out',immediateRender:false}},{ct(41.04):.3f});",
           f"tl.to('#ff',{{x:'+=10',duration:.05,yoyo:true,repeat:7,ease:'none'}},{ct(43.04):.3f});",     # "tous mes bugs"
           f"tl.to('#ff',{{autoAlpha:0,scale:.8,duration:.15}},{ct(44.58):.3f});",
           f"tl.fromTo('#fok',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.3,ease:'back.out(2)',immediateRender:false}},{ct(44.62):.3f});"]
    sfx += [('whoosh-short', ct(41.04), .35), ('glitch2', ct(43.04), .25), ('sparkle', ct(44.62), .3)]

    # 7. "mettre du texte derrière" -> a giant word behind her head (cut-out on top)
    html.append('<div id="tb" class="tbh"><div class="bwall in"></div><div class="tbt">TEXTE</div></div>')
    a, b = ct(49.28), ct(50.80)
    tw += ["gsap.set('#tb',{autoAlpha:0});",
           f"tl.set('#tb',{{autoAlpha:1}},{a:.3f});",
           f"tl.fromTo('#tb .tbt',{{autoAlpha:0,scale:1.25}},{{autoAlpha:1,scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{a:.3f});",
           f"tl.to('#tb',{{autoAlpha:0,duration:.15}},{b - .15:.3f});", f"tl.set('#tb',{{autoAlpha:0}},{b:.3f});"]
    sfx += [('pop', a, .35)]

    # 8. "changer d'ambiance comme ça" -> warm film look until the end of that take
    tw += ["gsap.set('#bga',{opacity:0});", f"tl.set('#bga',{{opacity:1}},{ct(50.80):.3f});", f"tl.set('#bga',{{opacity:0}},{ct(51.36):.3f});"]
    sfx += [('whoosh-short', ct(50.80), .35)]

    # "agrandir les sous-titres": a brown block like the inspiration's "BIGGER captions"
    html.append('<div id="bg2" class="bigc"><div class="bc1">SOUS-TITRES</div><div class="bc2">plus grands.</div></div>')
    tw += show('#bg2', ct(52.84), ct(54.10), "{autoAlpha:0,scale:.8}", .25)
    sfx += [('pop', ct(52.84), .35)]

    # 9. "un plan plus large, plus serré, faire des cuts"
    tw += [f"tl.set('#cam',{{scale:1.18}},{ct(51.44):.3f});",
           f"tl.to('#cam',{{scale:1,duration:.45,ease:'power2.out'}},{ct(54.30):.3f});",            # plus large
           f"tl.to('#cam',{{scale:1.4,duration:.3,ease:'power2.out'}},{ct(55.02):.3f});",           # plus serré
           f"tl.set('#cam',{{scale:1.12}},{ct(55.62):.3f});", f"tl.set('#cam',{{scale:1.32}},{ct(55.82):.3f});",
           f"tl.set('#cam',{{scale:1}},{ct(56.10):.3f});"]                                         # des cuts
    html.append('<div id="fl" class="fl"></div>')
    tw += ["gsap.set('#fl',{autoAlpha:0});"] + [f"tl.fromTo('#fl',{{autoAlpha:.7}},{{autoAlpha:0,duration:.12,immediateRender:false}},{ct(t):.3f});" for t in (55.62, 55.82)]
    sfx += [('whoosh-short', ct(54.30), .3), ('whoosh-short', ct(55.02), .3), ('click', ct(55.62), .4), ('click', ct(55.82), .4)]
    # "en deux secondes"
    html.append('<div id="tm" class="tm"><span class="td"></span><span id="tmv">0,0 s</span></div>')
    a = ct(56.70)
    tw += show('#tm', a, ct(57.20) + .35, "{autoAlpha:0,scale:.6}", .25)
    tw += [f"tl.set('#tmv',{{textContent:'{str(v).replace('.', ',')} s'}},{a + .02 + k * .06:.3f});" for k, v in enumerate([0.4, 0.8, 1.2, 1.6, 2.0])]
    sfx += [('click-soft', a + .3, .4)]

    # 10. CTA: her real guide, comment MONTAGE, the DM
    html.append('<div id="gd" class="gd"><img src="assets/guide.png"/><div class="gb">GUIDE OFFERT</div></div>')
    tw += show('#gd', ct(67.26), ct(69.72), "{autoAlpha:0,y:-60,rotation:-6,scale:.8}", .4)
    tw += [f"tl.to('#gd',{{rotation:-3,duration:.4}},{ct(67.66):.3f});"]
    sfx += [('whoosh-short', ct(67.26), .35)]
    html.append('<div id="cm" class="cm"><div class="cav"></div><div><div class="cw">toi · maintenant</div><div id="cmt" class="ct"></div></div>'
                '<div class="ch">♥</div></div>')
    tw += show('#cm', ct(69.74), ct(71.20), "{autoAlpha:0,y:-30}", .3)
    tw += typing('#cmt', 'MONTAGE', ct(70.10), ct(70.50))
    tw += [f"tl.fromTo('#cm .ch',{{scale:0}},{{scale:1,duration:.25,ease:'back.out(3)',immediateRender:false}},{ct(70.55):.3f});"]
    sfx += [('pop', ct(69.74), .3), ('click-soft', ct(70.55), .4)]
    html.append('<div id="dm" class="dm"><img src="assets/avatar.png"/><div><div class="dt">thestrategicboost.fr</div>'
                '<div class="ds">t\'a envoyé le guide 🎁</div></div></div>')
    tw += show('#dm', ct(71.16), DUR + .2, "{autoAlpha:0,y:-80}", .35, 'power3.out')
    sfx += [('pop', ct(71.16), .4)]
    return html, tw, sfx


SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click': .36, 'click-soft': .36, 'sparkle': 1.8, 'glitch2': .8}


def audio(sfx):
    out, lanes = [], []
    for k, (n, t, v) in enumerate(sorted(sfx, key=lambda x: x[1])):
        d = min(SFX_LEN[n], DUR - t)
        lane = next((i for i, e in enumerate(lanes) if e <= t), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{v * .75:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.hook{{position:absolute;left:0;right:0;top:{TOP + 10}px;z-index:20;text-align:center;color:#fff;font-family:Anton;line-height:.95;
  text-shadow:0 5px 0 rgba(0,0,0,.35),0 0 30px rgba(0,0,0,.45)}}
.h1{{font-size:118px;letter-spacing:.02em}}
.h2{{font-size:96px;letter-spacing:.02em;margin-top:8px}}
.h2 span{{display:inline-block;background:{DARK};padding:4px 22px 0;margin-left:8px}}
.lg{{position:absolute;top:{TOP + 20}px;width:310px;text-align:center;z-index:20}}
.lg img{{width:170px;height:170px;border-radius:38px;box-shadow:0 14px 34px rgba(0,0,0,.35);display:block;margin:0 auto}}
.ln{{font:700 30px/1.2 Poppins;color:#fff;margin-top:12px;text-shadow:0 3px 12px rgba(0,0,0,.6)}}
.strike{{position:absolute;left:55px;top:-15px;width:200px;height:200px;overflow:visible}}
.strike path{{stroke:#E5262B;stroke-width:16;stroke-linecap:round;fill:none}}
.cl{{position:absolute;left:0;right:0;top:{TOP + 10}px;z-index:21;text-align:center}}
.cl svg{{display:block;margin:0 auto;filter:drop-shadow(0 8px 20px rgba(0,0,0,.35))}}
.cn{{font:400 104px/1 Anton;color:#fff;letter-spacing:.02em;margin-top:8px;text-shadow:0 4px 0 rgba(0,0,0,.35),0 0 26px rgba(0,0,0,.45)}}
.pb{{position:absolute;left:90px;right:90px;top:{TOP}px;z-index:20;height:150px;background:#fff;border-radius:34px;overflow:hidden;
  box-shadow:0 18px 44px rgba(0,0,0,.3);padding:22px 120px 0 34px}}
.pl{{font:600 20px/1 Poppins;letter-spacing:.24em;color:{BROWN}}}
.pt{{font:500 38px/1.25 Poppins;color:#222;margin-top:16px;white-space:nowrap;overflow:hidden}}
.ps{{position:absolute;right:26px;top:40px;width:70px;height:70px;border-radius:50%;background:{BROWN};display:flex;align-items:center;justify-content:center}}
.pp{{position:absolute;left:0;right:0;bottom:0;height:8px;background:{GOLD}}}
.ok{{position:absolute;left:0;right:0;top:{TOP + 170}px;z-index:20;text-align:center}}
.ok{{font:400 50px/1 Anton;letter-spacing:.04em;color:#fff}}
#ok1{{width:420px;left:330px;padding:16px 0 12px;background:{DARK};box-shadow:0 12px 28px rgba(0,0,0,.3)}}
.cut{{z-index:3}}
.fd{{position:absolute;left:110px;right:110px;top:{TOP}px;height:210px;z-index:20;border-radius:34px;border:3px dashed rgba(255,255,255,.85);
  background:rgba(58,38,26,.55);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);box-shadow:0 18px 44px rgba(0,0,0,.3)}}
.fz{{position:absolute;left:0;right:0;top:18px;text-align:center;font:600 28px/1 Poppins;color:rgba(255,255,255,.85)}}
.ff{{position:absolute;left:60px;right:60px;top:66px;height:118px;border-radius:22px;background:#fff;display:flex;align-items:center;gap:22px;padding:0 22px;
  box-shadow:0 12px 26px rgba(0,0,0,.3)}}
.fth{{width:56px;height:90px;border-radius:10px;background:linear-gradient(160deg,#9AA3B5,#5E6678)}}
.fn{{font:700 32px/1.1 Poppins;color:#111}}
.fs{{font:500 24px/1.3 Poppins;color:#777}}
.fok{{position:absolute;left:0;right:0;top:86px;text-align:center;font:400 64px/1 Anton;letter-spacing:.04em;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.4)}}
.fl{{position:absolute;inset:0;z-index:30;background:#fff}}
.tm{{position:absolute;left:340px;width:400px;top:{TOP + 20}px;z-index:20;height:120px;border-radius:60px;background:{DARK};display:flex;align-items:center;
  justify-content:center;gap:20px;font:400 72px/1 Anton;color:#fff;box-shadow:0 14px 30px rgba(0,0,0,.3)}}
.td{{width:30px;height:30px;border-radius:50%;background:#E5262B}}
.gd{{position:absolute;left:300px;top:{TOP - 10}px;width:480px;z-index:20;background:#fff;box-shadow:0 22px 50px rgba(0,0,0,.4);transform-origin:50% 0}}
.gd img{{width:100%;height:330px;object-fit:cover;object-position:top;display:block}}
.gb{{position:absolute;left:-30px;bottom:-26px;padding:12px 26px 10px;background:{DARK};font:400 46px/1 Anton;letter-spacing:.05em;color:#fff;
  box-shadow:0 10px 24px rgba(0,0,0,.3)}}
.cm{{position:absolute;left:110px;right:110px;top:{TOP + 20}px;z-index:20;height:150px;border-radius:34px;background:#fff;display:flex;align-items:center;
  gap:22px;padding:0 30px;box-shadow:0 18px 44px rgba(0,0,0,.3)}}
.cav{{width:74px;height:74px;border-radius:50%;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.cw{{font:500 22px/1 Poppins;color:#888}}
.ct{{font:400 56px/1.1 Anton;letter-spacing:.04em;color:#111;margin-top:8px;min-height:60px}}
.ch{{margin-left:auto;font:400 50px/1 Poppins;color:#ED4956}}
.dm{{position:absolute;left:110px;right:110px;top:{TOP + 200}px;z-index:21;height:130px;border-radius:30px;background:rgba(255,255,255,.96);display:flex;
  align-items:center;gap:22px;padding:0 26px;box-shadow:0 18px 44px rgba(0,0,0,.3)}}
.dm img{{width:84px;height:84px;border-radius:50%;object-fit:cover}}
.dt{{font:700 30px/1.2 Poppins;color:#111}}
.ds{{font:500 28px/1.2 Poppins;color:#555}}
.bwall{{position:absolute;inset:0;z-index:2;background:radial-gradient(110% 70% at 50% 35%,#9C6B4E 0%,{BROWN} 45%,{DARK} 100%)}}
.bht{{position:absolute;left:0;right:0;top:300px;z-index:2;text-align:center;font:400 250px/.9 Anton;color:#fff;letter-spacing:.01em;
  text-shadow:0 10px 40px rgba(0,0,0,.25)}}
.bht.gold{{top:330px;font-size:280px;background:{GOLD};-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none}}
.bs1{{font:italic 600 58px/1 Poppins;letter-spacing:0;margin-bottom:14px;color:#F3DFB2}}
.wall{{position:absolute;inset:0;z-index:2;background:radial-gradient(110% 70% at 50% 35%,#9C6B4E 0%,{BROWN} 45%,{DARK} 100%);perspective:1300px;overflow:hidden}}
.wallin{{position:absolute;left:-60px;right:-60px;top:-260px;bottom:-260px;display:flex;gap:22px;justify-content:center;transform-style:preserve-3d}}
.col{{display:flex;flex-direction:column;gap:22px;width:250px}}
.wall .rc{{width:250px;height:444px;flex:none;border-radius:20px;overflow:hidden;border:3px solid #E9C98F;box-shadow:0 18px 40px rgba(0,0,0,.45),0 0 24px rgba(214,174,102,.35)}}
.wall .rc img{{width:100%;height:100%;object-fit:cover;display:block}}
.tbh .bwall.in{{z-index:0}}
.tbh{{position:absolute;inset:0;z-index:2}}
.tbt{{position:absolute;left:0;right:0;top:{TOP + 150}px;text-align:center;font:400 340px/1 Anton;letter-spacing:.02em;color:#fff;text-shadow:0 10px 40px rgba(0,0,0,.3)}}
.bigc{{position:absolute;left:150px;right:150px;top:{TOP + 10}px;z-index:20;background:{DARK};padding:22px 0 26px;text-align:center;box-shadow:0 16px 40px rgba(0,0,0,.35)}}
.bc1{{font:400 104px/1 Anton;color:#fff;letter-spacing:.02em}}
.bc2{{font:italic 600 54px/1.1 Poppins;color:#F3DFB2;margin-top:6px}}
.cap{{position:absolute;left:90px;right:90px;top:1380px;z-index:25;text-align:center;font:700 62px/1 Poppins;color:#fff;
  text-shadow:0 4px 0 rgba(0,0,0,.85),0 0 18px rgba(0,0,0,.6)}}
.cap.big{{font-size:118px;top:1330px}}
'''


BEHIND = ('bw1', 'hk1', 'hk2', 'cl2', 'wall', 'tb')   # drawn between the video and her cut-out


def build():
    sh, st, sfx = scenes()
    ch, ct_ = captions()
    nl = '\n'
    vid = lambda i, src, ti, extra='': (f'<video id="{i}" class="full {extra}" src="{src}" muted playsinline data-start="0" data-media-start="0" '
                                        f'data-duration="{DUR:.3f}" data-track-index="{ti}"></video>')
    wall_a = 13.1   # cut-outs (lilac look) rendered for these two windows of the edit (cut.py clock)
    text_a = 23.4
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
  <audio id="voice" src="assets/aroll_nat.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(audio(sfx))}
  <div id="cam">
    {vid('bgn', 'assets/aroll_nat.mp4', 0)}
    {vid('bgl', 'assets/aroll_lilac.mp4', 1)}
    {vid('bga', 'assets/aroll_amb.mp4', 3)}
{nl.join(h for h in sh if any(f'id="{i}"' in h for i in BEHIND))}
    <video id="ci" class="full cut" src="assets/intro_cut.webm" muted playsinline data-start="0" data-media-start="0" data-duration="5.6" data-track-index="6"></video>
    <video id="cw" class="full cut" src="assets/wall_cut.webm" muted playsinline data-start="{wall_a}" data-media-start="0" data-duration="1.85" data-track-index="4"></video>
    <video id="ctx" class="full cut" src="assets/text_cut.webm" muted playsinline data-start="{text_a}" data-media-start="0" data-duration="1.8" data-track-index="5"></video>
  </div>
{nl.join(h for h in sh if not any(f'id="{i}"' in h for i in BEHIND))}
{nl.join(ch)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(st + ct_)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s')
