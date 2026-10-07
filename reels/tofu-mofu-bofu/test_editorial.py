#!/usr/bin/env python3
"""15 s test of the "editorial" captions (Maé's reference: save_this... .MP4), on cut 4.20-19.40.

Words pop in one by one and stack into small 1-3 line blocks that move around her (left / right / centre, never
on the face): a clean white sans for most words, the key word in a big cream serif italic, and the odd heavy
capitals word. No stars, no brackets (Maé does not want them).

PY test_editorial.py   writes test_editorial.html (render with: HF render -c test_editorial.html ...)
"""
T0, DUR = 4.20, 15.20
ZOOMS = [(9.267, 10.033)]
CREAM = '#F2E2C4'

# blocks: (start, end, anchor, top, [line, ...]); line = [(t, text), ...] + style ('s' sans, 'i' serif italic, 'C' caps)
BLOCKS = [
    (4.30, 5.45, 'L', 1110, [('s', [(4.38, 'premièrement,')]), ('s', [(4.76, 'dans'), (4.82, 'ta')]), ('i', [(5.06, 'stratégie')])]),
    (5.45, 7.05, 'R', 1110, [('s', [(5.52, 'tu'), (5.54, 'dois'), (5.68, 'créer')]), ('s', [(5.92, 'du'), (6.08, 'contenu')]),
                             ('C', [(6.56, 'TOFU')])]),
    (7.05, 8.05, 'C', 1180, [('s', [(7.10, 'le')]), ('i', [(7.26, 'top'), (7.46, 'of'), (7.62, 'funnel')])]),
    (8.05, 9.05, 'L', 1110, [('s', [(8.10, 'ça,'), (8.30, 'c’est'), (8.36, 'du')]), ('s', [(8.52, 'contenu')]), ('i', [(8.74, 'large')])]),
    (9.05, 10.05, 'R', 1230, [('s', [(9.00, 'qui'), (9.00, 'va'), (9.10, 'toucher')]), ('i', [(9.40, 'beaucoup')]),
                              ('s', [(9.68, 'de'), (9.84, 'monde')])]),
    (10.05, 11.85, 'L', 1110, [('s', [(10.10, 'du'), (10.16, 'coup'), (10.32, 'tu'), (10.34, 'vas')]),
                               ('s', [(10.50, 'pouvoir'), (10.78, 'toucher')]), ('s', [(11.08, 'beaucoup'), (11.34, 'plus')]),
                               ('i', [(11.52, 'de'), (11.70, 'personnes')])]),
    (11.85, 13.00, 'C', 1200, [('s', [(11.88, 'et'), (12.00, 'avoir'), (12.20, 'plus'), (12.42, 'de')]), ('i', [(12.60, 'visibilité')])]),
    (13.00, 14.40, 'R', 1110, [('s', [(13.08, 'les'), (13.16, 'types'), (13.32, 'de')]), ('s', [(13.44, 'contenus')]),
                               ('C', [(13.64, 'TOFU')]), ('s', [(13.94, 'qui'), (14.16, 'marchent')])]),
    (14.40, 15.30, 'L', 1150, [('s', [(14.48, 'c’est'), (14.54, 'les'), (14.68, 'vidéos'), (14.80, 'de')]), ('i', [(14.98, 'classement')])]),
    (15.30, 16.10, 'R', 1150, [('s', [(15.36, 'vidéos'), (15.50, 'de')]), ('i', [(15.66, 'notation')])]),
    (16.10, 17.15, 'L', 1150, [('s', [(16.18, 'vidéos'), (16.48, 'de'), (16.78, 'type')]), ('i', [(17.00, 'liste')])]),
    (17.15, 17.95, 'C', 1180, [('s', [(17.22, 'vidéos')]), ('i', [(17.54, 'storytelling')])]),
    (17.95, 19.40, 'R', 1110, [('s', [(18.02, 'après,'), (18.48, 'on'), (18.52, 'a'), (18.64, 'le')]), ('s', [(18.80, 'contenu')]),
                               ('C', [(19.16, 'MOFU')])]),
]


def L(t):
    """cut time -> test time"""
    return t - T0


def blocks():
    html, tw = [], []
    for b, (a, e, anchor, top, lines) in enumerate(BLOCKS):
        pos = {'L': 'left:70px;text-align:left', 'R': 'right:70px;text-align:right', 'C': 'left:0;right:0;text-align:center'}[anchor]
        rows = []
        for li, (style, words) in enumerate(lines):
            spans = ' '.join(f'<span id="b{b}l{li}w{k}" class="w">{txt}</span>' for k, (_, txt) in enumerate(words))
            n = len(' '.join(txt for _, txt in words))
            fit = f' style="font-size:{min(168, round(940 / (0.40 * n)))}px"' if style == 'i' else ''   # long italic words shrink to fit
            rows.append(f'<div class="ln {style}"{fit}>{spans}</div>')
            for k, (t, _) in enumerate(words):
                wid = f'#b{b}l{li}w{k}'
                tw.append(f"gsap.set('{wid}',{{autoAlpha:0}});")
                y = 26 if style == 'i' else 14
                tw.append(f"tl.fromTo('{wid}',{{autoAlpha:0,y:{y},filter:'blur(6px)'}},{{autoAlpha:1,y:0,filter:'blur(0px)',"
                          f"duration:.18,ease:'power2.out',immediateRender:false}},{max(L(a), L(t) - .03):.3f});")
        html.append(f'<div id="blk{b}" class="blk" style="{pos};top:{top}px">{"".join(rows)}</div>')
        if e < T0 + DUR - .01:
            tw.append(f"tl.to('#blk{b}',{{autoAlpha:0,duration:.12}},{L(e) - .12:.3f});")
            tw.append(f"tl.set('#blk{b}',{{autoAlpha:0}},{L(e):.3f});")
    return html, tw


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#stage{{position:absolute;inset:0;transform-origin:50% 36%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.blk{{position:absolute;z-index:10;text-shadow:0 0 28px rgba(0,0,0,.55),0 2px 8px rgba(0,0,0,.5),0 0 3px rgba(0,0,0,.35)}}
.ln{{white-space:nowrap}}
.w{{display:inline-block}}
.s{{font:600 70px/1 Inter;letter-spacing:-.045em;color:#fff}}
.i{{font:italic 400 168px/.78 'Instrument Serif';color:{CREAM};letter-spacing:-.01em;margin:-6px 0 -2px}}
.C{{font:900 128px/.9 'Inter Tight';color:#fff;letter-spacing:-.04em;margin-top:2px}}
'''


def build():
    b_html, b_tw = blocks()
    tw = b_tw + [f"tl.set('#stage',{{scale:1.3}},{L(a):.3f});tl.set('#stage',{{scale:1}},{L(b):.3f});" for a, b in ZOOMS]
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
  <audio id="bga" src="assets/aroll.mp4" data-start="0" data-media-start="{T0:.3f}" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
  <div id="stage">
    <video id="bgv" class="full" src="assets/aroll_graded.mp4" muted playsinline data-start="0" data-media-start="{T0:.3f}" data-duration="{DUR:.3f}" data-track-index="0"></video>
  </div>
{nl.join(b_html)}
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


with open('test-editorial/index.html', 'w', encoding='utf-8', newline='\n') as _f:
    _f.write(build())
print('wrote test-editorial/index.html')
