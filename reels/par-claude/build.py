#!/usr/bin/env python3
"""Reel "cette vidéo, c'est Claude qui l'a montée", edited after the "Drop Edit Below" inspiration, every detail on
the word that calls it: kinetic hook with a running timecode, CapCut / Premiere struck out, a "to Claude" prompt bar
that types her requests and sends them, an editing-studio timeline, a before/after slider for "plus de rose", her real
reels floating in 3D behind her, "RIEN" / "TEXTE" behind her head, the raw footage card with "prise ratée" stamps and a
flip timer (raw 1:13 -> reel), a moody grade, BIGGER-captions style blocks, zoom out / in / cuts, her guide as a video
card, comment MONTAGE. Captions in brown label boxes with the spoken word lit.

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll_nat.mp4'], capture_output=True, text=True).stdout.strip())
SEGS = json.load(open('work/segs.json'))
BROWN, DARK, INK = '#8C5C41', '#573307', '#2A1A10'
CREAM = '#F4EEE6'
GOLD = 'linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)'
TOP = 262        # top band for the inserts (Instagram UI above 240)
CUTS = {'wall': (11.45, 1.75), 'rien': (13.9, 0.95), 'text': (20.9, 1.6)}   # cut-out windows (edit clock), see cut.py


def ct(t):
    """raw-clip time -> edit time (takes kept and sped up by cut.py)"""
    out = 0.0
    for a, b, sp in SEGS:
        if t >= b:
            out += (b - a) / sp
        else:
            return out + max(0.0, t - a) / sp
    return out


# ------------------------------------------------------------------ captions: short phrases in a brown box, word lit
FIX = {'bleu': 'bla', '-bleu': '-bla', '-bleu,': '-bla,', 'grandir': 'agrandir', 'Adios': 'tchus', 'adios': 'tchus'}


def words():
    raw = []
    for seg in json.load(open('work/raw_words.json')):
        for w in seg['words']:
            if any(a - .02 <= w['s'] and w['e'] <= b + .1 for a, b, _ in SEGS):
                raw.append({'w': w['w'].strip(), 's': ct(w['s']), 'e': ct(min(w['e'], w['s'] + 1.2))})
    out = []
    for w in raw:
        t = w['w']
        if (t.startswith("'") or t.startswith('-')) and out:
            out[-1]['w'] += FIX.get(t, t)
            out[-1]['e'] = w['e']
            continue
        out.append(dict(w, w=FIX.get(t, t)))
    for k, w in enumerate(out):
        if w['w'] == 'à' and k + 1 < len(out) and out[k + 1]['w'].startswith('agrandir'):
            w['w'] = ''
        if w['w'] == '!':
            w['w'] = ''
    return [w for w in out if w['w']]


def phrases(ws):
    """2-3 word chunks, broken on punctuation and pauses"""
    out, cur = [], []
    for k, w in enumerate(ws):
        cur.append(w)
        nxt = ws[k + 1] if k + 1 < len(ws) else None
        if len(cur) >= 3 or re.search(r'[,.!?…]$', w['w']) or nxt is None or nxt['s'] - w['e'] > .35:
            out.append(cur)
            cur = []
    return out


BIG = (ct(52.84), ct(53.72))


def captions():
    html, tw = [], []
    ps = phrases(words())
    for k, p in enumerate(ps):
        a = p[0]['s']
        nxt = ps[k + 1][0]['s'] if k + 1 < len(ps) else DUR
        b = min(nxt, p[-1]['e'] + .35, DUR)
        big = ' big' if BIG[0] - .05 <= a < BIG[1] else ''
        spans = ' '.join(f'<span id="c{k}_{j}">{re.sub(r"[,.!?…]", "", w["w"])}</span>' for j, w in enumerate(p))
        html.append(f'<div id="c{k}" class="cap{big}"><div class="cb">{spans}</div></div>')
        tw += [f"gsap.set('#c{k}',{{autoAlpha:0}});", f"tl.set('#c{k}',{{autoAlpha:1}},{a:.3f});",
               f"tl.fromTo('#c{k} .cb',{{y:14,scale:.94}},{{y:0,scale:1,duration:.14,ease:'power2.out',immediateRender:false}},{a:.3f});",
               f"tl.set('#c{k}',{{autoAlpha:0}},{b:.3f});"]
        for j, w in enumerate(p):
            tw.append(f"tl.set('#c{k}_{j}',{{color:'#FFFFFF'}},{w['s']:.3f});")
    return html, tw


# ------------------------------------------------------------------ helpers
def show(sel, a, b, frm="{autoAlpha:0,y:-30,scale:.92}", d=.3, ease='back.out(1.7)'):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{frm},{{autoAlpha:1,y:0,x:0,scale:1,rotation:0,duration:{d},ease:'{ease}',immediateRender:false}},{a:.3f});",
            f"tl.to('{sel}',{{autoAlpha:0,y:-16,duration:.18}},{b - .18:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def typing(sel, text, a, b):
    out = [f"tl.set('{sel}',{{textContent:''}},{a - .01:.3f});"]
    n = len(text)
    for i in range(1, n + 1):
        out.append(f"tl.set('{sel}',{{textContent:{json.dumps(text[:i])}}},{a + (b - a) * i / n:.3f});")
    return out


def setseq(sel, prop, values, a, step):
    return [f"tl.set('{sel}',{{{prop}:{json.dumps(v)}}},{a + i * step:.3f});" for i, v in enumerate(values)]


CLAUDE = ('<svg viewBox="0 0 100 100" width="{s}" height="{s}"><g fill="#D97757">' +
          ''.join(f'<rect x="46" y="6" width="8" height="44" rx="4" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 30)) +
          '</g></svg>')
SEND = ('<svg viewBox="0 0 24 24" width="30" height="30"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def scenes():
    H, T, S = [], [], []      # html, tweens, sfx

    # 1. hook: kinetic words at the top + a running timecode (she "didn't edit a second": the clock runs)
    H.append('<div id="hk" class="hk"><div id="hkw" class="hkw"></div><div id="tc" class="tc">00:00:00:00</div></div>')
    a0, a1 = ct(1.74), ct(4.10)
    T += ["gsap.set('#hk',{autoAlpha:1});", f"tl.set('#hk',{{autoAlpha:0}},{a1:.3f});"]
    for txt, t, cls in (('TU VOIS', 1.74, 'w1'), ('CETTE VIDÉO ?', 2.24, 'w1'), ('Claude', 3.10, 'w2'), ("Claude l'a <b>montée.</b>", 3.46, 'w2')):
        T += [f"tl.set('#hkw',{{innerHTML:{json.dumps(txt)},className:'hkw {cls}'}},{ct(t):.3f});",
              f"tl.fromTo('#hkw',{{scale:1.25,autoAlpha:0}},{{scale:1,autoAlpha:1,duration:.16,ease:'expo.out',immediateRender:false}},{ct(t):.3f});"]
        S.append(('whoosh-short', ct(t), .22))
    n = int((a1 - a0) * 30)
    T += [f"tl.set('#tc',{{textContent:'00:00:{i // 30:02d}:{i % 30:02d}'}},{a0 + i / 30:.3f});" for i in range(0, n, 2)]

    # 2. "pas de CapCut, pas de logiciel de montage" -> app icons struck; "juste Claude" -> they fall, Claude stays
    for k, (logo, name, at, hit) in enumerate((('capcut', 'CapCut', 4.48, 4.80), ('premiere', 'Premiere', 5.46, 5.98))):
        H.append(f'<div id="lg{k}" class="lg" style="left:{310 + 260 * k}px"><img src="assets/logos/{logo}.png"/>'
                 f'<div class="ln">{name}</div><svg class="strike" viewBox="0 0 200 200"><path d="M22 34 L178 166"/></svg></div>')
        T += [f"gsap.set('#lg{k}',{{autoAlpha:0}});",
              f"tl.fromTo('#lg{k}',{{autoAlpha:0,scale:.4,y:-40}},{{autoAlpha:1,scale:1,y:0,duration:.25,ease:'back.out(2)',immediateRender:false}},{ct(at):.3f});",
              f"gsap.set('#lg{k} .strike path',{{strokeDasharray:230,strokeDashoffset:230}});",
              f"tl.to('#lg{k} .strike path',{{strokeDashoffset:0,duration:.16,ease:'power2.out'}},{ct(hit):.3f});",
              f"tl.to('#lg{k} img',{{opacity:.5,duration:.15}},{ct(hit):.3f});",
              f"tl.to('#lg{k}',{{y:1300,rotation:{-25 + 50 * k},duration:.55,ease:'power2.in'}},{ct(6.62):.3f});",
              f"tl.set('#lg{k}',{{autoAlpha:0}},{ct(6.62) + .55:.3f});"]
        S += [('pop', ct(at), .3), ('click', ct(hit), .45)]
    H.append(f'<div id="cl" class="cl">{CLAUDE.format(s=96)}<div class="cn"><i>juste</i> Claude.</div></div>')
    T += show('#cl', ct(6.66), ct(7.50) + .15, "{autoAlpha:0,scale:.7}", .25)
    T += [f"tl.fromTo('#cl svg',{{rotation:-120}},{{rotation:0,duration:.6,ease:'power3.out',immediateRender:false}},{ct(6.66):.3f});"]
    S += [('whoosh-short', ct(6.62), .3), ('sparkle', ct(6.66), .28)]

    # 3. the "À CLAUDE" prompt bar: typed, sent, sending
    H.append(f'<div id="pb" class="pb"><div id="pl" class="pl">À CLAUDE</div><div id="pt" class="pt"></div><div id="ps" class="ps">{SEND}</div>'
             '<div id="pw" class="pw"></div></div>')
    T += ["gsap.set('#pb, #pw',{autoAlpha:0});"]
    for txt, a, b, send, end in (('Monte ma vidéo dans ma charte', 15.80, 16.60, 16.86, 17.40),
                                 ('Mets un peu plus de rose', 18.72, 19.90, 20.06, 20.40),
                                 ('Fais un mur de réels derrière moi', 21.40, 23.10, 23.36, 23.62)):
        T += [f"tl.fromTo('#pb',{{autoAlpha:0,y:-30}},{{autoAlpha:1,y:0,duration:.2,ease:'power3.out',immediateRender:false}},{ct(a) - .12:.3f});",
              f"tl.set('#pl',{{textContent:'À CLAUDE'}},{ct(a) - .12:.3f});", f"tl.set('#ps',{{autoAlpha:1}},{ct(a) - .12:.3f});",
              f"tl.set('#pw',{{autoAlpha:0}},{ct(a) - .12:.3f});", f"tl.set('#pt',{{color:'#222'}},{ct(a) - .12:.3f});"]
        T += typing('#pt', txt, ct(a), ct(b))
        T += [f"tl.to('#ps',{{scale:.8,duration:.07,yoyo:true,repeat:1}},{ct(send):.3f});",
              f"tl.set('#pl',{{textContent:'ENVOYÉ'}},{ct(send) + .12:.3f});", f"tl.set('#ps',{{autoAlpha:0}},{ct(send) + .12:.3f});",
              f"tl.set('#pw',{{autoAlpha:1}},{ct(send) + .12:.3f});", f"tl.set('#pt',{{color:'#9A9087'}},{ct(send) + .12:.3f});",
              f"tl.to('#pw',{{rotation:'+=540',duration:.6,ease:'none'}},{ct(send) + .12:.3f});",
              f"tl.to('#pb',{{autoAlpha:0,y:-20,duration:.15}},{ct(end) - .15:.3f});"]
        S += [('click-soft', ct(a), .2), ('click-soft', (ct(a) + ct(b)) / 2, .2), ('click', ct(send), .5)]

    # "et là toute la vidéo est montée": quick blur cut, the editing studio timeline fills itself
    T += [f"tl.fromTo('#cam',{{filter:'blur(0px)'}},{{filter:'blur(14px)',duration:.1,yoyo:true,repeat:1,immediateRender:false}},{ct(17.30):.3f});"]
    clips = ''.join(f'<div class="vc" style="left:{x}px;width:{w}px"><img src="assets/thumbs/t{i % 6}.jpg"/></div>'
                    for i, (x, w) in enumerate([(0, 120), (124, 90), (218, 150), (372, 70), (446, 130), (580, 100), (684, 120)]))
    gold = ''.join(f'<div class="tc2" style="left:{x}px;width:{w}px"></div>' for x, w in [(30, 90), (220, 110), (430, 80), (600, 140)])
    wave = ''.join(f'<i style="height:{6 + (i * 37) % 26}px"></i>' for i in range(96))
    H.append(f'<div id="tl" class="tlp"><div class="th"><span>Montage</span><span id="tlc">00:00:00:00</span><span class="dots">● ● ●</span></div>'
             f'<div class="tr"><b>T1</b><div class="trk">{gold}</div></div><div class="tr"><b>V1</b><div class="trk">{clips}</div></div>'
             f'<div class="tr"><b>A1</b><div class="trk wv">{wave}</div></div><div id="phd" class="phd"></div></div>')
    a, b = ct(17.46), ct(18.62)
    T += show('#tl', a, b, "{autoAlpha:0,y:-40,scale:.95}", .25, 'power3.out')
    T += [f"tl.fromTo('#tl .vc, #tl .tc2',{{scaleX:0}},{{scaleX:1,duration:.12,stagger:.04,ease:'power2.out',immediateRender:false}},{a + .05:.3f});",
          f"tl.fromTo('#phd',{{x:0}},{{x:780,duration:{b - a:.2f},ease:'none',immediateRender:false}},{a:.3f});"]
    T += setseq('#tlc', 'textContent', [f'00:00:{s:02d}:00' for s in range(0, 39, 3)], a, (b - a) / 13)
    S += [('whoosh-short', ct(17.30), .35), ('pop', a, .25)]

    # 4. "un peu plus de rose, hop" -> before / after slider sweeps, the lilac look stays
    H.append('<div id="sl" class="sl"><div class="sll"></div><div class="slh">‹ ›</div></div>'
             '<div id="sla" class="sltag" style="right:40px">APRÈS</div><div id="slb" class="sltag" style="left:40px">AVANT</div>')
    a = ct(20.20)
    T += ["gsap.set('#bgl',{clipPath:'inset(0 100% 0 0)'});",
          f"tl.to('#bgl',{{clipPath:'inset(0 0% 0 0)',duration:.7,ease:'power2.inOut'}},{a:.3f});",
          "gsap.set('#sl, #sla, #slb',{autoAlpha:0});", f"tl.set('#sl, #sla, #slb',{{autoAlpha:1}},{a:.3f});",
          f"tl.fromTo('#sl',{{x:0}},{{x:1080,duration:.7,ease:'power2.inOut',immediateRender:false}},{a:.3f});",
          f"tl.set('#sl, #sla, #slb',{{autoAlpha:0}},{a + .72:.3f});"]
    S += [('whoosh-short', a, .35), ('sparkle', a + .4, .25)]

    # 5. "(snap) hop, il met un mur de réel derrière moi" -> her reels float in, in 3D, behind her
    reels = [f'assets/reels/r{i}.jpg' for i in range(1, 17)]
    cols = ''
    for c in range(4):
        cols += f'<div class="col c{c}">' + ''.join(f'<div class="rc"><img src="{reels[(c * 4 + j) % 16]}"/></div>' for j in range(6)) + '</div>'
    H.append(f'<div id="wall" class="wall"><div class="wsh"></div><div class="wallin">{cols}</div></div>')
    a, b = ct(25.85), ct(27.50)
    T += ["gsap.set('#wall',{autoAlpha:0});", f"tl.set('#wall',{{autoAlpha:1}},{a:.3f});",
          f"tl.fromTo('#wall .wallin',{{rotationY:-65,rotationX:12,scale:.7}},{{rotationY:-22,rotationX:6,scale:1,duration:.6,ease:'power3.out',immediateRender:false}},{a:.3f});",
          f"tl.fromTo('#wall .rc',{{autoAlpha:0,z:-500}},{{autoAlpha:1,z:0,duration:.4,ease:'back.out(1.3)',stagger:{{each:.015,from:'random'}},immediateRender:false}},{a:.3f});"]
    for c in range(4):
        up = c % 2 == 0
        T.append(f"tl.fromTo('#wall .c{c}',{{y:{0 if up else -320}}},{{y:{-320 if up else 0},duration:{b - a:.2f},ease:'none',immediateRender:false}},{a:.3f});")
    T += [f"tl.to('#wall',{{autoAlpha:0,duration:.2}},{b - .2:.3f});", f"tl.set('#wall',{{autoAlpha:0}},{b:.3f});"]
    S += [('whoosh-short', a, .45), ('sparkle', a + .15, .25)]

    # 6. "j'y connais RIEN en montage" -> blur cut + RIEN behind her head
    T += [f"tl.fromTo('#cam',{{filter:'blur(0px)'}},{{filter:'blur(14px)',duration:.1,yoyo:true,repeat:1,immediateRender:false}},{ct(38.46):.3f});"]
    H.append('<div id="rien" class="bht"><div class="bsm">j\'y connais</div>RIEN</div>')
    T += ["gsap.set('#rien',{autoAlpha:0});",
          f"tl.fromTo('#rien',{{autoAlpha:0,scale:1.3}},{{autoAlpha:1,scale:1,duration:.18,ease:'expo.out',immediateRender:false}},{ct(39.50):.3f});",
          f"tl.set('#rien',{{autoAlpha:0}},{CUTS['rien'][0] + CUTS['rien'][1] - .05:.3f});"]
    S += [('whoosh-short', ct(38.46), .3), ('pop', ct(39.50), .35)]

    # 7. the raw footage: drop zone -> file -> raw card with "prise ratée" stamps -> flip timer raw 1:13 -> reel
    H.append('<div id="dz" class="dz"><div class="dzt">⇩ Dépose ta vidéo brute</div><div id="fc" class="fc"><div class="fth"></div>'
             '<div><div class="fn">IMG_4807.MOV</div><div class="fs">1,2 Go · 4K</div></div></div></div>')
    T += show('#dz', ct(40.58), ct(41.95), "{autoAlpha:0,y:-30}", .22, 'power3.out')
    T += ["gsap.set('#fc',{autoAlpha:0});",
          f"tl.fromTo('#fc',{{autoAlpha:0,x:-420,y:-80,rotation:-16,scale:.7}},{{autoAlpha:1,x:0,y:0,rotation:0,scale:1,duration:.35,ease:'power3.out',immediateRender:false}},{ct(40.90):.3f});"]
    H.append('<div id="rw" class="rw"><video id="rwv" src="assets/rawclip.mp4" muted playsinline data-start="0" data-media-start="0" '
             f'data-duration="{DUR:.3f}" data-track-index="7"></video><div class="rwl">1:13 de vidéo brute</div>'
             '<div id="st1" class="stamp" style="top:70px;left:-24px">PRISE RATÉE</div><div id="st2" class="stamp" style="top:210px;left:34px">BLA BLA BLA</div></div>')
    T += show('#rw', ct(41.95), ct(44.56), "{autoAlpha:0,scale:.6,rotation:-6}", .3)
    T += ["gsap.set('#st1, #st2',{autoAlpha:0});"] + [
        f"tl.fromTo('{s}',{{autoAlpha:0,scale:2.2}},{{autoAlpha:1,scale:1,duration:.14,ease:'power3.in',immediateRender:false}},{ct(t):.3f});"
        for s, t in (('#st1', 43.04), ('#st2', 43.74))]
    S += [('whoosh-short', ct(40.90), .3), ('pop', ct(41.95), .3), ('impact', ct(43.04), .25), ('impact', ct(43.74), .25)]
    H.append('<div id="fl" class="flip"><div id="fll" class="fll">VIDÉO BRUTE</div><div id="flv" class="flv">1:13</div></div>')
    a = ct(44.56)
    T += show('#fl', a, ct(45.52) + .2, "{autoAlpha:0,scale:.8}", .2)
    T += setseq('#flv', 'textContent', ['1:13', '1:02', '0:51', '0:43', '0:38', '0:34'], a + .1, .09)
    T += [f"tl.set('#fll',{{textContent:'RÉEL MONTÉ'}},{a + .55:.3f});"] + \
         [f"tl.fromTo('#flv',{{rotationX:-80}},{{rotationX:0,duration:.08,immediateRender:false}},{a + .1 + i * .09:.3f});" for i in range(6)]
    S += [('click-soft', a + .1 + i * .09, .25) for i in range(0, 6, 2)] + [('sparkle', a + .55, .25)]

    # 8. "mettre du TEXTE derrière" -> giant word behind her head; "changer d'ambiance comme ça" -> moody look
    H.append('<div id="texte" class="bht">TEXTE</div>')
    T += ["gsap.set('#texte',{autoAlpha:0});",
          f"tl.fromTo('#texte',{{autoAlpha:0,scale:1.3}},{{autoAlpha:1,scale:1,duration:.2,ease:'expo.out',immediateRender:false}},{ct(49.24):.3f});",
          f"tl.set('#texte',{{autoAlpha:0}},{CUTS['text'][0] + CUTS['text'][1] - .05:.3f});"]
    T += ["gsap.set('#bgm',{opacity:0});", f"tl.to('#bgm',{{opacity:1,duration:.25}},{ct(50.78):.3f});", f"tl.set('#bgm',{{opacity:0}},{ct(51.36):.3f});"]
    H.append('<div id="mood" class="chip">AMBIANCE · moody</div>')
    T += show('#mood', ct(50.78), ct(51.36), "{autoAlpha:0,y:-20}", .2)
    S += [('pop', ct(49.24), .35), ('whoosh-short', ct(50.78), .35)]

    # 9. "agrandir les sous-titres" -> BIGGER-captions style blocks; "plan plus large, plus serré, des cuts" -> word tiles
    H.append('<div id="bg" class="bgc"><div class="bg1">SOUS-TITRES</div><div class="bg2">plus grands.</div></div>')
    T += show('#bg', ct(52.84), ct(53.80), "{autoAlpha:0,x:-60}", .22, 'power3.out')
    S += [('pop', ct(52.84), .35)]
    H.append('<div id="tiles" class="tiles"><span id="ti0">PLAN LARGE</span><span id="ti1">PLUS SERRÉ</span><span id="ti2" class="it">des cuts.</span></div>')
    T += ["gsap.set('#tiles span',{autoAlpha:0});", "gsap.set('#tiles',{autoAlpha:0});", f"tl.set('#tiles',{{autoAlpha:1}},{ct(54.10):.3f});"]
    for i, t in enumerate((54.12, 55.02, 55.52)):
        T.append(f"tl.fromTo('#ti{i}',{{autoAlpha:0,y:30,scale:.8}},{{autoAlpha:1,y:0,scale:1,duration:.18,ease:'back.out(2)',immediateRender:false}},{ct(t):.3f});")
        S.append(('pop', ct(t), .3))
    T += [f"tl.to('#tiles',{{autoAlpha:0,duration:.15}},{ct(56.20):.3f});"]
    T += [f"tl.set('#cam',{{scale:1.18}},{ct(51.44):.3f});",
          f"tl.to('#cam',{{scale:1,duration:.4,ease:'power2.out'}},{ct(54.30):.3f});",
          f"tl.to('#cam',{{scale:1.4,duration:.25,ease:'power2.out'}},{ct(55.02):.3f});",
          f"tl.set('#cam',{{scale:1.1}},{ct(55.62):.3f});", f"tl.set('#cam',{{scale:1.3}},{ct(55.82):.3f});",
          f"tl.set('#cam',{{scale:1}},{ct(56.10):.3f});"]
    H.append('<div id="fls" class="fls"></div>')
    T += ["gsap.set('#fls',{autoAlpha:0});"] + [f"tl.fromTo('#fls',{{autoAlpha:.7}},{{autoAlpha:0,duration:.1,immediateRender:false}},{ct(t):.3f});" for t in (55.62, 55.82)]
    S += [('click', ct(55.62), .4), ('click', ct(55.82), .4)]
    # "en deux secondes" -> flip timer 0:02
    H.append('<div id="f2" class="flip sm"><div class="fll">MODIFICATION</div><div id="f2v" class="flv">0:00</div></div>')
    a = ct(56.70)
    T += show('#f2', a, ct(57.20) + .3, "{autoAlpha:0,scale:.8}", .18)
    T += setseq('#f2v', 'textContent', ['0:00', '0:01', '0:02'], a + .08, .1)
    S += [('click-soft', a + .1, .3), ('click-soft', a + .2, .3)]

    # 10. CTA: her guide as a video card, then "Commente MONTAGE" with the comment typed, the DM
    H.append('<div id="vcd" class="vcd"><div class="vimg"><img src="assets/guide.png"/><div class="play">▶</div></div>'
             '<div class="vt">Monter ses réels avec Claude</div><div id="vch" class="vch">01 · La vidéo brute</div></div>')
    a, b = ct(65.38), ct(69.66)
    T += show('#vcd', a, b, "{autoAlpha:0,y:-50,scale:.9}", .3, 'power3.out')
    T += setseq('#vch', 'textContent', ['01 · La vidéo brute', '02 · Le prompt', '03 · Les effets', '04 · Le réel fini'], ct(66.58), (b - ct(66.58)) / 4)
    S += [('whoosh-short', a, .3)]
    H.append('<div id="cta" class="cta">Commente « MONTAGE » et<br/>je t\'envoie le guide</div>'
             f'<div id="cin" class="cin"><div class="cav"></div><div id="cit" class="cit">Ajouter un commentaire…</div><div id="cis" class="cis">{SEND}</div></div>')
    T += show('#cta', ct(69.70), DUR + .2, "{autoAlpha:0,y:-20}", .22)
    T += show('#cin', ct(69.70), DUR + .2, "{autoAlpha:0,y:-20}", .22)
    T += [f"tl.set('#cit',{{color:'#111'}},{ct(70.10):.3f});"] + typing('#cit', 'MONTAGE', ct(70.10), ct(70.45))
    T += [f"tl.to('#cis',{{scale:.8,duration:.07,yoyo:true,repeat:1}},{ct(70.62):.3f});"]
    S += [('pop', ct(69.70), .3), ('click', ct(70.62), .45)]
    H.append('<div id="dm" class="dm"><img src="assets/avatar.png"/><div><div class="dt">thestrategicboost.fr</div>'
             '<div class="ds">t\'a envoyé le guide 🎁</div></div></div>')
    T += show('#dm', ct(71.10), DUR + .2, "{autoAlpha:0,y:-60}", .3, 'power3.out')
    S += [('pop', ct(71.10), .4)]
    return H, T, S


SFX_LEN = {'pop': .72, 'whoosh-short': .57, 'click': .36, 'click-soft': .36, 'sparkle': 1.8, 'glitch2': .8, 'impact': .6}
SFX_FILE = {'impact': 'glitch2'}


def audio(sfx):
    out, lanes = [], []
    for k, (n, t, v) in enumerate(sorted(sfx, key=lambda x: x[1])):
        d = min(SFX_LEN[n], DUR - t)
        lane = next((i for i, e in enumerate(lanes) if e <= t), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{SFX_FILE.get(n, n)}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{v * .8:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.cut{{z-index:5}}
.hk{{position:absolute;left:60px;right:60px;top:{TOP + 10}px;z-index:20;text-align:center}}
.hkw{{display:inline-block;color:#fff;text-shadow:0 4px 0 rgba(0,0,0,.25),0 0 30px rgba(0,0,0,.4)}}
.hkw.w1{{font:400 150px/1 Anton;letter-spacing:.01em}}
.hkw.w2{{font:italic 600 92px/1.05 Poppins;letter-spacing:-.02em}}
.hkw b{{font-weight:600;background:{GOLD};-webkit-background-clip:text;background-clip:text;color:transparent}}
.tc{{margin-top:14px;font:500 26px/1 'JetBrains Mono',monospace;letter-spacing:.12em;color:rgba(255,255,255,.85)}}
.lg{{position:absolute;top:{TOP + 20}px;width:200px;text-align:center;z-index:20}}
.lg img{{width:150px;height:150px;border-radius:34px;box-shadow:0 14px 30px rgba(0,0,0,.35);display:block;margin:0 auto}}
.ln{{font:600 26px/1.2 Poppins;color:#fff;margin-top:10px;text-shadow:0 3px 12px rgba(0,0,0,.6)}}
.strike{{position:absolute;left:10px;top:-20px;width:180px;height:190px;overflow:visible}}
.strike path{{stroke:#E5262B;stroke-width:15;stroke-linecap:round;fill:none}}
.cl{{position:absolute;left:0;right:0;top:{TOP + 10}px;z-index:21;text-align:center}}
.cl svg{{display:block;margin:0 auto 6px;filter:drop-shadow(0 8px 20px rgba(0,0,0,.35))}}
.cn{{font:italic 600 92px/1 Poppins;color:#fff;letter-spacing:-.02em;text-shadow:0 0 26px rgba(0,0,0,.45)}}
.cn i{{font-size:54px;font-weight:500;opacity:.9}}
.pb{{position:absolute;left:80px;right:80px;top:{TOP}px;z-index:20;height:128px;background:{CREAM};border-radius:26px;
  box-shadow:0 18px 44px rgba(0,0,0,.3);padding:20px 110px 0 30px}}
.pl{{font:600 18px/1 'JetBrains Mono',monospace;letter-spacing:.2em;color:#8B7F74}}
.pt{{font:500 36px/1.25 Poppins;color:#222;margin-top:14px;white-space:nowrap;overflow:hidden}}
.ps{{position:absolute;right:24px;top:30px;width:66px;height:66px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center}}
.pw{{position:absolute;right:30px;top:36px;width:54px;height:54px;border-radius:50%;border:5px solid #D9CFC4;border-top-color:{DARK}}}
.tlp{{position:absolute;left:70px;right:70px;top:{TOP}px;z-index:20;height:330px;border-radius:24px;background:{INK};border:1.5px solid rgba(255,255,255,.12);
  box-shadow:0 22px 50px rgba(0,0,0,.45);padding:16px 20px;overflow:hidden}}
.th{{display:flex;justify-content:space-between;font:500 22px/1 'JetBrains Mono',monospace;color:#E9D9C4;margin-bottom:16px}}
.th span:first-child{{font-family:Poppins;font-weight:600}}
.dots{{color:#7A6658;letter-spacing:.2em}}
.tr{{display:flex;align-items:center;gap:12px;height:72px;margin-bottom:10px}}
.tr b{{font:600 18px/1 'JetBrains Mono',monospace;color:#9C8775;width:30px}}
.trk{{position:relative;flex:1;height:64px;background:rgba(255,255,255,.04);border-radius:8px;overflow:hidden}}
.vc{{position:absolute;top:2px;bottom:2px;border-radius:6px;overflow:hidden;transform-origin:0 50%;border:2px solid #C9A27E}}
.vc img{{width:100%;height:100%;object-fit:cover;display:block}}
.tc2{{position:absolute;top:14px;height:36px;border-radius:6px;background:{GOLD};transform-origin:0 50%}}
.wv{{display:flex;align-items:center;gap:3px;padding:0 6px}}
.wv i{{display:block;width:5px;border-radius:2px;background:#C9A27E}}
.phd{{position:absolute;left:62px;top:50px;bottom:10px;width:4px;background:#fff;box-shadow:0 0 10px rgba(255,255,255,.6)}}
.sl{{position:absolute;left:0;top:0;bottom:0;width:0;z-index:15}}
.sll{{position:absolute;left:-3px;top:0;bottom:0;width:6px;background:#fff;box-shadow:0 0 18px rgba(0,0,0,.4)}}
.slh{{position:absolute;left:-38px;top:880px;width:76px;height:76px;border-radius:50%;background:{DARK};border:4px solid #fff;color:#fff;
  font:700 30px/68px Poppins;text-align:center}}
.sltag{{position:absolute;top:{TOP + 10}px;z-index:16;font:600 26px/1 'JetBrains Mono',monospace;letter-spacing:.2em;color:#fff;background:rgba(0,0,0,.35);padding:8px 14px}}
.wall{{position:absolute;inset:0;z-index:2;perspective:1200px;overflow:hidden}}
.wsh{{position:absolute;inset:0;background:rgba(20,12,8,.45)}}
.wallin{{position:absolute;left:-40px;right:-40px;top:-300px;bottom:-300px;display:flex;gap:24px;justify-content:center;transform-style:preserve-3d}}
.col{{display:flex;flex-direction:column;gap:24px;width:250px}}
.rc{{width:250px;height:444px;flex:none;border-radius:20px;overflow:hidden;border:3px solid #E9C98F;box-shadow:0 20px 44px rgba(0,0,0,.5),0 0 26px rgba(214,174,102,.35)}}
.rc img{{width:100%;height:100%;object-fit:cover;display:block}}
.bht{{position:absolute;left:0;right:0;top:{TOP + 120}px;z-index:2;text-align:center;font:400 330px/.95 Anton;letter-spacing:.01em;color:#fff;
  text-shadow:0 10px 40px rgba(0,0,0,.3)}}
.bsm{{font:italic 600 56px/1 Poppins;letter-spacing:-.01em;margin-bottom:8px}}
.dz{{position:absolute;left:110px;right:110px;top:{TOP}px;height:200px;z-index:20;border-radius:26px;border:3px dashed rgba(233,201,143,.8);background:rgba(42,26,16,.82);
  box-shadow:0 18px 44px rgba(0,0,0,.35)}}
.dzt{{position:absolute;left:0;right:0;top:16px;text-align:center;font:600 26px/1 Poppins;color:#E9D9C4}}
.fc{{position:absolute;left:50px;right:50px;top:58px;height:112px;border-radius:18px;background:{CREAM};display:flex;align-items:center;gap:20px;padding:0 20px}}
.fth{{width:52px;height:84px;border-radius:8px;background:linear-gradient(160deg,#9AA3B5,#5E6678)}}
.fn{{font:700 32px/1.1 Poppins;color:#111}}
.fs{{font:500 22px/1.3 Poppins;color:#7a7068}}
.rw{{position:absolute;left:390px;top:{TOP - 10}px;width:300px;z-index:20}}
.rw video{{width:300px;height:400px;object-fit:cover;border-radius:18px;border:4px solid #fff;display:block;box-shadow:0 18px 40px rgba(0,0,0,.4)}}
.rwl{{margin:10px auto 0;width:max-content;padding:8px 16px;background:#fff;border-radius:10px;font:700 24px/1 Poppins;color:#111}}
.stamp{{position:absolute;padding:8px 16px 6px;border:5px solid #E5262B;color:#E5262B;background:rgba(255,255,255,.9);font:400 44px/1 Anton;letter-spacing:.04em;
  transform:rotate(-10deg)}}
.flip{{position:absolute;left:340px;width:400px;top:{TOP}px;z-index:20;padding:16px 0 18px;border-radius:22px;background:{INK};text-align:center;
  box-shadow:0 18px 40px rgba(0,0,0,.45);perspective:400px}}
.fll{{font:600 20px/1 'JetBrains Mono',monospace;letter-spacing:.24em;color:#C9A27E}}
.flv{{font:400 130px/1.05 Anton;color:#F4EEE6;letter-spacing:.04em}}
.flip.sm .flv{{font-size:110px}}
.chip{{position:absolute;left:300px;width:480px;top:{TOP + 20}px;z-index:20;padding:16px 0;border-radius:40px;background:rgba(42,26,16,.85);text-align:center;
  font:600 30px/1 Poppins;color:#F4EEE6;letter-spacing:.02em}}
.bgc{{position:absolute;left:110px;top:{TOP + 10}px;z-index:20}}
.bg1{{display:inline-block;background:{CREAM};color:{INK};font:400 116px/1 Anton;padding:10px 26px 4px}}
.bg2{{display:block;width:max-content;margin:-6px 0 0 120px;background:{DARK};color:#F3DFB2;font:italic 600 66px/1.2 Poppins;padding:6px 24px 10px}}
.tiles{{position:absolute;left:90px;right:90px;top:{TOP + 20}px;z-index:20;display:flex;flex-wrap:wrap;gap:12px;justify-content:center}}
.tiles span{{background:{DARK};color:#fff;font:400 60px/1 Anton;letter-spacing:.03em;padding:12px 20px 8px}}
.tiles span.it{{background:{CREAM};color:{INK};font:italic 600 58px/1.1 Poppins;padding:8px 22px 12px}}
.fls{{position:absolute;inset:0;z-index:30;background:#fff}}
.vcd{{position:absolute;left:150px;right:150px;top:{TOP - 10}px;z-index:20;background:{INK};border-radius:22px;overflow:hidden;box-shadow:0 22px 50px rgba(0,0,0,.45)}}
.vimg{{position:relative;height:300px;overflow:hidden}}
.vimg img{{width:100%;height:100%;object-fit:cover;object-position:top}}
.play{{position:absolute;left:50%;top:50%;width:90px;height:90px;margin:-45px 0 0 -45px;border-radius:50%;background:rgba(42,26,16,.8);color:#fff;
  font:400 40px/90px Poppins;text-align:center}}
.vt{{font:600 34px/1.2 Poppins;color:#F4EEE6;padding:16px 24px 4px}}
.vch{{font:500 24px/1.2 'JetBrains Mono',monospace;color:#C9A27E;padding:0 24px 18px}}
.cta{{position:absolute;left:80px;right:80px;top:{TOP}px;z-index:21;text-align:center;font:700 44px/1.2 Poppins;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.6)}}
.cin{{position:absolute;left:110px;right:110px;top:{TOP + 135}px;z-index:21;height:96px;border-radius:48px;background:#fff;display:flex;align-items:center;gap:18px;
  padding:0 16px 0 18px;box-shadow:0 14px 34px rgba(0,0,0,.3)}}
.cav{{width:60px;height:60px;border-radius:50%;background:linear-gradient(45deg,#FEDA75,#FA7E1E,#D62976,#962FBF);flex:none}}
.cit{{flex:1;font:600 34px/1 Poppins;color:#9A9087}}
.cis{{width:64px;height:64px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center}}
.dm{{position:absolute;left:110px;right:110px;top:{TOP + 250}px;z-index:22;height:120px;border-radius:28px;background:rgba(255,255,255,.97);display:flex;
  align-items:center;gap:20px;padding:0 24px;box-shadow:0 18px 44px rgba(0,0,0,.3)}}
.dm img{{width:78px;height:78px;border-radius:50%;object-fit:cover}}
.dt{{font:700 28px/1.2 Poppins;color:#111}}
.ds{{font:500 26px/1.2 Poppins;color:#555}}
.cap{{position:absolute;left:80px;right:80px;top:1260px;z-index:25;text-align:center}}
.cb{{display:inline-block;background:rgba(87,51,7,.92);padding:10px 20px 12px;font:600 46px/1.15 Poppins;color:rgba(243,223,178,.55);
  box-shadow:0 8px 20px rgba(0,0,0,.25)}}
.cap.big .cb{{font-size:84px;padding:14px 28px}}
'''


BEHIND = ('wall', 'rien', 'texte')


def build():
    sh, st, sfx = scenes()
    ch, ct_ = captions()
    nl = '\n'

    def vid(i, src, ti):
        return (f'<video id="{i}" class="full" src="{src}" muted playsinline data-start="0" data-media-start="0" '
                f'data-duration="{DUR:.3f}" data-track-index="{ti}"></video>')

    def cutv(name, ti):
        a, d = CUTS[name]
        return (f'<video id="cut_{name}" class="full cut" src="assets/{name}_cut.webm" muted playsinline data-start="{a}" '
                f'data-media-start="0" data-duration="{d}" data-track-index="{ti}"></video>')
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
    {vid('bgm', 'assets/aroll_moody.mp4', 3)}
{nl.join(h for h in sh if any(f'id="{i}"' in h for i in BEHIND))}
    {cutv('wall', 4)}
    {cutv('rien', 5)}
    {cutv('text', 6)}
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
