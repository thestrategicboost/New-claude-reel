#!/usr/bin/env python3
"""Reel "réels vs carrousels vs stories", edited after the "Reels get followers, carousels get engagement" inspiration:
a fixed row of the inspiration's three icons on top (Reels / carousel / Story, "vs" between them), the one she names
popping on the word itself, and under it one card per clause in her caption style (Poppins white, black shadow): a
small lead line that builds word by word, the key word landing huge on its spoken word, sometimes a small line under it. Lilac look, alternate punch-ins hide the jump cuts.

PY build.py    writes index.html
"""
import json
import re
import shutil
import subprocess

DUR = float(subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                            'csv=p=0', 'assets/aroll.mp4'], capture_output=True, text=True).stdout.strip())
SEGS = json.load(open('work/segs.json'))
TOP = 250


def ct(t):
    """raw time -> edit time"""
    out = 0.0
    for a, b in SEGS:
        if t >= b:
            out += b - a
        else:
            return out + max(0.0, t - a)
    return out


# (raw start of the card, active format, lead line, big word, raw time the big word is said, small line, its raw time)
CARDS = [
    (112.12, 'reels', 'les réels sont montrés à', 'TES ABONNÉS', 113.28, '', 0),
    (114.04, 'reels', 'mais surtout à tes', 'NON-ABONNÉS', 114.68, '', 0),
    (115.44, 'reels', "n'oublie pas l'option", "RÉEL D'ESSAI", 116.72, "c'est un banger", 117.54),
    (118.48, 'reels', 'pour pousser tes réels vers des', 'NON-ABONNÉS', 120.30, '', 0),
    (121.16, 'carrousel', 'les carrousels sont montrés à', 'TES ABONNÉS', 122.42, '+ quelques non-abonnés', 123.18),
    (124.14, 'story', 'et les stories uniquement à', 'TES ABONNÉS', 125.42, '', 0),
    (129.10, 'reels', 'les réels génèrent des', 'ABONNEMENTS', 130.30, '', 0),
    (131.08, 'carrousel', "les carrousels génèrent de l'", 'ENREGISTREMENT', 132.26, '', 0),
    (132.98, 'story', "et les stories de l'", 'ENGAGEMENT', 134.34, '', 0),
    (138.82, 'reels', "les réels te permettent d'être", 'VISIBLE', 140.34, '', 0),
    (141.12, 'carrousel', "les carrousels te permettent d'", 'ÉDUQUER', 142.18, '', 0),
    (143.08, 'story', 'et les stories te permettent de', 'VENDRE', 144.20, '', 0),
    (152.30, 'reels', 'pour les réels, publie', '4 À 7 FOIS', 153.12, 'par semaine', 153.74),
    (154.56, 'carrousel', 'pour les carrousels', '1 À 2 FOIS', 155.26, 'par semaine', 155.74),
    (156.18, 'carrousel', 'ou alors', 'PAS DU TOUT', 156.60, '', 0),
    (157.34, 'story', 'et les stories', '1 À 2 FOIS', 158.06, 'par jour', 158.44),
    (160.30, None, 'commente', 'CHIRAC', 160.84, 'pour avoir mon kit du créateur au complet', 161.10),
]

# the three icons of the inspiration, redrawn as vectors: Instagram's gradient Reels icon, the neon carousel, the
# white Story disc in its gradient ring
IGG = ('<defs><linearGradient id="gr" x1="0" y1="0" x2=".35" y2="1"><stop offset="0" stop-color="#C72A9C"/>'
       '<stop offset=".5" stop-color="#F0335C"/><stop offset="1" stop-color="#FA8F2C"/></linearGradient>'
       '<linearGradient id="gs" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FBB13C"/><stop offset=".45" stop-color="#F2365E"/>'
       '<stop offset="1" stop-color="#9B33C9"/></linearGradient></defs>')
ICONS = {
    'reels': '<svg viewBox="0 0 48 48">' + IGG + '<g fill="none" stroke="url(#gr)" stroke-width="3.8" stroke-linejoin="round" stroke-linecap="round">'
             '<rect x="4.5" y="4.5" width="39" height="39" rx="11"/><path d="M5 16h38M16.5 5l6 11M28.5 5l6 11"/></g>'
             '<path d="M19.5 22.5v13l11-6.5z" fill="#F0353B" stroke="#F0353B" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    'carrousel': '<svg viewBox="0 0 76 48"><g fill="none" stroke-linejoin="miter"><path id="cb" d="M24 6H16V42H24M16 10H9V38H16M52 6H60V42H52M60 10H67V38H60" stroke="#D4FF3A" stroke-width="4.4"/>'
                 '<path d="M24 6H16V42H24M16 10H9V38H16M52 6H60V42H52M60 10H67V38H60" stroke="#fff" stroke-width="1.6"/></g>'
                 '<rect x="25" y="3" width="26" height="42" fill="#fff"/></svg>',
    'story': '<svg viewBox="0 0 48 48">' + IGG + '<circle cx="24" cy="24" r="20.5" fill="none" stroke="url(#gs)" stroke-width="3.2"/>'
             '<circle cx="24" cy="24" r="18" fill="#fff"/></svg>',
}
NAMES = {'reels': 'RÉELS', 'carrousel': 'CARROUSEL', 'story': 'STORY'}


def scenes():
    H, T, S = [], [], []
    # format row: the one she names pops (as in the inspiration), its label at full white
    H.append('<div id="row" class="row">' + ''.join(
        ('<b class="vs">vs</b>' if j else '') + f'<div id="ic-{k}" class="ic"><div class="ig">{ICONS[k]}</div><span>{NAMES[k]}</span></div>'
        for j, k in enumerate(ICONS)) + '</div>')
    T += ["gsap.set('.ic',{scale:1});", "gsap.set('.ic span',{opacity:.6});"]
    raw = json.load(open('work/take3_words.json'))
    key = {'reels': 'réel', 'carrousel': 'carousel', 'story': 'stor'}
    last = None
    for i, (t, fmt, *_rest) in enumerate(CARDS):
        if fmt is None or fmt == last:
            continue
        hit = next((w['s'] for w in raw if w['s'] >= t - .05 and key[fmt] in w['w'].lower()), t)
        a = ct(hit)
        for k in ICONS:
            if k == fmt:      # one frame squeezed, then pops a bit bigger and settles
                T += [f"tl.set('#ic-{k}',{{scale:.86}},{a:.3f});",
                      f"tl.to('#ic-{k}',{{scale:1.3,duration:.08,ease:'power2.out'}},{a + .034:.3f});",
                      f"tl.to('#ic-{k}',{{scale:1.22,duration:.2,ease:'power1.out'}},{a + .12:.3f});",
                      f"tl.set('#ic-{k} span',{{opacity:1}},{a + .034:.3f});"]
                S.append(('pop', a, .38))
            elif k == last:
                T += [f"tl.to('#ic-{k}',{{scale:1,duration:.12,ease:'power2.out'}},{a:.3f});",
                      f"tl.set('#ic-{k} span',{{opacity:.6}},{a:.3f});"]
        last = fmt
    T += [f"tl.to('#row',{{autoAlpha:0,y:-30,duration:.25}},{ct(160.30) - .1:.3f});"]

    # captions: her usual one word at a time (Poppins white, black shadow, lowercase); the key words of each clause
    # land together, huge, and stay until the next clause; the words said after them show one at a time under them
    raw = []
    for w in json.load(open('work/take3_words.json')):
        t = w['w'].strip()
        if (t.startswith("'") or t.startswith('-')) and raw:
            raw[-1]['w'] += t
            raw[-1]['e'] = w['e']
        else:
            raw.append(dict(w, w=t))
    n = 0
    for i, (t, fmt, lead, big, tb, small, ts) in enumerate(CARDS):
        t_next = CARDS[i + 1][0] if i + 1 < len(CARDS) else 1e9
        ws = [w for w in raw if t - .05 <= w['s'] < t_next - .05]
        kb = next(k for k, w in enumerate(ws) if w['s'] >= tb - .05)
        nb = len(big.replace(',', '').replace('!', '').split())
        card_end = ct(t_next) - .02 if i + 1 < len(CARDS) else DUR + .1
        a_big = ct(ws[kb]['s'])
        if fmt is None:
            # the CTA as an Instagram comment bar above her head: it slides in on "commente", CHIRAC types itself on the
            # word, the send button is tapped, the bar pulses
            send = ('<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="2.6" '
                    'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
            H.append(f'<div id="cb" class="cb"><img class="cav" src="assets/avatar.png"/><div class="cw"><span id="cph" class="cph">Ajouter un commentaire…</span>'
                     f'<span id="cty" class="cty"></span><i id="ccr" class="ccr"></i></div><div id="csd" class="csd">{send}</div></div>')
            a_in = ct(t)
            T += ["gsap.set('#cb',{autoAlpha:0});",
                  f"tl.fromTo('#cb',{{autoAlpha:0,y:-50,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.8)',immediateRender:false}},{a_in:.3f});",
                  "gsap.set('#cty',{textContent:''});", "gsap.set('#cph',{display:'inline'});",
                  f"tl.set('#cty',{{textContent:''}},{a_in:.3f});", f"tl.set('#cph',{{display:'inline'}},{a_in:.3f});",
                  f"tl.set('#cph',{{display:'none'}},{a_big:.3f});"]
            T += [f"tl.set('#cty',{{textContent:{json.dumps(big[:q])}}},{a_big + (q - 1) * .07:.3f});" for q in range(1, len(big) + 1)]
            ts_ = a_big + len(big) * .07 + .15
            T += ["gsap.set('#ccr',{opacity:1});"] + [f"tl.set('#ccr',{{opacity:{q % 2}}},{a_in + .3 + q * .25:.3f});" for q in range(int((DUR - a_in) / .25))]
            T += [f"tl.to('#csd',{{scale:.78,duration:.07,yoyo:true,repeat:1}},{ts_:.3f});",
                  f"tl.to('#cb',{{boxShadow:'0 0 0 7px #573307, 0 16px 36px rgba(0,0,0,.3)',scale:1.05,duration:.18,yoyo:true,repeat:1}},{ts_ + .1:.3f});"]
            S += [('pop', a_in, .45), ('click', ts_, .6)]
            singles = [(w, False) for w in ws[:kb]] + [(w, False) for w in ws[kb + nb:]]
        else:
            a_big = card_end          # no big words here: every word is a one-word caption, the cards below carry the point
            singles = [(w, False) for w in ws]
        for k, (w, under) in enumerate(singles):
            txt = re.sub(r'[,.!?…]', '', w['w']).lower().replace('carousel', 'carrousel')
            if not txt:
                continue
            a = ct(w['s'])
            nxt = singles[k + 1][0]['s'] if k + 1 < len(singles) and singles[k + 1][1] == under else None
            end = ct(nxt) if nxt is not None and nxt - w['e'] < .5 else ct(w['e']) + .3
            end = min(end, a_big if w['s'] < ws[kb]['s'] else card_end, card_end)
            if end <= a:
                continue
            H.append(f'<div id="w{n}" class="cap{" un" if under else ""}">{txt}</div>')
            T += [f"gsap.set('#w{n}',{{autoAlpha:0}});", f"tl.set('#w{n}',{{autoAlpha:1}},{a:.3f});",
                  f"tl.fromTo('#w{n}',{{scale:.8}},{{scale:1,duration:{min(.12, end - a):.3f},ease:'back.out(2.5)',immediateRender:false}},{a:.3f});",
                  f"tl.set('#w{n}',{{autoAlpha:0}},{end:.3f});"]
            n += 1

    # under the captions, a small Instagram UI card per clause (as in the inspiration): who sees it, the trial-reel
    # switch, followers, saves, story replies, reach, carousel slides, money, the week planning
    def win(i0, i1):
        a = ct(CARDS[i0][0]) + .05
        b = ct(CARDS[i1 + 1][0]) - .03 if i1 + 1 < len(CARDS) else DUR
        return a, b

    def shw(sel, a, b):        # cards come in silently: only the actions on them make a sound
        return [f"gsap.set('{sel}',{{autoAlpha:0}});",
                f"tl.fromTo('{sel}',{{autoAlpha:0,y:40,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.25,ease:'back.out(1.8)',immediateRender:false}},{a:.3f});",
                f"tl.to('{sel}',{{autoAlpha:0,duration:.12}},{b - .12:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]

    def bars(k, title, rows):
        h = ''.join(f'<div class="br"><span>{lab}</span><div class="bt"><i id="bf{k}_{q}"></i></div></div>' for q, (lab, _, _) in enumerate(rows))
        return f'<div id="ui{k}" class="ui"><div class="ut">{title} <em>ⓘ</em></div>{h}</div>'

    def bar_tw(k, rows):
        out = []
        for q, (_, pct, t) in enumerate(rows):
            out += [f"gsap.set('#bf{k}_{q}',{{scaleX:0,transformOrigin:'0 50%'}});",
                    f"tl.to('#bf{k}_{q}',{{scaleX:{pct / 100:.2f},duration:.45,ease:'power2.out'}},{ct(t):.3f});"]
        return out

    def week(k, marks, label):
        days = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM', 'DIM']
        cells = ''.join(f'<span class="wd">{d}</span>' for d in days) + ''.join(
            f'<span class="wc"><i id="wm{k}_{q}" class="{"lt" if m == 2 else ""}">{"✓" if m else ""}</i></span>' for q, m in enumerate(marks))
        return f'<div id="ui{k}" class="ui wk"><div class="ut">{label}</div><div class="wg">{cells}</div></div>'

    # 0-1 réels: seen by followers, mostly by non-followers
    a, b = win(0, 1)
    rows = [('Abonnés', 30, 113.28), ('Non-abonnés', 92, 114.68)]
    H.append(bars(0, 'Qui a vu ton réel', rows)); T += shw('#ui0', a, b) + bar_tw(0, rows)
    # 2-3 the trial-reel switch
    a, b = win(2, 3)
    H.append('<div id="ui1" class="ui tg"><div><b>Réel d’essai</b><small>Partager d’abord avec des non-abonnés</small></div><i id="sw1" class="sw"><i id="kn1"></i></i></div>')
    T += shw('#ui1', a, b) + ["gsap.set('#kn1',{x:0});", f"tl.to('#sw1',{{backgroundColor:'#0095F6',duration:.15}},{ct(116.72):.3f});",
                               f"tl.to('#kn1',{{x:52,duration:.15,ease:'power2.out'}},{ct(116.72):.3f});"]
    S.append(('click', ct(116.72), .45))
    # 4 carrousels: followers + some non-followers
    a, b = win(4, 4)
    rows = [('Abonnés', 85, 122.42), ('Non-abonnés', 22, 123.30)]
    H.append(bars(2, 'Qui a vu ton carrousel', rows)); T += shw('#ui2', a, b) + bar_tw(2, rows)
    # 5 stories: followers only
    a, b = win(5, 5)
    rows = [('Abonnés', 100, 125.42), ('Non-abonnés', 0, 125.42)]
    H.append(bars(3, 'Qui a vu ta story', rows)); T += shw('#ui3', a, b) + bar_tw(3, rows)
    # 6 réels -> follows
    a, b = win(6, 6)
    H.append('<div id="ui4" class="ui fl"><i class="ico">👤＋</i><div><b>Abonnés en plus</b><small>grâce à ce réel</small></div><em id="ar4">↑</em></div>')
    T += shw('#ui4', a, b) + [f"tl.fromTo('#ar4',{{y:20,autoAlpha:0}},{{y:0,autoAlpha:1,duration:.3,ease:'back.out(2)',immediateRender:false}},{ct(130.30):.3f});"]
    S.append(('ding', ct(130.30), .45))          # a new follower: the notification ding
    # 7 carrousels -> saves
    a, b = win(7, 7)
    H.append('<div id="ui5" class="ui sv"><svg viewBox="0 0 24 24" width="74" height="74"><path id="bk5" d="M6 3h12v18l-6-5-6 5z" fill="none" stroke="#111" '
             'stroke-width="2" stroke-linejoin="round"/></svg><b>Enregistrer</b></div>')
    T += shw('#ui5', a, b) + [f"tl.set('#bk5',{{attr:{{fill:'#111'}}}},{ct(132.26):.3f});",
                               f"tl.fromTo('#ui5 svg',{{scale:1}},{{scale:1.25,duration:.1,yoyo:true,repeat:1,immediateRender:false}},{ct(132.26):.3f});"]
    S.append(('click', ct(132.26), .45))
    # 8 stories -> engagement: replies
    a, b = win(8, 8)
    H.append('<div id="ui6" class="ui rp"><span id="rp6a">trop bien ce conseil 😍</span><span id="rp6b">merci, je teste ! 🙏</span></div>')
    T += shw('#ui6', a, b) + ["gsap.set('#rp6a, #rp6b',{autoAlpha:0});",
                               f"tl.fromTo('#rp6a',{{autoAlpha:0,x:-30}},{{autoAlpha:1,x:0,duration:.2,immediateRender:false}},{ct(134.34):.3f});",
                               f"tl.fromTo('#rp6b',{{autoAlpha:0,x:30}},{{autoAlpha:1,x:0,duration:.2,immediateRender:false}},{ct(134.34) + .35:.3f});"]
    S += [('bloop', ct(134.34), .4), ('bloop', ct(134.34) + .35, .35)]   # each reply lands like a message
    # 9 réels -> visible: reach
    a, b = win(9, 9)
    H.append('<div id="ui7" class="ui rc"><span><small>Vues</small><b>↑</b></span><span><small>Comptes touchés</small><b>↑</b></span></div>')
    S.append(('whoosh-short', ct(140.34), .22))   # the reach arrows shoot up
    T += shw('#ui7', a, b) + [f"tl.fromTo('#ui7 b',{{y:16,autoAlpha:0}},{{y:0,autoAlpha:1,duration:.25,stagger:.12,ease:'back.out(2)',immediateRender:false}},{ct(140.34):.3f});"]
    # 10 carrousels -> educate: her guide pages as carousel slides
    a, b = win(10, 10)
    H.append('<div id="ui8" class="fan">' + ''.join(f'<img src="assets/gpages/p-0{p}.png"/>' for p in (1, 3, 5)) + '</div>')
    S.append(('whoosh-short', ct(142.18), .18))   # the slides fan out
    T += shw('#ui8', a, b) + [f"tl.fromTo('#ui8 img',{{rotation:0,x:0}},{{rotation:(i)=>[-12,0,12][i],x:(i)=>[-120,0,120][i],duration:.35,ease:'back.out(1.6)',immediateRender:false}},{ct(142.18):.3f});"]
    # 11-12 stories -> sell: money
    a, b = win(11, 11)
    H.append('<div id="ui9" class="mny">💰</div>')
    S.append(('kaching', ct(144.20), .45))        # money: the till
    T += shw('#ui9', ct(144.20), b) + [f"tl.to('#ui9',{{y:-18,duration:.18,yoyo:true,repeat:3,ease:'sine.inOut'}},{ct(144.30):.3f});"]
    # 13 réels 4-7 / week
    a, b = win(12, 12)
    H.append(week(10, [1, 0, 1, 2, 1, 2, 1], 'Réels · 4 à 7 / semaine')); T += shw('#ui10', a, b)
    T += [f"tl.fromTo('#ui10 .wc i',{{scale:0}},{{scale:1,duration:.15,stagger:.05,ease:'back.out(3)',immediateRender:false}},{ct(153.12):.3f});"]
    # 14-15 carrousels 1-2 / week, or not at all
    a, b = win(13, 14)
    H.append(week(11, [0, 1, 0, 0, 2, 0, 0], 'Carrousels · 1 à 2 / semaine')); T += shw('#ui11', a, b)
    T += [f"tl.fromTo('#ui11 .wc i',{{scale:0}},{{scale:1,duration:.15,stagger:.05,ease:'back.out(3)',immediateRender:false}},{ct(155.26):.3f});",
          f"tl.to('#ui11 .wc i',{{autoAlpha:.25,duration:.2}},{ct(156.60):.3f});"]
    # "ou alors pas du tout": a big red cross stamps the carrousel week
    H.append('<div id="nx" class="nx"><i></i><i></i></div>')
    T += ["gsap.set('#nx',{autoAlpha:0});",
          f"tl.fromTo('#nx',{{autoAlpha:0,scale:2.2,rotation:-12}},{{autoAlpha:1,scale:1,rotation:0,duration:.18,ease:'power3.in',immediateRender:false}},{ct(156.60):.3f});",
          f"tl.set('#nx',{{autoAlpha:0}},{b:.3f});"]
    S.append(('nope', ct(156.60), .35))
    # 16 stories 1-2 / day
    a, b = win(15, 15)
    H.append(week(12, [1, 1, 1, 1, 1, 1, 1], 'Stories · 1 à 2 / jour')); T += shw('#ui12', a, b)
    T += [f"tl.fromTo('#ui12 .wc i',{{scale:0}},{{scale:1,duration:.12,stagger:.04,ease:'back.out(3)',immediateRender:false}},{ct(158.06):.3f});"]

    # alternate punch-ins hide the jump cuts between the kept pieces
    edge = 0.0
    for k, (sa, sb) in enumerate(SEGS):
        T.append(f"tl.set('#cam',{{scale:{1.0 if k % 2 == 0 else 1.14}}},{edge:.3f});")
        edge += sb - sa
    return H, T, S


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:50% 42%}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.row{{position:absolute;left:24px;right:24px;top:{TOP}px;z-index:20;display:flex;justify-content:space-between;align-items:flex-start}}
.ic{{width:300px;text-align:center;transform-origin:50% 0%}}
.ig{{height:176px;display:flex;justify-content:center;filter:drop-shadow(0 0 5px rgba(240,255,170,.5)) drop-shadow(0 3px 8px rgba(0,0,0,.25))}}
.ig svg{{height:176px;width:auto}}
.ic span{{display:block;margin-top:10px;font:800 50px/1 Poppins;letter-spacing:.01em;color:#fff;text-shadow:0 3px 0 rgba(0,0,0,.6)}}
.vs{{margin-top:66px;font:800 40px/1 Poppins;color:#fff;text-shadow:0 2px 0 rgba(0,0,0,.6)}}
.cap{{position:absolute;left:40px;right:40px;top:1150px;z-index:25;text-align:center;font:700 66px/1 Poppins;letter-spacing:-.01em;color:#fff;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.cap.un{{top:1370px;font-size:52px}}
.big{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1235px;z-index:26;font:800 108px/1.05 Poppins;color:#fff;white-space:nowrap;
  text-shadow:0 3px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.55)}}
.big.s{{font-size:78px;top:1262px}}
.cb{{position:absolute;left:90px;right:90px;top:470px;z-index:30;height:118px;border-radius:59px;background:#fff;display:flex;align-items:center;gap:20px;
  padding:0 18px 0 18px;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.cav{{width:80px;height:80px;border-radius:50%;object-fit:cover;flex:none;border:3px solid #573307}}
.cw{{flex:1;display:flex;align-items:center;min-width:0}}
.cph{{font:500 36px/1 Poppins;color:#9A9087}}
.cty{{font:400 66px/1 Anton;letter-spacing:.06em;color:#2A1A10}}
.ccr{{width:4px;height:56px;background:#573307;margin-left:6px}}
.csd{{width:84px;height:84px;border-radius:50%;background:#573307;display:flex;align-items:center;justify-content:center;flex:none}}
.ui{{position:absolute;left:120px;right:120px;top:1255px;z-index:24;background:#fff;border-radius:22px;padding:16px 22px;
  box-shadow:0 14px 34px rgba(0,0,0,.28);font-family:Poppins;color:#111}}
.ut{{font:700 34px/1 Poppins;margin-bottom:14px}}
.ut em{{font-style:normal;color:#888;font-weight:500}}
.br{{display:flex;align-items:center;gap:16px;margin-top:10px;font:600 30px/1 Poppins;color:#333}}
.br span{{width:210px;white-space:nowrap}}
.bt{{flex:1;height:20px;border-radius:10px;background:#EFEFEF;overflow:hidden}}
.bt i{{display:block;height:100%;width:100%;background:linear-gradient(90deg,#D62976,#962FBF)}}
.tg{{display:flex;align-items:center;gap:20px}}
.tg div{{flex:1}} .tg b{{display:block;font:700 36px/1.2 Poppins}} .tg small{{display:block;font:500 27px/1.3 Poppins;color:#777}}
.sw{{position:relative;width:100px;height:56px;border-radius:28px;background:#D9D9D9;flex:none}}
.sw i{{position:absolute;left:4px;top:4px;width:48px;height:48px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.25)}}
.fl{{display:flex;align-items:center;gap:18px}} .fl div{{flex:1}} .fl b{{display:block;font:700 36px/1.2 Poppins}} .fl small{{display:block;font:500 27px/1.3 Poppins;color:#777}}
.fl .ico{{font-style:normal;font-size:52px}} .fl em{{font:800 56px/1 Poppins;font-style:normal;color:#18A957}}
.sv{{left:400px;right:400px;display:flex;flex-direction:column;align-items:center;gap:6px}} .sv b{{font:700 30px/1 Poppins}}
.rp{{background:none;box-shadow:none;padding:0;display:flex;flex-direction:column;gap:12px;align-items:flex-start}}
.rp span{{background:#fff;border-radius:30px;padding:16px 26px;font:600 36px/1.2 Poppins;color:#111;box-shadow:0 10px 26px rgba(0,0,0,.25)}}
.rp span:last-child{{align-self:flex-end}}
.rc{{display:flex;gap:16px;background:none;box-shadow:none;padding:0}}
.rc span{{flex:1;background:#fff;border-radius:18px;padding:16px 20px;box-shadow:0 10px 26px rgba(0,0,0,.25);display:flex;justify-content:space-between;align-items:center}}
.rc small{{font:600 32px/1 Poppins;color:#555}} .rc b{{font:800 52px/1 Poppins;color:#18A957}}
.fan{{position:absolute;left:0;right:0;top:1230px;height:240px;z-index:24}}
.fan img{{position:absolute;left:450px;top:0;width:180px;height:255px;object-fit:cover;border-radius:10px;box-shadow:0 10px 24px rgba(0,0,0,.35);transform-origin:50% 100%}}
.mny{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1250px;z-index:24;font:400 150px/1 sans-serif;filter:drop-shadow(0 10px 18px rgba(0,0,0,.35))}}
.wk{{left:70px;right:70px}}
.wg{{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}}
.wd{{font:700 26px/1 Poppins;color:#555;text-align:center}}
.wc{{height:66px;border-radius:10px;background:#F2F2F2;display:flex;align-items:center;justify-content:center}}
.wc i{{font:800 40px/1 Poppins;font-style:normal;color:#573307}}
.wc i.lt{{color:#C9B8A6}}
.nx{{position:absolute;left:0;right:0;margin:0 auto;width:220px;height:220px;top:1235px;z-index:26}}
.nx i{{position:absolute;left:-10px;top:95px;width:240px;height:30px;border-radius:15px;background:#E5262B;box-shadow:0 4px 14px rgba(0,0,0,.3)}}
.nx i:first-child{{transform:rotate(45deg)}} .nx i:last-child{{transform:rotate(-45deg)}}
'''


def build():
    H, T, S = scenes()
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
  <audio id="voice" src="assets/voice.mp4" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="2" data-volume="1"></audio>
{nl.join(f'<audio id="sfx{k}" src="assets/sfx/{n}.mp3" data-start="{t:.3f}" data-duration="{ {'kaching': .9, 'ding': .75, 'bloop': .3, 'nope': .35}.get(n, .7) }" data-track-index="{10 + k % 3}" data-volume="{v:.2f}"></audio>' for k, (n, t, v) in enumerate(sorted(S, key=lambda x: x[1])))}
  <div id="cam"><video id="bgv" class="full" src="assets/aroll.mp4" muted playsinline data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video></div>
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
