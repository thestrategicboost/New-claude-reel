#!/usr/bin/env python3
"""Reel "planifier un mois de contenu en 45 min" (two Maé: the one who asks, the one who explains).

Edit idea from the reel Maé sent (hook title, step titles over the speaker, a full-screen infographic per step,
small recap cards above the asker's head, comment + DM call to action), dressed in her branding: brown screens
(#8C5C41), white Anton titles, white symbols, gold-to-white only on highlighted words, small white captions.
Niche: coach sportif.

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
DUR_S = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=duration', '-of', 'csv=p=0', 'assets/aroll.mp4'],
                           capture_output=True, encoding='utf-8', errors='replace').stdout.strip().split(',')[0])
# the a-roll is slowed to 0.9x (Maé talks fast): every time below is written on the ORIGINAL clock (words.json too)
# and the timeline is stretched by K at the end; DUR is the original-clock length
SPEED = 0.9
K = 1 / SPEED
DUR = DUR_S * SPEED
CUT_HOOK = (0.0, 3.2)        # cutouts of her (assets/cut_*.webm) so reels / the guide can scroll behind her head
CUT_CTA = (37.833, 41.6)
BROWN = '#8C5C41'
GRAD_T = 'linear-gradient(180deg,#FFFFFF 0%,#FBEFD2 30%,#E2BF77 55%,#B8873A 78%,#F1D9A0 100%)'   # gold-white text
GRAD = 'linear-gradient(160deg,#7A5420 0%,#C99A4E 26%,#F3DFB2 44%,#FFFFFF 51%,#E6C681 60%,#A9792F 84%,#6E4A1B 100%)'
CTA_END = 42.70

# step titles over the explaining Maé: (start, end, step, title)
STEPS = [(5.20, 7.00, 1, 'RYTHME'), (10.18, 11.45, 2, 'PLANNING'), (16.93, 18.50, 3, 'THÉMATIQUES'),
         (21.24, 22.60, 4, 'TYPES DE CONTENU'), (26.12, 27.40, 5, 'TON MOIS')]
# full-screen brown infographics
SCREENS = {'rythme': (7.00, 8.867), 'planning': (11.45, 14.50), 'themes': (18.50, 21.20), 'types': (22.60, 24.600),
           'mois': (27.40, 32.567)}

PACES = [('CHILL', 3, 7.30, 'LMV'), ('MOYEN', 5, 7.88, 'LMMJV'), ('INTENSE', 7, 8.60, 'LMMJVSD')]
DAYS = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
LIT = {'CHILL': (0, 2, 4), 'MOYEN': (0, 1, 2, 3, 4), 'INTENSE': (0, 1, 2, 3, 4, 5, 6)}
TOPICS = [('Musculation', 'dumbbell'), ('Nutrition', 'apple'), ('Cardio', 'heart'), ('Mindset', 'brain'), ('Récupération', 'moon')]
TYPES = ['Tutoriel', 'Storytelling', 'Avant / Après', 'Liste', 'Q / R']
IDEAS = [['Le squat parfait', 'Mon 1er 100 kg', '6 mois de muscu', '5 erreurs en salle', 'Combien de séries ?'],
         ['Mon bowl protéiné', 'Ma relation à la bouffe', 'Mon assiette avant / après', '7 snacks healthy', 'Faut-il compter ?'],
         ['HIIT en 15 min', 'Mon 1er 10 km', 'Cardio : J1 vs J30', '3 cardios sans courir', 'Cardio à jeun ?'],
         ['Rester motivé', 'Le jour où j’ai lâché', 'Mon mental avant / après', '4 excuses à bannir', 'Comment tenir ?'],
         ['Étirements du soir', 'Ma blessure', 'Sommeil avant / après', '5 clés de récup', 'Repos ou pas ?']]
TYPE_TAG = ['Tuto', 'Story', 'Av / Ap', 'Liste', 'Q / R']
TAG_BG = ['#FFFFFF', '#F3DFB2', '#E2BF77', '#C99A4E', '#6E4A1B']
TAG_FG = ['#5A3F1F', '#5A3F1F', '#4A3010', '#FFFFFF', '#FFFFFF']

ICONS = {   # white line icons, 100x100
    'dumbbell': '<path d="M14 50h72M24 34v32M34 28v44M66 28v44M76 34v32"/>',
    'apple': '<path d="M50 34c-8-8-30-6-30 16 0 18 14 32 22 32 4 0 6-2 8-2s4 2 8 2c8 0 22-14 22-32 0-22-22-24-30-16z"/><path d="M50 34c0-10 6-16 14-18"/>',
    'heart': '<path d="M50 80S16 60 16 38c0-12 9-20 19-20 7 0 12 4 15 9 3-5 8-9 15-9 10 0 19 8 19 20 0 22-34 42-34 42z"/><path d="M22 50h16l6-10 8 20 6-10h20"/>',
    'brain': '<path d="M50 20v60M50 24c-6-8-20-6-22 4-10 2-12 14-6 20-6 8 0 20 10 20 2 8 12 12 18 6M50 24c6-8 20-6 22 4 10 2 12 14 6 20 6 8 0 20-10 20-2 8-12 12-18 6"/>',
    'moon': '<path d="M64 16a34 34 0 1 0 20 46A28 28 0 0 1 64 16z"/><path d="M30 24l3 6 6 3-6 3-3 6-3-6-6-3 6-3z" stroke-width="3"/>',
}

with open('words.json', encoding='utf-8') as _f:
    RAW = json.load(_f)


def words():
    out = []
    for w in RAW:
        t = w['text']
        if out and t[:1] in "'’-" and len(t) > 1:
            out[-1]['text'] += t; out[-1]['end'] = w['end']; continue
        out.append(dict(w))
    fix = {'girl': 'girl', 'te': 'commente', 'level': 'LEVEL', 'up': 'UP'}
    res = []
    for w in out:
        t = re.sub(r'[.,!?;:«»"]', '', w['text']).strip().replace("'", '’')
        if not t:
            continue
        res.append({'text': t, 'start': w['start'], 'end': w['end']})
    # "comment te level up" is "commente LEVEL UP"
    for i, w in enumerate(res):
        if w['text'].lower() == 'te' and i + 1 < len(res) and res[i + 1]['text'].lower() == 'level':
            res[i - 1]['text'] = 'commente'; w['text'] = ''
            res[i + 1]['text'] = 'LEVEL'; res[i + 2]['text'] = 'UP'
        if w['text'] == 'as' and res[i - 1]['text'] == 'Tu' and res[i + 1]['text'] == 'une':   # "t'as autre chose"
            w['text'] = 'as'; res[i + 1]['text'] = 'autre'
    return [w for w in res if w['text']]


WORDS = words()
GOLD_WORDS = {'45', 'minutes', 'mois', 'chill', 'moyen', 'intense', 'discipline', 'rigueur', 'niche', 'tableau',
              'incroyable', 'gratuit', 'LEVEL', 'UP', 'vendredi', 'lundi'}


def show(sel, a, b):
    tw = [f"gsap.set('{sel}',{{autoAlpha:0}});", f"tl.set('{sel}',{{autoAlpha:1}},{a:.3f});"]
    if b < DUR - .01:
        tw.append(f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});")
    return tw


def pop(sel, t, d=.3, s=.6):
    return [f"gsap.set('{sel}',{{autoAlpha:0}});",
            f"tl.fromTo('{sel}',{{autoAlpha:0,scale:{s}}},{{autoAlpha:1,scale:1,duration:{d},ease:'back.out(1.8)',immediateRender:false}},{t:.3f});"]


ICONS_F = {   # filled white glyphs (phone app style), 100x100
    'dumbbell': '<rect x="6" y="38" width="11" height="24" rx="4"/><rect x="19" y="27" width="13" height="46" rx="5"/>'
                '<rect x="68" y="27" width="13" height="46" rx="5"/><rect x="83" y="38" width="11" height="24" rx="4"/><rect x="30" y="45" width="40" height="10" rx="3"/>',
    'apple': '<path d="M50 32c-6-6-30-8-30 18 0 20 13 36 21 36 4 0 6-2 9-2s5 2 9 2c8 0 21-16 21-36 0-26-24-24-30-18z"/><path d="M52 28c0-10 7-16 16-17 0 9-7 16-16 17z"/>',
    'heart': '<path d="M50 86S10 63 10 36c0-13 10-23 22-23 8 0 14 4 18 10 4-6 10-10 18-10 12 0 22 10 22 23 0 27-40 50-40 50z"/>',
    'brain': '<path d="M50 8c-18 0-30 13-30 29 0 11 6 18 11 23 3 3 4 6 4 9v5h30v-5c0-3 1-6 4-9 5-5 11-12 11-23 0-16-12-29-30-29z"/>'
             '<rect x="36" y="80" width="28" height="7" rx="3.5"/><rect x="41" y="90" width="18" height="6" rx="3"/>',
    'moon': '<path d="M60 10a40 40 0 1 0 30 56A33 33 0 0 1 60 10z"/>',
}


def icon(name, size):
    return f'<svg class="icf" width="{size}" height="{size}" viewBox="0 0 100 100">{ICONS_F[name]}</svg>'


def app(name, size):
    """gold app-icon tile with a white glyph"""
    return f'<div class="app" style="width:{size}px;height:{size}px;border-radius:{size * .26:.0f}px">{icon(name, round(size * .56))}</div>'


def in_screen(t):
    return any(a <= t < b for a, b in SCREENS.values())


# ------------------------------------------------------------------ captions: 1-3 words, small white, key words gold
CUTS = [3.2, 4.033, 5.067, 8.867, 10.067, 15.9, 16.933, 24.6, 25.933, 27.733, 32.567, 35.333, 37.833, 42.7]


def chunks():
    out, cur = [], []
    for w in WORDS:
        if w['start'] >= 41.0 and w['start'] < CTA_END:     # the comment bar carries the CTA
            continue
        # never run a caption across a pause or a cut (two different Maé)
        if cur and (w['start'] - cur[-1]['end'] > .3 or any(cur[-1]['start'] < c <= w['start'] for c in CUTS)):
            out.append(cur); cur = []
        cur.append(w)
        if len(cur) == 3 or w['text'][-1:] in '.!?' or len(' '.join(x['text'] for x in cur)) > 14:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def captions():
    """one word at a time (as on her TOFU MOFU BOFU reel): white Poppins, black shadow, a quick pop on each word"""
    html, tw = [], []
    ws = [w for w in WORDS if not 41.0 <= w['start'] < CTA_END]     # the comment bar carries the CTA
    for k, w in enumerate(ws):
        a = w['start'] - .03
        b = ws[k + 1]['start'] - .03 if k + 1 < len(ws) else DUR
        b = min(b, a + 1.2, next((x for x in CUTS if a + .05 < x), DUR))
        if a < 41.0 < b:
            b = 41.0
        if b - a < .06:      # words closer than two frames: skip, the next one takes over
            continue
        cls = 'cap low' if in_screen(a + .05) else 'cap'
        html.append(f'<div id="cp{k}" class="{cls}">{w["text"]}</div>')
        tw += show(f'#cp{k}', a, b)
        tw.append(f"tl.fromTo('#cp{k}',{{scale:1.3,y:10}},{{scale:1,y:0,duration:.14,ease:'back.out(2.2)',immediateRender:false}},{a:.3f});")
    return html, tw


# ------------------------------------------------------------------ hook: something moves from frame 0
WALL_X = [-30, 245, 520, 795]


def hook():
    a, b = CUT_HOOK
    html, tw = [], []
    # a wall of her reels scrolling BEHIND her (the cutout video sits on top of it)
    cols = []
    for c, x in enumerate(WALL_X):
        cards = ''.join(f'<div class="wc"><img src="assets/reels/r{(c * 3 + i) % 10 + 1}.jpg"/></div>' for i in range(8))
        cols.append(f'<div id="wl{c}" class="wcol" style="left:{x}px">{cards}</div>')
    html.append(f'<div id="wall">{"".join(cols)}</div>')
    # visible on the very first frame: no hide/show at 0, only hidden at the end of the hook
    tw += ["gsap.set('#wall',{opacity:.42});", f"tl.set('#wall',{{autoAlpha:0}},{b:.3f});"]
    tw.append("tl.to('#wall',{opacity:.78,duration:.3},2.30);")
    for c in range(len(WALL_X)):
        y0, y1 = (-300, -1500) if c % 2 == 0 else (-1500, -300)
        tw.append(f"tl.fromTo('#wl{c}',{{y:{y0}}},{{y:{y1},duration:{b - a:.3f},ease:'none',immediateRender:false}},{a:.3f});")
    # punch-in of the whole picture on frame 0
    tw.append("tl.fromTo('#stage',{scale:1.14},{scale:1,duration:.45,ease:'power3.out',immediateRender:true},0);")
    # title already on screen at frame 0, the second line lands on "45 minutes"
    html.append('<div id="hook"><div class="hk1">UN MOIS DE CONTENU</div><div id="hk2" class="hk2">en <span class="gd">45 MINUTES</span></div></div>')
    tw.append(f"tl.set('#hook',{{autoAlpha:0}},{b:.3f});")
    tw.append("tl.fromTo('#hook .hk1',{scale:1.3,filter:'blur(4px)'},{scale:1,filter:'blur(0px)',duration:.3,ease:'power3.out',immediateRender:true},0);")
    tw += pop('#hk2', .90, .3, .4)
    # phone-widget style cards (frosted brown glass): a timer on "45 minutes", a month on "planifier"
    html.append('<div id="hkW" class="wdg" style="left:50px;top:590px"><div class="wl">MINUTEUR</div>'
                '<div class="ring"><svg width="170" height="170" viewBox="0 0 170 170"><circle cx="85" cy="85" r="74" class="rb"/>'
                '<circle id="rgf" cx="85" cy="85" r="74" class="rf"/></svg><div class="rt">45:00</div></div></div>')
    tw += pop('#hkW', .94, .3, .6)
    tw.append("tl.fromTo('#rgf',{strokeDashoffset:0},{strokeDashoffset:300,duration:2.2,ease:'none',immediateRender:false},.94);")
    dots = ''.join(f'<i id="hd{i}"></i>' for i in range(7))
    html.append(f'<div id="hkC" class="wdg" style="left:800px;top:590px"><div class="wl">CE MOIS</div><div class="wn">30</div>'
                f'<div class="ws">jours planifiés</div><div class="wd">{dots}</div></div>')
    tw += pop('#hkC', 1.68, .3, .6)
    tw.append("tl.fromTo('#hkC .wd i',{backgroundColor:'rgba(255,255,255,.25)'},{backgroundColor:'#E2BF77',duration:.08,stagger:.08,immediateRender:false},1.85);")
    html += ['<div id="hkM" class="calPos" style="left:340px;top:960px">'] + mini_cal('calH') + ['</div>']
    tw += pop('#hkM', 2.38, .35, .5)
    tw += ["gsap.set('#calH .md i',{scale:0});",
           "tl.to('#calH .md i',{scale:1,duration:.08,stagger:.025,ease:'back.out(3)'},2.50);"]
    for sel in ('#hkW', '#hkC', '#hkM'):
        tw.append(f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});")
    return html, tw


# ------------------------------------------------------------------ step titles over the explaining Maé
def fit(title, big=270, width=1000):
    """Anton caps are ~.46em wide: long titles shrink to stay on one line"""
    return min(big, round(width / (.46 * len(title))))


# magazine titles BEHIND her head (Maé's 2nd inspiration): a small plain label, then a huge serif word revealed letter
# by letter; her cutout (assets/cut_st*.webm) sits on top, so her hair covers the bottom of the letters
STEP_LABEL = {4: ('types de', 'CONTENU')}
CUT_ST = [(5.767, 2.100), (11.300, 1.533), (18.800, 1.867), (23.600, 1.600), (29.033, 1.867)]   # slowed clock


def step_titles():
    html, tw = [], []
    for k, (a, b, n, title) in enumerate(STEPS):
        extra, word = STEP_LABEL.get(n, ('', title))
        letters = ''.join(f'<span class="lt">{c}</span>' if c != ' ' else ' ' for c in word)
        html.append(f'<div id="st{k}" class="stepT"><div class="inner"><div class="sl">Étape {n}{" · " + extra if extra else ""}</div>'
                    f'<div class="sn" style="font-size:{fit(word)}px">{letters}</div></div></div>')
        tw += show(f'#st{k}', a, b)
        tw.append(f"tl.fromTo('#st{k} .sl',{{autoAlpha:0,y:12}},{{autoAlpha:1,y:0,duration:.25,ease:'power2.out',immediateRender:false}},{a:.3f});")
        tw.append(f"tl.fromTo('#st{k} .lt',{{autoAlpha:0,y:50,filter:'blur(12px)'}},{{autoAlpha:1,y:0,filter:'blur(0px)',duration:.32,stagger:.05,"
                  f"ease:'power3.out',immediateRender:false}},{a + .05:.3f});")
        tw.append(f"tl.to('#st{k} .inner',{{autoAlpha:0,filter:'blur(10px)',duration:.18}},{b - .18:.3f});")
    return html, tw


def header(n, title):
    extra, word = STEP_LABEL.get(n, ('', title))
    return (f'<div class="hd"><div class="inner"><div class="hl">Étape {n}{" · " + extra if extra else ""}</div>'
            f'<div class="ht" style="font-size:{fit(word, 190)}px">{word}</div></div></div>')


# ------------------------------------------------------------------ the five brown screens
def scr_rythme():
    a, b = SCREENS['rythme']
    h = ['<div id="sRy" class="screen">', header(1, 'RYTHME')]
    tw = show('#sRy', a, b)
    for k, (name, n, t, _) in enumerate(PACES):
        cx = 200 + k * 340
        thumbs = ''.join(f'<div class="th" id="ry{k}t{i}"><img src="assets/reels/r{(i + k * 3) % 10 + 1}.jpg"/></div>' for i in range(n))
        h.append(f'<div id="ry{k}" class="paceCol" style="left:{cx - 150}px"><div class="tag">{name}</div>'
                 f'<div class="per">{n} posts / sem</div><div class="thumbs">{thumbs}</div></div>')
        tw += pop(f'#ry{k}', t - .05, .25, .7)
        tw += [f"gsap.set('#ry{k} .th',{{autoAlpha:0}});",
               f"tl.fromTo('#ry{k} .th',{{autoAlpha:0,y:20}},{{autoAlpha:1,y:0,duration:.2,stagger:.05,ease:'power2.out',immediateRender:false}},{t + .05:.3f});"]
    h.append('</div>')
    return h, tw


def week(name, lit, cls=''):
    cells = ''.join(f'<div class="day{" on" if i in lit else ""}">{d}</div>' for i, d in enumerate(DAYS))
    return f'<div class="week {cls}">{cells}</div>'


def scr_planning():
    a, b = SCREENS['planning']
    h = ['<div id="sPl" class="screen">', header(2, 'PLANNING')]
    tw = show('#sPl', a, b)
    for k, (name, n, _, _) in enumerate(PACES):
        h.append(f'<div id="pl{k}" class="plRow" style="top:{590 + k * 285}px"><div class="tag">{name}</div>'
                 f'<div class="per">{n} posts / sem</div>{week(name, LIT[name])}</div>')
        t = a + .2 + k * .5
        tw += pop(f'#pl{k}', t, .25, .8)
        tw += [f"gsap.set('#pl{k} .day.on',{{backgroundPosition:'0% 0%'}});",
               f"tl.fromTo('#pl{k} .day.on',{{scale:.6,opacity:.3}},{{scale:1,opacity:1,duration:.18,stagger:.07,ease:'back.out(2)',immediateRender:false}},{t + .2:.3f});"]
    h.append('</div>')
    return h, tw


def scr_themes():
    a, b = SCREENS['themes']
    h = ['<div id="sTh" class="screen">', header(3, 'THÉMATIQUES')]
    tw = show('#sTh', a, b)
    cx, cy, R = 540, 1010, 330
    import math
    pts = []
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        pts.append((cx + R * math.cos(ang), cy + R * .92 * math.sin(ang)))
    svg = '<svg class="full" viewBox="0 0 1080 1920">' + ''.join(
        f'<path id="tha{k}" d="M{cx + (x - cx) * .32:.0f} {cy + (y - cy) * .32:.0f} L{cx + (x - cx) * .7:.0f} {cy + (y - cy) * .7:.0f}" '
        f'stroke="#fff" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round" fill="none" opacity=".85"/>' for k, (x, y) in enumerate(pts)) + '</svg>'
    h.append(svg)
    h.append(f'<div id="thc" class="niche glass" style="left:{cx - 200}px;top:{cy - 78}px"><div class="wl">MA NICHE</div><div class="nn">Coach sportif</div></div>')
    tw += pop('#thc', 19.10, .3, .6)
    for k, ((name, ic), (x, y)) in enumerate(zip(TOPICS, pts)):
        h.append(f'<div id="thn{k}" class="node" style="left:{x - 120:.0f}px;top:{y - 80:.0f}px">{app(ic, 128)}'
                 f'<div class="nodeL">{name}</div></div>')
        t = 19.56 + k * .28
        tw += pop(f'#thn{k}', t, .3, .5)
        tw += [f"gsap.set('#tha{k}',{{opacity:0}});", f"tl.to('#tha{k}',{{opacity:.85,duration:.2}},{t - .1:.3f});"]
    h.append('</div>')
    return h, tw


def scr_types():
    a, b = SCREENS['types']
    h = ['<div id="sTy" class="screen">', header(4, 'TYPES DE CONTENU')]
    tw = show('#sTy', a, b)
    x0, y0, cw, ch, lw, hh = 40, 600, 172, 140, 140, 96
    cells = [f'<div class="tbl" style="left:{x0}px;top:{y0}px;width:{lw + 5 * cw}px;height:{hh + 5 * ch}px">']
    for j, t in enumerate(TYPES):
        cells.append(f'<div class="tc th2" style="left:{lw + j * cw}px;top:0;width:{cw}px;height:{hh}px">{t}</div>')
    for i, (name, ic) in enumerate(TOPICS):
        cells.append(f'<div class="tc rh" style="left:0;top:{hh + i * ch}px;width:{lw}px;height:{ch}px">{app(ic, 58)}<span>{name}</span></div>')
        for j in range(5):
            cells.append(f'<div class="tc idea" id="tc{i}{j}" style="left:{lw + j * cw}px;top:{hh + i * ch}px;width:{cw}px;height:{ch}px">'
                         f'<span>{IDEAS[i][j]}</span></div>')
    cells.append('</div>')
    h += cells
    tw += ["gsap.set('#sTy .idea span',{autoAlpha:0});",
           f"tl.fromTo('#sTy .idea span',{{autoAlpha:0,scale:.7}},{{autoAlpha:1,scale:1,duration:.12,stagger:.055,ease:'power2.out',immediateRender:false}},{23.05:.3f});"]
    h.append('</div>')
    return h, tw


def mini_cal(cid):
    """phone-widget month (frosted brown glass): Mon-Fri content days get a gold dot"""
    cells = ''.join(f'<div class="mh">{d}</div>' for d in 'LMMJVSD')
    for day in range(1, 31):
        on = (day - 1) % 7 < 5
        cells += f'<div class="md{" on" if on else ""}"><span>{day}</span>{"<i></i>" if on else ""}</div>'
    return [f'<div id="{cid}" class="mcal"><div class="wl">OCTOBRE</div><div class="mtt">Mon mois de contenu</div><div class="mgrid">{cells}</div></div>']


def calendar(cid, scale=1.0):
    """month grid Mon-Sun x 5 weeks, Mon-Fri filled with a content-type tag (cycles through the 5 types)"""
    cw, ch = 140, 150
    out = [f'<div id="{cid}" class="cal" style="width:{7 * cw}px;height:{56 + 5 * ch}px;transform:scale({scale})">']
    for j, d in enumerate(['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']):
        out.append(f'<div class="ch" style="left:{j * cw}px;width:{cw}px">{d}</div>')
    n = 0
    for w in range(5):
        for j in range(7):
            day = w * 7 + j + 1
            if day > 30:
                continue
            tag = ''
            if j < 5:
                k = n % 5
                topic = TOPICS[(n // 5 + n) % 5][0]
                tag = (f'<div class="tag2" style="background:{TAG_BG[k]};color:{TAG_FG[k]}">{TYPE_TAG[k]}</div>'
                       f'<div class="topic">{topic}</div>')
                n += 1
            out.append(f'<div class="cd{" on" if tag else ""}" style="left:{j * cw + 4}px;top:{56 + w * ch + 4}px;width:{cw - 8}px;height:{ch - 8}px">'
                       f'<div class="dn">{day}</div>{tag}</div>')
    out.append('</div>')
    return out


def scr_mois():
    a, b = SCREENS['mois']
    h = ['<div id="sMo" class="screen">', header(5, 'TON MOIS'), '<div class="calwrap">'] + calendar('calA') + ['</div>']
    tw = show('#sMo', a, b)
    tw += ["gsap.set('#calA .cd.on .tag2, #calA .cd.on .topic',{autoAlpha:0});",
           f"tl.fromTo('#calA .cd.on .tag2',{{autoAlpha:0,scale:.5}},{{autoAlpha:1,scale:1,duration:.16,stagger:.17,ease:'back.out(2)',immediateRender:false}},{28.10:.3f});",
           f"tl.fromTo('#calA .cd.on .topic',{{autoAlpha:0}},{{autoAlpha:1,duration:.16,stagger:.17,immediateRender:false}},{28.16:.3f});"]
    h.append('</div>')
    return h, tw


# ------------------------------------------------------------------ recap cards (above the asker / beside the expert)
def recap():
    html, tw = [], []
    html.append(f'<div id="rcM" class="recap" style="left:290px;top:236px"><div class="tag">MOYEN</div><div class="per">5 posts / sem</div></div>')
    tw += pop('#rcM', 9.25, .3, .6) + ["tl.set('#rcM',{autoAlpha:0},10.067);"]
    html.append(f'<div id="rcW" class="recap wide" style="left:200px;top:236px"><div class="per">Du lundi au vendredi</div>{week("MOYEN", LIT["MOYEN"], "small")}</div>')
    tw += pop('#rcW', 15.95, .3, .6) + ["tl.set('#rcW',{autoAlpha:0},16.933);"]
    # "here you go": her month, beside her head
    html += ['<div id="rcC" class="calPos" style="left:690px;top:236px">'] + mini_cal('calB') + ['</div>']
    tw += pop('#rcC', 32.80, .35, .5) + ["tl.set('#rcC',{autoAlpha:0},35.333);"]
    return html, tw


# ------------------------------------------------------------------ call to action
def cta():
    # her real guide scrolling behind her head (the cta cutout sits on top), gone before her own IG card at 41.7
    cols = []
    for c, x in enumerate(WALL_X):
        cards = ''.join(f'<div class="gc"><img src="assets/gpages/g-{(c * 3 + i) % 12 + 1:02d}.jpg"/></div>' for i in range(10))
        cols.append(f'<div id="gl{c}" class="wcol" style="left:{x}px">{cards}</div>')
    html = [f'<div id="gwall">{"".join(cols)}</div>',
            '<div id="gtag">GUIDE GRATUIT</div>']
    tw = ["gsap.set('#gwall',{autoAlpha:0});",
          "tl.fromTo('#gwall',{autoAlpha:0},{autoAlpha:.8,duration:.25,immediateRender:false},38.20);"]
    for c in range(len(WALL_X)):
        y0, y1 = (-200, -2600) if c % 2 == 0 else (-2600, -200)
        tw.append(f"tl.fromTo('#gl{c}',{{y:{y0}}},{{y:{y1},duration:3.4,ease:'none',immediateRender:false}},38.20);")
    tw += pop('#gtag', 38.26, .3, .5)
    tw += ["tl.to('#gwall, #gtag',{autoAlpha:0,duration:.15},41.45);", "tl.set('#gwall, #gtag',{autoAlpha:0},41.6);"]
    html.append('<div id="cm"><div class="cmav"><img src="assets/avatar.png"/></div><div class="cmbar"><span id="cmtext"></span>'
                '<span class="caret"></span></div><div id="cmsend" class="cmsend"><svg viewBox="0 0 24 24" width="40" height="40">'
                '<path d="M12 19V6M6 11l6-6 6 6" fill="none" stroke="#2A1E16" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>')
    tw += show('#cm', 41.0, CTA_END) + ["tl.fromTo('#cm',{y:40,scale:.92},{y:0,scale:1,duration:.3,ease:'back.out(1.7)',immediateRender:false},41.0);",
                                       "gsap.set('#cmtext',{textContent:''});"]
    word = 'LEVEL UP'
    for i in range(1, len(word) + 1):
        tw.append(f"tl.set('#cmtext',{{textContent:'{word[:i]}'}},{41.20 + (i - 1) * .05:.3f});")
    tw.append("tl.to('#cmsend',{scale:.82,duration:.07,yoyo:true,repeat:1},41.66);")
    html.append('<div id="dm" class="dm"><div class="dmav"><img src="assets/avatar.png"/></div><div class="dmb">'
                '<div class="dmt">Je t’ai envoyé le lien</div><div class="dml"><svg viewBox="0 0 24 24" width="30" height="30">'
                '<path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1" fill="none" stroke="#5A3F1F" stroke-width="2.4" stroke-linecap="round"/>'
                '</svg><span>Guide gratuit</span></div></div></div>')
    tw += pop('#dm', 41.98, .35, .6) + [f"tl.set('#dm',{{autoAlpha:0}},{CTA_END:.3f});"]
    return html, tw


def sfx_list():
    out = [('impact-bass-1', 0.0, .32), ('whoosh-short', 0.0, .22), ('pop', .90, .26), ('pop', 1.68, .24),
           ('whoosh-short', 2.30, .2), ('sparkle', 2.40, .14)]
    out += [('whoosh-short', a, .22) for a, *_ in STEPS]
    out += [('whoosh-short', a, .26) for a, _ in SCREENS.values()]
    out += [('pop', t - .05, .24) for _, _, t, _ in PACES]
    out += [('pop', SCREENS['planning'][0] + .2 + k * .5, .2) for k in range(3)]
    out += [('pop', 19.10, .24)] + [('pop', 19.56 + k * .28, .18) for k in range(5)]
    out += [('click-soft', 23.05 + k * .3, .3) for k in range(5)]
    out += [('click-soft', 28.10 + k * .85, .3) for k in range(5)]
    out += [('pop', 9.25, .26), ('pop', 15.95, .26), ('pop', 32.80, .28), ('whoosh-short', 38.20, .26), ('pop', 38.40, .26), ('pop', 41.0, .28)]
    out += [('click-soft', 41.20 + i * .05 * 2, .2) for i in range(4)]
    out += [('click', 41.66, .45), ('sparkle', 41.98, .16)]
    return out


SFX_LEN = {'impact-bass-1': 1.2, 'whoosh-short': .57, 'pop': .72, 'sparkle': 1.8, 'click': .36, 'click-soft': .36}
SFX_GAIN = 0.75


def audio():
    out, lanes = [], []
    for k, (name, t, vol) in enumerate(sorted(sfx_list(), key=lambda x: x[1])):
        t *= K
        d = min(SFX_LEN[name], DUR_S - t)
        lane = next((i for i, end in enumerate(lanes) if end <= t), None)
        if lane is None:
            lanes.append(0); lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{name}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{vol * SFX_GAIN:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#bgv{{z-index:0;filter:contrast(1.03) saturate(.97) brightness(1.02)}}
.gd{{background:{GRAD_T};-webkit-background-clip:text;background-clip:text;color:transparent;padding-top:.12em;margin-top:-.12em}}
.ic{{fill:none;stroke:#fff;stroke-width:6;stroke-linecap:round;stroke-linejoin:round}}
/* captions */
.cap{{position:absolute;left:0;right:0;top:1350px;z-index:30;text-align:center;font:700 82px/1.1 Poppins;color:#fff;letter-spacing:-.03em;
  text-shadow:0 0 24px rgba(0,0,0,.6),0 4px 12px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.5);white-space:nowrap;transform-origin:50% 50%}}
.cap.low{{top:1500px}}
/* hook */
#stage{{position:absolute;inset:0;z-index:0;transform-origin:50% 35%}}
.cut{{z-index:8;filter:contrast(1.03) saturate(.97) brightness(1.02)}}
#wall{{position:absolute;inset:0;z-index:5;
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 80%);mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 80%)}}
.wcol{{position:absolute;top:0;width:262px;display:flex;flex-direction:column;gap:18px}}
.wc{{width:262px;height:466px;flex:none;border-radius:22px;overflow:hidden;border:4px solid rgba(255,255,255,.9)}}
.wc img{{width:100%;height:100%;object-fit:cover;display:block}}
#hook{{position:absolute;left:0;right:0;top:226px;z-index:12;text-align:center;filter:drop-shadow(0 6px 18px rgba(0,0,0,.55))}}
.hk1{{font:400 112px/1 Anton;color:#fff}}
.hk2{{font:italic 800 76px/1.1 Poppins;color:#fff;margin-top:4px}}
.wdg{{position:absolute;z-index:12;width:230px;height:250px;border-radius:44px;background:rgba(58,38,26,.55);
  -webkit-backdrop-filter:blur(22px) saturate(1.2);backdrop-filter:blur(22px) saturate(1.2);border:1.5px solid rgba(255,255,255,.35);
  box-shadow:0 20px 50px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.25);color:#fff;text-align:center;padding-top:22px}}
.wl{{font:600 20px/1 Poppins;letter-spacing:.14em;color:#E2BF77}}
.ring{{position:relative;width:170px;height:170px;margin:14px auto 0}}
.ring svg{{transform:rotate(-90deg)}}
.rb{{fill:none;stroke:rgba(255,255,255,.18);stroke-width:9}}
.rf{{fill:none;stroke:#fff;stroke-width:9;stroke-linecap:round;stroke-dasharray:465}}
.rt{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:700 42px/1 Poppins;letter-spacing:-.01em}}
.wn{{font:800 104px/1 Poppins;letter-spacing:-.04em;margin-top:12px}}
.ws{{font:600 22px/1 Poppins;opacity:.9;margin-top:6px}}
.wd{{display:flex;justify-content:center;gap:8px;margin-top:18px}}
.wd i{{width:14px;height:14px;border-radius:50%;background:rgba(255,255,255,.25)}}
.calPos{{position:absolute;z-index:15}}
.mcal{{width:360px;padding:24px 22px 20px;border-radius:44px;background:rgba(58,38,26,.55);-webkit-backdrop-filter:blur(22px) saturate(1.2);
  backdrop-filter:blur(22px) saturate(1.2);border:1.5px solid rgba(255,255,255,.35);box-shadow:0 20px 50px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.25);color:#fff}}
.mcal .wl{{text-align:left;padding-left:6px}}
.mtt{{font:700 26px/1.2 Poppins;margin:6px 0 12px 6px}}
.mgrid{{display:grid;grid-template-columns:repeat(7,1fr);row-gap:6px;text-align:center}}
.mh{{font:600 15px/1 Poppins;opacity:.6;padding-bottom:4px}}
.md{{position:relative;height:38px;font:600 19px/30px Poppins}}
.md i{{position:absolute;left:50%;bottom:2px;width:7px;height:7px;margin-left:-3.5px;border-radius:50%;background:#E2BF77}}

/* step titles: magazine serif behind her head */
.stepT{{position:absolute;left:0;right:0;top:196px;z-index:6;text-align:center;color:#FFF8EE}}
.stepT .inner,.hd .inner{{display:inline-block;text-align:left}}
.stepT .sl{{font:600 40px/1 Poppins;color:#fff;margin-left:.3em;text-shadow:0 2px 10px rgba(0,0,0,.35)}}
.stepT .sn{{font-family:Anton;font-weight:400;line-height:1.05;letter-spacing:.01em;white-space:nowrap;margin-top:6px;
  text-shadow:0 6px 30px rgba(0,0,0,.25)}}
.lt{{display:inline-block}}
/* brown screens */
.screen{{position:absolute;inset:0;z-index:20;background:radial-gradient(120% 80% at 50% 38%,#9C6B4E 0%,{BROWN} 55%,#734A33 100%);color:#fff}}
.glass{{background:rgba(255,255,255,.12);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);border:1.5px solid rgba(255,255,255,.3);
  box-shadow:0 18px 44px rgba(40,22,10,.3),inset 0 1px 0 rgba(255,255,255,.3)}}
.app{{margin:0 auto;display:flex;align-items:center;justify-content:center;background:linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%);
  box-shadow:inset 0 2px 0 rgba(255,255,255,.65),inset 0 -3px 6px rgba(80,45,10,.25),0 12px 26px rgba(40,22,10,.35)}}
.icf{{fill:#fff;filter:drop-shadow(0 2px 3px rgba(80,45,10,.35))}}
.hd{{position:absolute;left:0;right:0;top:250px;text-align:center}}
.hl{{font:600 40px/1 Poppins;margin-left:.3em;opacity:.95}}
.ht{{font-family:Anton;font-weight:400;line-height:1.05;letter-spacing:.01em;margin-top:6px;white-space:nowrap}}
.tag{{display:inline-block;font:400 46px/1 Anton;letter-spacing:.03em;color:#5A3F1F;background:#fff;padding:10px 24px 8px;border-radius:40px;box-shadow:0 8px 20px rgba(40,22,10,.25)}}
.per{{font:600 30px/1 Poppins;margin-top:12px}}
.paceCol{{position:absolute;top:540px;width:310px;height:740px;text-align:center;padding:26px 0 28px;border-radius:40px;background:rgba(255,255,255,.12);
  border:1.5px solid rgba(255,255,255,.3);box-shadow:0 18px 44px rgba(40,22,10,.3),inset 0 1px 0 rgba(255,255,255,.3)}}
.thumbs{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:24px}}
.th{{width:100px;height:160px;border-radius:18px;overflow:hidden;border:2px solid rgba(255,255,255,.8);box-shadow:0 8px 18px rgba(0,0,0,.3)}}
.th img{{width:100%;height:100%;object-fit:cover;display:block}}
.plRow{{position:absolute;left:40px;right:40px;text-align:center;padding:22px 0 26px;border-radius:40px;background:rgba(255,255,255,.12);
  border:1.5px solid rgba(255,255,255,.3);box-shadow:0 18px 44px rgba(40,22,10,.3),inset 0 1px 0 rgba(255,255,255,.3)}}
.week{{display:flex;justify-content:center;gap:12px;margin-top:22px}}
.day{{width:104px;height:84px;border-radius:26px;background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.3);
  display:flex;align-items:center;justify-content:center;font:400 40px/1 Anton;color:#fff}}
.day.on{{background:linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%);color:#fff;border-color:rgba(255,255,255,.6);
  box-shadow:inset 0 2px 0 rgba(255,255,255,.65),0 8px 18px rgba(40,22,10,.3);text-shadow:0 2px 4px rgba(80,45,10,.4)}}
.week.small{{gap:7px;margin-top:12px}}
.week.small .day{{width:72px;height:60px;font-size:30px;border-radius:20px}}
.niche{{position:absolute;width:400px;height:156px;border-radius:44px;color:#fff;text-align:center;padding-top:26px}}
.nl{{font:600 30px/1 Poppins;letter-spacing:.1em}}
.nn{{font:800 54px/1.15 Poppins;letter-spacing:-.02em;margin-top:8px}}
.node{{position:absolute;width:240px;text-align:center}}
.nodeIc{{width:118px;height:118px;margin:0 auto;border-radius:30%;border:3px solid #fff;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center}}
.nodeL{{margin-top:14px;font:600 30px/1 Poppins;color:#fff;text-shadow:0 2px 8px rgba(40,22,10,.35)}}
.tbl{{position:absolute}}
.tc{{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center;padding:8px;border-radius:22px;
  background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.26);box-shadow:inset 0 1px 0 rgba(255,255,255,.25);
  transform:scale(.94)}}
.th2{{font:400 30px/1.05 Anton;background:#fff;color:#5A3F1F;border-color:#fff;border-radius:40px;box-shadow:0 8px 18px rgba(40,22,10,.25)}}
.rh{{flex-direction:column;gap:8px;font:600 19px/1.1 Poppins;background:none;border:none;box-shadow:none}}
.idea span{{font:600 22px/1.15 Poppins}}
.calwrap{{position:absolute;left:30px;top:540px;padding:20px;border-radius:44px;background:rgba(255,255,255,.1);border:1.5px solid rgba(255,255,255,.28);
  box-shadow:0 18px 44px rgba(40,22,10,.3),inset 0 1px 0 rgba(255,255,255,.3)}}
.cal{{position:relative;transform-origin:0 0}}
.ch{{position:absolute;top:0;height:48px;text-align:center;font:600 26px/48px Poppins;opacity:.7}}
.cd{{position:absolute;border-radius:22px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.18);padding:10px}}
.cd.on{{background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.3)}}
.dn{{font:700 22px/1 Poppins;opacity:.85}}
.tag2{{display:inline-block;margin-top:12px;font:700 21px/1 Poppins;padding:7px 12px;border-radius:30px;box-shadow:0 4px 10px rgba(40,22,10,.25)}}
.topic{{font:600 17px/1.1 Poppins;margin-top:8px}}
/* recaps */
.recap{{position:absolute;z-index:15;width:500px;text-align:center;background:rgba(58,38,26,.55);-webkit-backdrop-filter:blur(22px) saturate(1.2);
  backdrop-filter:blur(22px) saturate(1.2);border:1.5px solid rgba(255,255,255,.35);border-radius:44px;padding:24px 18px 26px;color:#fff;
  box-shadow:0 20px 50px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.25)}}
.recap.wide{{width:680px}}
.recapCal{{position:absolute;z-index:15;left:690px;top:236px;width:350px;height:290px;border-radius:18px;overflow:hidden;background:{BROWN};
  border:4px solid #fff;box-shadow:0 14px 34px rgba(0,0,0,.35);color:#fff}}
.recapCal .cal{{transform:scale(.33)!important;left:10px;top:12px}}
/* cta */
#gwall{{position:absolute;inset:0;z-index:5;
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 66%,transparent 84%);mask-image:linear-gradient(180deg,#000 0%,#000 66%,transparent 84%)}}
.gc{{width:262px;height:370px;flex:none;border-radius:18px;overflow:hidden;border:4px solid rgba(255,255,255,.9);background:#fff}}
.gc img{{width:100%;height:100%;object-fit:cover;display:block}}
#gtag{{position:absolute;left:0;right:0;top:232px;z-index:12;text-align:center;font:400 120px/1 Anton;color:#fff;
  filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))}}
#cm{{position:absolute;left:70px;right:70px;top:1160px;z-index:25;height:116px;display:flex;align-items:center;gap:18px}}
.cmav{{width:104px;height:104px;border-radius:50%;padding:5px;background:#fff;flex:none}}
.cmav img,.dmav img{{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block}}
.cmbar{{flex:1;height:96px;border-radius:48px;background:rgba(30,22,16,.62);border:2px solid rgba(255,255,255,.4);
  display:flex;align-items:center;padding:0 34px;font:700 50px/1 Poppins;color:#fff;letter-spacing:.02em}}
.caret{{display:inline-block;width:4px;height:52px;background:#fff;margin-left:6px}}
.cmsend{{position:absolute;right:16px;width:76px;height:76px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}}
.dm{{position:absolute;z-index:25;left:150px;top:1300px;display:flex;gap:14px;align-items:flex-start}}
.dmav{{width:70px;height:70px;border-radius:50%;border:3px solid #fff;overflow:hidden;flex:none}}
.dmb{{background:rgba(30,22,16,.8);border:2px solid rgba(255,255,255,.35);border-radius:22px;padding:16px 22px;color:#fff}}
.dmt{{font:600 30px/1.2 Poppins}}
.dml{{display:inline-flex;align-items:center;gap:8px;margin-top:12px;background:{GRAD};color:#5A3F1F;font:700 28px/1 Poppins;
  padding:10px 18px;border-radius:12px;box-shadow:inset 0 2px 0 rgba(255,255,255,.7)}}
'''

SAFE_GUIDE = ('<div style="position:absolute;inset:0;z-index:99;pointer-events:none">'
              '<div style="position:absolute;left:0;right:0;top:0;height:220px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;right:0;top:1470px;bottom:0;background:rgba(255,0,0,.28)"></div></div>')


def build():
    hk, ct = hook(), cta()
    st = step_titles()
    stage = [hk[0].pop(0), ct[0].pop(0)] + st[0]      # wall, guide window and step titles live under the cutouts
    (ha, hb), (ca, cb) = CUT_HOOK, CUT_CTA
    cuts = [f'<video id="cutH" class="full cut" src="assets/cut_hook.webm" muted playsinline data-start="{ha * K:.3f}" data-media-start="0" '
            f'data-duration="{(hb - ha) * K:.3f}" data-track-index="1"></video>',
            f'<video id="cutC" class="full cut" src="assets/cut_cta.webm" muted playsinline data-start="{ca * K:.3f}" data-media-start="0" '
            f'data-duration="{(cb - ca) * K:.3f}" data-track-index="3"></video>']
    cuts += [f'<video id="cutS{k}" class="full cut" src="assets/cut_st{k}.webm" muted playsinline data-start="{t:.3f}" data-media-start="0" '
             f'data-duration="{d:.3f}" data-track-index="{4 + k}"></video>' for k, (t, d) in enumerate(CUT_ST)]
    parts = [hk, ([], st[1]), scr_rythme(), scr_planning(), scr_themes(), scr_types(), scr_mois(), recap(), ct, captions()]
    html = '\n'.join('\n'.join(h) for h, _ in parts)
    tw = '\n'.join('\n'.join(t) for _, t in parts)
    # stretch every timeline position to the slowed clock (durations stay as they are)
    tw = re.sub(r'\},(\d+(?:\.\d+)?)\);', lambda m: f'}},{float(m.group(1)) * K:.3f});', tw)
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
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR_S:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR_S:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(audio())}
  <div id="stage">
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR_S:.3f}" data-track-index="0"></video>
{nl.join(stage)}
{nl.join(cuts)}
  </div>
{html}
{SAFE_GUIDE if SAFE else ''}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{tw}
tl.set({{}}, {{}}, {DUR_S:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR_S:.3f}s  {len(chunks())} caption chunks')
