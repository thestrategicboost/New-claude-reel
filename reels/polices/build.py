#!/usr/bin/env python3
"""Reel "les polices", edited after the "Use these fonts for..." inspiration: a fixed header "Utilise ces polices"
on top; on each line four white chips pop in, each written in the font it names (real Google Fonts, in assets/gf),
and "pour les vidéos ..." lands under them in her gold pill. Her one-word captions, her lilac look, her
profile follow card on "abonne-toi". v2 opens with hook 2 under a hook title.

PY cut.py v1|v2      then      PY build.py v1|v2      writes index.html
"""
import json
import re
import shutil
import subprocess
import sys

V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
HEAD = sys.argv[2] if len(sys.argv) > 2 else 'B'      # her choice: the one-line brown header
ROW_Y = 250 + (235 if HEAD == 'A' else 145)      # chips under the header; the kind of video lands 125px lower
SEG = json.load(open(f'work/{V}/segs.json'))
SEGS, DURS = SEG['segs'], SEG['durs']
DUR = round(sum(DURS), 3)
WORDS = {'base': json.load(open('work/base_words.json')), 'hook2': json.load(open('work/hook2_words.json'))}
DARK, GOLD = '#573307', '#C99A55'
PILL = 'linear-gradient(135deg,#EBCB8B 0%,#C99A55 55%,#A97A3E 100%)'
TOP = 250

EDGES, _e = [], 0.0
for _d in DURS:
    EDGES.append(_e)
    _e += _d


def at(src, t):
    """time in a source clip -> edit time (first kept piece of that source that holds it)"""
    for (s, a, b), e in zip(SEGS, EDGES):
        if s == src and a - .05 <= t <= b + .05:
            return e + max(0.0, t - a)
    raise ValueError((src, t))


FIX = {'tchüss': 'tchus', 'tchuss': 'tchus', 'c-police': 'ces polices', 'bireaux': 'b-roll', 'story-telling': 'storytelling', 'réels': 'réels'}


def words():
    out = []
    for (src, a, b), e in zip(SEGS, EDGES):
        cur = []
        for w in WORDS[src]:
            if not (a - .05 <= w['s'] < b):
                continue
            t = w['w'].strip()
            if (t.startswith('-') or t.startswith("'")) and cur:
                cur[-1]['w'] += t
                cur[-1]['e'] = w['e']
            else:
                cur.append(dict(w, w=t))
        for w in cur:
            k = re.sub(r'[,.!?…]', '', w['w']).lower()
            k = FIX.get(k, k)
            if k:
                out.append({'t': k, 's': e + max(0.0, w['s'] - a), 'e': e + min(b, w['e']) - a})
    return out


# (body piece, fonts [(name, family, css extra)], label, word that names it)
CATS = [
    (0, [('Anton', 'Anton', ''), ('BEBAS NEUE', 'BebasNeue', ''), ('Archivo Black', 'ArchivoBlack', ''), ('Dancing', 'DancingScript', '')],
     'pour les vidéos facecam', 10.04),
    (1, [('Playfair Display', 'PlayfairDisplay', ''), ('Garamond', 'EBGaramond', ''), ('Inter', 'Inter', ''), ('Fraunces', 'Fraunces', '')],
     'pour les vidéos storytelling', 15.02),
    (2, [('Montserrat', 'Montserrat', ''), ('Instrument Serif', 'InstrumentSerif', 'font-style:italic;'), ('Outfit', 'Outfit', ''),
         ('Poppins', 'Poppins', '')], 'pour les vidéos éducatives', 19.96),
    (3, [('CINZEL', 'Cinzel', ''), ('UNBOUNDED', 'Unbounded', ''), ('Bodoni', 'BodoniModa', ''), ('Great Vibes', 'GreatVibes', '')],
     'pour les vidéos avec des b-roll', 32.86),
    (4, [('Montserrat', 'Montserrat', ''), ('Poppins', 'Poppins', ''), ('Outfit', 'Outfit', ''), ('Jost', 'Jost', '')],
     'pour tes sous-titres', 37.78),
]
CAT_START = [0, 1, 3, 5, 6, 7]                    # first body piece of each line (cut.py BODY), then the CTA piece


def show(sel, a, b, frm='{autoAlpha:0,scale:.6}', d=.26, ease='back.out(2)'):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,scale:1,y:0,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def scenes():
    H, T, S = [], [], []
    nh = len(SEGS) - 8                      # pieces before the body (the hook)
    body0 = EDGES[nh]
    if nh:
        H.append('<div id="hk" class="hk"><div class="hk1"><span>QUELLE POLICE</span></div><div class="hk2">utiliser sur tes réels ?</div></div>')
        T += show('#hk', .1, body0, '{autoAlpha:0,y:-30,scale:.9}', .3, 'power3.out')
        S.append(('whoosh-short', .1, .3))
    end_cats = EDGES[nh + 7]
    if HEAD == 'A':      # small white "utilise" above, "CES POLICES" in the brown block
        H.append('<div id="hd" class="hd"><div class="hds">utilise</div><div class="hd1"><span>CES POLICES</span></div></div>')
    else:                # the whole line in the brown block
        H.append('<div id="hd" class="hd"><div class="hd1 one"><span>UTILISE CES POLICES</span></div></div>')
    T += show('#hd', body0 + .05, end_cats, '{autoAlpha:0,y:-30}', .25, 'power3.out')
    for k, (piece, fonts, label, tw) in enumerate(CATS):
        a, b = EDGES[nh + CAT_START[k]], EDGES[nh + CAT_START[k + 1]]
        tc = a + .05                         # the fonts are up as soon as she starts the line
        chips = ''.join(f'<span class="ch" style="font-family:\'{fam}\';{extra}">{name}</span>' for name, fam, extra in fonts)
        H.append(f'<div id="row{k}" class="row{" sm" if k in (1, 3) else ""}">{chips}</div><div id="lb{k}" class="lb">{label}</div>')
        T += [f"gsap.set('#row{k} .ch',{{autoAlpha:0}});", f"gsap.set('#row{k}',{{autoAlpha:1}});",
              f"tl.fromTo('#row{k} .ch',{{autoAlpha:0,scale:.5,y:20}},{{autoAlpha:1,scale:1,y:0,duration:.22,stagger:.07,ease:'back.out(2.2)',immediateRender:false}},{tc:.3f});",
              f"tl.to('#row{k} .ch',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('#row{k} .ch',{{autoAlpha:0}},{b:.3f});"]
        T += show(f'#lb{k}', at('base', tw), b, '{autoAlpha:0,scale:.6,y:14}', .24)
        S += [('pop', tc, .3), ('click-soft', at('base', tw), .4)]
    # CTA: her profile follow card
    t_ab = at('base', 39.2)
    H.append('<div id="fol"><div class="fav"><img src="assets/avatar.png"/></div><div class="fnm">thestrategicboost.fr<div class="fsub">Stratégie Instagram</div></div>'
             '<div id="fbtn" class="fbtn">S’abonner</div><div id="fbtn2" class="fbtn on">Abonné</div></div>')
    T += ["gsap.set('#fol, #fbtn2',{autoAlpha:0});",
          f"tl.fromTo('#fol',{{autoAlpha:0,scale:.6,y:30}},{{autoAlpha:1,scale:1,y:0,duration:.35,ease:'back.out(1.8)',immediateRender:false}},{t_ab - .05:.3f});",
          f"tl.to('#fbtn',{{scale:.85,duration:.08,yoyo:true,repeat:1}},{t_ab + .45:.3f});", f"tl.set('#fbtn',{{autoAlpha:0}},{t_ab + .61:.3f});",
          f"tl.fromTo('#fbtn2',{{autoAlpha:0,scale:.8}},{{autoAlpha:1,scale:1,duration:.15,ease:'back.out(2)',immediateRender:false}},{t_ab + .61:.3f});"]
    S += [('pop', t_ab - .05, .35), ('click', t_ab + .45, .5)]
    # her one-word captions
    ws = words()
    for n, w in enumerate(ws):
        nxt = ws[n + 1]['s'] if n + 1 < len(ws) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        if end <= w['s']:
            continue
        H.append(f'<div id="w{n}" class="cap">{w["t"]}</div>')
        T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
              f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
              f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
    return H, T, S


FACES = ['Anton', 'BebasNeue', 'ArchivoBlack', 'DancingScript', 'PlayfairDisplay', 'EBGaramond', 'Inter', 'Fraunces', 'Montserrat',
         'InstrumentSerif', 'Outfit', 'Cinzel', 'BodoniModa', 'Unbounded', 'GreatVibes', 'Poppins', 'Jost']
CSS = ''.join(f"@font-face{{font-family:'{f}';src:url(assets/gf/{f}.woff2) format('woff2');}}\n" for f in FACES) + f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.hk{{position:absolute;left:0;right:0;top:{TOP + 40}px;z-index:20;text-align:center}}
.hk1 span{{display:inline-block;background:{DARK};color:#fff;font:400 112px/1.05 Anton;letter-spacing:.03em;padding:10px 30px 6px}}
.hk2{{display:inline-block;margin-top:-6px;padding:12px 44px 16px;border-radius:999px;background:#fff;font:italic 800 52px/1 Poppins;color:{DARK};
  box-shadow:0 8px 20px rgba(0,0,0,.18)}}
.hd{{position:absolute;left:0;right:0;top:{TOP + 10}px;z-index:20;text-align:center}}
.hd1 span{{display:inline-block;background:{DARK};color:#fff;font:400 96px/1.05 Anton;letter-spacing:.03em;padding:8px 28px 4px}}
.hds{{font:700 46px/1.1 Poppins;color:#fff;text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.5);margin:2px 0}}
.hd1.one span{{font-size:78px;padding:10px 26px 6px}}
.row{{position:absolute;left:40px;right:40px;top:{ROW_Y}px;z-index:20;display:flex;justify-content:center;align-items:center;gap:10px}}
.row.sm .ch{{font-size:36px}}
.ch{{background:#fff;color:#111;border-radius:12px;padding:10px 14px 8px;font-size:42px;line-height:1.1;white-space:nowrap;box-shadow:0 8px 20px rgba(0,0,0,.25)}}
.lb{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{ROW_Y + 125}px;z-index:21;padding:12px 40px 16px;border-radius:999px;background:{PILL};
  font:italic 700 50px/1 Poppins;color:#fff;text-shadow:0 3px 0 rgba(70,35,5,.7)}}
#fol{{position:absolute;z-index:22;left:110px;top:{TOP + 120}px;width:860px;height:150px;background:#fff;border-radius:28px;display:flex;align-items:center;
  gap:22px;padding:0 26px;box-shadow:0 18px 50px rgba(0,0,0,.3)}}
.fav{{width:100px;height:100px;border-radius:50%;padding:4px;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.fav img{{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid #fff;display:block}}
.fnm{{flex:1;font:700 34px/1.2 Poppins;color:#111}} .fsub{{font:500 26px/1.2 Poppins;color:#777}}
.fbtn{{position:absolute;right:26px;width:220px;height:74px;border-radius:16px;background:#0095F6;color:#fff;font:700 30px/74px Poppins;text-align:center}}
.fbtn.on{{background:#EFEFEF;color:#111}}
.cap{{position:absolute;left:40px;right:40px;top:1230px;z-index:25;text-align:center;font:700 66px/1 Poppins;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
'''
SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click': .36, 'click-soft': .36}


def build():
    H, T, S = scenes()
    nl = '\n'
    sfx = [f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(SFX_LEN[n], DUR - t):.3f}" '
           f'data-track-index="{10 + k % 3}" data-volume="{v:.2f}"></audio>' for k, (n, t, v) in enumerate(sorted(S, key=lambda x: x[1]))]
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
  <audio id="voice" src="work/{V}/voice.m4a" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(sfx)}
  <video id="bgv" class="full" src="work/{V}/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(H)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(T)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


if __name__ == '__main__':
    with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
        _f.write(build())
    print(f'wrote index.html ({V}) {DUR:.3f}s')
