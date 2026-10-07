#!/usr/bin/env python3
"""Reel "tofu mofu bofu" v2: Maé's own edit rebuilt (style "pédagogique marron").

Timeline = her cut (edl.json: 3 segments, see her "TOFU bien monté"). Every position below was measured on her
render (1080x1920):
  hook          TOFU (behind the head) / MOFU / BOFU in big white Anton, popping on each word
  wide shot     TOFU MOFU BOFU above the three Maé + view badges (1M / 100K / 10K)
  captions      one word at a time, white Poppins bold, soft dark glow
  brown screens #8C5C41 full frame: the funnel that builds up (TOFU, then MOFU, then BOFU) and the
                "Vidéos de CLASSEMENT" cards with her own example reels (assets/cards, cropped from her edit)
  zooms         1.3x punch-ins at 9.27-10.03 and 53.80-54.87
  cta           Instagram card: Follow -> Following with a cursor click
The grade (brighter, cooler) is baked into assets/aroll_graded.mp4.

PY build.py            writes index.html
PY build.py --safe     same + red Instagram safe-zone guide (snapshots only)
"""
import json
import os
import re
import shutil
import subprocess
import sys

SAFE = '--safe' in sys.argv or bool(os.environ.get('SAFE'))
DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=duration', '-of', 'csv=p=0', 'assets/aroll.mp4'],
                           capture_output=True, encoding='utf-8', errors='replace').stdout.strip().split(',')[0])
BROWN = '#8C5C41'
T1, T2, T3 = '#EFE6D7', '#DEBCA0', '#BF9067'          # funnel tiers, light to dark
HOOK_END, WIDE_END = 0.898, 4.133
ZOOMS = [(9.267, 10.033), (53.800, 54.867)]
IG_IN = 55.97

with open('words.json', encoding='utf-8') as _f:
    RAW = json.load(_f)


def words():
    """medium words -> caption tokens: merge c + 'est, abonne + -toi; lowercase; no punctuation; spoken fixes"""
    out = []
    for w in RAW:
        t = w['text']
        if out and (t[:1] in "'’-" and len(t) > 1):
            out[-1]['text'] += t
            out[-1]['end'] = w['end']
            continue
        out.append(dict(w))
    for w in out:
        t = re.sub(r'[.,!?;:«»"]', '', w['text']).strip().lower().replace("'", '’')
        w['text'] = {'up': 'of', 'list': 'liste', 'étroits': '3', 'd’étroits': '3'}.get(t, t)
    return [w for w in out if w['text']]


# the wide shot (before 4.2s): medium drifts there and invents "et", so use the ingest (small) timings; the
# cut starts at source 0, so source time = cut time for these
WIDE_WORDS = [('il', 1.10), ('y', 1.16), ('a', 1.18), ('trois', 1.22), ('types', 1.42), ('de', 1.60), ('contenus', 1.76),
              ('que', 2.04), ('tu', 2.12), ('dois', 2.16), ('publier', 2.28), ('le', 2.70), ('tofu', 2.80), ('mofu', 3.40),
              ('bofu', 3.86)]
WORDS = [{'text': t, 'start': s, 'end': s + .3} for t, s in WIDE_WORDS] + [w for w in words() if w['start'] >= 4.2]


def at(word, after=0.0):
    """start time of the first caption token equal to `word` after `after`"""
    return next(w['start'] for w in WORDS if w['text'] == word and w['start'] >= after)


# ------------------------------------------------------------------ brown screens
FUNNELS = [(5.933, 8.033, 1), (18.467, 20.167, 2), (38.300, 40.900, 3)]
# card screens: (start, end, label, title, [(t, subtitle)], [(t0, t1, video, x, y, w, h)])
CARDS = [
    (12.833, 15.233, 'Vidéos de', 'CLASSEMENT', [], [(12.833, 16.167, 'c1', 271, 621, 538, 954)]),
    (15.233, 16.167, 'Vidéos de', 'NOTATION', [], []),
    (16.167, 17.133, 'Vidéos de', 'TYPE LISTE', [], [(16.167, 17.133, 'c2', 274, 640, 532, 948)]),
    (17.133, 18.033, 'Vidéos', 'STORYTELLING', [], [(17.133, 18.033, 'c3', 257, 610, 566, 1004)]),
    (26.367, 29.267, 'Contenu', 'ÉDUCATIF', [(26.367, 'approfondi')], [(26.367, 29.267, 'c4', 289, 662, 502, 890)]),
    (29.267, 30.667, 'Vidéos', 'TUTORIEL', [(29.267, 'pas à pas')], [(29.267, 30.667, 'c5', 288, 675, 506, 898)]),
    (30.667, 34.067, 'Vidéos', 'STORYTELLING', [(30.667, 'sur tes réussites'), (at('échecs', 30) - .05, 'sur tes échecs'),
                                                  (at('expériences', 30) - .05, 'sur tes expériences personnelles')],
     [(30.667, 33.400, 'c6', 293, 679, 494, 878), (33.400, 34.067, 'c7', 288, 667, 504, 894)]),
    (40.900, 45.400, 'Vidéos', 'AVANT/APRÈS', [(40.900, 'personnelles'), (at('celles', 40) - .05, 'de tes clients')],
     [(40.900, 42.200, 'c8', 218, 746, 644, 696), (42.200, 43.400, 'c9', 304, 712, 474, 850),
      (43.400, 45.400, 'c10', 302, 700, 476, 846)]),
    (45.400, 48.633, 'Vidéos', 'VOICI CE QUE JE FERAIS', [], [(45.400, 48.633, 'c11', 272, 662, 538, 958)]),
]
BROWN_SPANS = [(a, b) for a, b, _ in FUNNELS] + [(12.833, 18.033), (26.367, 34.067), (40.900, 48.633)]


def show(sel, a, b):
    tw = [f"gsap.set('{sel}',{{autoAlpha:0}});", f"tl.set('{sel}',{{autoAlpha:1}},{a:.3f});"]
    if b < DUR - .01:
        tw.append(f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});")
    return tw


def eye_badge(text, x, y, w, h, fs):
    """dark view-count badge with an eye icon (as in her funnel and wide shot)"""
    s = h * .62
    return (f'<div class="badge" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;font-size:{fs}px">'
            f'<svg width="{s:.0f}" height="{s:.0f}" viewBox="0 0 24 24"><path d="M2 12c3-5 6.5-7 10-7s7 2 10 7c-3 5-6.5 7-10 7s-7-2-10-7z" '
            f'fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="12" cy="12" r="3.6" fill="#fff"/></svg><span>{text}</span></div>')


ARROWS = {   # white hand-drawn arrows: path, arrow head (polyline)
    1: ('M330 630 C318 545 368 494 440 492', '414 470 443 492 416 512'),
    2: ('M360 938 C292 922 222 948 192 1010', '176 980 190 1013 222 1004'),
    3: ('M646 1200 C700 1206 730 1250 733 1306', '712 1285 733 1310 752 1284'),
}


def funnel(k, a, b):
    fid = f'fun{k}'
    svg = (f'<svg class="full" viewBox="0 0 1080 1920">'
           f'<polygon points="270,683 810,683 734,896 346,896" fill="{T1}" stroke="{T1}" stroke-width="22" stroke-linejoin="round"/>'
           f'<polygon points="346,918 734,918 659,1074 421,1074" fill="{T2}" stroke="{T2}" stroke-width="18" stroke-linejoin="round"/>'
           f'<polygon points="415,1097 665,1097 600,1199 600,1296 540,1339 480,1296 480,1199" fill="{T3}" stroke="{T3}" '
           f'stroke-width="14" stroke-linejoin="round"/>')
    for n in range(1, k + 1):
        p, head = ARROWS[n]
        svg += (f'<g id="{fid}a{n}"><path d="{p}" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'
                f'<polyline points="{head}" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>')
    svg += '</svg>'
    parts = [svg, eye_badge('1M', 432, 730, 216, 97, 56)]
    labels = [('TOFU', 'Top of Funnel', 486, 745, 421, 566)]
    if k >= 2:
        parts.append(f'<div id="{fid}b2">{eye_badge("100K", 443, 950, 194, 76, 46)}</div>')
        labels.append(('MOFU', 'Middle of Funnel', 76, 350, 1048, 1177))
    if k >= 3:
        parts.append(f'<div id="{fid}b3">{eye_badge("10K", 458, 1112, 190, 72, 44)}</div>')
        labels.append(('BOFU', 'Bottom of Funnel', 566, 810, 1361, 1490))
    for i, (big, small, x0, x1, ty, sy) in enumerate(labels, 1):
        cx = (x0 + x1) / 2
        parts.append(f'<div id="{fid}l{i}"><div class="flab" style="left:{cx - 300:.0f}px;top:{ty - 10}px">{big}</div>'
                     f'<div class="fsub" style="left:{cx - 300:.0f}px;top:{sy - 8}px">{small}</div></div>')
    html = f'<div id="{fid}" class="screen">{"".join(parts)}</div>'
    tw = show(f'#{fid}', a, b)
    # what is new in this screen pops in: the newest label at once, its arrow and badge a beat later
    tw.append(f"tl.fromTo('#{fid}l{k}',{{autoAlpha:0,scale:.8}},{{autoAlpha:1,scale:1,duration:.25,ease:'back.out(2)',immediateRender:false}},{a:.3f});")
    tw.append(f"gsap.set('#{fid}a{k}',{{autoAlpha:0}});")
    tw.append(f"tl.to('#{fid}a{k}',{{autoAlpha:1,duration:.2}},{a + .5:.3f});")
    if k >= 2:
        tw.append(f"gsap.set('#{fid}b{k}',{{autoAlpha:0}});")
        tw.append(f"tl.fromTo('#{fid}b{k}',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.25,ease:'back.out(2)',immediateRender:false}},{a + .6:.3f});")
    return [html], tw


def title_size(title):
    return min(134, round(860 / (0.43 * len(title))))


def card_screens():
    html, tw = [], []
    for k, (a, b, label, title, subs, vids) in enumerate(CARDS):
        sid = f'cs{k}'
        fs = title_size(title)
        sub_html = ''.join(f'<div id="{sid}s{j}" class="csub">{s}</div>' for j, (_, s) in enumerate(subs))
        html.append(f'<div id="{sid}" class="screen"><div class="tblock" style="top:{352}px"><div class="clab">{label}</div>'
                    f'<div class="ctit" style="font-size:{fs}px">{title}</div><div class="subs">{sub_html}</div></div></div>')
        tw += show(f'#{sid}', a, b)
        for j, (t, _) in enumerate(subs):
            end = subs[j + 1][0] if j + 1 < len(subs) else b
            tw += show(f'#{sid}s{j}', t, end)
        for v0, v1, vid, x, y, w, h in vids:
            html.append(f'<div id="w{vid}" class="cardv" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                        f'<video id="{vid}" src="assets/cards/{vid}.mp4" muted playsinline data-start="{v0:.3f}" data-media-start="0" '
                        f'data-duration="{v1 - v0:.3f}" data-track-index="{20 + int(vid[1:])}"></video></div>')
            tw += show(f'#w{vid}', v0, v1)
    return html, tw


# ------------------------------------------------------------------ hook + wide shot
def hook():
    back = ['<div id="hk1" class="anton hook" style="left:108px;top:318px;font-size:226px">TOFU</div>']
    front = ['<div id="hk2" class="anton hook" style="left:578px;top:932px;font-size:226px">MOFU</div>',
             '<div id="hk3" class="anton hook" style="left:84px;top:1382px;font-size:226px">BOFU</div>']
    tw = []
    for k, t in ((1, 0.0), (2, 0.33), (3, 0.60)):
        tw += show(f'#hk{k}', t, HOOK_END)
        tw.append(f"tl.fromTo('#hk{k}',{{scale:1.25}},{{scale:1,duration:.16,ease:'power3.out',immediateRender:false}},{t:.3f});")
    wide = []
    for k, (word, x0, x1, badge, bx, bw) in enumerate([('TOFU', 60, 307, '1M', 104, 172), ('MOFU', 393, 656, '100K', 438, 201),
                                                       ('BOFU', 767, 1020, '10K', 782, 233)]):
        wide.append(f'<div class="anton hook" style="left:{(x0 + x1) / 2 - 200:.0f}px;width:400px;text-align:center;top:398px;'
                    f'font-size:151px">{word}</div>')
        wide.append(eye_badge(badge, bx, 596, bw, 68, 44))
    front.append(f'<div id="wide">{"".join(wide)}</div>')
    tw += show('#wide', HOOK_END, WIDE_END)
    return back, front, tw


# ------------------------------------------------------------------ captions: one word at a time
def screen_at(t):
    for a, b, *_ in CARDS:
        if a <= t < b:
            return 'card'
    for a, b, _ in FUNNELS:
        if a <= t < b:
            return 'funnel'
    return None


def cap_y(t):
    if t >= IG_IN:
        return 470
    if t < WIDE_END:
        return 1340
    s = screen_at(t)
    if s == 'funnel':
        return 1135
    if s == 'card':
        for a, b, *_rest, vids in CARDS:
            if a <= t < b and vids:
                bottom = max(y + h for v0, v1, _, x, y, w, h in vids if v0 <= t < v1) if any(v0 <= t < v1 for v0, v1, *_ in vids) else 1575
                return bottom - 20
        return 1560
    return 1100


def captions():
    html, tw = [], []
    ws = [w for w in WORDS if w['start'] >= HOOK_END - .05]
    for k, w in enumerate(ws):
        a = max(HOOK_END, w['start'] - .03)
        b = ws[k + 1]['start'] - .03 if k + 1 < len(ws) else DUR
        b = min(b, a + 1.2)
        if b - a < .06:      # words closer than two frames: skip, the next one takes over
            continue
        if FUNNELS[2][0] <= a < FUNNELS[2][1]:   # she leaves the full funnel without captions
            continue
        html.append(f'<div id="cp{k}" class="cap" style="top:{cap_y(a)}px">{w["text"]}</div>')
        tw += show(f'#cp{k}', a, b)
        tw.append(f"tl.fromTo('#cp{k}',{{scale:1.18}},{{scale:1,duration:.1,ease:'power2.out',immediateRender:false}},{a:.3f});")
    return html, tw


# ------------------------------------------------------------------ instagram follow card
def ig_card():
    verified = ('<svg width="42" height="42" viewBox="0 0 24 24"><path fill="#1C96F0" d="M12 1.5l2.4 1.8 3-.3 1.2 2.8 2.8 1.2-.3 3 '
                '1.8 2.4-1.8 2.4.3 3-2.8 1.2-1.2 2.8-3-.3L12 22.5l-2.4-1.8-3 .3-1.2-2.8-2.8-1.2.3-3L1.1 12l1.8-2.4-.3-3 2.8-1.2 '
                '1.2-2.8 3 .3z"/><path d="M7.6 12.3l3 3 5.8-6" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>')
    cursor = ('<svg width="52" height="70" viewBox="0 0 26 35"><path d="M2 2v26l7-6 5 11 4-2-5-10h9z" fill="#fff" stroke="#111" '
              'stroke-width="1.6" stroke-linejoin="round"/></svg>')
    html = [f'<div id="ig"><div class="igcard"><div class="igav"><img src="assets/avatar.png"/></div>'
            f'<div class="igname">Instagram</div><div id="ighandle" class="ighandle"><span>@thestrategicboost.fr</span></div>'
            f'<div id="igver" class="igver">{verified}</div>'
            f'<div id="igfollow" class="igbtn follow">Follow</div><div id="igfollowing" class="igbtn following">Following</div></div>'
            f'<div id="igcur" class="igcur">{cursor}</div></div>']
    tw = show('#ig', IG_IN, DUR)
    tw += [f"tl.fromTo('#ig .igcard',{{scale:.86,autoAlpha:0}},{{scale:1,autoAlpha:1,duration:.22,ease:'back.out(1.8)',immediateRender:false}},{IG_IN:.3f});",
           "gsap.set('#ighandle',{clipPath:'inset(0 100% 0 0)'});",
           f"tl.to('#ighandle',{{clipPath:'inset(0 0% 0 0)',duration:.55,ease:'none'}},{IG_IN + .3:.3f});",
           "gsap.set('#igver',{autoAlpha:0,scale:.4});",
           f"tl.to('#igver',{{autoAlpha:1,scale:1,duration:.2,ease:'back.out(2.5)'}},{IG_IN + .85:.3f});",
           "gsap.set('#igfollowing',{autoAlpha:0});",
           "gsap.set('#igcur',{autoAlpha:0,x:60,y:110});",
           f"tl.to('#igcur',{{autoAlpha:1,duration:.1}},{IG_IN + .75:.3f});",
           f"tl.to('#igcur',{{x:0,y:0,duration:.3,ease:'power2.out'}},{IG_IN + .75:.3f});",
           f"tl.to('#igcur',{{scale:.82,duration:.06,yoyo:true,repeat:1}},{IG_IN + 1.05:.3f});",
           f"tl.set('#igfollow',{{autoAlpha:0}},{IG_IN + 1.1:.3f});",
           f"tl.set('#igfollowing',{{autoAlpha:1}},{IG_IN + 1.1:.3f});"]
    return html, tw


def zooms():
    tw = []
    for a, b in ZOOMS:
        tw += [f"tl.set('#stage',{{scale:1.3}},{a - .002:.3f});", f"tl.set('#stage',{{scale:1}},{b - .002:.3f});"]
    return tw


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;inset:0;transform-origin:50% 36%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#bgv{{z-index:0}}
#cutwrap{{position:absolute;inset:0;z-index:4}}
.anton{{font-family:Anton;font-weight:400;line-height:1;white-space:nowrap;color:#fff}}
.hook{{position:absolute;z-index:6;text-shadow:0 0 38px rgba(0,0,0,.55),0 0 12px rgba(0,0,0,.35);transform-origin:50% 50%}}
#hk1{{z-index:3}}
.badge{{position:absolute;z-index:7;display:flex;align-items:center;justify-content:center;gap:.22em;border-radius:6px;
  background:rgba(40,44,48,.88);color:#fff;font-family:Poppins;font-weight:600;letter-spacing:-.02em}}
.screen{{position:absolute;inset:0;z-index:10;background:{BROWN}}}
.flab{{position:absolute;width:600px;text-align:center;font:400 126px/1 Anton;color:#fff}}
.fsub{{position:absolute;width:600px;text-align:center;font:600 44px/1 Poppins;color:#fff;letter-spacing:-.02em}}
.tblock{{position:absolute;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;color:#fff}}
.clab{{font:600 44px/1 Poppins;letter-spacing:-.02em;align-self:flex-start;margin-left:4px}}
.ctit{{font-family:Anton;line-height:1.02;white-space:nowrap;letter-spacing:.045em}}
.subs{{position:relative;height:44px}}
.csub{{position:absolute;right:2px;top:0;font:600 38px/1 Poppins;letter-spacing:-.02em;white-space:nowrap}}
.cardv{{position:absolute;z-index:11;overflow:hidden}}
.cardv video{{width:100%;height:100%;object-fit:cover;display:block}}
.cap{{position:absolute;left:0;right:0;z-index:20;text-align:center;color:#fff;font:700 78px/1 Poppins;letter-spacing:-.03em;
  text-shadow:0 0 22px rgba(0,0,0,.55),0 3px 10px rgba(0,0,0,.45);white-space:nowrap;transform-origin:50% 50%}}
#ig{{position:absolute;inset:0;z-index:15}}
.igcard{{position:absolute;left:116px;top:1208px;width:848px;height:174px;background:#fff;border-radius:4px;
  box-shadow:0 18px 50px rgba(0,0,0,.25)}}
.igav{{position:absolute;left:25px;top:24px;width:128px;height:128px;border-radius:50%;padding:7px;
  background:conic-gradient(from 200deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5,#feda75)}}
.igav img{{width:100%;height:100%;border-radius:50%;border:5px solid #fff;object-fit:cover;display:block}}
.igname{{position:absolute;left:184px;top:22px;font:400 74px/1 Cookie;color:#111}}
.ighandle{{position:absolute;left:164px;top:106px;font:700 27px/1 Poppins;color:#111;letter-spacing:-.01em}}
.igver{{position:absolute;left:446px;top:90px}}
.igbtn{{position:absolute;left:502px;top:57px;width:318px;height:66px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font:600 40px/1 Poppins;letter-spacing:-.01em}}
.follow{{background:#1A8CF1;color:#fff}}
.following{{background:#E8E9EC;color:#262626}}
.igcur{{position:absolute;left:660px;top:1310px;z-index:16;filter:drop-shadow(0 2px 4px rgba(0,0,0,.35))}}
'''

SAFE_GUIDE = ('<div style="position:absolute;inset:0;z-index:99;pointer-events:none">'
              '<div style="position:absolute;left:0;right:0;top:0;height:220px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;right:0;top:1470px;bottom:0;background:rgba(255,0,0,.28)"></div></div>')


def build():
    hb, hf, htw = hook()
    f_html, f_tw = [], []
    for k, (a, b, n) in enumerate(FUNNELS):
        h, t = funnel(n, a, b)
        f_html += h; f_tw += t
    c_html, c_tw = card_screens()
    cap_html, cap_tw = captions()
    ig_html, ig_tw = ig_card()
    tweens = zooms() + htw + f_tw + c_tw + cap_tw + ig_tw
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
  <div id="stage">
    <video id="bgv" class="full" src="assets/aroll_graded.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(hb)}
    <div id="cutwrap"><video id="cut" class="full" src="assets/subject_hook_g.webm" muted playsinline data-start="0" data-media-start="0" data-duration="{HOOK_END:.3f}" data-track-index="1"></video></div>
{nl.join(hf)}
  </div>
{nl.join(f_html)}
{nl.join(c_html)}
{nl.join(ig_html)}
{nl.join(cap_html)}
{SAFE_GUIDE if SAFE else ''}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tweens)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s  {len(WORDS)} caption words')
