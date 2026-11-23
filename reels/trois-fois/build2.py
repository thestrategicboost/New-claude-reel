#!/usr/bin/env python3
"""« Une fois par jour, une fois par semaine, une fois par mois » — new graphics (v2, her ask): a 3-line planner in her
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


def build():
    H, T = [], []
    for f, (lab, y) in ROWS.items():
        H.append(f'<div id="r{f}" class="row" style="top:{y}px"><div class="lab"><small>UNE FOIS</small><b>{lab}</b><i id="g{f}"></i></div>'
                 f'<div class="pill"><span id="ph{f}" class="ph">…</span><div class="dots">'
                 + ''.join(f'<i id="d{f}{n}"></i>' for n in range(3)) + '</div></div></div>')
        T += [f"gsap.set('#r{f}',{{autoAlpha:0}});", f"gsap.set('#g{f}',{{scaleY:0}});"]
    T += [f"tl.fromTo('#r{f}',{{autoAlpha:0,x:-40}},{{autoAlpha:1,x:0,duration:.25,ease:'power3.out',immediateRender:false}},{.0 + .06 * i:.3f});"
          for i, f in enumerate('jsm')]
    count = {'j': 0, 's': 0, 'm': 0}
    seen = set()
    for k, (t, f, kind, label) in enumerate(MOMENTS):
        nxt = MOMENTS[k + 1][0] if k + 1 < len(MOMENTS) else DUR
        H.append(f'<div id="h{k}" class="hab" style="top:{ROWS[f][1]}px"><span class="ic"><svg viewBox="0 0 24 24" width="40" height="40" fill="none" '
                 f'stroke="#fff" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">{ICON[kind]}</svg></span><b>{label}</b></div>')
        T.append(f"gsap.set('#h{k}',{{autoAlpha:0}});")
        T.append(f"tl.fromTo('#h{k}',{{autoAlpha:0,scale:.7,x:30}},{{autoAlpha:1,scale:1,x:0,duration:.24,ease:'back.out(2)',immediateRender:false}},{t + .02:.3f});")
        if f not in seen:
            T.append(f"tl.set('#ph{f}',{{autoAlpha:0}},{t + .02:.3f});")
            seen.add(f)
        # hide the previous habit of this line when the next one of the same line lands
        later = [kk for kk in range(k + 1, len(MOMENTS)) if MOMENTS[kk][1] == f]
        if later:
            tt = MOMENTS[later[0]][0]
            T.append(f"tl.to('#h{k}',{{autoAlpha:0,scale:.9,duration:.12}},{tt - .1:.3f});")
        # this line lights up, the others soften
        for g in 'jsm':
            T.append(f"tl.to('#r{g}',{{opacity:{1 if g == f else .5},duration:.15}},{t:.3f});")
            T.append(f"tl.to('#h{kk}',{{opacity:{1 if g == f else .5},duration:.15}},{t:.3f});" if False else '')
        T.append(f"tl.fromTo('#g{f}',{{scaleY:0}},{{scaleY:1,duration:.2}},{t:.3f});")
        T.append(f"tl.to('#g{f}',{{scaleY:0,duration:.2}},{nxt - .05:.3f});")
        T.append(f"tl.fromTo('#d{f}{count[f]}',{{scale:.4,backgroundColor:'#E8DFD5'}},{{scale:1,backgroundColor:'{GOLD}',duration:.25,ease:'back.out(3)',immediateRender:false}},{t + .1:.3f});")
        count[f] += 1
    # soften the habits of inactive lines too
    for k, (t, f, kind, label) in enumerate(MOMENTS):
        for kk, (t2, f2, _, _) in enumerate(MOMENTS):
            if t2 > t:
                T.append(f"tl.to('#h{k}',{{opacity:{1 if f2 == f else .5},duration:.15}},{t2:.3f});")
    nl = '\n'
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" /><script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}} .full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.row{{position:absolute;left:110px;width:860px;height:100px;z-index:20;filter:drop-shadow(0 10px 18px rgba(0,0,0,.18))}}
.lab{{position:absolute;left:0;top:0;width:290px;height:100px;background:{DARK};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.lab small{{font:600 20px/1 Poppins;letter-spacing:.18em;opacity:.85;margin-bottom:4px}}
.lab b{{font:400 46px/1 Anton;letter-spacing:.04em}}
.lab i{{position:absolute;left:-14px;top:10px;bottom:10px;width:7px;border-radius:4px;background:#fff;transform-origin:50% 50%}}
.pill{{position:absolute;left:304px;top:9px;width:556px;height:82px;border-radius:41px;background:#fff;display:flex;align-items:center;padding:0 24px 0 100px}}
.ph{{flex:1;font:italic 800 36px/1 Poppins;color:#C9BBAE}}
.dots{{position:absolute;right:24px;top:50%;transform:translateY(-50%);display:flex;gap:8px}}
.dots i{{width:13px;height:13px;border-radius:50%;background:#E8DFD5}}
.hab{{position:absolute;left:422px;height:100px;z-index:21;display:flex;align-items:center;gap:16px;transform-origin:0 50%}}
.hab .ic{{width:66px;height:66px;border-radius:50%;background:{DARK};display:flex;align-items:center;justify-content:center;margin-left:-4px}}
.hab b{{font:italic 800 37px/1 Poppins;letter-spacing:-.04em;color:{DARK};white-space:nowrap}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video>
{nl.join(H)}
</div>
<script>const tl = gsap.timeline({{ paused: true }});
{nl.join(x for x in T if x)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;</script></body></html>
'''


if __name__ == '__main__':
    open('index.html', 'w', encoding='utf-8').write(build())
    print(f'wrote index.html {DUR:.2f}s', [round(m[0], 2) for m in MOMENTS])
