#!/usr/bin/env python3
"""Second art direction of the "c'est Claude qui l'a montée" reel, so it can be re-posted as a trial reel without
Instagram flagging a duplicate: same cut and voice, everything on screen redone - footage mirrored, warm golden grade,
tighter framing, phrase captions with the spoken word on a gold pill, chat bubbles for the hook, a checklist for the
apps, a chat thread for the prompts, a progress loader, a top-down colour wipe, a polaroid collage behind her, outlined
words behind her head, a rush polaroid with scissor cuts and duration bars, a resize frame, a REC viewfinder, a
stopwatch, the guide pages as a carousel behind her and a lock-screen notification for the DM.

PY build2.py    writes index.html (PY build.py restores the first version)
"""
import json
import re

import build as B
from build import CLAUDE, CREAM, CUTS, DARK, DUR, INK, SEND, TOP, ct, setseq, show, typing, words

PILL = 'linear-gradient(135deg,#EBCB8B 0%,#C99A55 55%,#A97A3E 100%)'


# ------------------------------------------------------------------ captions: 2-3 word phrases, the spoken word on a gold pill
def captions():
    ws = []
    for w in words():
        t = re.sub(r'[,.!?…]', '', w['w']).lower().replace('dm', 'DM')
        if t:
            ws.append(dict(w, w=t))
    groups, cur = [], []
    for k, w in enumerate(ws):
        cur.append(w)
        nxt = ws[k + 1] if k + 1 < len(ws) else None
        if len(cur) >= 3 or nxt is None or nxt['s'] - w['e'] > .35 or len(' '.join(x['w'] for x in cur)) > 16:
            groups.append(cur)
            cur = []
    html, tw = [], []
    for g, ph in enumerate(groups):
        nxt = groups[g + 1][0]['s'] if g + 1 < len(groups) else DUR
        end = min(ph[-1]['e'] + .3, nxt, DUR)
        spans = ''.join(f'<span id="c{g}_{j}">{w["w"]}</span>' for j, w in enumerate(ph))
        html.append(f'<div id="c{g}" class="cap2">{spans}</div>')
        tw += [f"gsap.set('#c{g}',{{autoAlpha:0}});", f"tl.set('#c{g}',{{autoAlpha:1}},{ph[0]['s']:.3f});",
               f"tl.fromTo('#c{g}',{{y:24}},{{y:0,duration:.14,ease:'power3.out',immediateRender:false}},{ph[0]['s']:.3f});",
               f"tl.set('#c{g}',{{autoAlpha:0}},{end:.3f});"]
        for j, w in enumerate(ph):
            off = ph[j + 1]['s'] if j + 1 < len(ph) else end
            tw += [f"tl.set('#c{g}_{j}',{{backgroundImage:'{PILL}',fontStyle:'italic'}},{w['s']:.3f});",
                   f"tl.set('#c{g}_{j}',{{backgroundImage:'none',fontStyle:'normal'}},{off:.3f});"]
    return html, tw


CHECK = '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M5 12.5l4.5 4.5L19 7.5" stroke="#fff" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M6 6l12 12M18 6L6 18" stroke="#fff" stroke-width="3.2" fill="none" stroke-linecap="round"/></svg>'


def scenes():
    H, T, S = [], [], []
    # the lilac layer is revealed later by a top-down wipe
    T += ["gsap.set('#bgl',{clipPath:'inset(0 0 100% 0)'});"]

    # 1. hook as a chat: "tu vois cette vidéo ?" in a white bubble, Claude answers in a gold bubble, gold rings pulse behind her
    H.append('<div id="b1" class="bub wh">tu vois cette vidéo ?</div>'
             f'<div id="b2" class="bub au"><span class="bav">{CLAUDE.format(s=64)}</span><span>c\'est <b>Claude</b><br/>qui l\'a montée</span></div>')
    a0, a1, end = ct(1.74), ct(2.92), ct(4.10)
    T += show('#b1', a0, end, "{autoAlpha:0,scale:.5,y:40}", .3)
    T += show('#b2', a1, end, "{autoAlpha:0,scale:.5,y:40}", .3)
    S += [('pop', a0, .3), ('pop', a1, .3)]
    H += [f'<i id="rg{k}" class="ring"></i>' for k in range(4)]
    T += ["gsap.set('.ring',{autoAlpha:0});"]
    rend = CUTS['intro'][0] + CUTS['intro'][1] - .05
    for k in range(4):
        t = a1 + k * .3
        if t < rend - .3:
            T.append(f"tl.fromTo('#rg{k}',{{autoAlpha:.9,scale:.3}},{{autoAlpha:0,scale:1.6,duration:{min(.9, rend - t):.2f},ease:'power2.out',immediateRender:false}},{t:.3f});")
    T.append(f"tl.set('.ring',{{autoAlpha:0}},{rend:.3f});")

    # 2. "pas de CapCut, pas de logiciel de montage, juste Claude" -> a checklist card; JUSTE CLAUDE behind her head (no sound)
    H.append('<div id="ck" class="ck">'
             '<div id="ck0" class="row"><img src="assets/logos/capcut.png"/><span>CapCut</span><em id="ckx0" class="no">' + CROSS + '</em></div>'
             '<div id="ck1" class="row"><img src="assets/logos/premiere.png"/><span>logiciel de montage</span><em id="ckx1" class="no">' + CROSS + '</em></div>'
             f'<div id="ck2" class="row gold"><b>{CLAUDE.format(s=58)}</b><span>juste Claude</span><em class="ok">' + CHECK + '</em></div></div>')
    a, b = ct(4.48), CUTS['claude'][0] + CUTS['claude'][1] - .03
    T += show('#ck', a, ct(6.62) + .3, "{autoAlpha:0,x:-80}", .3, 'power3.out')
    T += ["gsap.set('#ck1, #ck2, #ckx0, #ckx1',{autoAlpha:0});",
          f"tl.fromTo('#ckx0',{{autoAlpha:0,scale:2}},{{autoAlpha:1,scale:1,duration:.15,immediateRender:false}},{ct(4.80):.3f});",
          f"tl.fromTo('#ck1',{{autoAlpha:0,x:-40}},{{autoAlpha:1,x:0,duration:.2,immediateRender:false}},{ct(5.46):.3f});",
          f"tl.fromTo('#ckx1',{{autoAlpha:0,scale:2}},{{autoAlpha:1,scale:1,duration:.15,immediateRender:false}},{ct(5.98):.3f});",
          f"tl.fromTo('#ck2',{{autoAlpha:0,x:-40}},{{autoAlpha:1,x:0,duration:.2,immediateRender:false}},{ct(6.62):.3f});"]
    S += [('pop', a, .3), ('pop', ct(5.46), .25)]
    H.append('<div id="jc" class="jc"><div class="jcs">juste</div>CLAUDE</div>')
    a = ct(6.62) + .25
    T += ["gsap.set('#jc',{autoAlpha:0});",
          f"tl.fromTo('#jc',{{autoAlpha:0,y:120}},{{autoAlpha:1,y:0,duration:.35,ease:'power3.out',immediateRender:false}},{a:.3f});",
          f"tl.set('#jc',{{autoAlpha:0}},{b:.3f});"]

    # 3. the prompts as a chat thread with Claude: her message types itself, Claude answers "c'est fait"
    H.append(f'<div id="ch" class="chat"><div class="chh"><span class="bav sm">{CLAUDE.format(s=40)}</span>Claude<em>en ligne</em></div>'
             '<div id="cm" class="cm"><span id="cmt"></span></div><div id="cr" class="cr">c\'est fait ✨</div></div>')
    T += ["gsap.set('#ch',{autoAlpha:0});"]
    for txt, a, b, send, end in (('Monte ma vidéo dans ma charte', 15.80, 16.50, 16.62, 16.86),
                                 ('Mets un peu plus de rose', 18.72, 19.90, 20.06, 20.40),
                                 ('Fais un mur de réels derrière moi', 21.40, 23.10, 23.36, 23.62)):
        T += [f"tl.fromTo('#ch',{{autoAlpha:0,y:-40}},{{autoAlpha:1,y:0,duration:.22,ease:'power3.out',immediateRender:false}},{ct(a) - .12:.3f});",
              f"tl.set('#cr',{{autoAlpha:0}},{ct(a) - .12:.3f});",
              f"tl.fromTo('#cm',{{scale:.6,autoAlpha:0}},{{scale:1,autoAlpha:1,duration:.18,ease:'back.out(2)',immediateRender:false}},{ct(a) - .05:.3f});"]
        T += typing('#cmt', txt, ct(a), ct(b))
        T += [f"tl.fromTo('#cr',{{autoAlpha:0,scale:.5}},{{autoAlpha:1,scale:1,duration:.2,ease:'back.out(2.2)',immediateRender:false}},{ct(send):.3f});",
              f"tl.to('#ch',{{autoAlpha:0,y:-20,duration:.15}},{ct(end) - .15:.3f});"]
        S += [('pop', ct(send), .35)]

    # "et là toute la vidéo est montée": a progress loader, 0 -> 100 %, three steps ticked
    H.append('<div id="ld" class="ld"><div class="ldt">montage en cours…</div><div id="ldp" class="ldp">0%</div>'
             '<div class="ldb"><i id="ldf"></i></div><div class="lds"><span id="ls0">coupes ✓</span><span id="ls1">sous-titres ✓</span><span id="ls2">effets ✓</span></div></div>')
    a, b = ct(16.86), ct(18.66)
    T += show('#ld', a, b, "{autoAlpha:0,scale:.85}", .3)
    T += ["gsap.set('#ldf',{scaleX:0,transformOrigin:'0 50%'});",
          f"tl.to('#ldf',{{scaleX:1,duration:{b - a - .5:.2f},ease:'power1.inOut'}},{a + .2:.3f});"]
    T += setseq('#ldp', 'textContent', [f'{p}%' for p in range(0, 101, 5)], a + .2, (b - a - .5) / 20)
    T += ["gsap.set('#ls0, #ls1, #ls2',{autoAlpha:0});"] + \
         [f"tl.fromTo('#ls{i}',{{autoAlpha:0,y:12}},{{autoAlpha:1,y:0,duration:.15,immediateRender:false}},{a + .5 + i * .35:.3f});" for i in range(3)]
    S += [('whoosh-short', a, .3)]

    # 4. "un peu plus de rose, hop" -> the rosy look washes down from the top under a gold line
    H.append('<div id="wl" class="wl"></div><div id="rose" class="pill2">+ de rose</div>')
    a = ct(20.20)
    T += [f"tl.to('#bgl',{{clipPath:'inset(0 0 0% 0)',duration:.7,ease:'power2.inOut'}},{a:.3f});",
          "gsap.set('#wl',{autoAlpha:0});", f"tl.set('#wl',{{autoAlpha:1}},{a:.3f});",
          f"tl.fromTo('#wl',{{y:0}},{{y:1920,duration:.7,ease:'power2.inOut',immediateRender:false}},{a:.3f});",
          f"tl.set('#wl',{{autoAlpha:0}},{a + .72:.3f});"]
    T += show('#rose', a + .2, ct(20.40) + .9, "{autoAlpha:0,scale:.5}", .25)
    S += [('whoosh-short', a, .35)]

    # 5. "il met un mur de réel derrière moi" -> her reels drop in as a scattered polaroid collage behind her
    pol = ''
    for k in range(12):
        x, y = 30 + (k % 4) * 255 + (k // 4 % 2) * 40 - 20, 150 + (k // 4) * 360
        pol += (f'<div class="pol" style="left:{x}px;top:{y}px;transform:rotate({(-9, 6, -4, 10, 5, -8, 8, -5, -6, 7, -10, 4)[k]}deg)">'
                f'<img src="assets/reels/r{k + 1}.jpg"/></div>')
    H.append(f'<div id="col" class="colg"><div class="wsh2"></div>{pol}</div>')
    a, b = ct(25.85), ct(27.50)
    T += ["gsap.set('#col',{autoAlpha:0});", f"tl.set('#col',{{autoAlpha:1}},{a:.3f});",
          f"tl.fromTo('#col .pol',{{autoAlpha:0,y:-500,scale:1.4}},{{autoAlpha:1,y:0,scale:1,duration:.35,ease:'power3.out',stagger:{{each:.04,from:'random'}},immediateRender:false}},{a:.3f});",
          f"tl.fromTo('#col',{{scale:1}},{{scale:1.08,duration:{b - a:.2f},ease:'none',immediateRender:false}},{a:.3f});",
          f"tl.to('#col',{{autoAlpha:0,duration:.2}},{b - .2:.3f});", f"tl.set('#col',{{autoAlpha:0}},{b:.3f});"]
    S += [('whoosh-short', a, .45)]

    # 6. "j'y connais RIEN en montage" -> punch-in cut, outlined RIEN behind her head
    T += [f"tl.fromTo('#cam',{{scale:1.15}},{{scale:1,duration:.3,ease:'power3.out',immediateRender:false}},{ct(38.46):.3f});"]
    H.append('<div id="rien2" class="olw"><div class="ols">j\'y connais</div><div class="olt">RIEN</div></div>')
    T += ["gsap.set('#rien2',{autoAlpha:0});",
          f"tl.fromTo('#rien2',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.25,ease:'back.out(1.8)',immediateRender:false}},{ct(39.50):.3f});",
          f"tl.set('#rien2',{{autoAlpha:0}},{CUTS['rien'][0] + CUTS['rien'][1] - .05:.3f});"]
    S += [('pop', ct(39.50), .35)]

    # 7. the raw footage: upload pill, rush polaroid cut twice with scissors, then duration bars 1:13 -> 0:34
    H.append('<div id="up" class="up"><span>↑ envoi de ta vidéo brute</span><div class="upb"><i id="upf"></i></div></div>')
    T += show('#up', ct(40.58), ct(41.95), "{autoAlpha:0,y:-30}", .22, 'power3.out')
    T += ["gsap.set('#upf',{scaleX:0,transformOrigin:'0 50%'});", f"tl.to('#upf',{{scaleX:1,duration:1.1,ease:'power1.inOut'}},{ct(40.70):.3f});"]
    H.append('<div id="rp" class="rp"><video id="rpv" src="assets/rawclip.mp4" muted playsinline data-start="0" data-media-start="0" '
             f'data-duration="{DUR:.3f}" data-track-index="7"></video><div class="rpl">mes rushs · 1:13</div>'
             '<div id="sc0" class="scl" style="top:150px"><i></i><b>✂</b></div><div id="sc1" class="scl" style="top:300px"><i></i><b>✂</b></div></div>')
    T += show('#rp', ct(41.95), ct(44.56), "{autoAlpha:0,y:80,rotation:8}", .3, 'power3.out')
    T += ["gsap.set('#sc0, #sc1',{autoAlpha:0});"]
    for i, t in enumerate((43.04, 43.74)):
        T += [f"tl.set('#sc{i}',{{autoAlpha:1}},{ct(t):.3f});",
              f"tl.fromTo('#sc{i} i',{{scaleX:0}},{{scaleX:1,duration:.2,ease:'power2.out',immediateRender:false}},{ct(t):.3f});",
              f"tl.fromTo('#sc{i} b',{{x:-40}},{{x:330,duration:.2,ease:'power2.out',immediateRender:false}},{ct(t):.3f});"]
    S += [('pop', ct(41.95), .3), ('click-soft', ct(43.04), .5), ('click-soft', ct(43.74), .5)]
    H.append('<div id="du" class="du"><div class="dur"><span>brut</span><div class="dbar"><i id="db0"></i></div><b>1:13</b></div>'
             '<div class="dur"><span>réel</span><div class="dbar"><i id="db1" class="gd"></i></div><b id="dv1">1:13</b></div></div>')
    a = ct(44.56)
    T += show('#du', a, ct(45.52) + .2, "{autoAlpha:0,scale:.85}", .22)
    T += ["gsap.set('#db0, #db1',{scaleX:1,transformOrigin:'0 50%'});",
          f"tl.to('#db1',{{scaleX:.47,duration:.55,ease:'power3.inOut'}},{a + .15:.3f});"]
    T += setseq('#dv1', 'textContent', ['1:13', '1:02', '0:51', '0:43', '0:38', '0:34'], a + .15, .1)
    S += [('whoosh-short', a, .3)]

    # 8. "mettre du TEXTE derrière" -> echoed TEXTE behind her head; "changer d'ambiance" -> moody look + a moon badge
    H.append('<div id="tx2" class="ech"><div class="o">TEXTE</div><div>TEXTE</div><div class="o">TEXTE</div></div>')
    T += ["gsap.set('#tx2',{autoAlpha:0});",
          f"tl.set('#tx2',{{autoAlpha:1}},{ct(49.24):.3f});",
          f"tl.fromTo('#tx2 div',{{autoAlpha:0,y:60}},{{autoAlpha:1,y:0,duration:.2,stagger:.06,ease:'power3.out',immediateRender:false}},{ct(49.24):.3f});",
          f"tl.set('#tx2',{{autoAlpha:0}},{CUTS['text'][0] + CUTS['text'][1] - .05:.3f});"]
    T += ["gsap.set('#bgm',{opacity:0});", f"tl.to('#bgm',{{opacity:1,duration:.25}},{ct(50.78):.3f});", f"tl.set('#bgm',{{opacity:0}},{ct(51.36):.3f});"]
    H.append('<div id="moon" class="moon">☾<span>ambiance</span></div>')
    T += show('#moon', ct(50.78), ct(51.36) + .1, "{autoAlpha:0,scale:.4,rotation:-40}", .25)
    S += [('pop', ct(49.24), .35), ('whoosh-short', ct(50.78), .3)]

    # 9. "agrandir les sous-titres" -> a resize frame grows the word; "plan large, plus serré, des cuts" -> REC viewfinder
    H.append('<div id="rz" class="rz"><div id="rzb" class="rzb"><i class="h tl"></i><i class="h tr"></i><i class="h bl"></i><i class="h br"></i>'
             '<span id="rzt">sous-titres</span></div></div>')
    a = ct(52.84)
    T += show('#rz', a, ct(53.80), "{autoAlpha:0}", .15, 'none')
    T += [f"tl.fromTo('#rzb',{{scale:.42}},{{scale:1,duration:.5,ease:'back.out(1.6)',immediateRender:false}},{a + .1:.3f});"]
    S += [('pop', a, .3)]
    H.append('<div id="vf" class="vf"><i class="cn tl"></i><i class="cn tr"></i><i class="cn bl"></i><i class="cn br"></i>'
             '<div class="rec"><b></b>REC</div><div id="vfl" class="vfl">plan large</div></div>')
    a, b = ct(54.10), ct(56.20)
    T += show('#vf', a, b, "{autoAlpha:0,scale:1.1}", .2, 'power3.out')
    for t, lab in ((55.02, 'plus serré'), (55.52, 'des cuts')):
        T += [f"tl.set('#vfl',{{textContent:{json.dumps(lab)}}},{ct(t):.3f});",
              f"tl.fromTo('#vfl',{{scale:1.3}},{{scale:1,duration:.15,immediateRender:false}},{ct(t):.3f});"]
    T += ["gsap.set('.rec b',{opacity:1});"] + [f"tl.set('.rec b',{{opacity:{k % 2}}},{a + k * .25:.3f});" for k in range(int((b - a) / .25))]
    S += [('whoosh-short', a, .3)]
    T += [f"tl.set('#cam',{{scale:1.18}},{ct(51.44):.3f});",
          f"tl.to('#cam',{{scale:1,duration:.4,ease:'power2.out'}},{ct(54.30):.3f});",
          f"tl.to('#cam',{{scale:1.4,duration:.25,ease:'power2.out'}},{ct(55.02):.3f});",
          f"tl.set('#cam',{{scale:1.1}},{ct(55.62):.3f});", f"tl.set('#cam',{{scale:1.3}},{ct(55.82):.3f});",
          f"tl.set('#cam',{{scale:1}},{ct(56.10):.3f});"]
    # "en deux secondes" -> a stopwatch ring fills up
    H.append('<div id="sw" class="sw"><svg viewBox="0 0 120 120" width="220" height="220"><circle cx="60" cy="60" r="50" class="swb"/>'
             '<circle id="swr" cx="60" cy="60" r="50" class="swr"/></svg><div class="swt">2 s</div></div>')
    a = ct(56.70)
    T += show('#sw', a, ct(57.20), "{autoAlpha:0,scale:.6}", .15)
    T += ["gsap.set('#swr',{strokeDasharray:315,strokeDashoffset:315});", f"tl.to('#swr',{{strokeDashoffset:0,duration:.35,ease:'none'}},{a + .05:.3f});"]

    # 10. the guide: its pages slide by as a carousel behind her, a brown Anton label; then comment MONTAGE, DM notification
    row = ''.join(f'<div class="cpg"><img src="assets/gpages/p-{p:02d}.png"/></div>' for p in list(range(1, 12)) + [1, 2])
    H.append(f'<div id="gcar" class="gcar"><div class="wsh2"></div><div id="gcr" class="gcr">{row}</div></div>')
    H.append('<div id="glb" class="glb">LE GUIDE COMPLET</div>')
    a, b = ct(65.38), CUTS['guide'][0] + CUTS['guide'][1] - .05
    T += ["gsap.set('#gcar',{autoAlpha:0});", f"tl.set('#gcar',{{autoAlpha:1}},{a:.3f});",
          f"tl.fromTo('#gcar .cpg',{{autoAlpha:0,y:200}},{{autoAlpha:1,y:0,duration:.35,stagger:.03,ease:'power3.out',immediateRender:false}},{a:.3f});",
          f"tl.fromTo('#gcr',{{x:60}},{{x:-3600,duration:{b - a:.2f},ease:'power1.inOut',immediateRender:false}},{a:.3f});",
          f"tl.to('#gcar',{{autoAlpha:0,duration:.2}},{b - .2:.3f});", f"tl.set('#gcar',{{autoAlpha:0}},{b:.3f});"]
    T += show('#glb', a + .6, b, "{autoAlpha:0,x:-80}", .3, 'power3.out')
    S += [('whoosh-short', a, .3)]
    H.append('<div id="cta2" class="cta2"><div class="ctl">commente</div><div id="mtg" class="mtg">MONTAGE</div><div class="ctl sm">et je t\'envoie le guide</div></div>')
    T += show('#cta2', ct(69.70), DUR + .2, "{autoAlpha:0,y:-20}", .22)
    T += [f"tl.fromTo('#mtg',{{scale:.4,rotation:-8}},{{scale:1,rotation:-3,duration:.35,ease:'back.out(2.2)',immediateRender:false}},{ct(70.10):.3f});",
          f"tl.to('#mtg',{{scale:1.08,duration:.18,yoyo:true,repeat:1}},{ct(70.62):.3f});"]
    S += [('pop', ct(70.10), .35)]
    H.append('<div id="nt" class="nt"><img src="assets/avatar.png"/><div><div class="ntt">thestrategicboost.fr<em>maintenant</em></div>'
             '<div class="nts">t\'a envoyé le guide 🎁</div></div></div>')
    T += show('#nt', ct(71.10), DUR + .2, "{autoAlpha:0,y:-120}", .35, 'power3.out')
    S += [('pop', ct(71.10), .4)]
    return H, T, S


CSS2 = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.cut{{z-index:5}}
#cam video{{transform:scaleX(-1) scale(1.06);filter:sepia(.6) saturate(1.35) hue-rotate(-8deg) contrast(1.1) brightness(1.03)}}
.cap2{{position:absolute;left:60px;right:60px;top:1320px;z-index:25;text-align:center;font:800 60px/1.3 Poppins;color:#fff;
  text-shadow:0 3px 0 rgba(40,20,5,.75)}}
.cap2 span{{display:inline-block;padding:2px 14px 6px;border-radius:999px;margin:0 2px}}
.bub{{position:absolute;z-index:20;padding:22px 34px;border-radius:44px;font:700 52px/1.15 Poppins;box-shadow:0 16px 36px rgba(0,0,0,.28)}}
.bub.wh{{left:70px;top:{TOP + 10}px;background:#fff;color:{INK};border-bottom-left-radius:10px;transform-origin:0 100%}}
.bub.au{{right:70px;top:{TOP + 150}px;background:{PILL};color:#fff;display:flex;align-items:center;gap:22px;font-style:italic;
  text-shadow:0 3px 0 rgba(70,35,5,.6);border-bottom-right-radius:10px;transform-origin:100% 100%}}
.bub.au b{{font-weight:800}}
.bav{{width:92px;height:92px;flex:none;border-radius:50%;background:{CREAM};display:flex;align-items:center;justify-content:center}}
.bav.sm{{width:58px;height:58px}}
.ring{{position:absolute;left:190px;top:380px;width:700px;height:700px;border-radius:50%;border:6px solid #E9C98F;z-index:2}}
.ck{{position:absolute;left:90px;right:90px;top:{TOP}px;z-index:20}}
.row{{display:flex;align-items:center;gap:20px;height:100px;padding:0 24px;margin-bottom:14px;border-radius:28px;background:{CREAM};
  font:700 42px/1 Poppins;color:{INK};box-shadow:0 14px 32px rgba(0,0,0,.28)}}
.row img,.row b{{width:62px;height:62px;border-radius:16px;flex:none;display:flex;align-items:center;justify-content:center}}
.row span{{flex:1}}
.row em{{width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.row em.no{{background:#C8453A}}
.row em.ok{{background:{DARK}}}
.row.gold span{{font-style:italic;color:{DARK}}}
.jc{{position:absolute;left:0;right:0;top:{TOP + 60}px;z-index:2;text-align:center;font:400 250px/.9 Anton;color:{CREAM};letter-spacing:.01em;
  text-shadow:0 8px 0 rgba(87,51,7,.55)}}
.jcs{{font:italic 700 80px/1 Poppins;color:#E9C98F;text-shadow:0 4px 0 rgba(70,35,5,.6);margin-bottom:10px}}
.chat{{position:absolute;left:70px;right:70px;top:{TOP}px;z-index:20;background:rgba(244,238,230,.97);border-radius:30px;padding:0 0 22px;
  box-shadow:0 20px 44px rgba(0,0,0,.3);overflow:hidden}}
.chh{{display:flex;align-items:center;gap:16px;padding:16px 24px;background:{DARK};font:700 32px/1 Poppins;color:#fff}}
.chh em{{font:italic 600 22px/1 Poppins;color:#E9C98F;margin-left:auto}}
.cm{{margin:22px 24px 0 auto;width:max-content;max-width:820px;padding:18px 26px;border-radius:30px;border-bottom-right-radius:8px;background:#8C5C41;
  font:600 36px/1.25 Poppins;color:#fff;transform-origin:100% 100%;min-height:80px}}
.cr{{margin:14px auto 0 24px;width:max-content;padding:14px 24px;border-radius:28px;border-bottom-left-radius:8px;background:{PILL};
  font:italic 700 34px/1 Poppins;color:#fff;text-shadow:0 2px 0 rgba(70,35,5,.6);transform-origin:0 100%}}
.ld{{position:absolute;left:140px;right:140px;top:{TOP}px;z-index:20;background:{INK};border-radius:30px;padding:28px 36px 30px;text-align:center;
  box-shadow:0 22px 50px rgba(0,0,0,.45)}}
.ldt{{font:italic 600 34px/1 Poppins;color:#E9C98F}}
.ldp{{font:400 150px/1.05 Anton;color:{CREAM}}}
.ldb{{height:18px;border-radius:9px;background:rgba(255,255,255,.12);overflow:hidden}}
.ldb i{{display:block;height:100%;background:{PILL}}}
.lds{{display:flex;justify-content:space-between;margin-top:20px;font:600 28px/1 Poppins;color:#F4EEE6}}
.wl{{position:absolute;left:0;right:0;top:0;height:8px;z-index:6;background:{PILL};box-shadow:0 0 30px rgba(233,201,143,.9)}}
.pill2{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP + 20}px;z-index:22;padding:14px 44px 18px;border-radius:999px;
  background:{PILL};font:italic 700 60px/1 Poppins;color:#fff;text-shadow:0 3px 0 rgba(70,35,5,.7)}}
.colg{{position:absolute;inset:0;z-index:2;overflow:hidden;transform-origin:50% 40%}}
.wsh2{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(42,26,16,.75),rgba(87,51,7,.55))}}
.pol{{position:absolute;width:250px;padding:12px 12px 40px;background:#FBF7F1;box-shadow:0 14px 30px rgba(0,0,0,.45)}}
.pol img{{width:100%;height:300px;object-fit:cover;display:block}}
.olw{{position:absolute;left:0;right:0;top:{TOP + 40}px;z-index:2;text-align:center}}
.ols{{font:italic 700 74px/1 Poppins;color:#fff;text-shadow:0 4px 0 rgba(70,35,5,.6)}}
.olt{{font:400 400px/.95 Anton;color:transparent;-webkit-text-stroke:7px #E9C98F;letter-spacing:.02em}}
.up{{position:absolute;left:150px;right:150px;top:{TOP + 10}px;z-index:20;background:rgba(244,238,230,.96);border-radius:26px;padding:22px 30px;
  font:600 34px/1 Poppins;color:{INK};box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.upb{{height:14px;border-radius:7px;background:rgba(87,51,7,.15);margin-top:18px;overflow:hidden}}
.upb i{{display:block;height:100%;background:{DARK}}}
.rp{{position:absolute;left:370px;top:{TOP - 10}px;width:340px;z-index:20;padding:14px 14px 60px;background:#FBF7F1;box-shadow:0 18px 40px rgba(0,0,0,.45);
  transform:rotate(-4deg)}}
.rp video{{width:312px;height:420px;object-fit:cover;display:block}}
.rpl{{position:absolute;left:0;right:0;bottom:14px;text-align:center;font:italic 700 32px/1 Poppins;color:{DARK}}}
.scl{{position:absolute;left:14px;right:14px;height:0}}
.scl i{{position:absolute;left:0;right:0;top:-2px;border-top:5px dashed #fff;transform-origin:0 50%;filter:drop-shadow(0 1px 2px rgba(0,0,0,.6))}}
.scl b{{position:absolute;left:0;top:-34px;font:400 60px/1 Poppins;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.6)}}
.du{{position:absolute;left:110px;right:110px;top:{TOP}px;z-index:20;background:{INK};border-radius:28px;padding:26px 30px;box-shadow:0 22px 50px rgba(0,0,0,.45)}}
.dur{{display:flex;align-items:center;gap:20px;height:80px;font:italic 700 34px/1 Poppins;color:#E9C98F}}
.dur span{{width:90px}}
.dur b{{font:400 64px/1 Anton;color:{CREAM};width:140px;text-align:right}}
.dbar{{flex:1;height:34px}}
.dbar i{{display:block;height:100%;border-radius:17px;background:#8C5C41}}
.dbar i.gd{{background:{PILL}}}
.ech{{position:absolute;left:0;right:0;top:{TOP + 20}px;z-index:2;text-align:center;font:400 230px/.86 Anton;color:{CREAM};letter-spacing:.02em}}
.ech .o{{color:transparent;-webkit-text-stroke:5px #E9C98F}}
.moon{{position:absolute;left:0;right:0;margin:0 auto;width:250px;height:250px;top:{TOP}px;z-index:20;border-radius:50%;background:rgba(42,26,16,.9);
  border:4px solid #E9C98F;text-align:center;font:400 110px/1.3 Poppins;color:#E9C98F}}
.moon span{{display:block;font:italic 700 30px/1 Poppins;color:#fff;margin-top:-18px}}
.rz{{position:absolute;left:0;right:0;top:{TOP + 30}px;z-index:20;text-align:center}}
.rzb{{position:relative;display:inline-block;transform-origin:50% 50%;padding:16px 36px;border:3px dashed #E9C98F}}
.rzb span{{font:800 104px/1.1 Poppins;color:#fff;text-shadow:0 4px 0 rgba(40,20,5,.75)}}
.h{{position:absolute;width:24px;height:24px;background:#fff;border:3px solid {DARK}}}
.h.tl{{left:-14px;top:-14px}} .h.tr{{right:-14px;top:-14px}} .h.bl{{left:-14px;bottom:-14px}} .h.br{{right:-14px;bottom:-14px}}
.vf{{position:absolute;left:70px;right:70px;top:{TOP}px;bottom:420px;z-index:19}}
.cn{{position:absolute;width:90px;height:90px;border:0 solid #fff}}
.cn.tl{{left:0;top:0;border-left-width:8px;border-top-width:8px}} .cn.tr{{right:0;top:0;border-right-width:8px;border-top-width:8px}}
.cn.bl{{left:0;bottom:0;border-left-width:8px;border-bottom-width:8px}} .cn.br{{right:0;bottom:0;border-right-width:8px;border-bottom-width:8px}}
.rec{{position:absolute;left:40px;top:34px;font:700 36px/1 Poppins;color:#fff;display:flex;align-items:center;gap:12px;text-shadow:0 2px 8px rgba(0,0,0,.5)}}
.rec b{{width:24px;height:24px;border-radius:50%;background:#E0453A}}
.vfl{{position:absolute;right:40px;top:26px;padding:10px 26px 14px;border-radius:999px;background:{PILL};font:italic 700 40px/1 Poppins;color:#fff;
  text-shadow:0 2px 0 rgba(70,35,5,.7);transform-origin:100% 0}}
.sw{{position:absolute;left:430px;top:{TOP}px;width:220px;height:220px;z-index:20}}
.sw svg{{transform:rotate(-90deg);filter:drop-shadow(0 10px 22px rgba(0,0,0,.4))}}
.swb{{fill:rgba(42,26,16,.9);stroke:rgba(255,255,255,.15);stroke-width:10}}
.swr{{fill:none;stroke:#E9C98F;stroke-width:10;stroke-linecap:round}}
.swt{{position:absolute;inset:0;text-align:center;font:400 84px/220px Anton;color:{CREAM}}}
.gcar{{position:absolute;inset:0;z-index:2;overflow:hidden}}
.gcr{{position:absolute;left:0;top:{TOP + 120}px;display:flex;gap:36px}}
.cpg{{width:420px;height:594px;flex:none;border-radius:12px;overflow:hidden;box-shadow:0 20px 44px rgba(0,0,0,.5)}}
.cpg img{{width:100%;height:100%;object-fit:cover;display:block}}
.glb{{position:absolute;left:70px;top:{TOP + 10}px;z-index:22;padding:10px 26px 6px;background:{DARK};font:400 64px/1.1 Anton;color:{CREAM};letter-spacing:.03em}}
.cta2{{position:absolute;left:0;right:0;top:{TOP}px;z-index:21;text-align:center}}
.ctl{{font:italic 700 56px/1.1 Poppins;color:#fff;text-shadow:0 3px 0 rgba(40,20,5,.75)}}
.ctl.sm{{font-size:40px;margin-top:16px}}
.mtg{{display:inline-block;margin-top:14px;padding:16px 50px 10px;border-radius:24px;background:{PILL};font:400 120px/1 Anton;color:#fff;letter-spacing:.05em;
  text-shadow:0 5px 0 rgba(70,35,5,.6);transform:rotate(-3deg)}}
.nt{{position:absolute;left:60px;right:60px;top:{TOP + 380}px;z-index:22;padding:22px 26px;border-radius:34px;background:rgba(250,246,240,.94);display:flex;
  align-items:center;gap:22px;box-shadow:0 20px 44px rgba(0,0,0,.3)}}
.nt img{{width:84px;height:84px;border-radius:22px;object-fit:cover}}
.ntt{{font:700 32px/1.1 Poppins;color:{INK};display:flex;gap:16px;align-items:baseline}}
.ntt em{{font:500 24px/1 Poppins;color:#9A8C7E;font-style:normal}}
.nts{{font:500 32px/1.3 Poppins;color:#3A2A1E;margin-top:4px}}
'''

B.scenes = scenes
B.captions = captions
B.CSS = CSS2
B.BEHIND = ('rg0', 'rg1', 'rg2', 'rg3', 'jc', 'col', 'rien2', 'tx2', 'gcar')

if __name__ == '__main__':
    with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
        _f.write(B.build())
    print(f'wrote index.html (DA 2) {DUR:.3f}s')
