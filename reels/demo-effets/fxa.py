"""Effects 33-41 (module A): clone, stack, sticky text, spotlight, freeze+label, pointer callout, odometer,
freeze sticker, blackout.  Each fn(a, b, k) -> dict(front, behind, tw, css)."""
import os

from build import show, frame, cutframe, TOP, BROWN, DARK, INK, CREAM, PILL

GOLD = '#E9C98F'
SHADOW = '0 18px 40px rgba(20,10,4,.45)'


def hide_all(sels, b):
    return [f"gsap.set('{s}',{{autoAlpha:0}});" for s in sels] + [f"tl.set('{s}',{{autoAlpha:0}},{b:.3f});" for s in sels]


def fade_out(sels, b, d=.15):
    return [f"tl.to('{s}',{{autoAlpha:0,duration:{d}}},{b - d:.3f});" for s in sels]


def flash(k, a):
    """quick white flash (front)"""
    html = f'<div id="{k}fl" style="position:absolute;inset:0;background:#fff;z-index:60"></div>'
    tw = [f"gsap.set('#{k}fl',{{autoAlpha:0}});",
          f"tl.set('#{k}fl',{{autoAlpha:.9}},{a:.3f});",
          f"tl.to('#{k}fl',{{autoAlpha:0,duration:.22,ease:'power2.out'}},{a + .02:.3f});"]
    return html, tw


# ------------------------------------------------------------------ 33 CLONE
def clone(a, b, k):
    behind, tw = [], []
    sides = [(-400, 0), (400, 1)]
    for x, j in sides:
        w = f'{k}w{j}'
        behind.append(
            f'<div id="{w}" class="{k}cl"><video id="{k}v{j}" class="full" src="assets/cut.webm" muted playsinline '
            f'data-start="{a:.3f}" data-media-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{100 + 33 * 3 + j}"></video></div>')
        d = j * .12
        tw += [f"gsap.set('#{w}',{{autoAlpha:0,x:0,scale:.55}});",
               f"tl.fromTo('#{w}',{{autoAlpha:0,x:0,scale:.55}},{{autoAlpha:1,x:{x},scale:.8,duration:.32,ease:'back.out(1.6)',immediateRender:false}},{a + d:.3f});",
               f"tl.to('#{w}',{{x:{x * 1.04:.0f},duration:{b - a - .6:.2f},ease:'sine.inOut'}},{a + d + .32:.3f});"]
    tw += fade_out([f'#{k}w0', f'#{k}w1'], b) + [f"tl.set('#{k}w{j}',{{autoAlpha:0}},{b:.3f});" for j in (0, 1)]
    # title
    front = [f'<div id="{k}t" class="{k}t">1 tournage <i>=</i> 3 réels</div>']
    tw += show(f'#{k}t', a + .2, b, "{autoAlpha:0,y:-40,scale:.9}", .3)
    css = f'''
.{k}cl{{position:absolute;inset:0;transform-origin:50% 100%;filter:brightness(.86) saturate(.92)}}
.{k}t{{position:absolute;top:{TOP + 70}px;left:0;right:0;margin:0 auto;width:fit-content;z-index:40;font:400 110px/1 Anton;
  color:{CREAM};text-transform:uppercase;letter-spacing:.01em;text-shadow:0 6px 30px rgba(20,10,4,.55)}}
.{k}t i{{font-style:normal;color:{GOLD}}}
'''
    return dict(front=front, behind=behind, tw=tw, css=css)


# ------------------------------------------------------------------ 34 THE STACK
def stack(a, b, k):
    rows = [('Réels montés / mois', .92, 24, ''), ('Heures gagnées', .58, 15, ' h'), ('Vues moyennes', .76, 18, 'K')]
    front, tw = [], []
    y0 = TOP + 40
    for i, (lab, w, n, suf) in enumerate(rows):
        cid = f'{k}c{i}'
        front.append(
            f'<div id="{cid}" class="{k}card" style="top:{y0 + i * 128}px">'
            f'<div class="{k}lab">{lab}</div><div class="{k}trk"><div id="{cid}b" class="{k}bar" style="width:{w * 100:.0f}%"></div></div>'
            f'<div class="{k}num"><span id="{cid}n">0</span>{suf}</div></div>')
        # bottom card lands first, the next ones stack above it
        t = a + (2 - i) * .09
        tw += [f"gsap.set('#{cid}',{{autoAlpha:0}});",
               f"gsap.set('#{cid}b',{{scaleX:0}});",
               f"tl.fromTo('#{cid}',{{autoAlpha:0,y:-70,scale:.9}},{{autoAlpha:1,y:0,scale:1,duration:.28,ease:'back.out(1.8)',immediateRender:false}},{t:.3f});",
               f"tl.fromTo('#{cid}b',{{scaleX:0}},{{scaleX:1,duration:.6,ease:'power3.out',immediateRender:false}},{t + .12:.3f});",
               f"tl.fromTo('#{cid}n',{{textContent:0}},{{textContent:{n},duration:.6,ease:'power3.out',snap:{{textContent:1}},immediateRender:false}},{t + .12:.3f});",
               f"tl.to('#{cid}',{{autoAlpha:0,y:-20,duration:.15}},{b - .15:.3f});",
               f"tl.set('#{cid}',{{autoAlpha:0}},{b:.3f});"]
    css = f'''
.{k}card{{position:absolute;left:0;right:0;margin:0 auto;width:700px;height:112px;z-index:40;border-radius:22px;
  background:rgba(42,26,16,.92);box-shadow:{SHADOW};display:grid;grid-template-columns:1fr 120px;grid-template-rows:44px 30px;
  padding:16px 26px;column-gap:20px;border:1px solid rgba(233,201,143,.25)}}
.{k}lab{{font:600 28px/44px Poppins;color:{CREAM};letter-spacing:.01em}}
.{k}trk{{grid-column:1;height:16px;margin-top:8px;border-radius:99px;background:rgba(244,238,230,.12);overflow:hidden}}
.{k}bar{{height:100%;border-radius:99px;background:{PILL};transform-origin:0 50%}}
.{k}num{{grid-column:2;grid-row:1/3;align-self:center;text-align:right;font:400 60px/1 Anton;color:{GOLD}}}
'''
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 35 STICKY TEXT
def sticky(a, b, k):
    s = f'#{k}s'
    front = [f'<div id="{k}s" class="{k}s"><div class="{k}big">MONTAGE</div><div class="{k}sm">@thestrategicboost.fr</div></div>']
    n = max(1, int((b - a - .5) / .5))
    tw = [f"gsap.set('{s}',{{autoAlpha:0,rotation:-7}});",
          f"tl.fromTo('{s}',{{autoAlpha:0,scale:1.7,rotation:-22}},{{autoAlpha:1,scale:1,rotation:-7,duration:.28,ease:'back.out(2.2)',immediateRender:false}},{a:.3f});",
          # follow wobble: small sway like it is stuck to her moving chest
          f"tl.to('{s}',{{x:10,y:-8,rotation:-4,duration:.5,ease:'sine.inOut',yoyo:true,repeat:{n - 1}}},{a + .28:.3f});",
          f"tl.to('{s}',{{autoAlpha:0,scale:.9,duration:.15}},{b - .15:.3f});",
          f"tl.set('{s}',{{autoAlpha:0}},{b:.3f});"]
    css = f'''
.{k}s{{position:absolute;left:150px;top:1290px;z-index:40;padding:14px 24px 12px;border-radius:14px;background:{CREAM};
  border:5px solid #fff;box-shadow:0 10px 26px rgba(20,10,4,.35);text-align:center;transform-origin:50% 50%}}
.{k}big{{font:400 74px/1 Anton;color:{INK};letter-spacing:.04em}}
.{k}sm{{font:700 24px/1.3 Poppins;color:{BROWN};margin-top:6px}}
'''
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 36 SPOTLIGHT
def spotlight(a, b, k):
    behind = [f'<div id="{k}dk" class="{k}dk"><div class="{k}dki"></div><div class="{k}glow"></div></div>']
    front = [f'<div id="{k}w1" class="{k}w {k}w1">ZÉRO</div>', f'<div id="{k}w2" class="{k}w {k}w2">MONTAGE</div>']
    tw = [f"gsap.set('#{k}dk',{{autoAlpha:0}});",
          f"tl.fromTo('#{k}dk',{{autoAlpha:0}},{{autoAlpha:1,duration:.18,ease:'power2.in',immediateRender:false}},{a:.3f});",
          f"tl.to('#{k}dk',{{autoAlpha:0,duration:.15}},{b - .15:.3f});",
          f"tl.set('#{k}dk',{{autoAlpha:0}},{b:.3f});"]
    for i, sel in enumerate([f'#{k}w1', f'#{k}w2']):
        tw += show(sel, a + .16 + i * .14, b, "{autoAlpha:0,scale:1.9,y:0}", .3, 'expo.out')
    css = f'''
.{k}dk{{position:absolute;inset:0}}
.{k}dki{{position:absolute;inset:0;background:#0d0805;opacity:.78}}
.{k}glow{{position:absolute;inset:0;background:radial-gradient(ellipse 520px 760px at 540px 1060px,rgba(244,226,200,.6) 0%,rgba(244,226,200,.22) 45%,rgba(244,226,200,0) 75%)}}
.{k}w{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;z-index:40;font:400 190px/1 Anton;color:{CREAM};
  letter-spacing:.02em;text-shadow:0 8px 40px rgba(0,0,0,.6)}}
.{k}w1{{top:{TOP + 20}px;font-size:120px;color:transparent;background:{PILL};-webkit-background-clip:text;background-clip:text;text-shadow:none}}
.{k}w2{{top:{TOP + 140}px}}
'''
    return dict(front=front, behind=behind, tw=tw, css=css)


# ------------------------------------------------------------------ 37 FREEZE AND LABEL
def freeze_label(a, b, k):
    ft = a + .1
    img = frame(ft)
    fh, ftw = flash(k, ft)
    # (label text, label box left/top, target point on her)
    # (label text, label box left/top, line start on the label, target point on her)
    labs = [('la lumière', 70, 560, (220, 624), (250, 960)),
            ('le micro', 710, 1010, (710, 1042), (640, 1290)),
            ('le cadrage', 700, 1460, (850, 1460), (900, 1330))]
    front = [f'<img id="{k}fz" class="full" src="{img}" style="z-index:30">', fh,
             f'<div id="{k}chip" class="{k}chip"><span class="{k}pz"></span>ARRÊT SUR IMAGE</div>']
    svg = [f'<svg id="{k}svg" class="{k}svg" viewBox="0 0 1080 1920">']
    tw = hide_all([f'#{k}fz', f'#{k}svg'], b) + [f"tl.set('#{k}fz',{{autoAlpha:1}},{ft:.3f});", f"tl.set('#{k}svg',{{autoAlpha:1}},{ft:.3f});",
                                                 f"tl.fromTo('#{k}fz',{{scale:1}},{{scale:1.035,duration:{b - ft:.2f},ease:'none',immediateRender:false}},{ft:.3f});"]
    tw += ftw + show(f'#{k}chip', ft + .05, b, "{autoAlpha:0,x:-30}", .25, 'power3.out')
    for i, (txt, lx, ly, (sx, sy), (px, py)) in enumerate(labs):
        lid = f'{k}l{i}'
        front.append(f'<div id="{lid}" class="{k}lab" style="left:{lx}px;top:{ly}px">{txt}</div>')
        # line from label edge to the point
        ln = ((px - sx) ** 2 + (py - sy) ** 2) ** .5
        svg.append(f'<line id="{lid}ln" x1="{sx}" y1="{sy}" x2="{px}" y2="{py}" stroke="{CREAM}" stroke-width="4" stroke-linecap="round" '
                   f'stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"/>'
                   f'<circle id="{lid}d" cx="{px}" cy="{py}" r="11" fill="{BROWN}" stroke="{CREAM}" stroke-width="5"/>')
        t = ft + .12 + i * .08
        tw += [f"gsap.set('#{lid}ln',{{strokeDashoffset:{ln:.0f}}});",
               f"tl.fromTo('#{lid}ln',{{strokeDashoffset:{ln:.0f}}},{{strokeDashoffset:0,duration:.25,ease:'power2.out',immediateRender:false}},{t:.3f});",
               f"gsap.set('#{lid}d',{{scale:0,transformOrigin:'50% 50%'}});",
               f"tl.fromTo('#{lid}d',{{scale:0}},{{scale:1,duration:.2,ease:'back.out(3)',immediateRender:false}},{t + .2:.3f});"]
        tw += show(f'#{lid}', t, b, "{autoAlpha:0,scale:.6,y:10}", .26, 'back.out(2)')
    svg.append('</svg>')
    front.insert(2, ''.join(svg))
    css = f'''
.{k}svg{{position:absolute;inset:0;width:1080px;height:1920px;z-index:35;filter:drop-shadow(0 3px 6px rgba(20,10,4,.5))}}
.{k}lab{{position:absolute;z-index:40;width:300px;text-align:center;padding:14px 0 12px;border-radius:999px;background:{CREAM};
  font:700 italic 36px/1.1 Poppins;color:{INK};box-shadow:{SHADOW};border:3px solid {BROWN}}}
.{k}chip{{position:absolute;left:70px;top:{TOP + 30}px;z-index:40;padding:12px 22px;border-radius:12px;background:rgba(42,26,16,.85);
  font:500 26px/1 'JetBrains Mono';color:{CREAM};letter-spacing:.08em;display:flex;align-items:center;gap:14px}}
.{k}pz{{width:20px;height:24px;border-left:7px solid {GOLD};border-right:7px solid {GOLD}}}
'''
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 38 POINTER CALLOUT
def pointer(a, b, k):
    cards = [('ÉTAPE 1', 'Coupe les<br>silences', 70, 360, (250, 1380)),
             ('ÉTAPE 2', 'Ajoute les<br>sous-titres', 700, 520, (600, 1250))]
    front, tw = [], []
    svg = [f'<svg id="{k}svg" class="{k}svg" viewBox="0 0 1080 1920">']
    for i, (top, txt, x, y, (px, py)) in enumerate(cards):
        cid = f'{k}c{i}'
        front.append(f'<div id="{cid}" class="{k}card" style="left:{x}px;top:{y}px"><div class="{k}k">{top}</div><div class="{k}t">{txt}</div></div>')
        sx, sy = x + 155, y + 190
        cx, cy = (sx + px) / 2 + (-90 if i == 0 else 90), (sy + py) / 2
        ln = 1.15 * (((px - sx) ** 2 + (py - sy) ** 2) ** .5)
        svg.append(f'<path id="{cid}ln" d="M{sx},{sy} Q{cx:.0f},{cy:.0f} {px},{py}" fill="none" stroke="{CREAM}" stroke-width="5" stroke-linecap="round" '
                   f'stroke-dasharray="{ln:.0f}" stroke-dashoffset="{ln:.0f}"/>'
                   f'<circle id="{cid}d" cx="{px}" cy="{py}" r="13" fill="{BROWN}" stroke="{CREAM}" stroke-width="6"/>')
        t = a + i * .12
        tw += show(f'#{cid}', t, b, "{autoAlpha:0,scale:.7,y:30}", .3, 'back.out(1.8)')
        tw += [f"tl.to('#{cid}',{{y:{-12 if i == 0 else 12},x:{6 if i == 0 else -6},duration:{b - t - .5:.2f},ease:'sine.inOut'}},{t + .31:.3f});",
               f"gsap.set('#{cid}ln',{{strokeDashoffset:{ln:.0f}}});",
               f"tl.fromTo('#{cid}ln',{{strokeDashoffset:{ln:.0f}}},{{strokeDashoffset:0,duration:.3,ease:'power2.inOut',immediateRender:false}},{t + .12:.3f});",
               f"gsap.set('#{cid}d',{{scale:0,transformOrigin:'50% 50%'}});",
               f"tl.fromTo('#{cid}d',{{scale:0}},{{scale:1,duration:.22,ease:'back.out(3)',immediateRender:false}},{t + .38:.3f});"]
    svg.append('</svg>')
    front.insert(0, ''.join(svg))
    tw += hide_all([f'#{k}svg'], b) + [f"tl.set('#{k}svg',{{autoAlpha:1}},{a:.3f});"] + fade_out([f'#{k}svg'], b)
    css = f'''
.{k}svg{{position:absolute;inset:0;width:1080px;height:1920px;z-index:38;filter:drop-shadow(0 3px 6px rgba(20,10,4,.45))}}
.{k}card{{position:absolute;z-index:40;width:310px;padding:22px 26px 24px;border-radius:24px;background:{CREAM};box-shadow:{SHADOW};
  border-top:8px solid {BROWN}}}
.{k}k{{font:500 22px/1 'JetBrains Mono';color:{BROWN};letter-spacing:.12em;margin-bottom:12px}}
.{k}t{{font:800 38px/1.08 Poppins;color:{INK}}}
'''
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 39 ODOMETER
def odometer(a, b, k):
    digits = '10000'
    H = 200
    cols = []
    tw = []
    for i, d in enumerate(digits):
        cid = f'{k}d{i}'
        nums = ''.join(f'<span>{n % 10}</span>' for n in range(20))
        cols.append(f'<div class="{k}win"><div id="{cid}" class="{k}col">{nums}</div></div>' + ('<div class="{0}gap"></div>'.format(k) if i == 1 else ''))
        end = -(10 + int(d)) * H
        t = a + .08 + (len(digits) - 1 - i) * .06
        tw += [f"gsap.set('#{cid}',{{y:0}});",
               f"tl.fromTo('#{cid}',{{y:0}},{{y:{end},duration:{.75 + i * .08:.2f},ease:'power3.out',immediateRender:false}},{t:.3f});"]
    front = [f'<div id="{k}box" class="{k}box"><div class="{k}row">{"".join(cols)}</div>'
             f'<div class="{k}cap"><span class="{k}line"></span>vues sur un seul réel</div></div>']
    tw = show(f'#{k}box', a, b, "{autoAlpha:0,y:-40,scale:.9}", .26, 'back.out(1.6)') + tw
    css = f'''
.{k}box{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP + 30}px;z-index:40;padding:26px 34px 24px;border-radius:30px;
  background:rgba(42,26,16,.93);box-shadow:{SHADOW};border:1px solid rgba(233,201,143,.3)}}
.{k}row{{display:flex;gap:8px}}
.{k}gap{{width:22px}}
.{k}win{{position:relative;width:118px;height:{H}px;overflow:hidden;border-radius:14px;background:linear-gradient(180deg,#1a0f08,#3a2414 50%,#1a0f08)}}
.{k}win:after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,10,4,.75) 0%,rgba(20,10,4,0) 26%,rgba(20,10,4,0) 74%,rgba(20,10,4,.75) 100%)}}
.{k}col span{{display:block;height:{H}px;font:400 170px/{H}px Anton;color:{CREAM};text-align:center}}
.{k}cap{{margin-top:18px;display:flex;align-items:center;justify-content:center;gap:16px;font:700 italic 38px/1 Poppins;color:{CREAM}}}
.{k}line{{width:60px;height:8px;border-radius:9px;background:{PILL}}}
'''
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 40 FREEZE STICKER
def die_cut(t):
    """cut-out at t, cropped to her bust, scaled .6, with a thick white die-cut outline baked in"""
    out = f'assets/frames/stk{t:.2f}.png'
    if os.path.exists(out) or not os.path.exists('assets/cut.webm'):
        return out
    from PIL import Image, ImageFilter
    im = Image.open(cutframe(t)).convert('RGBA')
    bbox = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox() or (0, 0, im.width, im.height)
    im = im.crop((bbox[0], bbox[1], bbox[2], im.height))
    s = .66
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    pad = 40
    can = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    can.paste(im, (pad, pad))
    al = can.getchannel('A').point(lambda v: 255 if v > 60 else 0)
    dil = al
    for _ in range(3):
        dil = dil.filter(ImageFilter.MaxFilter(9))
    dil = dil.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 100 else 0).filter(ImageFilter.GaussianBlur(.8))
    white = Image.new('RGBA', can.size, (255, 255, 255, 255))
    white.putalpha(dil)
    shadow = Image.new('RGBA', can.size, (20, 10, 4, 0))
    shadow.putalpha(dil.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * .55)))
    res = Image.new('RGBA', can.size, (0, 0, 0, 0))
    res.alpha_composite(shadow, (0, 10))
    res.alpha_composite(white)
    res.alpha_composite(can)
    res = res.crop((0, 0, res.width, pad + im.height + 14))
    res.save(out)
    return out


def freeze_sticker(a, b, k):
    ft = a + .1
    img = frame(ft)
    stk = die_cut(ft)
    fh, ftw = flash(k, ft)
    front = [f'<div id="{k}bg" class="{k}bg"><img class="full" src="{img}"><div class="{k}dim"></div></div>', fh,
             f'<div id="{k}st" class="{k}st"><img src="{stk}"></div>',
             f'<div id="{k}n1" class="{k}n" style="left:70px;top:{TOP + 40}px;transform:rotate(-6deg)">moi, en plein tournage</div>',
             f'<div id="{k}n2" class="{k}n" style="right:70px;top:1440px;transform:rotate(-3deg)">montage : Claude</div>',
             f'<svg id="{k}ar" class="{k}ar" viewBox="0 0 1080 1920">'
             f'<path id="{k}a1" d="M330,{TOP + 120} C400,{TOP + 190} 420,{TOP + 240} 400,{TOP + 330}" fill="none" stroke="{CREAM}" stroke-width="6" stroke-linecap="round" stroke-dasharray="260" stroke-dashoffset="260"/>'
             f'<path id="{k}a1h" d="M372,{TOP + 300} L400,{TOP + 334} L424,{TOP + 296}" fill="none" stroke="{CREAM}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path id="{k}a2" d="M595,1482 C540,1482 528,1432 545,1370" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-dasharray="200" stroke-dashoffset="200"/>'
             f'<path id="{k}a2h" d="M523,1394 L545,1366 L569,1392" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
             '</svg>']
    tw = hide_all([f'#{k}bg', f'#{k}ar'], b) + [f"tl.set('#{k}bg',{{autoAlpha:1}},{ft:.3f});", f"tl.set('#{k}ar',{{autoAlpha:1}},{ft:.3f});"]
    tw += fade_out([f'#{k}bg', f'#{k}ar'], b)
    tw += [f"gsap.set('#{k}dim',{{opacity:0}});", f"tl.fromTo('#{k}dim',{{opacity:0}},{{opacity:1,duration:.2,immediateRender:false}},{ft:.3f});"]
    tw += ftw
    tw += [f"gsap.set('#{k}st',{{autoAlpha:0,rotation:-5}});",
           f"tl.fromTo('#{k}st',{{autoAlpha:0,scale:1.35,rotation:9}},{{autoAlpha:1,scale:1,rotation:-5,duration:.34,ease:'back.out(1.7)',immediateRender:false}},{ft + .04:.3f});",
           f"tl.to('#{k}st',{{rotation:-3,y:-10,duration:{b - ft - .6:.2f},ease:'sine.inOut'}},{ft + .38:.3f});",
           f"tl.to('#{k}st',{{autoAlpha:0,scale:.95,duration:.15}},{b - .15:.3f});", f"tl.set('#{k}st',{{autoAlpha:0}},{b:.3f});"]
    for i, n in enumerate(['1', '2']):
        t = ft + .3 + i * .12
        tw += [f"gsap.set('#{k}n{n}',{{autoAlpha:0}});",
               f"tl.fromTo('#{k}n{n}',{{autoAlpha:0,y:16}},{{autoAlpha:1,y:0,duration:.22,ease:'power2.out',immediateRender:false}},{t:.3f});",
               f"tl.to('#{k}n{n}',{{autoAlpha:0,duration:.15}},{b - .15:.3f});", f"tl.set('#{k}n{n}',{{autoAlpha:0}},{b:.3f});",
               f"gsap.set('#{k}a{n}h',{{autoAlpha:0}});",
               f"tl.fromTo('#{k}a{n}',{{strokeDashoffset:{260 if n == '1' else 200}}},{{strokeDashoffset:0,duration:.22,ease:'power2.out',immediateRender:false}},{t + .08:.3f});",
               f"tl.set('#{k}a{n}h',{{autoAlpha:1}},{t + .28:.3f});", f"tl.set('#{k}a{n}h',{{autoAlpha:0}},{b:.3f});"]
    css = f'''
.{k}bg{{position:absolute;inset:0;z-index:30;overflow:hidden}}
.{k}bg img{{filter:blur(6px) saturate(.7);transform:scale(1.04)}}
.{k}dim{{position:absolute;inset:0;background:rgba(42,26,16,.62)}}
.{k}st{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP + 300}px;z-index:36;transform-origin:50% 60%}}
.{k}st img{{display:block;height:860px}}
.{k}n{{position:absolute;z-index:40;font:600 64px/1 Caveat;color:{CREAM};text-shadow:0 3px 12px rgba(0,0,0,.45)}}
#{k}n2{{color:{GOLD}}}
.{k}ar{{position:absolute;inset:0;width:1080px;height:1920px;z-index:39}}
'''
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 41 BLACKOUT
def blackout(a, b, k):
    t0, t1 = a + .12, a + .62
    front = [f'<div id="{k}bk" class="{k}bk"><div id="{k}tx" class="{k}tx">et là… <b>coupez.</b></div></div>']
    tw = [f"gsap.set('#{k}bk',{{autoAlpha:0}});",
          f"tl.set('#{k}bk',{{autoAlpha:1}},{t0:.3f});",
          f"tl.fromTo('#{k}tx',{{scale:1.12,autoAlpha:0}},{{scale:1,autoAlpha:1,duration:.16,ease:'power3.out',immediateRender:false}},{t0 + .04:.3f});",
          f"tl.to('#{k}tx',{{scale:.97,duration:{t1 - t0 - .2:.2f},ease:'none'}},{t0 + .2:.3f});",
          f"tl.set('#{k}bk',{{autoAlpha:0}},{t1:.3f});",
          # lights flicker once on the way back
          f"tl.set('#{k}bk',{{autoAlpha:.55}},{t1 + .07:.3f});",
          f"tl.set('#{k}tx',{{autoAlpha:0}},{t1 + .07:.3f});",
          f"tl.set('#{k}bk',{{autoAlpha:0}},{t1 + .11:.3f});",
          f"tl.set('#{k}bk',{{autoAlpha:0}},{b:.3f});"]
    css = f'''
.{k}bk{{position:absolute;inset:0;z-index:70;background:#000;display:flex;align-items:center;justify-content:center}}
.{k}tx{{font:600 italic 76px/1 Poppins;color:#fff;letter-spacing:-.01em}}
.{k}tx b{{font-weight:800}}
'''
    return dict(front=front, tw=tw, css=css)


EFFECTS = [(33, 'CLONE', clone), (34, 'THE STACK', stack), (35, 'STICKY TEXT', sticky), (36, 'SPOTLIGHT', spotlight),
           (37, 'FREEZE AND LABEL', freeze_label), (38, 'POINTER CALLOUT', pointer), (39, 'ODOMETER', odometer),
           (40, 'FREEZE STICKER', freeze_sticker), (41, 'BLACKOUT', blackout)]
