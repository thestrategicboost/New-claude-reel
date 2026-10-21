"""Effects 51-59 (depth / light / lists / UI). fn(a, b, k) -> dict(front, behind, tw, css)."""
import random

from build import show, typing, frame, cutframe, TOP, BROWN, DARK, INK, CREAM, PILL  # noqa: F401

GOLD = '#E9C98F'
CAP_SHADOW = '0 4px 0 #000,0 0 18px rgba(0,0,0,.55)'          # her caption style
LAB_SHADOW = '2px 2px 0 rgba(42,26,16,.9)'                     # her label style (sharp dark)


def _sc(a, b):
    """time scale: the design is timed for a 1.3 s slot; longer test slots stretch it a little."""
    return min(max((b - a) / 1.3, 1.0), 2.2)


def _hide(sel, b, d=.15):
    return [f"tl.to('{sel}',{{autoAlpha:0,duration:{d}}},{b - d:.3f});", f"tl.set('{sel}',{{autoAlpha:0}},{b:.3f});"]


def _init(*sels):
    return [f"gsap.set('{s}',{{autoAlpha:0}});" for s in sels]


# ------------------------------------------------------------------ 51 rack focus
def rack_focus(a, b, k):
    pb = b - .4
    css = f'''
#{k}{{position:absolute;left:70px;right:70px;top:300px;z-index:40;text-align:center;font:400 196px/.92 Anton;color:{CREAM};
  text-transform:uppercase;letter-spacing:.005em;text-shadow:0 10px 40px rgba(42,26,16,.55)}}
#{k} .{k}g{{display:block;font-size:150px;background:{PILL};-webkit-background-clip:text;background-clip:text;color:transparent;
  text-shadow:none;filter:drop-shadow(0 8px 24px rgba(42,26,16,.5))}}
'''
    front = [f'<div id="{k}"><span>monté</span><span class="{k}g">avec claude</span></div>']
    tw = _init(f'#{k}') + [
        f"tl.to('#cam',{{filter:'blur(12px)',scale:1.035,duration:.3,ease:'power2.inOut'}},{a:.3f});",
        f"tl.fromTo('#{k}',{{autoAlpha:0,filter:'blur(22px)',scale:1.14}},{{autoAlpha:1,filter:'blur(0px)',scale:1,duration:.34,ease:'power3.out',immediateRender:false}},{a + .04:.3f});",
        f"tl.to('#{k}',{{scale:1.03,duration:{pb - a - .42:.3f},ease:'none'}},{a + .4:.3f});",
        f"tl.to('#{k}',{{filter:'blur(20px)',scale:.94,autoAlpha:0,duration:.3,ease:'power2.in'}},{pb:.3f});",
        f"tl.to('#cam',{{filter:'blur(0px)',scale:1,duration:.32,ease:'power2.inOut'}},{pb:.3f});",
        f"tl.set('#{k}',{{autoAlpha:0}},{b:.3f});",
        f"tl.set('#cam',{{filter:'blur(0px)',scale:1}},{b:.3f});",
    ]
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 52 god rays
def _rays(seed, n, alpha):
    rnd = random.Random(seed)
    stops, ang = [], 0.0
    while ang < 360:
        gap = rnd.uniform(4, 14)
        w = rnd.uniform(2, 7)
        al = alpha * rnd.uniform(.35, 1)
        stops += [f'rgba(235,203,139,0) {ang:.1f}deg', f'rgba(235,203,139,{al:.2f}) {ang + w / 2:.1f}deg',
                  f'rgba(235,203,139,0) {ang + w:.1f}deg']
        ang += w + gap
    return f"conic-gradient(from 0deg at 50% 50%,{','.join(stops)})"


def god_rays(a, b, k):
    cx, cy, R = 560, 700, 1100
    css = f'''
#{k}d{{position:absolute;inset:0;background:radial-gradient(circle at {cx}px {cy}px,rgba(42,26,16,.15) 0,rgba(26,16,9,.72) 55%,rgba(14,8,4,.86) 100%)}}
.{k}r{{position:absolute;left:{cx - R}px;top:{cy - R}px;width:{2 * R}px;height:{2 * R}px;mix-blend-mode:screen;
  -webkit-mask-image:radial-gradient(circle,#000 0,#000 9%,rgba(0,0,0,.55) 26%,transparent 52%);mask-image:radial-gradient(circle,#000 0,#000 9%,rgba(0,0,0,.55) 26%,transparent 52%)}}
#{k}r1{{background:{_rays(7, 0, .75)};filter:blur(5px)}}
#{k}r2{{background:{_rays(21, 0, .5)};filter:blur(10px)}}
#{k}g{{position:absolute;left:{cx - 520}px;top:{cy - 520}px;width:1040px;height:1040px;border-radius:50%;mix-blend-mode:screen;
  background:radial-gradient(circle,rgba(255,222,170,.85) 0,rgba(233,180,110,.45) 22%,rgba(140,92,65,.18) 45%,transparent 68%)}}
'''
    behind = [f'<div id="{k}d"></div>', f'<div id="{k}r2" class="{k}r"></div>', f'<div id="{k}r1" class="{k}r"></div>',
              f'<div id="{k}g"></div>']
    hold = b - a - .5
    tw = _init(f'#{k}d', f'#{k}r1', f'#{k}r2', f'#{k}g') + [
        f"tl.fromTo('#{k}d',{{autoAlpha:0}},{{autoAlpha:1,duration:.25,ease:'power2.out',immediateRender:false}},{a:.3f});",
        f"tl.fromTo('#{k}g',{{autoAlpha:0,scale:.4}},{{autoAlpha:1,scale:1,duration:.35,ease:'power3.out',immediateRender:false}},{a + .05:.3f});",
        f"tl.fromTo('#{k}r1',{{autoAlpha:0,scale:.55,rotation:-14}},{{autoAlpha:1,scale:1,rotation:0,duration:.45,ease:'power3.out',immediateRender:false}},{a + .08:.3f});",
        f"tl.fromTo('#{k}r2',{{autoAlpha:0,scale:.7,rotation:10}},{{autoAlpha:.9,scale:1.05,rotation:0,duration:.5,ease:'power3.out',immediateRender:false}},{a + .1:.3f});",
        f"tl.to('#{k}r1',{{rotation:{6 + 3 * hold:.1f},duration:{hold:.3f},ease:'none'}},{a + .53:.3f});",
        f"tl.to('#{k}r2',{{rotation:{-4 - 2 * hold:.1f},duration:{hold:.3f},ease:'none'}},{a + .6:.3f});",
        f"tl.to('#{k}g',{{scale:1.08,duration:{hold:.3f},ease:'sine.inOut'}},{a + .4:.3f});",
    ] + sum([_hide(s, b, .2) for s in (f'#{k}d', f'#{k}r1', f'#{k}r2', f'#{k}g')], [])
    return dict(behind=behind, tw=tw, css=css)


# ------------------------------------------------------------------ 53 depth scatter
def depth_scatter(a, b, k):
    s = _sc(a, b)
    # text, centre x, centre y, size, exit ('back' recedes / 'past' flies past camera / None stays)
    words = [('tu', 250, 340, 150, 'back'), ('vois', 790, 330, 132, 'past'), ('cette', 300, 560, 118, 'back'),
             ('vidéo ?', 590, 450, 196, None)]
    css = f'''
.{k}w{{position:absolute;z-index:40;translate:-50% -50%;white-space:nowrap;font-family:Poppins;font-weight:800;color:#fff;
  text-transform:lowercase;letter-spacing:-.02em;line-height:1;text-shadow:{CAP_SHADOW}}}
'''
    front, tw = [], []
    iv = .22 * s
    for i, (txt, x, y, sz, ex) in enumerate(words):
        sel = f'#{k}w{i}'
        col = f'color:{GOLD};' if ex is None else ''
        front.append(f'<div id="{k}w{i}" class="{k}w" style="left:{x}px;top:{y}px;font-size:{sz}px;{col}">{txt}</div>')
        t = a + i * iv
        tw += _init(sel)
        tw.append(f"tl.fromTo('{sel}',{{autoAlpha:0,scale:1.9,filter:'blur(16px)'}},{{autoAlpha:1,scale:1,filter:'blur(0px)',duration:.2,ease:'power3.out',immediateRender:false}},{t:.3f});")
        if ex == 'back':
            tw.append(f"tl.to('{sel}',{{autoAlpha:.55,scale:.8,filter:'blur(6px)',duration:.28,ease:'power2.out'}},{t + iv:.3f});")
            tw.append(f"tl.to('{sel}',{{autoAlpha:.32,scale:.72,filter:'blur(10px)',duration:.3,ease:'power2.out'}},{t + 2 * iv:.3f});")
        elif ex == 'past':
            tw.append(f"tl.to('{sel}',{{autoAlpha:0,scale:2.8,filter:'blur(22px)',duration:.3,ease:'power2.in'}},{t + iv:.3f});")
        else:
            tw.append(f"tl.to('{sel}',{{scale:1.06,duration:{b - t - .4:.3f},ease:'none'}},{t + .22:.3f});")
        tw += _hide(sel, b)
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 54 stat stack
def stat_stack(a, b, k):
    s = _sc(a, b)
    css = f'''
#{k}{{position:absolute;left:70px;right:70px;top:290px;z-index:40;text-align:center}}
#{k}n{{font:400 260px/1 Anton;color:{CREAM};letter-spacing:-.01em;text-shadow:0 12px 44px rgba(42,26,16,.55)}}
#{k}u{{width:540px;height:14px;margin:6px auto 0;border-radius:7px;background:{PILL};transform-origin:0 50%;box-shadow:0 4px 18px rgba(42,26,16,.35)}}
#{k}t{{margin-top:22px;font:italic 600 44px/1 Poppins;color:{CREAM};text-shadow:0 3px 14px rgba(0,0,0,.6)}}
'''
    front = [f'<div id="{k}"><div id="{k}n">+300%</div><div id="{k}u"></div><div id="{k}t">de temps gagné</div></div>']
    vals = [0, 40, 90, 150, 210, 260, 290, 300]
    tw = _init(f'#{k}', f'#{k}t') + [f"gsap.set('#{k}u',{{scaleX:0}});"]
    tw += [f"tl.set('#{k}n',{{textContent:'+{v}%'}},{a + .3 * i / (len(vals) - 1):.3f});" for i, v in enumerate(vals)]
    tw += [
        f"tl.fromTo('#{k}',{{autoAlpha:0,y:50,scale:.82}},{{autoAlpha:1,y:0,scale:1,duration:.3,ease:'back.out(1.6)',immediateRender:false}},{a:.3f});",
        f"tl.fromTo('#{k}u',{{scaleX:0}},{{scaleX:1,duration:.3,ease:'power3.inOut',immediateRender:false}},{a + .22 * s:.3f});",
        f"tl.fromTo('#{k}t',{{autoAlpha:0,y:16}},{{autoAlpha:1,y:0,duration:.25,ease:'power2.out',immediateRender:false}},{a + .38 * s:.3f});",
        f"tl.to('#{k}n',{{scale:1.04,duration:{b - a - .7:.3f},ease:'none'}},{a + .4:.3f});",
    ] + _hide(f'#{k}', b) + [f"tl.set('#{k}t',{{autoAlpha:0}},{b:.3f});"]
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 55 dot counter
def dot_counter(a, b, k):
    s = _sc(a, b)
    D, G, W = 70, 24, 380
    total = W + 2 * (G + D)
    P0 = (1080 - total) // 2
    x0 = (1080 - (3 * D + 2 * G)) // 2
    top = 330
    css = f'''
.{k}o{{position:absolute;z-index:40;top:{top}px;height:{D}px;border-radius:{D // 2}px;background:{PILL};box-shadow:0 6px 20px rgba(42,26,16,.35)}}
#{k}p{{left:{P0}px;width:{W}px;transform-origin:{D // 2}px 50%;display:flex;align-items:center;justify-content:center;gap:12px;
  font:italic 700 42px/1 Poppins;color:#fff;text-shadow:{LAB_SHADOW};text-transform:lowercase}}
#{k}p b{{font:400 42px/1 Anton;font-style:normal;letter-spacing:.02em}}
#{k}l{{position:absolute;z-index:40;left:0;right:0;top:{top + D + 22}px;text-align:center;font:italic 600 42px/1 Poppins;color:{CREAM};
  text-shadow:0 3px 12px rgba(0,0,0,.65)}}
'''
    front = [f'<div id="{k}p" class="{k}o"><span id="{k}pt"><b>1/3</b> les coupes</span></div>']
    sels = [f'#{k}p']
    for i in (1, 2):
        fx = P0 + W + G + (i - 1) * (D + G)
        ix = x0 + i * (D + G)
        front.append(f'<div id="{k}d{i}" class="{k}o" style="left:{fx}px;width:{D}px"></div>')
        sels.append((f'#{k}d{i}', ix - fx))
    front.append(f'<div id="{k}l">3 choses à savoir</div>')
    clip0 = f"inset(0px {W - D}px 0px 0px round {D // 2}px)"
    clip1 = f"inset(0px 0px 0px 0px round {D // 2}px)"
    tp = a + .55 * s
    tw = _init(f'#{k}p', f'#{k}d1', f'#{k}d2', f'#{k}l', f'#{k}pt')
    tw += [f"gsap.set('#{k}p',{{clipPath:'{clip0}',x:{x0 - P0}}});",
           f"tl.fromTo('#{k}p',{{autoAlpha:0,scale:0}},{{autoAlpha:1,scale:1,duration:.22,ease:'back.out(2.6)',immediateRender:false}},{a:.3f});"]
    for i, (sel, dx) in enumerate(sels[1:], 1):
        tw += [f"gsap.set('{sel}',{{x:{dx}}});",
               f"tl.fromTo('{sel}',{{autoAlpha:0,scale:0,x:{dx}}},{{autoAlpha:1,scale:1,x:{dx},duration:.22,ease:'back.out(2.6)',immediateRender:false}},{a + i * .1 * s:.3f});",
               f"tl.to('{sel}',{{x:0,autoAlpha:.55,duration:.32,ease:'power3.inOut'}},{tp:.3f});"]
    tw += [
        f"tl.to('#{k}p',{{x:0,clipPath:'{clip1}',duration:.32,ease:'power3.inOut'}},{tp:.3f});",
        f"tl.fromTo('#{k}pt',{{autoAlpha:0,x:-14}},{{autoAlpha:1,x:0,duration:.2,ease:'power2.out',immediateRender:false}},{tp + .16:.3f});",
        f"tl.fromTo('#{k}l',{{autoAlpha:0,y:-10}},{{autoAlpha:1,y:0,duration:.25,ease:'power2.out',immediateRender:false}},{a + .3 * s:.3f});",
    ]
    for sel in (f'#{k}p', f'#{k}d1', f'#{k}d2', f'#{k}l', f'#{k}pt'):
        tw += _hide(sel, b)
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 56 chip row
def chip_row(a, b, k):
    s = _sc(a, b)
    items = ['coupes', 'sous-titres', 'effets']
    css = f'''
.{k}c{{position:absolute;z-index:40;left:0;right:0;top:1230px;text-align:center;font:800 84px/1 Poppins;color:#fff;
  text-transform:lowercase;letter-spacing:-.01em;text-shadow:{CAP_SHADOW}}}
#{k}r{{position:absolute;z-index:40;left:70px;right:70px;top:1360px;display:flex;justify-content:center;gap:18px}}
.{k}p{{padding:16px 32px 18px;border-radius:999px;background:{PILL};font:italic 700 44px/1 Poppins;color:#fff;
  text-shadow:{LAB_SHADOW};text-transform:lowercase;box-shadow:0 8px 22px rgba(42,26,16,.35);white-space:nowrap}}
'''
    front = [f'<div id="{k}c{i}" class="{k}c">{w}</div>' for i, w in enumerate(items)]
    front.append(f'<div id="{k}r">' + ''.join(f'<div id="{k}p{i}" class="{k}p">{w}</div>' for i, w in enumerate(items)) + '</div>')
    iv = .24 * s
    tw = []
    for i in range(len(items)):
        t = a + i * iv
        end = a + (i + 1) * iv if i < len(items) - 1 else b
        cs, ps = f'#{k}c{i}', f'#{k}p{i}'
        tw += _init(cs, ps)
        tw += [f"tl.fromTo('{cs}',{{autoAlpha:0,scale:.85}},{{autoAlpha:1,scale:1,duration:.12,ease:'back.out(2)',immediateRender:false}},{t:.3f});"]
        tw += [f"tl.set('{cs}',{{autoAlpha:0}},{end:.3f});"] if i < len(items) - 1 else _hide(cs, b)
        tw += [f"tl.fromTo('{ps}',{{autoAlpha:0,scale:.3,y:34}},{{autoAlpha:1,scale:1,y:0,duration:.26,ease:'back.out(2.2)',immediateRender:false}},{t + .04:.3f});"]
        tw += _hide(ps, b)
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 57 serif flow
def serif_flow(a, b, k):
    s = _sc(a, b)
    xs, ly = [170, 470, 770], 132
    steps = ['filmer', 'envoyer', 'poster']
    css = f'''
#{k}{{position:absolute;z-index:40;left:70px;top:296px;width:940px;height:270px;border-radius:34px;background:rgba(42,26,16,.94);
  border:1px solid rgba(233,201,143,.28);box-shadow:0 24px 60px rgba(0,0,0,.45)}}
#{k}h{{position:absolute;left:0;right:0;top:30px;text-align:center;font:italic 400 36px/1 'DM Serif Display';color:{GOLD};letter-spacing:.01em}}
#{k}ln{{position:absolute;left:{xs[0]}px;top:{ly - 1}px;width:{xs[-1] - xs[0]}px;height:3px;border-radius:2px;background:{PILL};transform-origin:0 50%}}
.{k}n{{position:absolute;top:{ly - 12}px;width:24px;height:24px;margin-left:-12px;border-radius:50%;background:{PILL};
  box-shadow:0 0 0 7px rgba(233,201,143,.16),0 0 22px rgba(233,201,143,.45)}}
.{k}s{{position:absolute;top:{ly + 34}px;width:300px;margin-left:-150px;text-align:center;font:400 64px/1 'DM Serif Display';color:{CREAM}}}
.{k}s i{{font-style:italic;color:{GOLD}}}
'''
    inner = [f'<div id="{k}h">le process</div>', f'<div id="{k}ln"></div>']
    for i, (x, w) in enumerate(zip(xs, steps)):
        lab = f'<i>{w}</i>' if i == len(steps) - 1 else w
        inner += [f'<div id="{k}n{i}" class="{k}n" style="left:{x}px"></div>', f'<div id="{k}s{i}" class="{k}s" style="left:{x}px">{lab}</div>']
    front = [f'<div id="{k}">' + ''.join(inner) + '</div>']
    l0, ld = a + .14 * s, .56 * s
    tw = _init(f'#{k}', f'#{k}h') + [f"gsap.set('#{k}ln',{{scaleX:0}});"] + [
        f"tl.fromTo('#{k}',{{autoAlpha:0,y:-24,scale:.96}},{{autoAlpha:1,y:0,scale:1,duration:.24,ease:'power3.out',immediateRender:false}},{a:.3f});",
        f"tl.fromTo('#{k}h',{{autoAlpha:0}},{{autoAlpha:1,duration:.2,immediateRender:false}},{a + .08:.3f});",
        f"tl.fromTo('#{k}ln',{{scaleX:0}},{{scaleX:1,duration:{ld:.3f},ease:'power1.inOut',immediateRender:false}},{l0:.3f});",
    ]
    for i, x in enumerate(xs):
        frac = (x - xs[0]) / (xs[-1] - xs[0])
        t = l0 + ld * frac - (.04 if i else 0)
        n, st = f'#{k}n{i}', f'#{k}s{i}'
        tw += _init(n, st) + [
            f"tl.fromTo('{n}',{{autoAlpha:0,scale:0}},{{autoAlpha:1,scale:1,duration:.2,ease:'back.out(3)',immediateRender:false}},{t:.3f});",
            f"tl.fromTo('{st}',{{autoAlpha:0,y:18,filter:'blur(6px)'}},{{autoAlpha:1,y:0,filter:'blur(0px)',duration:.26,ease:'power2.out',immediateRender:false}},{t + .03:.3f});",
            f"tl.set('{n}',{{autoAlpha:0}},{b:.3f});", f"tl.set('{st}',{{autoAlpha:0}},{b:.3f});"]
    tw += _hide(f'#{k}', b) + [f"tl.set('#{k}h',{{autoAlpha:0}},{b:.3f});"]
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 58 phone mockup
def phone_mockup(a, b, k):
    css = f'''
#{k}w{{position:absolute;z-index:40;left:84px;top:300px;width:290px;height:600px;perspective:1400px}}
#{k}{{position:absolute;inset:0;border-radius:48px;background:#15100c;padding:11px;border:2px solid #4a3627;
  box-shadow:inset 0 0 0 2px #000,30px 44px 80px rgba(0,0,0,.55);transform-style:preserve-3d}}
#{k}s{{position:relative;width:100%;height:100%;border-radius:38px;overflow:hidden;background:#000}}
#{k}v{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#{k}i{{position:absolute;left:50%;top:12px;width:84px;height:24px;margin-left:-42px;border-radius:12px;background:#000}}
#{k}f{{position:absolute;left:0;right:0;bottom:0;height:170px;background:linear-gradient(transparent,rgba(0,0,0,.7))}}
#{k}u{{position:absolute;left:16px;bottom:22px;display:flex;align-items:center;gap:8px;font:600 15px/1 Poppins;color:#fff}}
#{k}u img{{width:28px;height:28px;border-radius:50%;border:1.5px solid #fff;object-fit:cover}}
#{k}c{{position:absolute;left:16px;bottom:62px;font:italic 700 17px/1.1 Poppins;color:#fff;text-shadow:{LAB_SHADOW};
  padding:7px 12px;border-radius:999px;background:{PILL}}}
#{k}g{{position:absolute;inset:0;border-radius:38px;background:linear-gradient(115deg,rgba(255,255,255,.22) 0,rgba(255,255,255,0) 38%)}}
'''
    vid = (f'<video id="{k}v" src="assets/rawclip.mp4" muted playsinline data-start="{a:.3f}" data-media-start="0" '
           f'data-duration="{b - a:.3f}" data-track-index="{100 + 58 * 3}"></video>')
    front = [f'<div id="{k}w"><div id="{k}"><div id="{k}s">{vid}<div id="{k}f"></div>'
             f'<div id="{k}c">avant montage</div>'
             f'<div id="{k}u"><img src="assets/avatar.png" alt="">thestrategicboost.fr</div><div id="{k}i"></div><div id="{k}g"></div></div></div></div>']
    tw = _init(f'#{k}w') + [
        f"gsap.set('#{k}',{{rotationY:25,rotationZ:-5}});",
        f"tl.set('#{k}w',{{autoAlpha:1}},{a:.3f});",
        f"tl.fromTo('#{k}',{{x:-560,y:80,rotationY:75,rotationZ:-28,scale:.85}},{{x:0,y:0,rotationY:25,rotationZ:-5,scale:1,duration:.42,ease:'power3.out',immediateRender:false}},{a:.3f});",
        f"tl.to('#{k}',{{y:-16,rotationY:20,rotationZ:-3,duration:{b - a - .45:.3f},ease:'sine.inOut'}},{a + .42:.3f});",
    ] + _hide(f'#{k}w', b)
    return dict(front=front, tw=tw, css=css)


# ------------------------------------------------------------------ 59 comment bubble
def comment_bubble(a, b, k):
    s = _sc(a, b)
    word = 'MONTAGE'
    heart = ('<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#8C5C41" stroke-width="2">'
             '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>')
    css = f'''
#{k}{{position:absolute;z-index:40;left:70px;top:290px;width:940px;height:356px;border-radius:36px;background:{CREAM};
  box-shadow:0 26px 64px rgba(0,0,0,.42);overflow:hidden;font-family:Poppins;color:{INK}}}
#{k}gr{{position:absolute;left:50%;top:14px;width:70px;height:6px;margin-left:-35px;border-radius:3px;background:rgba(42,26,16,.18)}}
.{k}row{{position:absolute;display:flex;align-items:flex-start;gap:20px}}
.{k}av{{flex:none;border-radius:50%;object-fit:cover}}
.{k}ini{{display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,{BROWN},{DARK});color:{CREAM};font:700 30px/1 Poppins}}
.{k}nm{{font:700 26px/1.2 Poppins;color:{INK}}}
.{k}nm span{{font-weight:600;color:rgba(42,26,16,.5);margin-left:10px}}
.{k}tx{{font:600 34px/1.25 Poppins;color:{INK};margin-top:4px}}
#{k}r1{{left:36px;top:44px;right:36px}}
#{k}r1 .{k}h{{margin-left:auto;margin-top:16px}}
#{k}r2{{left:126px;top:156px}}
#{k}tag{{display:inline-block;margin-left:10px;padding:4px 12px 5px;border-radius:999px;background:{PILL};font:italic 700 18px/1 Poppins;color:#fff;text-shadow:1px 1px 0 rgba(42,26,16,.8);vertical-align:3px}}
#{k}in{{position:absolute;left:28px;right:28px;bottom:24px;height:78px;border-radius:39px;border:2px solid rgba(42,26,16,.16);background:#fff;
  display:flex;align-items:center;gap:16px;padding:0 12px 0 12px}}
#{k}tt{{font:600 32px/1 Poppins;color:{INK};letter-spacing:.02em}}
#{k}ph{{position:absolute;left:84px;font:500 30px/1 Poppins;color:rgba(42,26,16,.38)}}
#{k}ca{{width:3px;height:36px;background:{BROWN};margin-left:-12px}}
#{k}pb{{margin-left:auto;margin-right:14px;font:700 28px/1 Poppins;color:{BROWN}}}
'''
    front = [f'''<div id="{k}"><div id="{k}gr"></div>
  <div id="{k}r1" class="{k}row"><div class="{k}av {k}ini" style="width:72px;height:72px">c</div>
    <div><div class="{k}nm">camille.crea<span>à l'instant</span></div><div class="{k}tx">{word}</div></div><div class="{k}h">{heart}</div></div>
  <div id="{k}r2" class="{k}row"><img class="{k}av" src="assets/avatar.png" alt="" style="width:62px;height:62px">
    <div><div class="{k}nm">thestrategicboost.fr<b id="{k}tag">auteur</b></div><div class="{k}tx">je t'envoie le lien 🔗</div></div></div>
  <div id="{k}in"><div class="{k}av {k}ini" style="width:54px;height:54px;font-size:24px">c</div><div id="{k}ph">ajoute un commentaire…</div>
    <div id="{k}tt"></div><div id="{k}ca"></div><div id="{k}pb">Publier</div></div>
</div>''']
    t1, t2 = a + .06, a + .36 * s
    tp, tr = t2 + .06, a + .62 * s
    tw = _init(f'#{k}', f'#{k}r1', f'#{k}r2', f'#{k}ph') + [
        f"gsap.set('#{k}pb',{{opacity:.35}});",
        f"tl.fromTo('#{k}',{{autoAlpha:0,y:-30,scale:.95}},{{autoAlpha:1,y:0,scale:1,duration:.24,ease:'power3.out',immediateRender:false}},{a:.3f});",
        f"tl.set('#{k}ph',{{autoAlpha:1}},{a:.3f});", f"tl.set('#{k}ph',{{autoAlpha:0}},{t1:.3f});",
    ] + typing(f'#{k}tt', word, t1, t2) + [
        f"tl.set('#{k}pb',{{opacity:1}},{t1 + .05:.3f});",
        f"tl.to('#{k}pb',{{scale:.88,duration:.06,yoyo:true,repeat:1}},{t2:.3f});",
        f"tl.set('#{k}tt',{{textContent:''}},{tp:.3f});", f"tl.set('#{k}pb',{{opacity:.35}},{tp:.3f});",
        f"tl.set('#{k}ph',{{autoAlpha:1}},{tp:.3f});",
        f"tl.fromTo('#{k}r1',{{autoAlpha:0,y:60,scale:.96}},{{autoAlpha:1,y:0,scale:1,duration:.24,ease:'back.out(1.6)',immediateRender:false}},{tp:.3f});",
        f"tl.fromTo('#{k}r2',{{autoAlpha:0,x:40,y:20}},{{autoAlpha:1,x:0,y:0,duration:.26,ease:'back.out(1.7)',immediateRender:false}},{tr:.3f});",
    ] + _hide(f'#{k}', b) + [f"tl.set('{s_}',{{autoAlpha:0}},{b:.3f});" for s_ in (f'#{k}r1', f'#{k}r2', f'#{k}ph')]
    return dict(front=front, tw=tw, css=css)


EFFECTS = [
    (51, 'RACK FOCUS', rack_focus),
    (52, 'GOD RAYS', god_rays),
    (53, 'DEPTH SCATTER', depth_scatter),
    (54, 'STAT STACK', stat_stack),
    (55, 'DOT COUNTER', dot_counter),
    (56, 'CHIP ROW', chip_row),
    (57, 'SERIF FLOW', serif_flow),
    (58, 'PHONE MOCKUP', phone_mockup),
    (59, 'COMMENT BUBBLE', comment_bubble),
]
