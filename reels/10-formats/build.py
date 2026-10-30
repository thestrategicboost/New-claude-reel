#!/usr/bin/env python3
"""Reel "les 10 formats viraux": she counts the ten formats on her fingers; each one lands as a huge white word with
a 1/10 -> 10/10 counter in her gold pill on top, and is shown in action on her for its second: facecam (REC frame +
punch-in), POV (POV text), storytelling (sepia + "il était une fois"), fond vert (her cut-out on green), écran scindé
(split screen), checklist (ticking card), tableau (planning grid), série (episode badge), FAQ (question bubble),
réaction (her reel full screen, her in a circle). Hook title, her usual one-word captions, lilac look.

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


FIX = {'cendé': 'scindé', 'chairlist': 'checklist', 'facecam': 'facecam', 'pov': 'POV', 'faq': 'FAQ'}


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
           ('vert', 'FOND VERT', 'fond'), ('split', 'ÉCRAN SCINDÉ', "l'écran"), ('check', 'CHECKLIST', 'checklist'),
           ('table', 'TABLEAU', 'tableau'), ('serie', 'SÉRIE', 'série'), ('faq', 'FAQ', 'FAQ'), ('react', 'RÉACTION', 'réaction')]


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
          f"tl.to('#hk',{{autoAlpha:0,y:-30,duration:.2}},{edges[1] - .2:.3f});"]
    S += [('whoosh-short', 0.04, .3), ('pop', 1.26, .3)]

    # the counter pill
    H.append('<div id="cnt" class="cnt"><b id="cntn">1</b>/10</div>')
    T += ["gsap.set('#cnt',{autoAlpha:0});", f"tl.fromTo('#cnt',{{autoAlpha:0,y:-30}},{{autoAlpha:1,y:0,duration:.25,ease:'back.out(2)',immediateRender:false}},{edges[1]:.3f});",
          f"tl.to('#cnt',{{autoAlpha:0,duration:.2}},{win[9][1] - .1:.3f});"]

    big_words = set()
    for k, (key, big, name) in enumerate(FORMATS):
        a, b = win[k]
        hit = next(w for w in ws if w['s'] >= a - .05 and w['t'].lower() == name.lower())
        tb = hit['s']
        big_words |= {id(w) for w in ws if a - .05 <= w['s'] < b - .02 and w['s'] >= tb - .02}
        H.append(f'<div id="bg{k}" class="big{" mid" if key == "split" else ""}">{big}</div>')
        T += [f"gsap.set('#bg{k}',{{autoAlpha:0}});",
              f"tl.fromTo('#bg{k}',{{autoAlpha:0,scale:1.35,y:10}},{{autoAlpha:1,scale:1,y:0,duration:.16,ease:'back.out(2.2)',immediateRender:false}},{tb:.3f});",
              f"tl.set('#bg{k}',{{autoAlpha:0}},{b - .02:.3f});",
              f"tl.set('#cntn',{{textContent:'{k + 1}'}},{a:.3f});",
              f"tl.fromTo('#cnt',{{scale:1.25}},{{scale:1,duration:.2,ease:'back.out(2)',immediateRender:false}},{a:.3f});"]
        S.append(('pop', a, .35))
        d = b - a
        if key == 'facecam':      # REC frame + punch-in on her face
            H.append('<div id="rec" class="rec"><i class="cn tl"></i><i class="cn tr"></i><i class="cn bl"></i><i class="cn br"></i><span><b></b>REC</span></div>')
            T += ["gsap.set('#rec',{autoAlpha:0});", f"tl.set('#rec',{{autoAlpha:1}},{a:.3f});", f"tl.set('#rec',{{autoAlpha:0}},{b:.3f});",
                  f"tl.fromTo('#cam',{{scale:1}},{{scale:1.22,duration:.18,ease:'power2.out',immediateRender:false}},{a:.3f});",
                  f"tl.set('#cam',{{scale:1}},{b:.3f});"]
        elif key == 'pov':
            H.append('<div id="pov" class="pov"><b>POV :</b> tu as enfin trouvé<br/>le format qui marche</div>')
            T += [f"gsap.set('#pov',{{autoAlpha:0}});", f"tl.fromTo('#pov',{{autoAlpha:0,y:-20}},{{autoAlpha:1,y:0,duration:.18,immediateRender:false}},{a:.3f});",
                  f"tl.set('#pov',{{autoAlpha:0}},{b:.3f});"]
        elif key == 'story':     # sepia + vignette + serif opener
            H.append('<div id="vig" class="vig"></div><div id="once" class="once">il était une fois…</div>')
            T += ["gsap.set('#vig, #once',{autoAlpha:0});", f"tl.set('#vig',{{autoAlpha:1}},{a:.3f});", f"tl.set('#vig',{{autoAlpha:0}},{b:.3f});",
                  f"tl.fromTo('#once',{{autoAlpha:0,filter:'blur(8px)'}},{{autoAlpha:1,filter:'blur(0px)',duration:.3,immediateRender:false}},{a:.3f});",
                  f"tl.set('#once',{{autoAlpha:0}},{b:.3f});",
                  f"tl.set('#bgv',{{filter:'sepia(.75) contrast(1.08) brightness(.95)'}},{a:.3f});", f"tl.set('#bgv',{{filter:'none'}},{b:.3f});"]
        elif key == 'vert':      # her cut-out on a green screen
            B.append('<div id="grn" class="grn"></div>')
            B.append(f'<video id="cutv" class="full" src="assets/cut.webm" muted playsinline data-start="{a:.3f}" data-media-start="{a:.3f}" '
                     f'data-duration="{d:.3f}" data-track-index="5"></video>')
            T += ["gsap.set('#grn',{autoAlpha:0});", f"tl.set('#grn',{{autoAlpha:1}},{a:.3f});", f"tl.set('#grn',{{autoAlpha:0}},{b:.3f});"]
        elif key == 'split':     # the frame splits in two, the bottom half mirrored
            H.append(f'<div id="spl" class="spl"><div class="h t">{vid("spv1", a, d, "hv")}</div><div class="h b">{vid("spv2", a, d, "hv m")}</div><i class="ln"></i></div>')
            T += ["gsap.set('#spl',{autoAlpha:0});", f"tl.set('#spl',{{autoAlpha:1}},{a:.3f});", f"tl.set('#spl',{{autoAlpha:0}},{b:.3f});",
                  f"tl.fromTo('#spl .t',{{y:-40}},{{y:0,duration:.2,ease:'power3.out',immediateRender:false}},{a:.3f});",
                  f"tl.fromTo('#spl .b',{{y:40}},{{y:0,duration:.2,ease:'power3.out',immediateRender:false}},{a:.3f});"]
        elif key == 'check':
            rows = ['une accroche', 'de la valeur', 'un appel à l\'action']
            H.append('<div id="chk" class="card chk">' + ''.join(f'<div class="cr"><i id="cb{q}" class="box"><b id="tk{q}" class="tk"></b></i>{r}</div>' for q, r in enumerate(rows)) + '</div>')
            T += [f"gsap.set('#chk',{{autoAlpha:0}});", f"tl.fromTo('#chk',{{autoAlpha:0,y:-20}},{{autoAlpha:1,y:0,duration:.18,immediateRender:false}},{a:.3f});",
                  f"tl.set('#chk',{{autoAlpha:0}},{b:.3f});"]
            T += [f"gsap.set('.tk',{{opacity:0}});"]
            for q in range(3):
                T += [f"tl.set('#cb{q}',{{backgroundColor:'{DARK}',borderColor:'{DARK}'}},{a + .15 + q * .18:.3f});",
                      f"tl.set('#tk{q}',{{opacity:1}},{a + .15 + q * .18:.3f});"]
        elif key == 'table':
            cols = ['LUN', 'MER', 'VEN']
            rows = ['réel', 'carrousel', 'story']
            cells = ''.join(f'<span class="th">{c}</span>' for c in [''] + cols)
            for r in rows:
                cells += f'<span class="rh">{r}</span>' + ''.join(f'<span class="td"><i></i></span>' for _ in cols)
            H.append(f'<div id="tab" class="card tab">{cells}</div>')
            T += [f"gsap.set('#tab',{{autoAlpha:0}});", f"tl.fromTo('#tab',{{autoAlpha:0,y:-20}},{{autoAlpha:1,y:0,duration:.18,immediateRender:false}},{a:.3f});",
                  f"tl.fromTo('#tab .td i',{{scale:0}},{{scale:1,duration:.12,stagger:.04,ease:'back.out(3)',immediateRender:false}},{a + .12:.3f});",
                  f"tl.set('#tab',{{autoAlpha:0}},{b:.3f});"]
        elif key == 'serie':
            H.append('<div id="ep" class="ep"><span>ÉPISODE 1</span><small>partie 1/3</small></div>')
            T += [f"gsap.set('#ep',{{autoAlpha:0}});", f"tl.fromTo('#ep',{{autoAlpha:0,x:-80}},{{autoAlpha:1,x:0,duration:.2,ease:'power3.out',immediateRender:false}},{a:.3f});",
                  f"tl.set('#ep',{{autoAlpha:0}},{b:.3f});"]
        elif key == 'faq':
            H.append('<div id="faq" class="faq"><i>?</i>« comment tu trouves<br/>tes idées de réels ? »</div>')
            T += [f"gsap.set('#faq',{{autoAlpha:0}});", f"tl.fromTo('#faq',{{autoAlpha:0,scale:.5}},{{autoAlpha:1,scale:1,duration:.22,ease:'back.out(2)',immediateRender:false}},{a:.3f});",
                  f"tl.set('#faq',{{autoAlpha:0}},{b:.3f});"]
        elif key == 'react':     # her own reel full screen, her reacting in a circle
            H.append(f'<div id="rea" class="rea"><img src="assets/reels/r3.jpg"/><div class="pip">{vid("pipv", a, d, "pv")}</div></div>')
            T += ["gsap.set('#rea',{autoAlpha:0});", f"tl.set('#rea',{{autoAlpha:1}},{a:.3f});", f"tl.set('#rea',{{autoAlpha:0}},{b:.3f});",
                  f"tl.fromTo('#rea .pip',{{scale:.3}},{{scale:1,duration:.22,ease:'back.out(1.8)',immediateRender:false}},{a:.3f});"]

    # CTA
    H.append('<div id="cta" class="pill">abonne-toi pour plus de conseils</div>')
    a_cta = edges[11]
    T += ["gsap.set('#cta',{autoAlpha:0});",
          f"tl.fromTo('#cta',{{autoAlpha:0,scale:.6,y:20}},{{autoAlpha:1,scale:1,y:0,duration:.3,ease:'back.out(2)',immediateRender:false}},{a_cta + .12:.3f});"]
    S.append(('pop', a_cta + .12, .35))

    # one-word captions for everything that is not a format name
    small = [w for w in ws if id(w) not in big_words]
    starts = sorted([win[k][0] for k in range(10)] + [a_cta])
    for n, w in enumerate(small):
        nxt = small[n + 1]['s'] if n + 1 < len(small) else DUR
        end = min(nxt if nxt - w['e'] < .5 else w['e'] + .3, nxt, DUR)
        for k, (key, big, name) in enumerate(FORMATS):   # the article stops when its format name lands
            a, b = win[k]
            if a - .05 <= w['s'] < b:
                tb = next(x['s'] for x in ws if x['s'] >= a - .05 and x['t'].lower() == name.lower())
                end = min(end, tb) if w['s'] < tb else end
        if end <= w['s']:
            continue
        H.append(f'<div id="w{n}" class="cap">{w["t"]}</div>')
        T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{w['s']:.3f});",
              f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - w['s']):.3f},ease:'back.out(2.5)',immediateRender:false}},{w['s']:.3f});",
              f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
    _ = starts
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
.pill{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP + 40}px;z-index:22;padding:16px 46px 20px;border-radius:999px;
  background:{PILL};font:italic 700 54px/1 Poppins;color:#fff;text-shadow:0 3px 0 rgba(70,35,5,.7)}}
'''

SFX_LEN = {'pop': .72, 'whoosh-short': .57}


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
