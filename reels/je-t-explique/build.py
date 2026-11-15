#!/usr/bin/env python3
"""« Au cas où ta mère ne t'aurait pas appris ça pour ton business… » — her reel (src/ref.mp4, 8.63 s) rebuilt on other B-rolls:
same texts, same timings (measured on her reel), same sound. 0-2.87 the hook in white boxes (Anton, her dark brown), 2.87-4.6 the
white pill "pour publier, tu dois suivre une stratégie en 3 étapes :", then three black notes cards TOFU (4.6) / MOFU (6.0) /
BOFU (7.3).

PY build.py <n>      writes index.html for assets/v<n>.mp4
"""
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
DUR = 8.634
DARK = '#573307'
CARDS = [
    (4.60, 6.00, 'TOFU — Top of Funnel', 'La personne ne te connaît pas encore.', 'attirer son attention et te faire découvrir.',
     ['Conseils simples', 'Erreurs fréquentes', 'Contenus éducatifs', 'Contenus partageables', 'Sujets qui répondent à un problème courant'],
     'TOFU = VISIBILITÉ → « Je te découvre. »'),
    (6.00, 7.30, 'MOFU — Middle of Funnel', 'La personne te connaît, mais elle n’est pas encore prête à acheter.',
     'créer de la confiance et démontrer ton expertise.',
     ['Études de cas', 'Démonstrations', 'Tutoriels approfondis', 'Explication de ta méthode', 'Coulisses de ton travail', 'Témoignages'],
     'MOFU = CONFIANCE → « Je commence à croire que tu peux m’aider. »'),
    (7.30, DUR, 'BOFU — Bottom of Funnel', 'La personne te connaît, te fait confiance et envisage d’acheter.', 'l’aider à prendre sa décision.',
     ['Présentation de ton offre', 'Résultats clients', 'Réponses aux objections', 'FAQ', 'Comparaison avant/après', 'Appel à l’action vers ton offre'],
     'BOFU = CONVERSION → « Je suis prête à acheter. »'),
]


def cuts(sel, a, b):
    t = [f"gsap.set('{sel}',{{autoAlpha:{1 if a == 0 else 0}}});"]
    if a > 0:
        t.append(f"tl.set('{sel}',{{autoAlpha:1}},{a:.3f});")
    if b < DUR - .01:
        t.append(f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});")
    return t


def build():
    H, T = [], []
    H.append('<div id="hook" class="hook"><span>AU CAS OÙ TA MÈRE</span><br/><span>NE T\'AURAIT PAS APPRIS ÇA</span><br/><span>POUR TON BUSINESS…</span></div>')
    T += cuts('#hook', 0, 2.87)
    H.append('<div id="p" class="pw"><span>pour publier, tu dois suivre</span><br/><span>une stratégie en 3 étapes :</span></div>')
    T += cuts('#p', 2.87, 4.60)
    for k, (a, b, head, who, goal, ex, eq) in enumerate(CARDS):
        lis = ''.join(f'<li>{e}</li>' for e in ex)
        H.append(f'<div id="c{k}" class="card"><p class="b">{head}</p><p class="b">{who}</p><p>Ton objectif : <b>{goal}</b></p>'
                 f'<p>Exemples de contenus :</p><ul>{lis}</ul><p class="b">{eq}</p></div>')
        T += cuts(f'#c{k}', a, b)
    return f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.hook{{position:absolute;left:0;right:0;top:862px;z-index:20;text-align:center;line-height:0}}
.hook span{{display:inline-block;background:#fff;color:{DARK};font:400 66px/1.4 Anton;letter-spacing:.05em;padding:0 22px;margin-top:-1px}}
.pw{{position:absolute;left:0;right:0;top:922px;z-index:20;text-align:center;line-height:0}}
.pw span{{display:inline-block;background:#fff;color:#2A1A10;font:italic 800 46px/1.5 Poppins;letter-spacing:-.04em;padding:0 28px;border-radius:40px;margin:-6px 0}}
.card{{position:absolute;left:210px;width:660px;top:930px;z-index:20;background:#000;color:#fff;padding:26px 28px 30px;font:500 27px/1.45 Inter}}
.card p{{margin-bottom:24px}} .card p.b, .card b{{font-weight:600}}
.card p.b:first-child{{margin-bottom:12px}}
.card ul{{margin:-12px 0 24px 46px}} .card li{{margin:2px 0}}
.card p:last-child{{margin-bottom:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <audio id="amb" src="assets/ref_audio.m4a" data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
  <video id="bgv" class="full" src="assets/v{N}.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR}" data-track-index="0"></video>
{chr(10).join(H)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(T)}
tl.set({{}}, {{}}, {DUR});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''


if __name__ == '__main__':
    with open('index.html', 'w', encoding='utf-8', newline='\n') as _f:
        _f.write(build())
    print(f'wrote index.html (variante {N})')
