#!/usr/bin/env python3
"""Reel "3 fois": once a day / once a week / once a month, said three times, each time with a new set of Instagram
habits, edited like the "3 fois modèle" reference (stacked "every day / week / month" headers with small picture
tiles under them) in Maé's branding (dark-brown Anton blocks, Instagram-gradient tiles, white Poppins labels).

PY build.py    writes index.html
"""
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
BLOCK = '#573307'
ROWS = [('PAR JOUR', 240), ('PAR SEMAINE', 462), ('PAR MOIS', 684)]     # header block, top y
TILE = 92

# when she says "jour", "semaine", "mois" in each of the three rounds (round 3 from the silences, whisper skipped it)
ROUNDS = [(0.00, 1.54, 2.66, 3.45), (3.50, 4.90, 6.04, 7.20), (7.33, 8.49, 9.64, None)]
# items per round: (day x3, week x2, month x2) as (icon, label)
ITEMS = [
    [[('story', 'Poster une story'), ('comment', 'Répondre aux coms'), ('dm', 'Engager en DM')],
     [('reel', 'Publier 3 réels'), ('chart', 'Lire ses stats')],
     [('calendar', 'Planifier son mois'), ('profile', 'Revoir sa bio')]],
    [[('bulb', 'Noter ses idées'), ('camera', 'S’entraîner face cam'), ('heart', '15 min d’interactions')],
     [('batch', 'Filmer en batch'), ('pen', 'Écrire ses scripts')],
     [('target', 'Fixer ses objectifs'), ('test', 'Tester un format')]],
    [[('story', 'Story coulisses'), ('dm', 'Répondre aux DM'), ('search', 'Faire sa veille')],
     [('live', 'Un live ou une collab'), ('recycle', 'Recycler un contenu')],
     [('offer', 'Lancer une offre'), ('audit', 'Auditer son profil')]],
]

G = {   # white glyphs, 24x24
    'story': '<circle cx="12" cy="12" r="8.5" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="4 2.2"/><path d="M12 8v8M8 12h8" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'comment': '<path d="M20 11.5a8 8 0 1 1-3.2-6.4 8 8 0 0 1 3.2 6.4zM20 20l-2-4" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'dm': '<path d="M21 3L3 10l7 3 3 7zM10 13L21 3" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>',
    'reel': '<rect x="3.5" y="3.5" width="17" height="17" rx="4.5" fill="none" stroke="#fff" stroke-width="2"/><path d="M3.5 8.5h17M9 3.5l2.5 5M14.5 3.5l2.5 5" stroke="#fff" stroke-width="2"/><path d="M10 11.5v6l5-3z" fill="#fff"/>',
    'chart': '<path d="M5 20V12M10 20V6M15 20v-9M20 20V9" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>',
    'calendar': '<rect x="3.5" y="5" width="17" height="15" rx="3" fill="none" stroke="#fff" stroke-width="2"/><path d="M3.5 10h17M8 3v4M16 3v4" stroke="#fff" stroke-width="2" stroke-linecap="round"/><path d="M8 14.5l2.5 2.5 5-5" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'profile': '<circle cx="12" cy="9" r="4" fill="none" stroke="#fff" stroke-width="2"/><path d="M4.5 20c1.2-3.6 4-5.2 7.5-5.2s6.3 1.6 7.5 5.2" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'bulb': '<path d="M12 3a6 6 0 0 0-3.6 10.8c.8.6 1.1 1.3 1.1 2.2h5c0-.9.3-1.6 1.1-2.2A6 6 0 0 0 12 3z" fill="none" stroke="#fff" stroke-width="2"/><path d="M9.5 19.5h5M10.5 22h3" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'camera': '<rect x="3" y="7" width="13" height="11" rx="3" fill="none" stroke="#fff" stroke-width="2"/><path d="M16 11l5-3v9l-5-3z" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>',
    'heart': '<path d="M12 21s-7.5-4.6-9.5-9.2C1 8.4 3.2 5 6.6 5c2.1 0 3.4 1.2 4.4 2.5C12 6.2 13.3 5 15.4 5 18.8 5 21 8.4 19.5 11.8 17.5 16.4 12 21 12 21z" fill="#fff"/>',
    'batch': '<rect x="3" y="6" width="11" height="13" rx="2" fill="none" stroke="#fff" stroke-width="2"/><path d="M17 8v11a2 2 0 0 1-2 2H7M20.5 10v10" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'pen': '<path d="M4 20l1-4L16 5l3 3L8 19z" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/><path d="M14 7l3 3" stroke="#fff" stroke-width="2"/>',
    'target': '<circle cx="12" cy="12" r="8.5" fill="none" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="4.5" fill="none" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="1.6" fill="#fff"/>',
    'test': '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M15.5 15.5L21 21" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
    'live': '<circle cx="12" cy="12" r="3" fill="#fff"/><path d="M7 7a7 7 0 0 0 0 10M17 7a7 7 0 0 1 0 10M4.2 4.2a11 11 0 0 0 0 15.6M19.8 4.2a11 11 0 0 1 0 15.6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'recycle': '<path d="M5 11V9a3 3 0 0 1 3-3h11M16 3l3 3-3 3M19 13v2a3 3 0 0 1-3 3H5M8 21l-3-3 3-3" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    'offer': '<circle cx="12" cy="12" r="9" fill="none" stroke="#fff" stroke-width="2"/><path d="M14.8 9.2c-.6-.8-1.6-1.2-2.8-1.2-1.7 0-2.8.9-2.8 2 0 2.8 5.6 1.4 5.6 4.2 0 1.1-1.2 2-2.8 2-1.3 0-2.4-.5-3-1.4M12 6.5v11" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    'audit': '<rect x="5" y="3.5" width="14" height="17" rx="2.5" fill="none" stroke="#fff" stroke-width="2"/><path d="M8.5 9h7M8.5 13h7M8.5 17h4" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
}


def tile_row(rid, items, y, a, b):
    """a row of Instagram-gradient tiles with their labels, popping in one after the other"""
    html, tw = [], []
    n = len(items)
    gap = 300
    x0 = 540 - (n - 1) * gap / 2
    for i, (ic, lab) in enumerate(items):
        tid = f'{rid}i{i}'
        html.append(f'<div id="{tid}" class="it" style="left:{x0 + i * gap - 150:.0f}px;top:{y}px"><div class="tl">'
                    f'<svg viewBox="0 0 24 24" width="{TILE * .56:.0f}" height="{TILE * .56:.0f}">{G[ic]}</svg></div><div class="lb">{lab}</div></div>')
        t = a + .12 + i * .14
        tw += [f"gsap.set('#{tid}',{{autoAlpha:0}});",
               f"tl.fromTo('#{tid}',{{autoAlpha:0,scale:.4,y:20}},{{autoAlpha:1,scale:1,y:0,duration:.28,ease:'back.out(1.8)',immediateRender:false}},{t:.3f});"]
        if b is not None:
            tw += [f"tl.to('#{tid}',{{autoAlpha:0,scale:.7,duration:.12}},{b - .12:.3f});", f"tl.set('#{tid}',{{autoAlpha:0}},{b:.3f});"]
    return html, tw


def board():
    html, tw = [], []
    firsts = ROUNDS[0][:3]
    for (title, y), t in zip(ROWS, firsts):      # headers land on their first mention and stay
        hid = f'h{y}'
        html.append(f'<div class="hrow" style="top:{y}px"><span id="{hid}" class="hb">{title}</span></div>')
        tw += [f"gsap.set('#{hid}',{{autoAlpha:0}});",
               f"tl.fromTo('#{hid}',{{autoAlpha:0,scale:.5}},{{autoAlpha:1,scale:1,duration:.26,ease:'back.out(2)',immediateRender:{'true' if t == 0 else 'false'}}},{t:.3f});"]
    for r, (tj, ts, tm, end) in enumerate(ROUNDS):
        end = end if end is not None else None
        for k, (t, (_, y)) in enumerate(zip((tj, ts, tm), ROWS)):
            h, w = tile_row(f'r{r}k{k}', ITEMS[r][k], y + 74, t, end)
            html += h
            tw += w
        if r:                                    # each new round: the headers pulse
            for (_, y), t in zip(ROWS, (tj, ts, tm)):
                tw.append(f"tl.fromTo('#h{y}',{{scale:1.15}},{{scale:1,duration:.22,ease:'power2.out',immediateRender:false}},{t:.3f});")
    return html, tw


def sfx_list():
    out = []
    for r, (tj, ts, tm, _e) in enumerate(ROUNDS):
        for k, t in enumerate((tj, ts, tm)):
            out.append(('click-soft', t, .35))
            for i in range(len(ITEMS[r][k])):
                out.append(('pop', t + .12 + i * .14, .18))
    return out


SFX_LEN = {'pop': .72, 'click-soft': .36}


def audio():
    out, lanes = [], []
    for k, (name, t, vol) in enumerate(sorted(sfx_list(), key=lambda x: x[1])):
        d = min(SFX_LEN[name], DUR - t)
        lane = next((i for i, end in enumerate(lanes) if end <= t), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = t + d
        out.append(f'<audio id="sfx{k}" src="assets/sfx/{name}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                   f'data-track-index="{10 + lane}" data-volume="{vol:.3f}"></audio>')
    return out


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#shade{{position:absolute;left:0;right:0;top:0;height:900px;z-index:1;background:linear-gradient(180deg,rgba(40,20,40,.22),rgba(40,20,40,0))}}
.hrow{{position:absolute;left:0;right:0;z-index:12;text-align:center}}
.hb{{display:inline-block;font:400 54px/1 Anton;letter-spacing:.02em;color:#fff;background:{BLOCK};padding:7px 24px 5px;box-shadow:0 10px 24px rgba(0,0,0,.28)}}
.it{{position:absolute;z-index:11;width:300px;text-align:center}}
.tl{{width:{TILE}px;height:{TILE}px;margin:0 auto;border-radius:27px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(225deg,#4F5BD5 0%,#962FBF 28%,#D62976 55%,#FA7E1E 80%,#FEDA75 100%);box-shadow:0 12px 26px rgba(60,20,60,.35)}}
.lb{{margin-top:8px;font:700 25px/1.1 Poppins;color:#fff;text-shadow:0 0 14px rgba(0,0,0,.55),0 2px 6px rgba(0,0,0,.5);white-space:nowrap}}
'''


def build():
    h, tw = board()
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
{nl.join(audio())}
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
  <div id="shade"></div>
{nl.join(h)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(tw)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print(f'wrote index.html {DUR:.3f}s')
