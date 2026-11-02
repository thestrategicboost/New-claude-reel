#!/usr/bin/env python3
"""10 hooks qui arrêtent le scroll, after her published "10 hooks" reel (src/modele.mp4): a big white "10" with "HOOKS"
in the brown block and a white pill that types "qui arrêtent le scroll"; then each hook in a white pill at the top
while she says it; the CTA as a brown block + white pill, with her one-word captions under it. Lilac look + her
retouch (cut.py), alternate punch-ins hide the cuts.

PY cut.py v1|v2      then      PY build.py v1|v2      writes index.html
"""
import json
import re
import sys

V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
SEG = json.load(open(f'work/{V}/segs.json'))
PIECES, DURS = SEG['pieces'], SEG['durs']
DUR = round(sum(DURS), 3)
WORDS = json.load(open(f'work/{V}/words.json'))
DARK = '#573307'
CTA_BIG = {'v1': 'COMMENTE', 'v2': 'ABONNE-TOI'}[V]
CTA_SFX = {'v1': 'bloop', 'v2': 'ding'}[V]          # a comment = message bloop, a follow = notification ding
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
                  "tl.fromTo('#hp',{autoAlpha:0,scaleX:.3},{autoAlpha:1,scaleX:1,duration:.18,ease:'power3.out',immediateRender:false},.5);",
                  "tl.set('#tx',{textContent:''},0);"]
            ws = [w for w in WORDS if w['s'] < end and w['w'].strip().lower().startswith('qui')]
            ta = ws[0]['s'] if ws else .7
            tb = min(end - .25, ta + .9)
            T += [f"tl.set('#tx',{{textContent:{json.dumps(text[:k])}}},{ta + (tb - ta) * k / len(text):.3f});" for k in range(1, len(text) + 1)]
            S += [('pop', .02, .5), ('typing', ta, .45, tb - ta + .1)]
        elif kind == 'hook':
            H.append(f'<div id="h{i}" class="hkw"><div class="pill hk">{text}</div></div>')
            T += show(f'#h{i}', e + .02, end, '{autoAlpha:0,scale:.7,y:-10}', .2)
            S.append(('click-soft', e + .02, .35))
        elif kind == 'cta':
            last = DUR
            H.append(f'<div id="cta" class="hd cta"><div class="hblk big">{CTA_BIG}</div><br/><div class="pill cp">{text}</div></div>')
            ws = [w for w in WORDS if w['s'] >= e - .05]
            key = 'commente' if V == 'v1' else 'abonne'
            t0 = next((w['s'] for w in ws if w['w'].strip().lower().startswith(key)), e + .1)
            T += show('#cta', t0 - .05, last, '{autoAlpha:0,scale:.7,y:-20}', .28)
            S += [('pop', t0 - .05, .45), (CTA_SFX, t0 + .3, .45)]
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
.hkw{{position:absolute;left:0;right:0;top:330px;z-index:20;text-align:center}}
.hk{{white-space:nowrap;font-size:36px;letter-spacing:-.03em;padding:12px 28px}}
.cp{{margin-top:-8px;font-size:56px;padding:6px 46px}}
.cap{{position:absolute;left:40px;right:40px;top:1400px;z-index:25;text-align:center;font:700 66px/1 Poppins;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
'''
SFX_LEN = {'pop': .72, 'click-soft': .36, 'bloop': .6, 'ding': 1.2}


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
