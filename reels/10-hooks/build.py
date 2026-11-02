#!/usr/bin/env python3
"""10 hooks qui arrêtent le scroll, after her published "10 hooks" reel (src/modele.mp4): a big white "10" with "HOOKS"
in the brown block and a white pill that types "qui arrêtent le scroll"; then a numbered list 1-10 with dotted
lines, each hook revealed in its row as she says it (and kept); the CTA as her Instagram comment banner (v1, "20" types
itself) or a brown block + white pill (v2), with her one-word captions under it. Lilac look + her
retouch (cut.py), alternate punch-ins hide the cuts.

PY cut.py v1|v2      then      PY build.py v1|v2      writes index.html
"""
import json
import re
import sys

V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
BLUR = 'blur' in sys.argv[2:]        # test: the hooks already on screen, blurred, each one coming sharp as she says it
SEG = json.load(open(f'work/{V}/segs.json'))
PIECES, DURS = SEG['pieces'], SEG['durs']
DUR = round(sum(DURS), 3)
WORDS = json.load(open(f'work/{V}/words.json'))
DARK = '#573307'
CTA_BIG = {'v1': 'COMMENTE', 'v2': 'ABONNE-TOI'}[V]
HOOKS = [p[3] for p in PIECES if p[2] == 'hook']
EDGES, _e = [], 0.0
for _d in DURS:
    EDGES.append(_e)
    _e += _d
FIX = {'tchüss': 'tchus', 'tchuss': 'tchus', 'dm': 'DM'}


def show(sel, a, b, frm='{autoAlpha:0,scale:.6}', d=.24, ease='back.out(2)'):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,scale:1,y:0,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,duration:.1}},{b - .1:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def scenes():
    H, T, S = [], [], []
    for i, ((_a, _b, kind, text), e, d) in enumerate(zip(PIECES, EDGES, DURS)):
        end = e + d
        T.append(f"tl.set('#bgv',{{scale:{1.0 if i % 2 == 0 else 1.08}}},{e:.3f});")     # alternate punch-in on every cut
        if kind == 'intro':
            H.append(f'<div id="hd" class="hd col"><div class="hrow"><span class="ten">10</span><span class="hblk">HOOKS</span></div>'
                     f'<div id="hp" class="pill hp"><span class="gh">{text}</span><span id="tx"></span></div></div>')
            T += show('#hd', .02, end, '{autoAlpha:0,scale:.8}', .26)
            T += ["gsap.set('#hp',{autoAlpha:0});",
                  "tl.fromTo('#hp',{autoAlpha:0,scaleX:.3},{autoAlpha:1,scaleX:1,duration:.18,ease:'power3.out',immediateRender:false},.3);",
                  "tl.set('#tx',{textContent:''},0);"]
            ta, tb = .45, min(end - .12, 1.75)          # the keyboard sound of her own viral reel (typing-ref), the text typed over it
            T += [f"tl.set('#tx',{{textContent:{json.dumps(text[:k])}}},{ta + (tb - ta) * k / len(text):.3f});" for k in range(1, len(text) + 1)]
            S += [('pop', .02, .5), ('typing-ref', ta, 1.0, min(1.8, end - ta))]
        elif kind == 'hook':
            # the numbered list: 1 to 10 with dotted lines, each hook revealed in its row as she says it, and kept
            k = len([p for p in PIECES[:i] if p[2] == 'hook'])
            if k == 0:
                list_end = EDGES[next(j for j, p in enumerate(PIECES) if p[2] == 'cta')]
                rows = ''.join(f'<div class="lr"><span id="n{q}" class="ln">{q + 1}</span>' + ('' if BLUR else f'<span id="d{q}" class="ld"></span>') +
                               (f'<span class="lp bl">{HOOKS[q]}</span>' if BLUR else '') + f'<span id="r{q}" class="lp">{HOOKS[q]}</span></div>' for q in range(len(HOOKS)))
                H.append(f'<div id="lst" class="lst">{rows}</div>')
                T += ["gsap.set('#lst',{autoAlpha:0});", "gsap.set('#lst .lr',{autoAlpha:0});",
                      f"tl.set('#lst',{{autoAlpha:1}},{e - .12:.3f});",
                      f"tl.fromTo('#lst .lr',{{autoAlpha:0,x:-40}},{{autoAlpha:1,x:0,duration:.16,stagger:.03,ease:'power3.out',immediateRender:false}},{e - .12:.3f});",
                      f"tl.to('#lst',{{autoAlpha:0,duration:.12}},{list_end - .12:.3f});", f"tl.set('#lst',{{autoAlpha:0}},{list_end:.3f});"]
                S.append(('whoosh-short', e - .14, .35))
            ta = e + (.08 if k else .25)
            T += [f"gsap.set('#r{k}',{{autoAlpha:0}});",
                  f"tl.fromTo('#r{k}',{{autoAlpha:0,scaleX:.2}},{{autoAlpha:1,scaleX:1,duration:.22,ease:'back.out(1.6)',immediateRender:false}},{ta:.3f});",
                  f"tl.fromTo('#n{k}',{{scale:1}},{{scale:1.3,duration:.12,yoyo:true,repeat:1,immediateRender:false}},{ta:.3f});"]
            if not BLUR:      # the dots leave once the hook is written
                T += [f"gsap.set('#d{k}',{{autoAlpha:1}});", f"tl.to('#d{k}',{{autoAlpha:0,duration:.12}},{ta + .1:.3f});"]
            S.append(('click-soft', ta, .4))
        elif kind == 'cta':
            last = DUR
            ws = [w for w in WORDS if w['s'] >= e - .05]
            key = 'commente' if V == 'v1' else 'abonne'
            t0 = next((w['s'] for w in ws if w['w'].strip().lower().startswith(key)), e + .1)
            if V == 'v1':
                # her Instagram comment banner: slides in on "commente", 20 types itself on the word, send is tapped
                big = text
                tb = next((w['s'] for w in ws if w['w'].strip() == big), t0 + .4)
                send = ('<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" '
                        'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
                H.append(f'<div id="cb" class="cb"><img class="cav" src="assets/avatar.png"/><div class="cw"><span id="cph" class="cph">Ajouter un commentaire…</span>'
                         f'<span id="cty" class="cty"></span><i id="ccr" class="ccr"></i></div><div id="csd" class="csd">{send}</div></div>')
                a_in = t0 - .1
                T += ["gsap.set('#cb',{autoAlpha:0});",
                      f"tl.fromTo('#cb',{{autoAlpha:0,y:-50,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:false}},{a_in:.3f});",
                      "gsap.set('#cty',{textContent:''});", "gsap.set('#cph',{display:'inline'});",
                      f"tl.set('#cty',{{textContent:''}},{a_in:.3f});", f"tl.set('#cph',{{display:'inline'}},{a_in:.3f});",
                      f"tl.set('#cph',{{display:'none'}},{tb:.3f});"]
                T += [f"tl.set('#cty',{{textContent:{json.dumps(big[:q])}}},{tb + (q - 1) * .08:.3f});" for q in range(1, len(big) + 1)]
                ts_ = tb + len(big) * .08 + .2
                T += ["gsap.set('#ccr',{opacity:1});"] + [f"tl.set('#ccr',{{opacity:{q % 2}}},{a_in + .3 + q * .25:.3f});" for q in range(int((DUR - a_in) / .25))]
                T += [f"tl.to('#csd',{{scale:.78,duration:.07,yoyo:true,repeat:1}},{ts_:.3f});",
                      f"tl.to('#cb',{{boxShadow:'0 0 0 7px {DARK}, 0 16px 36px rgba(0,0,0,.3)',scale:1.05,duration:.18,yoyo:true,repeat:1}},{ts_ + .1:.3f});"]
                S += [('pop', a_in, .45), ('click', ts_, .6)]
            else:
                # her profile follow card: slides in on "abonne-toi", the button is tapped and turns "Abonné(e)"
                H.append('<div id="fol"><div class="fav"><img src="assets/avatar.png"/></div><div class="fnm">thestrategicboost.fr<div class="fsub">Stratégie Instagram</div></div>'
                         '<div id="fbtn" class="fbtn">S’abonner</div><div id="fbtn2" class="fbtn on">Abonné(e)</div></div>')
                T += ["gsap.set('#fol, #fbtn2',{autoAlpha:0});",
                      f"tl.fromTo('#fol',{{autoAlpha:0,scale:.6,y:30}},{{autoAlpha:1,scale:1,y:0,duration:.35,ease:'back.out(1.8)',immediateRender:false}},{t0 - .1:.3f});",
                      f"tl.to('#fbtn',{{scale:.85,duration:.08,yoyo:true,repeat:1}},{t0 + .45:.3f});", f"tl.set('#fbtn',{{autoAlpha:0}},{t0 + .61:.3f});",
                      f"tl.fromTo('#fbtn2',{{autoAlpha:0,scale:.8}},{{autoAlpha:1,scale:1,duration:.15,ease:'back.out(2)',immediateRender:false}},{t0 + .61:.3f});"]
                S += [('pop', t0 - .1, .45), ('click', t0 + .45, .6)]
            # her one-word captions, CTA and goodbye only (as in her reel)
            cw = []
            for w in ws:
                t = w['w'].strip()
                if (t.startswith('-') or t.startswith("'")) and cw:
                    cw[-1]['t'] += t
                    cw[-1]['e'] = w['e']
                    continue
                k = re.sub(r'[,.!?…«»]', '', t).strip().lower()
                k = FIX.get(k, k)
                if k:
                    cw.append({'t': k, 's': w['s'], 'e': w['e']})
            for n, w in enumerate(cw):
                nxt = cw[n + 1]['s'] if n + 1 < len(cw) else DUR
                stop = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
                if stop <= w['s']:
                    continue
                H.append(f'<div id="w{n}" class="cap">{w["t"]}</div>')
                T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
                      f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, stop - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
                      f"tl.set('#w{n}',{{autoAlpha:0}},{stop:.3f});"]
    return H, T, S


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#bgv{{transform-origin:50% 30%}}
.hd{{position:absolute;left:0;right:0;top:260px;z-index:20;text-align:center}}
.hd.col{{display:flex;flex-direction:column;align-items:center}}
.hrow{{display:flex;align-items:flex-end}}
.ten{{font:400 250px/.8 Anton;color:#fff;text-shadow:0 6px 24px rgba(0,0,0,.25);margin-right:-34px;position:relative;z-index:2}}
.hblk{{display:inline-block;background:{DARK};color:#fff;font:400 96px/1.05 Anton;letter-spacing:.03em;padding:10px 28px 4px 50px;margin-bottom:46px}}
.hblk.big{{padding:10px 30px 4px;margin:0}}
.pill{{display:inline-block;max-width:820px;background:#fff;border-radius:40px;color:{DARK};font:italic 800 40px/1.25 Poppins;letter-spacing:-.02em;
  padding:10px 32px;box-shadow:0 4px 16px rgba(0,0,0,.22)}}
.hp{{position:relative;margin-top:-30px;white-space:nowrap;z-index:3}}
.gh{{visibility:hidden}}
#tx{{position:absolute;left:32px;top:10px}}
.lst{{position:absolute;left:180px;width:720px;top:195px;z-index:20}}
.lr{{position:relative;height:55px;display:flex;align-items:center}}
.ln{{flex:none;width:46px;height:46px;border-radius:50%;background:{DARK};color:#fff;font:400 28px/46px Anton;text-align:center;box-shadow:0 3px 10px rgba(0,0,0,.25)}}
.ld{{position:absolute;left:64px;width:600px;top:33px;border-bottom:5px dotted rgba(255,255,255,.95);filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))}}
.lp.bl{{filter:blur(9px);opacity:.9}}
.lp{{position:absolute;left:58px;top:4px;white-space:nowrap;background:#fff;border-radius:24px;color:{DARK};font:italic 800 31px/46px Poppins;letter-spacing:-.03em;
  padding:0 18px;box-shadow:0 3px 10px rgba(0,0,0,.22);transform-origin:0 50%}}
.cb{{position:absolute;left:90px;right:90px;top:330px;z-index:30;height:118px;border-radius:59px;background:#fff;display:flex;align-items:center;gap:20px;
  padding:0 18px;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.cav{{width:80px;height:80px;border-radius:50%;object-fit:cover;flex:none;border:3px solid {DARK}}}
.cw{{flex:1;display:flex;align-items:center;min-width:0}}
.cph{{font:500 36px/1 Poppins;color:#9A9087}}
.cty{{font:400 66px/1 Anton;letter-spacing:.06em;color:#2A1A10}}
.ccr{{width:4px;height:56px;background:{DARK};margin-left:6px}}
.csd{{width:84px;height:84px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center;flex:none}}
.fav{{width:100px;height:100px;border-radius:50%;padding:4px;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.fav img{{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid #fff;display:block}}
#fol{{position:absolute;z-index:22;left:130px;top:330px;width:820px;height:150px;background:#fff;border-radius:28px;display:flex;align-items:center;
  gap:22px;padding:0 26px;box-shadow:0 18px 50px rgba(0,0,0,.3)}}
.fnm{{flex:1;font:700 34px/1.2 Poppins;color:#111}} .fsub{{font:500 26px/1.2 Poppins;color:#777}}
.fbtn{{position:absolute;right:26px;width:220px;height:74px;border-radius:16px;background:#0095F6;color:#fff;font:700 30px/74px Poppins;text-align:center}}
.fbtn.on{{background:#EFEFEF;color:#111}}
.cp{{margin-top:-8px;font-size:56px;padding:6px 46px}}
.cap{{position:absolute;left:40px;right:40px;top:1400px;z-index:25;text-align:center;font:700 66px/1 Poppins;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
'''
SFX_LEN = {'pop': .72, 'click-soft': .36, 'click': .36, 'ding': 1.2, 'whoosh-short': .57, 'typing-ref': 1.8}


def build():
    H, T, S = scenes()
    nl = '\n'
    sfx = []
    for k, (n, t, v, *dd) in enumerate(sorted(S, key=lambda x: x[1])):
        d = dd[0] if dd else SFX_LEN[n]
        sfx.append(f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(d, DUR - t):.3f}" '
                   f'data-track-index="{10 + k % 3}" data-volume="{v:.2f}"></audio>')
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
