#!/usr/bin/env python3
"""Reel "3 types de contenus : tofu, mofu, bofu", edited after her own 3-band reel: the frame is split into three
landscape bands (TOFU on top, MOFU in the middle, BOFU at the bottom). The band of the part she is talking about
plays her take, bright; the two others play idle footage of her, dimmed. Each band gets its own small graphics on
the left (she sits on the right): the TOFU/MOFU/BOFU badge with its views, the funnel with its tier lit, view
badges, the reach ring, her profile card, her community, a shield, a crown, example reels. One-word captions in the
active band, her profile follow card on "abonne-toi".

PY cut.py      takes -> assets/aroll.mp4 (landscape) + voice + idle tracks
PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
SEGS = json.load(open('work/segs.json'))
PARTS = json.load(open('work/partdurs.json'))         # real length of each kept piece in assets/aroll.mp4
DARK, BROWN, GOLD = '#573307', '#8C5C41', '#C99A55'
BAND = 640


def ct(t):
    out = 0.0
    for (a, b), d in zip(SEGS, PARTS):
        if t >= b:
            out += d
        else:
            return out + max(0.0, t - a)
    return out


EDGES = []
_e = 0.0
for _d in PARTS:
    EDGES.append(_e)
    _e += _d

FIX = {'bouffou': 'bofu', "d'étroits": 'des trois', 'list': 'liste', 'tchuss': 'tchus', 'tchüss': 'tchus'}


def words():
    out = []
    for w in json.load(open('work/raw_words.json')):
        if not any(a - .05 <= w['s'] < b for a, b in SEGS):
            continue
        t = w['w'].strip()
        if (t.startswith("'") or t.startswith('-')) and out:
            out[-1]['w'] += t
            out[-1]['e'] = w['e']
        else:
            out.append(dict(w, w=t))
    for w in out:
        k = re.sub(r'[,.!?…]', '', w['w']).lower()
        w['t'] = FIX.get(k, k)
        w['s'], w['e'] = ct(w['s']), ct(min(w['e'], w['s'] + 1.2))
    return [w for w in out if w['t']]


def at(raw):
    return ct(raw)


# which band is lit, from when (edit time)
ACTIVE = [(0.0, 0), (at(7.88), 1), (at(8.52), 2), (EDGES[1], 0), (EDGES[5], 1), (EDGES[11], 2), (EDGES[14], 3)]   # 3 = all three bands


def band_of(t):
    k = 0
    for a, b in ACTIVE:
        if t >= a - 1e-6:
            k = b
    return k


def pop(sel, a, b, frm='{autoAlpha:0,scale:.6}', d=.28):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,scale:1,x:0,y:0,duration:{d},ease:'back.out(2)',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,duration:.15}},{b - .15:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


EYE = '<svg viewBox="0 0 24 24" width="26" height="26"><path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6S2 12 2 12z" fill="none" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="#fff"/></svg>'


def funnel(i, lit, label):
    tiers = ''
    for k, w in enumerate((380, 290, 200)):
        on = k == lit
        tiers += (f'<div class="ft{" on" if on else ""}" style="width:{w}px">' + (f'<b>{label}</b>' if on else '') + '</div>')
    return f'<div id="fn{i}" class="fun">{tiers}</div>'


def scenes():
    H, T, S = [], [], []
    # the three bands
    for k in range(3):
        H.append(f'<div id="bd{k}" class="band" style="top:{k * BAND}px">'
                 f'<video id="mv{k}" class="bv" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="{k}"></video>'
                 f'<img id="iv{k}" class="bv" src="assets/still/b{k}.jpg"/>'     # the bands not talking are frozen
                 f'<i id="dm{k}" class="dim"></i><div id="gx{k}" class="gx"></div></div>')
    T += [f"gsap.set('#dm{q}',{{opacity:{0 if q == 0 else 1}}});" for q in range(3)]
    last = None
    for a, k in ACTIVE:
        for q in range(3):
            on = q == k or k == 3
            T += [f"tl.set('#mv{q}',{{opacity:{1 if on else 0}}},{a:.3f});", f"tl.set('#iv{q}',{{opacity:{0 if on else 1}}},{a:.3f});",
                  f"tl.to('#dm{q}',{{opacity:{0 if on else 1},duration:.12}},{a:.3f});"]
        last = k
    _ = last

    g = {0: [], 1: [], 2: []}            # graphics per band (html), placed inside the band's .gx box (left side)

    def add(band, html, tw):
        g[band].append(html)
        T.extend(tw)

    # hook badges: TOFU 1M / MOFU 100K / BOFU 10K, one per band on its word
    for k, (name, views, t) in enumerate((('TOFU', '1M', 7.22), ('MOFU', '100K', 7.88), ('BOFU', '10K', 8.52))):
        add(k, f'<div id="hb{k}" class="badge"><b>{name}</b><span>{EYE}{views}</span></div>', pop(f'#hb{k}', at(t), EDGES[1]))
        S.append(('pop', at(t), .3))

    def clip(band, name, a, b):
        """one of her own example reels, cut out of her old 3-band edit (assets/ex), playing in a white frame"""
        vid = f'ex_{name}'
        add(band, f'<div id="{vid}" class="exv"><video id="{vid}v" src="assets/ex/{name}.mp4" muted playsinline data-start="{a:.3f}" '
                  f'data-media-start="0" data-duration="{b - a + .4:.3f}" data-track-index="{30 + len(S) % 60}"></video></div>',   # outlives its frame
            pop(f'#{vid}', a, b, '{autoAlpha:0,y:40,scale:.7}', .24))
        S.append(('pop', a, .26))

    # TOFU
    add(0, funnel(0, 0, 'TOFU'), pop('#fn0', at(16.66), EDGES[2], '{autoAlpha:0,y:-30,scale:.8}'))
    S.append(('whoosh-short', at(16.66), .25))
    add(0, '<div id="vw0" class="views">' + ''.join(f'<span>{EYE}{v}</span>' for v in ('806K', '414K', '614K', '599K')) + '</div>',
        pop('#vw0', at(24.76), EDGES[3]) + [f"tl.fromTo('#vw0 span',{{scale:0}},{{scale:1,duration:.18,stagger:.08,ease:'back.out(2.5)',immediateRender:false}},{at(24.76):.3f});"])
    S.append(('pop', at(24.76), .3))
    add(0, '<div id="rg0" class="ring"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="48" class="rb"/><circle id="rgc" cx="60" cy="60" r="48" class="rf"/></svg>'
           '<b id="rgn">0</b><small>comptes touchés</small></div>',
        pop('#rg0', at(33.66), EDGES[4]) + ["gsap.set('#rgc',{strokeDasharray:302,strokeDashoffset:302});",
                                            f"tl.to('#rgc',{{strokeDashoffset:40,duration:1.1,ease:'power2.out'}},{at(33.9):.3f});"]
        + [f"tl.set('#rgn',{{textContent:'{int(722218 * (q + 1) / 16):,}'.replace(',', ' ')}},{at(33.9) + q * .07:.3f});" for q in range(16)])
    S.append(('ding', at(33.66), .3))
    # "les vidéos de type liste / de notation / de storytelling": the same example reels as in her old edit
    clip(0, 'liste', at(46.92), at(47.80))
    clip(0, 'notation', at(47.80), at(48.58))
    clip(0, 'story', at(48.58), EDGES[5])

    # MOFU
    add(1, funnel(1, 1, 'MOFU'), pop('#fn1', at(56.0), EDGES[6] + .5, '{autoAlpha:0,y:-30,scale:.8}'))
    S.append(('whoosh-short', at(56.0), .25))
    # "une base d'abonnés solide": her real profile header (9 218 followers, from her own reel), the count circled
    add(1, '<div id="pf1" class="prof2"><img src="assets/still/profil.png"/><i id="pf1h" class="hl"></i></div>',
        pop('#pf1', at(58.42), EDGES[7]) + ["gsap.set('#pf1h',{autoAlpha:0});",
                                            f"tl.fromTo('#pf1h',{{autoAlpha:0,scale:1.4}},{{autoAlpha:1,scale:1,duration:.25,ease:'back.out(2)',immediateRender:false}},{at(58.74):.3f});"])
    S.append(('pop', at(58.42), .3))
    add(1, '<div id="cm1" class="comm"><img class="me" src="assets/avatar.png"/>' + ''.join(f'<i class="h h{q}">♥</i>' for q in range(4)) + '</div>',
        pop('#cm1', at(65.54), at(67.5)) + [f"tl.fromTo('#cm1 .h',{{scale:0}},{{scale:1,duration:.2,stagger:.1,ease:'back.out(3)',immediateRender:false}},{at(65.8):.3f});"])
    S.append(('bloop', at(65.54), .3))
    add(1, '<div id="sh1" class="shield"><svg viewBox="0 0 100 116"><defs><linearGradient id="shg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3DFB2"/>'
           '<stop offset=".5" stop-color="#D6AE66"/><stop offset="1" stop-color="#9E6E33"/></linearGradient></defs>'
           '<path d="M50 4 L92 18 V54 C92 82 74 102 50 112 C26 102 8 82 8 54 V18 Z" fill="url(#shg)" stroke="#fff" stroke-width="4"/>'
           '<path d="M30 58 L45 73 L72 44" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg></div>',
        pop('#sh1', at(67.58), EDGES[8]))
    S.append(('pop', at(67.58), .3))
    clip(1, 'educatif', at(76.80), EDGES[9])
    clip(1, 'tutoriels', at(90.04), EDGES[10])
    clip(1, 'reussites', at(110.42), at(112.10))
    clip(1, 'echecs', at(112.10), EDGES[11])

    # BOFU
    add(2, '<div id="cr2" class="comm"><img class="me" src="assets/avatar.png"/><i class="crown">👑</i>' + ''.join(f'<i class="h h{q}">♥</i>' for q in range(4)) + '</div>',
        pop('#cr2', at(122.05), at(126.0)))
    S.append(('sparkle', at(122.05), .22))
    add(2, funnel(2, 2, 'BOFU'), pop('#fn2', at(126.14), EDGES[13], '{autoAlpha:0,y:-30,scale:.8}'))
    S.append(('whoosh-short', at(126.14), .25))
    # "avant-après / transformations personnelles ou celles de tes clients": her stats before/after, a client's voice
    # note, client messages (same reels as in her old edit)
    clip(2, 'avantapres', at(133.17), at(134.61))
    clip(2, 'temoignage', at(134.61), at(136.79))
    clip(2, 'messages', at(136.79), EDGES[14])

    # the mix of the three: all tiers lit, in the middle band
    add(1, '<div id="fmix" class="fun mix"><div class="ft on" style="width:380px"><b>TOFU</b></div><div class="ft on" style="width:290px"><b>MOFU</b></div>'
           '<div class="ft on" style="width:200px"><b>BOFU</b></div></div>',
        pop('#fmix', at(153.66), at(162.22) - .05, '{autoAlpha:0,y:-30,scale:.8}'))
    S.append(('sparkle', at(153.66), .22))

    # CTA: her profile follow card
    t_ab = at(162.22)
    add(1, '<div id="fol"><div class="fav"><img src="assets/avatar.png"/></div><div class="fnm">thestrategicboost.fr<div class="fsub">Stratégie Instagram</div></div>'
           '<div id="fbtn" class="fbtn">S’abonner</div><div id="fbtn2" class="fbtn on">Abonné</div></div>',
        ["gsap.set('#fol, #fbtn2',{autoAlpha:0});",
         f"tl.fromTo('#fol',{{autoAlpha:0,scale:.6,y:30}},{{autoAlpha:1,scale:1,y:0,duration:.35,ease:'back.out(1.8)',immediateRender:false}},{t_ab - .05:.3f});",
         f"tl.to('#fbtn',{{scale:.85,duration:.08,yoyo:true,repeat:1}},{t_ab + .45:.3f});", f"tl.set('#fbtn',{{autoAlpha:0}},{t_ab + .61:.3f});",
         f"tl.fromTo('#fbtn2',{{autoAlpha:0,scale:.8}},{{autoAlpha:1,scale:1,duration:.15,ease:'back.out(2)',immediateRender:false}},{t_ab + .61:.3f});"])
    S += [('pop', t_ab - .05, .35), ('click', t_ab + .45, .5)]

    for k in range(3):
        H[k] = H[k].replace(f'<div id="gx{k}" class="gx"></div>', f'<div id="gx{k}" class="gx">{"".join(g[k])}</div>')

    # one-word captions inside the lit band
    ws = words()
    for n, w in enumerate(ws):
        nxt = ws[n + 1]['s'] if n + 1 < len(ws) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        if end <= w['s']:
            continue
        k = band_of(w['s'] + .01)
        k = 1 if k == 3 else k
        H.append(f'<div id="w{n}" class="cap" style="top:{k * BAND + 470}px">{w["t"]}</div>')
        T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
              f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
              f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
    return H, T, S


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#1a1410}}
.band{{position:absolute;left:0;width:1080px;height:{BAND}px;overflow:hidden}}
.bv{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 40%}}
.dim{{position:absolute;inset:0;background:rgba(36,24,18,.62);z-index:2;opacity:0}}
.gx{{position:absolute;inset:0;z-index:3}}
.badge{{position:absolute;left:90px;top:110px;text-align:center}}
.badge b{{display:block;background:{DARK};color:#fff;font:400 92px/1 Anton;letter-spacing:.03em;padding:12px 30px 6px}}
.badge span{{display:inline-flex;align-items:center;gap:8px;margin-top:6px;padding:4px 14px;border-radius:8px;background:rgba(30,20,14,.85);font:700 30px/1.2 Poppins;color:#fff}}
.fun{{position:absolute;left:70px;top:150px;width:400px;display:flex;flex-direction:column;align-items:center;gap:8px}}
.ft{{height:86px;background:{DARK};clip-path:polygon(0 0,100% 0,88% 100%,12% 100%);display:flex;align-items:center;justify-content:center}}
.ft.on{{background:{GOLD}}}
.ft b{{font:400 48px/1 Anton;color:#fff;letter-spacing:.04em}}
.views{{position:absolute;left:60px;top:200px;width:460px;display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.views span{{display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:10px;background:rgba(20,14,10,.85);font:700 38px/1 Poppins;color:#fff}}
.ring{{position:absolute;left:110px;top:120px;width:300px;height:340px;border-radius:26px;background:#14101c;text-align:center;padding-top:20px}}
.ring svg{{width:200px;height:200px;transform:rotate(-90deg)}}
.rb{{fill:none;stroke:#2c2638;stroke-width:12}}
.rf{{fill:none;stroke:#B07CF2;stroke-width:12;stroke-linecap:round}}
.ring b{{position:absolute;left:0;right:0;top:100px;font:700 36px/1 Poppins;color:#fff}}
.ring small{{display:block;margin-top:12px;font:500 24px/1 Poppins;color:#bbb}}
.ex{{position:absolute;top:150px;width:140px;height:250px;border-radius:12px;overflow:hidden;border:4px solid #fff;box-shadow:0 12px 26px rgba(0,0,0,.4)}}
.ex img{{width:100%;height:100%;object-fit:cover;display:block}}
.prof2{{position:absolute;left:30px;top:180px;width:560px;border-radius:14px;overflow:hidden;box-shadow:0 14px 30px rgba(0,0,0,.35)}}
.prof2 img{{width:100%;display:block}}
.prof2 .hl{{position:absolute;left:248px;top:57px;width:100px;height:30px;border:4px solid {GOLD};border-radius:18px}}
.exv{{position:absolute;left:150px;top:100px;width:250px;height:440px;border-radius:14px;overflow:hidden;border:4px solid #fff;
  box-shadow:0 14px 30px rgba(0,0,0,.4);background:#000}}
.exv video{{width:100%;height:100%;object-fit:cover;transform:scale(1.04);display:block}}
.note{{position:absolute;top:170px;width:170px;height:210px;border-radius:16px;background:#fff;text-align:center;padding-top:22px;box-shadow:0 12px 26px rgba(0,0,0,.35)}}
.note small{{display:block;font:600 22px/1 Poppins;color:#777}} .note b{{display:block;font:400 74px/1.1 Anton;color:{DARK}}}
.note span{{font:400 30px/1 sans-serif;color:{GOLD}}}
.ba{{position:absolute;left:60px;top:150px;width:400px;height:300px;border-radius:16px;overflow:hidden;border:4px solid #fff;box-shadow:0 12px 26px rgba(0,0,0,.4)}}
.ba img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.ba .bl{{position:absolute;left:0;top:0;bottom:0;width:6px;margin-left:-3px;background:#fff}}
.ba span{{position:absolute;bottom:10px;padding:4px 14px;border-radius:999px;background:#fff;font:italic 800 24px/1 Poppins;color:{DARK}}}
.ba .l{{left:10px}} .ba .r{{right:10px}}
.ex.wide{{width:220px;height:390px;top:110px}}
.ex .tag{{position:absolute;left:0;right:0;bottom:8px;margin:0 auto;width:fit-content;padding:4px 12px;border-radius:999px;background:#fff;font:italic 800 22px/1 Poppins;color:{DARK}}}
.prof{{position:absolute;left:50px;top:220px;width:520px;display:flex;align-items:center;gap:18px;padding:18px 22px;border-radius:22px;background:#fff;box-shadow:0 14px 30px rgba(0,0,0,.3)}}
.prof img{{width:90px;height:90px;border-radius:50%;object-fit:cover}}
.prof b{{display:block;font:700 32px/1.2 Poppins;color:#111}} .prof small{{font:500 24px/1.2 Poppins;color:#777}}
.comm{{position:absolute;left:110px;top:130px;width:360px;height:360px}}
.comm .me{{position:absolute;left:110px;top:110px;width:140px;height:140px;border-radius:50%;object-fit:cover;border:5px solid #fff}}
.comm .h{{position:absolute;width:70px;height:70px;border-radius:50%;background:#fff;color:#E0457B;font:400 40px/70px sans-serif;text-align:center;font-style:normal;
  box-shadow:0 8px 18px rgba(0,0,0,.3)}}
.comm .h0{{left:10px;top:20px}} .comm .h1{{left:280px;top:30px}} .comm .h2{{left:20px;top:270px}} .comm .h3{{left:280px;top:260px}}
.comm .crown{{position:absolute;left:135px;top:40px;font:400 80px/1 sans-serif;font-style:normal}}
.shield{{position:absolute;left:180px;top:130px;width:220px;height:255px;filter:drop-shadow(0 12px 20px rgba(0,0,0,.35))}}
.shield svg{{width:100%;height:100%}}
.pg{{position:absolute;left:150px;top:110px;width:250px;height:354px;border-radius:12px;overflow:hidden;box-shadow:0 14px 30px rgba(0,0,0,.4)}}
.pg img{{width:100%;height:100%;object-fit:cover}}
.quote{{position:absolute;left:50px;top:220px;width:540px;padding:22px 28px;border-radius:24px;background:#fff;font:italic 700 36px/1.3 Poppins;color:{DARK};
  box-shadow:0 14px 30px rgba(0,0,0,.3)}}
#fol{{position:absolute;left:40px;top:240px;width:640px;height:140px;background:#fff;border-radius:26px;display:flex;align-items:center;gap:18px;padding:0 22px;
  box-shadow:0 18px 50px rgba(0,0,0,.3)}}
.fav{{width:94px;height:94px;border-radius:50%;padding:4px;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.fav img{{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid #fff;display:block}}
.fnm{{flex:1;font:700 28px/1.2 Poppins;color:#111}} .fsub{{font:500 22px/1.2 Poppins;color:#777}}
.fbtn{{position:absolute;right:20px;width:180px;height:66px;border-radius:14px;background:#0095F6;color:#fff;font:700 26px/66px Poppins;text-align:center}}
.fbtn.on{{background:#EFEFEF;color:#111}}
.cap{{position:absolute;left:520px;width:520px;z-index:20;text-align:center;font:700 58px/1 Poppins;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
'''

SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click': .36, 'ding': .75, 'bloop': .3, 'sparkle': 1.0}


def build():
    H, T, S = scenes()
    nl = '\n'
    sfx = [f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(SFX_LEN[n], DUR - t):.3f}" '
           f'data-track-index="{20 + k % 3}" data-volume="{v:.2f}"></audio>' for k, (n, t, v) in enumerate(sorted(S, key=lambda x: x[1]))]
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
  <audio id="voice" src="assets/voice.m4a" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="9" data-volume="1"></audio>
{nl.join(sfx)}
{nl.join(h for h in H if h)}
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
    print(f'wrote index.html {DUR:.3f}s')
