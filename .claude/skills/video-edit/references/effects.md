# Effects library (32 named effects + recipes)

Source: the "Les effets Claude" reel (Drive, 20 s, 18 effects named on screen in a running checklist). Each effect
below says what it looks like, when to use it, and how to build it in HyperFrames/GSAP. Ask for an effect by its
name ("mets un Gravity drop sur le hook", "fais un Icon strike sur CapCut").

Maé's rules still win over the source look: his green panels become her dark brown #573307 / brown #8C5C41 with
gold accents (never yellow), titles Anton, text Poppins, captions one word at a time (white, black shadow, lowercase),
real logos/photos only, every element inside the safe zone (top 0-240, right x>920 from y1000, bottom from y1700,
~80px side margins). Only show what her script says.

Every recipe uses the build.py helpers (`tl`, `show()`, `pop()`, `audio()` SFX lanes). `t` = the word time from
faster_whisper. Hide each element with `tl.set(...,{autoAlpha:0},end)` so scrubbing stays clean.

## Text effects

### 01 Kinetic hook
Hook words slam in as two stacked lines of heavy type, the second line half-covered by a solid colour block that
wipes off. Use on the first 1-2 s.
- Anton 150-190px, white with black shadow, lines stacked tight (line-height .9).
- Each line: `fromTo({y:80,scaleY:1.4,autoAlpha:0},{y:0,scaleY:1,autoAlpha:1,duration:.28,ease:'expo.out'})`, 0.12 s stagger.
- A #573307 block covers line 2 then `scaleX:1→0` (transform-origin right) over .25 s. SFX: whoosh-short + pop.

### 02 Gravity drop
A small italic word ("gravity") sits above, then the big word drops letter by letter as if falling with weight.
- Split the word into `<span>` per letter. Letters `fromTo({y:-260,rotation:gsap.utils.random(-12,12)},{y:0,rotation:0,
  duration:.55,ease:'bounce.out',stagger:.06})`.
- The small word above: Poppins italic 54px in gold (or Anton small), fades in first.
- Good for one key word per sentence. SFX: a soft impact on the last letter.

### 03 Giant captions
One word fills the width, mixing a block-letter word (Anton on a #573307 band) with a big italic word under it that
runs off the screen edge. Use for the 1-2 words that carry the message, not for every line.
- Word A: Anton 140px white on a dark-brown band that wipes in (`clipPath inset(0 100% 0 0)→inset(0 0 0 0)`).
- Word B: Poppins italic 200px, slides in from the right (`x:300→0`) and is allowed to bleed past the side margin.
- Hold .6-.8 s, exit `y:-40, autoAlpha:0`.

### 13 Title card
A full-screen solid brown card with a timecode and a big title, then the card shrinks into a phone frame holding
the video. Use as a chapter break or the reveal of the main point.
- Card `#573307` full screen, timecode Poppins 28px gold letter-spacing .2em, title Anton 160px white.
- Out: the A-roll is wrapped in a rounded "phone" div (border 18px #F3E9DC, radius 70px); `fromTo(scale:1.25→.86)`
  while the card fades. Keep the phone frame inside the side margins.

## UI recreations (glass cards, real logos)

### 04 Prompt bar
An AI chat input bar types the line, then the send arrow pulses. Use when she says what she asked the AI.
- White card, radius 40px, small label "PROMPT" Poppins 18px letter-spacing .2em, text Poppins 34px #222.
- Typing: reveal characters with a stepped tween over the spoken duration, caret blinking.
- Send button: brown circle #8C5C41 with a white arrow, `scale 1→.85→1` on the last word. SFX: click-soft.

### 05 Storyboard deck
A row of 4-5 reel thumbnails (real covers from her account) fans in as a deck. Use for "mes vidéos", examples, series.
- Cards 160×280 radius 18, real screenshots. `from({y:200,rotation:-8,autoAlpha:0},{stagger:.07,ease:'back.out(1.6)'})`.
- Lay them in a gentle arc (rotation -6..6), placed bottom-third but above y1700.

### 06 Icon strike
Real app logos appear with their names, then one gets struck out with a hand-drawn red line (an italic word
"strike" may write above). Use for "pas besoin de X", "j'ai arrêté X".
- Logos 150px with radius 34 and drop shadow, label Poppins 26px.
- The strike: an SVG path with `stroke-dasharray`; animate `strokeDashoffset: len→0` over .25 s, red #E5262B,
  12px, round caps, slightly tilted. Logo then `scale:.9, opacity:.5`. SFX: a quick swish.

### 07 File drop
A dashed upload zone ("Dépose ta vidéo brute") appears, then a video file thumbnail flies in and lands in it with
its file name. Use for "j'envoie mes rushs", "je dépose ma vidéo".
- Zone: glass card (rgba(58,38,26,.55) + blur 22px), 2px dashed border white 60%, download icon + Poppins 32px.
- File: a small portrait thumbnail (a frame of her clip) + file name "IMG_4021.MOV", `fromTo({x:-260,y:-120,
  rotation:-14,scale:.6},{x:0,y:0,rotation:0,scale:1,duration:.45,ease:'power3.out'})`, zone border flashes gold.

### 08 NLE timeline
An editing timeline (video track of thumbnails, text track, waveform audio track) slides up and a playhead runs
across. Use when she talks about editing or "le montage".
- Dark-brown panel 900×330, tracks V1/V2/A1, thumbnails from her own clip (ffmpeg tile), gold text clips,
  waveform drawn as bars. Timecode Poppins mono-ish 22px at the top.
- Panel `from({y:120,autoAlpha:0})`, playhead `x:0→840` linear over the shot, clips `scaleX` in one by one.

### 09 Jiggle delete
The iPhone "edit mode": app icons jiggle with a minus badge, then one gets deleted and the others slide over.
Use for "j'ai supprimé…", "plus besoin de…".
- White glass bar with "EDIT MODE" label and real logos. Jiggle: `rotation:-3↔3, yoyo, repeat:-1, duration:.12`
  with random offset per icon. Delete: `scale→0, autoAlpha:0` then remaining icons `x` shift (Flip-style).
- Counter text updates ("4 apps" → "3 apps"). SFX: click-soft on delete.

### 10 Grade slider
Before/after colour slider: a vertical white line with a round handle sweeps across her face, "AVANT"/"APRÈS"
labels each side. Use for "regarde la différence", colour or lighting tips.
- Two stacked copies of the A-roll: raw under, graded (lilac.py output) on top with `clip-path: inset(0 0 0 X%)`.
- Animate X 100→50→0 with ease 'power2.inOut'; handle = 64px circle #573307 with ‹ › white.
- Both videos must share data-start/media-start so they stay frame-locked.

### 11 Eyedropper grade
An eyedropper cursor taps the frame, a palette strip of sampled hex swatches appears, and the image re-grades to
that palette. Use for colour/branding talk ("ma charte", "mes couleurs").
- Cursor: SVG eyedropper moving with `motionPath` or x/y keyframes, `scale .9` tap on each sample.
- Swatch strip: white card with 5 swatches + hex codes (her real colours #573307, #8C5C41, gold, white, lilac).
- The re-grade: crossfade between two pre-rendered grades of the A-roll (ffmpeg colour filters), never CSS filters
  on the video (slow and inconsistent in render).

### 12 Film look
A quick switch to a film look: grain, slight halation, warmer/softer contrast, a light gate weave. Use for one
nostalgic or "cinéma" beat.
- Pre-render the look with ffmpeg on the segment: `noise=alls=12:allf=t, curves=preset=vintage` (soften), plus a
  1-2px `crop`+`pad` jitter for weave; crossfade 0.15 s in and out.

## Social UI

### 14 Playing grid
A grid of her reels (real covers) playing at once, popping in tile by tile around her. Use for "j'ai posté X vidéos",
proof of consistency.
- 3×2 tiles 190×340 radius 16 around the head (keep the face clear), `stagger:{each:.05,from:'random'}`, scale .6→1.
- Each tile is a muted `<video>` of a real reel or a still cover.

### 15 Reel feed
Swipe through 2-3 real reels in the Instagram UI (right-side counters, name, follow), like scrolling the feed. Use
when she quotes another creator or shows examples.
- Full-screen inserts, each `y:1920→0` with 'power3.inOut' .35 s (the swipe), counters as real IG icons.
- Only real reels she gives us (no invented creators), and her own IG UI measurements for placement.

### 16 Video card
The talking head shrinks into a rounded video card (thumbnail + title + "01 · La prise brute" subtitle) in the top
third, like a YouTube/course card. Use to present a "step" or a module.
- Wrapper div around the A-roll: `scale 1→.42, x/y to the card spot, borderRadius 0→24`, card body (brown glass)
  grows under it with title Anton 46px and subtitle Poppins 24px.
- Return: reverse tween. Keep a second, full A-roll underneath only if the card is small; otherwise a brown backdrop.

### 17 Comment CTA
A comment bubble with her avatar types the keyword, then a reply notification slides in under it ("Envoyé, regarde
tes DM"). Use for "commente X".
- Bubble: white, radius 34, avatar 52px, "toi · maintenant" Poppins 18px grey, keyword Anton 40px.
- Typing as in Prompt bar, heart icon pops at the end; reply card `from({y:-30,autoAlpha:0})` .3 s later.
- The keyword in her caption line gets the brown highlight.

### 18 Comment drop
The keyword's letters fall one by one from above into an "Ajouter un commentaire…" field, then "Publier" lights up.
Use as the very last beat after the Comment CTA.
- Letters Anton 120px white, `from({y:-400,rotation:random(-20,20)}, {ease:'bounce.out',stagger:.08})`, each lands
  and swaps into the field text (Poppins 32px). Post button #8C5C41 → brighter on finish. SFX: pop per letter (low vol).

## Running checklist (the frame that ties them together)
The source keeps a side panel "DANS CETTE VIDÉO 03/18" listing every item, the current one highlighted in a white
pill and the counter ticking. For Maé, use it on list reels (tips, tools, steps) only:
- Brown glass panel 260px wide, left of x 920 (never under the IG buttons), from y 260, Poppins 22px items with
  "01" numbers in gold, active item white pill with dark text, `tl.to` the pill's `y` at each item's word time.
- A final gold tag ("+40 effets" style) only if her script says it.

# Second batch (reel "17 video effects claude can create", Drive 1bL21vorgOFQiUccVdxGEH4TMlASAGZhN)

Already covered above, so not repeated here: "phone mockup" is close to 13 Title card and 04 Prompt bar, "checklist"
to the Running checklist (see the variant below), "pull-back reveal" to 16 Video card (variant below), and the
end "comment STUDIO" to 17 Comment CTA. Most of these effects need her cut out (`$HF remove-background` →
transparent WebM layered over the background). Each name works as a request ("fais un Orbit sur l'intro").

### 19 Orbit
Small reel cards (real covers) circle around her, passing behind her body and then in front.
- Cutout on top of the A-roll; cards in two layers: `z-index` below the cutout during the back half of the orbit and
  above it during the front half (swap with `tl.set` at each half turn).
- Position on an ellipse: `x = cx + R*cos(a)`, `y = cy + r*sin(a)`, scale .7 at the back and 1 at the front; drive `a`
  with a proxy object `tl.to(o,{a:Math.PI*2,duration:2.4,ease:'none',onUpdate})`. 3-4 cards, 150×260, radius 16.

### 20 Couch wall
The wall behind her becomes a mosaic of her own reel screenshots, popping in tile by tile. Use for "j'ai fait des
dizaines de vidéos", proof or social proof.
- Cutout in front; behind it a grid of 6-9 real screenshots slightly rotated, `stagger:{each:.04,from:'center'}`,
  `scale .6→1`, darkened 15% so she stays the focus. Wall fades back to the real room after 1.5-2 s.

### 21 UI world
Her real background is replaced by a clean app world (soft white/cream gradient), with a prompt bar typing above her
head. Use when she talks about a tool, an AI or "dans l'appli".
- Cutout over a cream gradient (#F6EFE6 → #E9DCCB for her), Prompt bar (04) at the top, small app name above it.
- Crossfade room → UI world .2 s; she stays the same size and place, only the world changes.

### 22 Frame break
The video shrinks into a rounded phone-like frame on a dark blurred backdrop, and she leans out of the frame (her
head and hands go over the border). Use for a surprise beat or "sors de ta zone de confort".
- Layer order: blurred darkened A-roll (backdrop) → framed A-roll (rounded 40px, white 3px border) → cutout on top,
  clipped so only the part outside the frame shows above the top edge (`clip-path` on the cutout: inset to keep the
  part above the frame's top line and below its bottom).
- Frame `fromTo(scale:1→.62)` .4 s 'power3.inOut'.

### 23 Digital zoom
A punch-in on the face (scale 1→1.35) on a key word, held, then a cut back. The classic emphasis.
- Use the 4K source when available (crop, not upscale). `tl.to('#bgv',{scale:1.35,duration:.12,ease:'power2.out'})`,
  `transform-origin` on her face (eyes.json from eyes.py gives the point). Reset with a hard `tl.set` on the next cut.

### 24 Headline wall
Press-style clippings (paper cut-outs, a tweet card, a search bar "can claude edit videos") pin onto the wall around
her. Use for "tout le monde en parle", news, trends.
- 4-6 cards, each a different style: serif paper clipping, white notification card, search bar typing; gentle
  rotations -6..6, `from({scale:1.3,autoAlpha:0})` .2 s each, staggered .15 s. Real headlines only.
- Keep them in the side columns, clear of her face and of the IG right buttons.

### 25 Zoom-through cut
A transition: the camera pushes fast into a dark area (her jacket, a shadow) until the screen is black, and the next
shot starts from that darkness. Use between two parts of the reel.
- Shot A: `scale 1→4` in .25 s 'power3.in' toward a dark point + motion blur (a few semi-transparent copies or a
  pre-rendered ffmpeg `tblend`). Shot B starts at `scale 1.4→1` .3 s 'power3.out'. SFX: whoosh-short.

### 26 Chart grow
A glowing line chart draws itself behind her and shoots up at the end, with dots popping on each point. Use for
growth, stats, "+300 abonnées".
- SVG polyline over the room, behind the cutout; draw with `strokeDashoffset`, points `scale 0→1` as the line reaches
  them, last point gets a halo ring pulsing. Gold line (#D6AE66) with a soft glow (`drop-shadow`), thin white grid.
- Real numbers from her script only.

### 27 Green screen
She is cut out and stands in front of a different shot (a screenshot, another clip, a place), shown as a framed card
above her or full screen. Use to "show" what she talks about while she keeps talking.
- Backdrop dark brown or blurred; the other clip in a rounded card in the upper half; cutout in the lower half in
  front. Card `from({y:-60,autoAlpha:0})` .3 s.

### 28 Paper cut
Scrapbook collage: she becomes a sticker (white outline), on a background of paper scraps, tape, scribbles, with a
ransom-note title (letters cut from different papers). Use for a playful or "DIY" beat.
- Outline: dilate the cutout's alpha (ffmpeg `alphaextract`, `dilation` ×6, colour white) and stack under the cutout.
- Title: one `<span>` per letter, each with its own paper colour (cream, brown #8C5C41, gold, white), font (Anton /
  Poppins) and tilt; letters `from({scale:0,rotation:random(-30,30)},{stagger:.05,ease:'back.out(2)'})`.
- Background: real paper/tape textures (Unsplash), not drawn shapes.

### 29 Doodle boil
A hand-drawn white line traces around her body and "boils" (jitters like a cartoon), with small doodles (heart,
sparkles) next to her. Use for a light, fun moment.
- Same outline as Paper cut but as a thin stroke; boil = 3 slightly different versions (displace each with
  `feTurbulence` seeds 1/2/3) switched every 0.08 s (`tl.set` loop). Doodles in white or gold, same 3-frame boil.

### 30 Vertigo
Dolly zoom: she stays the same size while the room behind her stretches away (or rushes in). Use on a shock line
("et là, tout a changé").
- Needs the cutout: background layer `scale 1→1.5` while the cutout stays at scale 1 (or background 1.5→1). 1-1.5 s,
  'power1.inOut'. Works best with a deep room; slight blur on the background sells it.

### 31 Cover story
Her shot becomes a magazine cover: a huge serif masthead behind her head (e.g. "STUDIO"), small cover lines in the
corners, thin border. Use for a launch, a "nouvelle" or her own offer.
- Masthead behind the cutout (head overlaps it, behind-head formula in layout.md). For her use Anton (no serif), white,
  letter-spacing .05em, 220px; cover lines Poppins 18px uppercase. Letters reveal with `clip-path` from the bottom.

### 32 Glass type
A big 3D glass word sits behind her head: transparent letters with bevel highlights and the room refracted
through them. Use for one brand word ("CONTENU", "STRATÉGIE").
- Behind the cutout. Letters: Anton 200px, `color: transparent`, `-webkit-text-stroke: 2px rgba(255,255,255,.7)`,
  a white→transparent gradient fill with `background-clip:text` at 25% opacity, plus `backdrop-filter: blur(6px)` on a
  text-shaped mask for the frosted look. Fade + slow `y:20→0`.

## Bonus moves seen in this reel
- **Blur-in caption line**: the key part of a sentence appears big under the small line, going from `filter:blur(14px)`
  to sharp in .25 s, and the line blurs out at the end. For her: white Poppins, bigger, no yellow.
- **Profile follow card**: her real IG profile card (photo, counters, grid) slides up, a finger taps "Suivre" which
  turns into "Abonné(e)". Use on "abonne-toi". Real screenshot of her profile, just animate the button.
- **Checklist (variant of the running checklist)**: a small dark glass widget "3 étapes" whose items tick one by one
  (empty circle → gold check) on the words. Good for 3-step tips.
- **Pull-back reveal (variant of Video card)**: the video pulls back into an app window with a side panel "En cours"
  ticking tasks and a progress bar. For "voici comment je fais".
