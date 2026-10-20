# Looks (exact values)

All three live in `assets/template/build.py`. Accent everywhere: butter yellow `#FAE67A`.
The user's default look is in `config.json` (`defaultLook`); a line in the script that names a look
("you can get the cool girl aesthetic like this") switches that section to it.

## Bold (default base look)
Kinetic lowercase words placed around the speaker, the big ones tucked BEHIND the head.
- Grade on footage layers (`.g` = base video + cutout): `contrast(1.07) saturate(.9) brightness(.97)`, plus a soft-light teal/warm tone, light vignette, and dark gradients top/bottom for legibility. Keep skin natural: darker versions push faces red.
- Type: Inter Tight, lowercase, `letter-spacing:-.05em`, `line-height:.9`, white with soft shadow `0 10px 40px rgba(0,0,0,.55)`.
  - `sm` 84px/800 lead-in lines, `sm2` 56px/800 for long lines, `md` 150px, `big` 236px, `xl` 220px, `huge` 300px (900 weight). Yellow `y` class for the punch word.
- Layout: lead-in lines CENTRED in front of the speaker over the chest band (y ~950-1300). Lines pinned to the left edge look off.
- Big punch words BEHIND the head (`back` class sits below the cutout layer). Only the bottom ~25-30% of the letters may be covered (formula in layout.md); a fully hidden middle ("cla_de") reads as broken.
- Motion: each word blur-pops in on its spoken frame (`scale 1.22 + blur 22px -> 1`, .2s power3.out); groups blur out (.12s) and are hard-killed with `tl.set`.
- Every cut gets a punch (`#stage` scale 1.05 -> 1 over .32s).

## Cool girl
- Grade: `sepia(.18) saturate(.9) contrast(.93) brightness(1.05) hue-rotate(-5deg)` + warm soft-light overlay + soft warm vignette.
- Type: small calm lowercase Inter 500 (64px) + one punch line in **Instrument Serif italic** in butter yellow (200px in the top band, 150px for lower blocks so 3 words fit one line). Cream text `#FFF8EF`.
- Accents: yellow sparkles (✦) twinkling near the italic, optional handwritten note in Caveat 600 with a drawn SVG arrow (strokeDashoffset).
- No date/time stamps: they read as clutter.
- Signature move: the creator's own reels orbit them (orbit() in the template). Each reel tile exists twice (back copy below the cutout, front copy above), positions precomputed as GSAP keyframes every 0.1s around an ellipse, autoAlpha swapping at the ring's left/right extremes. Tiles 190x338, cream border. Keep the ring inside the safe zone.

## Cool dude (editorial studio look)
Inspired by high-end studio interview edits: dark room, lit subject, tiny tracked caps and big serif words.
- Grade: room `contrast(1.1) saturate(.84) brightness(.8) hue-rotate(-4deg)`, the speaker cutout lifted: `contrast(1.06) saturate(.86) brightness(.98)` so they stay lit while the room falls back. Teal soft-light tone + vignette (.5) + bottom gradient. Dark is good; NO film grain (it reads as noise on faces).
- Type: tiny wide-tracked caps in **Montserrat 500** (34px, letter-spacing .32em, words can be spread across the width with flex space-between) + heavy lowercase punch words in **DM Serif Display** (210-270px, italic for the final word). Cream `#F7F4EE`.
- Motion: serif letters rise from a mask (`yPercent 115 -> 0`, stagger .028, expo.out) with a blur/scale settle; tracked words "track in" via `scaleX 1.45 -> 1` + blur (NOT letterSpacing, lint rejects it); quick .45s blur-to-focus into the section; slow push-ins (scale 1 -> 1.05 across a shot) instead of cut punches; one soft light sweep (screen blend) when the section opens.
- Shots: wide, then a ~1.9x close-up cropped from the 4K original (alternate wide/close like a studio interview).
- Tried and dropped: replacing the room with an AI-generated background (looked fake), black and white, crushed-dark grades, film grain.

## Fonts on hand (assets/template/assets/fonts, latin woff2 + fonts.css, SIL Open Font License)
Inter 500/600, Inter Tight 800/900, Instrument Serif italic, DM Serif Display (+italic), Montserrat 500/600, JetBrains Mono 500, Caveat 600.
Add more with the Google Fonts CSS2 API + a Chrome user agent, keep only the `/* latin */` blocks, `font-display:block`.

## Avoid (they looked worse every time)
Orange captions, Anton / condensed poster caps, black and white grades, @handle watermarks in the corner, date stamps.

## Look "DA pro" (Maé's references "Exemple DA1" / "Exemple DA2", Drive)
Editorial, calm, magazine-like: reads as a pro editor, not an AI template. The footage carries it; graphics are rare
and typographic. Rules:
- **Two text levels only.** (1) Small lowercase serif subtitle, one short phrase at a time (2-4 words), white, ~34px,
  centered at chest height (y ~1000-1100), soft shadow only, no box, no pop animation (plain cut or 0.1 s fade).
  (2) On 1-3 key words per reel: a short lead-in in white Poppins SemiBold ~48px (words appearing one by one), then the
  KEY WORD huge in condensed Anton 200-300px, uppercase, brand colour, full width, tight line-height .9; often placed
  BEHIND her head (cutout on top, behind-head formula in layout.md). Lands with a fast scale 1.08→1 / no bounce.
- **Hand-drawn accents**, sparingly: a marker circle around a number ("Étape ①"), a curved arrow pointing to a word,
  a strike-through on the wrong word with the right word written above in a brush script (draw with SVG
  stroke-dashoffset, 0.3 s). Same brand colour.
- **Lists**: numbered lines stacked top-right ("1. son âge", "2. …"), each line appearing on its word, staying until
  the list ends. Step titles "Étape" white + circled number + subtitle line.
- **Camera / cut**: change angle or framing every few seconds (wide, top-down, close-up, lean-in), punch-ins 1.15-1.3
  on emphasis, natural warm grade, no glow/grain gimmicks, no stickers, no emoji, no SFX on every word (only a soft
  whoosh on the big words).
- **Brand mapping for Maé**: the source lime → her gold (#D6AE66) or white for the huge words (test both), the
  marker accents in gold, lead-ins white, subtitles white serif → keep Poppins Light italic if no serif is wanted.
  Her lilac grade stays.
- **Brown explainer screens (Maé loves these, mix them into the DA pro look)**: when she explains something
  (steps, a method, a planning, a comparison), cut to a full-screen brown background and explain it with type and
  widgets, her voice continuing underneath. Reference build: `reels/nouvelle/build.py` (reel "planifier ton contenu en
  45 min", FINAL v6; preview `reels/nouvelle/renders/apercu-v6.jpg`).
  - Background: `radial-gradient(120% 80% at 50% 38%,#9C6B4E 0%,#8C5C41 55%,#734A33 100%)` (`.screen` class there).
  - Header: small "Étape 1" Poppins 600 40px + huge white Anton title (fit to width, `fit()` helper) at top ~250px.
  - Content: frosted glass cards (rgba(255,255,255,.12), white 1.5px border, radius 40), white pill tags in Anton
    with dark-brown text, gold gradient tiles/buttons for highlights, real photos/reel thumbnails, a calendar, a
    table, a mind-map; elements pop in on her words. Captions keep running at the bottom (white, one word).
  - Variant "video in front": the same brown screen with HER VIDEO in a rounded framed card (white 3-4px border,
    radius 36-44, soft shadow) next to or under the explanation, or a small recap card of the screen above her head
    when the shot goes back to her (`.recap` / `.recapCal` there).
  - Rhythm with the DA pro look: talking shots with the subtle editorial text, then a brown screen for each "how",
    then back to her; 1 screen every 5-10 s at most so it still feels edited, not a slideshow.
- **Maé's label style (her charte, use it for every tag / badge / chip / "Étape" label, in reels and documents)**:
  a rounded pill (border-radius 999px) filled with her gold gradient
  `linear-gradient(150deg,#F3DFB2 0%,#D6AE66 45%,#9E6E33 100%)`, text in **Poppins Bold Italic** (700 italic, lowercase / sentence case,
  no letter-spacing) **white with a dark shadow** (`text-shadow:0 2px 4px rgba(50,25,5,.6)`), a light drop shadow under
  the pill. Ref: her "5 TENDANCES à refaire en *octobre*" cover. Not square dark-brown blocks.
