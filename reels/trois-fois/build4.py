#!/usr/bin/env python3
"""v3b (her ask): THREE tear-off calendars side by side (JOUR left, SEMAINE middle, MOIS right — she points at each),
each starts on a cover page; when she names a frequency, that calendar pops and its page is torn off to show the habit.
(older v3 doc:) v3 (added version, not a replacement — her ask): a tear-off CALENDAR (éphéméride) in brown and white. A brown binder
strip with rings; under it one page per moment (brown band « UNE FOIS / PAR JOUR… » in Anton, white body with a brown icon
badge and the habit in Poppins italic brown, « 1/3 » counter). On each new frequency the page is torn off (swings down
around its top edge and drops) and reveals the next one. No sound effects.
(v2 doc:) « Une fois par jour, une fois par semaine, une fois par mois » — new graphics (v2, her ask): a 3-line planner in her
charter in the empty wall above her head (below the « Reels d'essai » band). Each line = a brown block (« UNE FOIS » small
Poppins + « PAR JOUR / SEMAINE / MOIS » in Anton, white) + a white pill (Poppins italic 800, her brown) with a brown icon
badge. Every time she says a frequency its line lights up (the others soften), the habit pops into the pill and a gold
dot fills (round 1/2/3). No sound effects (her voice only). Lilac look + retouch (cut.py).

PY build2.py      writes index.html
"""
import subprocess

DUR = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'assets/aroll.mp4'],
                           capture_output=True, text=True).stdout)
DARK, GOLD = '#523301', '#523301'      # no gold at all (her ask: « pas des cartes gold »)
SPEED = 1.12
CUTS_1X = [(3.20, 3.66), (6.62, 7.25)]
MOMENTS_1X = [(0.00, 'j', 'story', 'Poster une story'), (1.54, 's', 'script', 'Écrire tes scripts'), (2.66, 'm', 'month', 'Planifier ton mois'),
              (3.50, 'j', 'dm', 'Répondre à tes DM'), (4.90, 's', 'stats', 'Analyser tes stats'), (6.04, 'm', 'goal', 'Fixer tes objectifs'),
              (7.33, 'j', 'ideas', 'Noter tes idées'), (8.49, 's', 'batch', 'Filmer en batch'), (9.64, 'm', 'audit', 'Auditer ton profil')]


def cut_time(t):
    for a, b in CUTS_1X:
        if t >= b:
            t -= b - a
        elif t > a:
            t = a
    return t


MOMENTS = [(cut_time(t) / SPEED, f, k, l) for t, f, k, l in MOMENTS_1X]
ROWS = {'j': ('PAR JOUR', 345), 's': ('PAR SEMAINE', 462), 'm': ('PAR MOIS', 579)}
ICON = {
    'story': '<circle cx="12" cy="12" r="8.5" stroke-dasharray="4 2.2"/><path d="M12 8.5v7M8.5 12h7"/>',
    'script': '<path d="M4 20l1-4L16 5l3 3L8 19z"/>',
    'month': '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    'dm': '<path d="M4 5h16v11H9l-5 4z"/>',
    'stats': '<path d="M5 19V12M10 19V8M15 19v-5M20 19V5"/>',
    'goal': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".8"/>',
    'ideas': '<path d="M12 3a6 6 0 0 0-3.6 10.8c.8.6 1.1 1.3 1.1 2.2h5c0-.9.3-1.6 1.1-2.2A6 6 0 0 0 12 3zM9.5 19.5h5"/>',
    'batch': '<rect x="3" y="7" width="13" height="10" rx="2"/><path d="M16 11l5-3v8l-5-3z"/>',
    'audit': '<circle cx="10" cy="8" r="3.5"/><path d="M3.5 19c0-3.3 2.9-5.5 6.5-5.5M14.5 17l2 2 4-4.5"/>',
}


COLX = {'j': 118, 's': 405, 'm': 692}
PW = 270


def build():
    H, T = [], []
    count = {'j': 0, 's': 0, 'm': 0}
    pages = {'j': [], 's': [], 'm': []}
    for k, (t, f, kind, label) in enumerate(MOMENTS):
        pages[f].append((k, t, kind, label))
    for f, x in COLX.items():
        lab = ROWS[f][0]
        H.append(f'<div id="cal{f}" class="cal" style="left:{x}px">')
        H.append('<div class="bind">' + ''.join('<i></i>' for _ in range(4)) + '</div>')
        stack = [('cover', None, None, None)] + pages[f]
        for i, it in enumerate(stack):
            pid = f'p{f}{i}'
            if it[0] == 'cover':
                inner = '<div class="pb cover"><span>…</span></div>'
            else:
                _, _, kind, label = it
                inner = (f'<div class="pb"><span class="ic"><svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#fff" stroke-width="2" '
                         f'stroke-linecap="round" stroke-linejoin="round">{ICON[kind]}</svg></span><b>{label}</b><em>{i}/3</em></div>')
            H.append(f'<div id="{pid}" class="pg" style="z-index:{40 - i}"><div class="band"><small>UNE FOIS</small><b>{lab}</b></div>{inner}</div>')
        H.append('</div>')
        T += [f"gsap.set('#cal{f}',{{autoAlpha:0}});"]
    T += [f"tl.fromTo('#cal{f}',{{autoAlpha:0,y:-30}},{{autoAlpha:1,y:0,duration:.25,ease:'back.out(1.6)',immediateRender:false}},{.05 * i:.3f});"
          for i, f in enumerate('jsm')]
    for f in 'jsm':
        for i, (k, t, kind, label) in enumerate(pages[f]):
            prev = f'#p{f}{i}'           # page on top before this moment (cover for i=0)
            tt = max(t - .06, 0.02 if i else 0.0)
            if k == 0:
                tt = 0.12                # first moment at 0 s: tear right after the calendars land
            T += [f"tl.to('{prev}',{{rotationX:80,y:240,rotation:{-6 if i % 2 else 6},duration:.32,ease:'power2.in'}},{tt:.3f});",
                  f"tl.to('{prev}',{{autoAlpha:0,duration:.1}},{tt + .24:.3f});",
                  f"tl.fromTo('#cal{f}',{{scale:1}},{{scale:1.08,duration:.14,yoyo:true,repeat:1,immediateRender:false}},{tt:.3f});"]
    # the calendar she is talking about stays full, the two others soften
    for k, (t, f, kind, label) in enumerate(MOMENTS):
        for g in 'jsm':
            T.append(f"tl.to('#cal{g}',{{opacity:{1 if g == f else .6},duration:.15}},{max(t - .06, 0):.3f});")
    nl = '\n'
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.cal{{position:absolute;top:345px;width:{PW}px;height:330px;z-index:20;perspective:1000px;transform-origin:50% 0}}
.bind{{position:absolute;left:-8px;right:-8px;top:0;height:28px;z-index:60;background:{DARK};border-radius:9px;display:flex;justify-content:space-around;align-items:center;
  box-shadow:0 6px 14px rgba(0,0,0,.2)}}
.bind i{{width:12px;height:38px;border-radius:6px;background:#fff;border:3px solid {DARK};margin-top:18px}}
.pg{{position:absolute;left:0;width:{PW}px;top:20px;height:290px;background:#fff;border-radius:0 0 18px 18px;overflow:hidden;transform-origin:50% 0;
  box-shadow:0 12px 26px rgba(0,0,0,.2)}}
.band{{height:92px;background:{DARK};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-top:12px}}
.band small{{font:600 16px/1 Poppins;letter-spacing:.2em;opacity:.85;margin-bottom:5px}}
.band b{{font:400 40px/1 Anton;letter-spacing:.04em}}
.pb{{position:relative;height:198px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:0 16px;text-align:center}}
.pb .ic{{flex:none;width:72px;height:72px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center}}
.pb b{{font:italic 800 32px/1.05 Poppins;letter-spacing:-.04em;color:{DARK}}}
.pb em{{position:absolute;right:14px;bottom:10px;font:700 18px/1 Poppins;font-style:normal;color:#B9A897}}
.pb.cover span{{font:italic 800 60px/1 Poppins;color:#D8CCC0}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(H)}
</div>
<script>const tl = gsap.timeline({{ paused: true }});
{nl.join(T)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;</script></body></html>
'''


if __name__ == '__main__':
    open('index.html', 'w', encoding='utf-8').write(build())
    print('wrote index.html (3 calendriers)')
