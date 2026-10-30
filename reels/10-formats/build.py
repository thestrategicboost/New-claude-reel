#!/usr/bin/env python3
"""Reel "les 10 formats viraux": she counts the ten formats on her fingers; as she names each one, the same example
clip as in her first "10 formats" reel (cut out of src/old.mp4 into assets/clips) pops in on her chest under a
numbered white pill (dark brown text, as in her first reel), with a soft pop. Hook title, her profile follow card on the CTA, her usual one-word captions on the hook and the CTA, lilac look.

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
SEGS = json.load(open('work/segs.json'))
PILL = 'linear-gradient(135deg,#EBCB8B 0%,#C99A55 55%,#A97A3E 100%)'
DARK, BROWN, INK, CREAM = '#573307', '#8C5C41', '#2A1A10', '#F4EEE6'
TOP = 250


def ct(t):
    out = 0.0
    for a, b in SEGS:
        if t >= b:
            out += b - a
        else:
            return out + max(0.0, t - a)
    return out


FIX = {'cendé': 'scindé', 'chairlist': 'tier list', 'facecam': 'facecam', 'pov': 'POV', 'faq': 'FAQ'}


def words():
    out = []
    for w in json.load(open('work/raw_words.json')):
        t = w['w'].strip()
        if (t.startswith("'") or t.startswith('-')) and out:
            out[-1]['w'] += t
            out[-1]['e'] = w['e']
        else:
            out.append(dict(w, w=t))
    for w in out:
        w['s'], w['e'] = ct(w['s']), ct(w['e'])
        k = re.sub(r'[,.!?…]', '', w['w']).lower()
        w['t'] = FIX.get(k, k)
    return [w for w in out if w['t']]


# (key, big word, word that names it)
FORMATS = [('facecam', 'FACECAM', 'facecam'), ('pov', 'POV', 'POV'), ('story', 'STORYTELLING', 'storytelling'),
           ('vert', 'FOND VERT', 'fond'), ('split', 'ÉCRAN SCINDÉ', "l'écran"), ('check', 'TIER LIST', 'checklist'),
           ('table', 'TABLEAU', 'tableau'), ('serie', 'LA SÉRIE', 'série'), ('faq', 'LA FAQ', 'FAQ'), ('react', 'LA RÉACTION', 'réaction')]


def vid(i, a, d, cls='full', extra=''):
    return (f'<video id="{i}" class="{cls}" src="assets/aroll.mp4" muted playsinline data-start="{a:.3f}" data-media-start="{a:.3f}" '
            f'data-duration="{d:.3f}" data-track-index="{20 + int(a * 10) % 40}"{extra}></video>')


def scenes():
    H, B, T, S = [], [], [], []           # front html, behind-her html, tweens, sfx
    ws = words()
    edges = []
    e = 0.0
    for a, b in SEGS:
        edges.append(e)
        e += b - a
    win = [(edges[k + 1], edges[k + 2] if k + 2 < len(edges) else DUR) for k in range(10)]   # format k lives in segment k+1

    # hook title over the first line
    H.append('<div id="hk" class="hk"><div class="hk1"><span>LES 10 FORMATS</span></div><div id="hk2" class="hk2">viraux</div></div>')
    T += ["gsap.set('#hk',{autoAlpha:0});", "tl.set('#hk',{autoAlpha:1},0.04);",
          "tl.fromTo('#hk .hk1',{y:80,scaleY:1.4,autoAlpha:0},{y:0,scaleY:1,autoAlpha:1,duration:.28,ease:'expo.out',immediateRender:true},0.04);",
          "tl.fromTo('#hk2',{autoAlpha:0,scale:.5},{autoAlpha:1,scale:1,duration:.3,ease:'back.out(2)',immediateRender:false},1.26);",
          f"tl.to('#hk',{{autoAlpha:0,y:-30,duration:.2}},{edges[11] - .2:.3f});"]
    S += [('whoosh-short', 0.04, .3), ('pop', 1.26, .3)]

    # each format: her old example clip (same videos as her first "10 formats" reel) pops in on her chest under a
    # numbered pill, while she names it
    for k, (key, big, name) in enumerate(FORMATS):
        a, b = win[k]
        H.append(f'<div id="fc{k}" class="fcard"><div class="fl">{k + 1}. {big}</div><div class="fv">'
                 f'<video id="fv{k}" src="assets/clips/f{k}.mp4" muted playsinline data-start="{a:.3f}" data-media-start="0" '
                 f'data-duration="{b - a:.3f}" data-track-index="{20 + k}"></video></div></div>')
        T += [f"gsap.set('#fc{k}',{{autoAlpha:0}});",
              f"tl.fromTo('#fc{k}',{{autoAlpha:0,scale:.6,y:40}},{{autoAlpha:1,scale:1,y:0,duration:.22,ease:'back.out(2)',immediateRender:false}},{a:.3f});",
              f"tl.set('#fc{k}',{{autoAlpha:0}},{b:.3f});"]
        S.append(('pop', a, .32))

    # CTA: her profile follow card (as in her earlier reels): it pops in on "abonne-toi", "S'abonner" is tapped and
    # turns into "Abonné"
    a_cta = edges[11]
    t_ab = next(w['s'] for w in ws if w['s'] >= a_cta - .05 and w['t'].startswith('abonne'))
    H.append('<div id="fol"><div class="fav"><img src="assets/avatar.png"/></div><div class="fnm">thestrategicboost.fr'
             '<div class="fsub">Stratégie Instagram</div></div><div id="fbtn" class="fbtn">S’abonner</div><div id="fbtn2" class="fbtn on">Abonné</div></div>')
    T += ["gsap.set('#fol, #fbtn2',{autoAlpha:0});",
          f"tl.fromTo('#fol',{{autoAlpha:0,scale:.6,y:30}},{{autoAlpha:1,scale:1,y:0,duration:.35,ease:'back.out(1.8)',immediateRender:false}},{t_ab - .05:.3f});",
          f"tl.to('#fbtn',{{scale:.85,duration:.08,yoyo:true,repeat:1}},{t_ab + .45:.3f});",
          f"tl.set('#fbtn',{{autoAlpha:0}},{t_ab + .61:.3f});",
          f"tl.fromTo('#fbtn2',{{autoAlpha:0,scale:.8}},{{autoAlpha:1,scale:1,duration:.15,ease:'back.out(2)',immediateRender:false}},{t_ab + .61:.3f});"]
    S += [('pop', t_ab - .05, .35), ('click', t_ab + .45, .6)]

    # her one-word captions on the hook and the CTA (the formats are named by their pills)
    small = [w for w in ws if not (win[0][0] - .05 <= w['s'] < win[9][1] - .02)]
    for n, w in enumerate(small):
        nxt = small[n + 1]['s'] if n + 1 < len(small) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        if w['s'] < win[0][0]:
            end = min(end, win[0][0])
        if end <= w['s']:
            continue
        H.append(f'<div id="w{n}" class="cap">{w["t"]}</div>')
        T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
              f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
              f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
    return H, B, T, S


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#cutv{{z-index:3}}
.hk{{position:absolute;left:0;right:0;top:{TOP + 40}px;z-index:20;text-align:center}}
.hk1 span{{display:inline-block;background:{DARK};color:#fff;font:400 112px/1.05 Anton;letter-spacing:.03em;padding:10px 30px 6px}}
.hk2{{display:inline-block;margin-top:-6px;padding:10px 46px 16px;border-radius:999px;background:{PILL};font:italic 700 66px/1 Poppins;color:#fff;
  text-shadow:0 3px 0 rgba(70,35,5,.7)}}
.cnt{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP}px;z-index:22;padding:8px 34px 10px;border-radius:999px;background:{PILL};
  font:italic 700 46px/1 Poppins;color:#fff;text-shadow:0 2px 0 rgba(70,35,5,.7)}}
.cnt b{{font:400 62px/1 Anton;font-style:normal;margin-right:2px}}
.big{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1250px;z-index:26;font:800 104px/1.05 Poppins;color:#fff;white-space:nowrap;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.big.mid{{top:905px;z-index:27}}
.cap{{position:absolute;left:40px;right:40px;top:1270px;z-index:25;text-align:center;font:700 66px/1 Poppins;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.rec{{position:absolute;left:70px;right:70px;top:{TOP + 100}px;bottom:430px;z-index:19}}
.cn{{position:absolute;width:90px;height:90px;border:0 solid #fff}}
.cn.tl{{left:0;top:0;border-left-width:8px;border-top-width:8px}} .cn.tr{{right:0;top:0;border-right-width:8px;border-top-width:8px}}
.cn.bl{{left:0;bottom:0;border-left-width:8px;border-bottom-width:8px}} .cn.br{{right:0;bottom:0;border-right-width:8px;border-bottom-width:8px}}
.rec span{{position:absolute;left:36px;top:30px;font:700 40px/1 Poppins;color:#fff;display:flex;align-items:center;gap:12px;text-shadow:0 2px 8px rgba(0,0,0,.5)}}
.rec span b{{width:26px;height:26px;border-radius:50%;background:#E0453A}}
.pov{{position:absolute;left:80px;right:80px;top:{TOP + 120}px;z-index:20;text-align:center;font:700 54px/1.25 Poppins;color:#fff;
  text-shadow:0 0 3px #000,0 0 3px #000,0 3px 0 #000}}
.pov b{{font-weight:800}}
.vig{{position:absolute;inset:0;z-index:10;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 45%,rgba(30,15,5,.75) 100%)}}
.once{{position:absolute;left:0;right:0;top:{TOP + 120}px;z-index:20;text-align:center;font:italic 400 92px/1 'DM Serif Display';color:{CREAM};
  text-shadow:0 4px 14px rgba(0,0,0,.5)}}
.grn{{position:absolute;inset:0;z-index:2;background:#00B140}}
.spl{{position:absolute;inset:0;z-index:15;background:#000}}
.spl .h{{position:absolute;left:0;right:0;height:960px;overflow:hidden}}
.spl .t{{top:0}} .spl .b{{top:960px}}
.hv{{position:absolute;left:0;top:-420px;width:1080px;height:1920px;object-fit:cover}}
.hv.m{{transform:scaleX(-1)}}
.spl .ln{{position:absolute;left:0;right:0;top:954px;height:12px;background:{CREAM};z-index:2}}
.card{{position:absolute;left:150px;right:150px;top:{TOP + 100}px;z-index:20;background:rgba(244,238,230,.96);border-radius:30px;padding:22px 34px;
  box-shadow:0 18px 40px rgba(0,0,0,.3)}}
.cr{{display:flex;align-items:center;gap:20px;font:700 40px/1.6 Poppins;color:{INK}}}
.box{{width:42px;height:42px;border-radius:10px;border:4px solid {BROWN};flex:none;position:relative}}
.tk{{position:absolute;left:11px;top:3px;width:10px;height:20px;border:solid #fff;border-width:0 5px 5px 0;transform:rotate(45deg)}}
.tab{{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:10px;padding:24px 30px}}
.tab span{{height:62px;display:flex;align-items:center;justify-content:center;font:700 32px/1 Poppins;color:{INK};border-radius:12px}}
.tab .th{{font:400 40px/1 Anton;color:{DARK}}}
.tab .rh{{justify-content:flex-start;padding-left:8px}}
.tab .td{{background:rgba(87,51,7,.08)}}
.tab .td i{{width:26px;height:26px;border-radius:50%;background:{BROWN}}}
.ep{{position:absolute;left:90px;top:{TOP + 120}px;z-index:20}}
.ep span{{display:block;background:{DARK};color:#fff;font:400 96px/1.05 Anton;letter-spacing:.04em;padding:10px 30px 6px}}
.ep small{{display:inline-block;margin-top:10px;padding:8px 26px 12px;border-radius:999px;background:{PILL};font:italic 700 42px/1 Poppins;color:#fff;
  text-shadow:0 2px 0 rgba(70,35,5,.7)}}
.faq{{position:absolute;left:110px;right:110px;top:{TOP + 110}px;z-index:20;background:#fff;border-radius:36px;padding:26px 30px 26px 120px;
  font:700 42px/1.25 Poppins;color:{INK};box-shadow:0 18px 40px rgba(0,0,0,.3)}}
.faq i{{position:absolute;left:26px;top:50%;margin-top:-38px;width:76px;height:76px;border-radius:50%;background:{PILL};color:#fff;font:400 58px/76px Anton;
  font-style:normal;text-align:center}}
.rea{{position:absolute;inset:0;z-index:15;background:#000}}
.rea img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.92)}}
.pip{{position:absolute;right:70px;top:340px;width:380px;height:380px;border-radius:50%;overflow:hidden;border:8px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.4)}}
.pv{{position:absolute;left:-14px;top:-150px;width:400px;height:711px;object-fit:cover}}
.fcard{{position:absolute;left:0;right:0;top:1165px;z-index:24;text-align:center}}
.fl{{display:inline-block;padding:10px 34px 14px;border-radius:999px;background:#fff;font:italic 800 46px/1 Poppins;letter-spacing:-.02em;
  color:{DARK};box-shadow:0 8px 20px rgba(0,0,0,.18);position:relative;z-index:2}}
.fv{{width:252px;height:448px;margin:-6px auto 0;border-radius:18px;overflow:hidden;border:5px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.35)}}
.fv video{{width:100%;height:100%;object-fit:cover;display:block}}
 #fol{{position:absolute;z-index:22;left:110px;top:{TOP + 90}px;width:860px;height:150px;background:#fff;border-radius:28px;display:flex;align-items:center;
  gap:22px;padding:0 26px;box-shadow:0 18px 50px rgba(0,0,0,.3)}}
.fav{{width:100px;height:100px;border-radius:50%;padding:4px;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.fav img{{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid #fff;display:block}}
.fnm{{flex:1;font:700 34px/1.2 Poppins;color:#111}}
.fsub{{font:500 26px/1.2 Poppins;color:#777}}
.fbtn{{position:absolute;right:26px;width:220px;height:74px;border-radius:16px;background:#0095F6;color:#fff;font:700 30px/74px Poppins;text-align:center}}
.fbtn.on{{background:#EFEFEF;color:#111}}
.pill{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP + 40}px;z-index:22;padding:16px 46px 20px;border-radius:999px;
  background:{PILL};font:italic 700 54px/1 Poppins;color:#fff;text-shadow:0 3px 0 rgba(70,35,5,.7)}}
'''

SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click': .36}


def build():
    H, B, T, S = scenes()
    nl = '\n'
    sfx = [f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{min(SFX_LEN[n], DUR - t):.3f}" '
           f'data-track-index="{10 + k % 2}" data-volume="{v:.2f}"></audio>' for k, (n, t, v) in enumerate(sorted(S, key=lambda x: x[1]))]
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
  <audio id="voice" src="assets/voice.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(sfx)}
  <div id="cam"><video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(B)}
  </div>
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
    print(f'wrote index.html {DUR:.3f}s')
