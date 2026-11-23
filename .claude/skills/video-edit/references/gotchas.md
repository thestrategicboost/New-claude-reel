# Gotchas (each one cost a render)

## Timing / sync
- ffmpeg concat -> 0.033s video start offset + VFR gaps -> remove-background outputs extra frames -> the cutout drifts
  (by 20s it lagged a few frames: two copies of the speaker on screen after a cut). assemble.py re-encodes with
  `setpts=N/30/TB -fps_mode cfr`; cutout.py asserts equal frame counts.
- `tl.set` at a rounded time fires one frame late: use `frame/30 - 0.002`.
- `hyperframes snapshot` seeks approximately at cut boundaries; it can show the next shot a frame early. Only frames
  extracted from the final render (`check_cuts.py`) prove a cut.
- When a segment's in-point is trimmed, every hard-coded word time after it shifts. Keep a `SHIFT` derived from
  segments.json and wrap later times in `S(t)` (see template) instead of retyping them.
- Whisper word starts can be ~0.1-0.3s off and it hallucinates a leading word at a cut. Confirm pauses with
  `silencedetect` (n=-40dB, d=0.08) before trimming dead air.

## Rendering
- CSS `-webkit-mask-image` does not survive the renderer. Bake alpha into a VP9 WebM with ffmpeg alphamerge instead.
- `autoAlpha:1` sets opacity to 1 and overrides a CSS `opacity` on the same element. A "3% grain" layer shown with
  autoAlpha ran at 100%. Put low opacity on an inner element or tween opacity to the target value.
- Every `<video>` needs an `id` or it renders frozen. Each overlapping media element needs its own `data-track-index`.
  `<audio>` SFX need ids too, and overlapping SFX need separate track indices (the template's lane allocator does it).
- Never tween autoAlpha/opacity on an element that has data-start (the framework forces opacity 1 on active clips):
  wrap it in a plain div and animate the wrapper.
- Lint rejects tweening letterSpacing (layout snapping): fake tracking with scaleX.
- Element ids cannot contain apostrophes ("i've" broke the whole inline script). Use keys like 'ive'.
- `fromTo` renders its from-state immediately: pass `immediateRender:false` for anything hidden until its time.
- Heavy backdrop-filter/blur on many elements can make captures go black; keep it to a few.

## Assets / tools
- Node 22+ for HyperFrames, pinned `hyperframes@0.8.34`. Start it with `HF` (`PY "SK/scripts/hf.py" <command>`): it
  puts a Node 22+ first on PATH on any OS (an nvm default of Node 20 otherwise gives "HyperFrames requires Node.js >= 22").
- Python scripts run in the skill's own venv. Its path differs per OS (`.venv/bin/python` on Mac and Linux,
  `.venv/Scripts/python.exe` on Windows), so read `python` from `SK/.platform.json` instead of typing it.
  The first transcription downloads the Whisper model (small.en ~0.5GB, medium.en ~1.5GB).
- Transcription dies with `open() got an unexpected keyword argument 'metadata_errors'`: the venv has PyAV 19, which
  faster-whisper 1.2.1 does not support. Run `scripts/setup.py` again (or the old `scripts/setup.sh`, which calls it);
  it pins `av<19` and repairs the venv.
- zsh: `for x in "a b"; do set -- $x` does not split; use `${=x}` or a Python loop.
- If a shell safety hook blocks inline heredoc scripts or moves into the Trash, write the script to a file and run
  it; download temp files into a scratch folder instead of moving things around. Never delete the user's files.
- Large file uploads to chat can fail: deliver a 720p crf 26-28 phone copy and keep the full render on disk.
- Pinterest/Instagram pages block logged-out browsing; curl the page HTML or use Apify.

## Windows (same skill, different shell)
- Claude Code on Windows runs commands in Git Bash when Git for Windows is installed, otherwise in PowerShell, and
  both can be available at once. Write commands that work in both: full paths in double quotes with forward
  slashes, one command per call, no `&&`, no `VAR=1 cmd`, no `~` in arguments. In PowerShell start a quoted program
  with `&`: `& "PY" "SK/scripts/assemble.py" "<project>"`.
- `python3` is usually a Microsoft Store stub ("Python was not found"). Use `PY` for everything. Before the venv
  exists, try `python`, then `py -3`.
- A program installed while Claude Code is open is not found until Claude Code is fully quit and reopened (it keeps
  the PATH it started with). setup.py says so when it sees ffmpeg installed but not visible.
- `npx` is `npx.cmd` there: Python cannot start it by bare name. `HF` and cutout.py start it through node directly.
- The background cutout has no GPU path on Windows (HyperFrames uses CoreML on Apple Silicon only, CUDA only with
  `HYPERFRAMES_CUDA=1` and a CUDA build of onnxruntime), so it runs on the CPU. Run it in the background.
- Windows opens text files as cp1252 unless told otherwise: every `open()` in build.py needs `encoding='utf-8'`,
  or accents, curly quotes and emoji in captions come out broken (the page says charset UTF-8).
- File paths inside an ffmpeg FILTER (subtitles=, movie=, a fonts file) need the drive colon and backslashes
  escaped (`C\:/Users/...`). Pass files with `-i` instead; the skill's scripts never put a path in a filter, and the
  concat list holds bare file names only.
- Git Bash rewrites arguments that start with `/` into Windows paths. Fine for file paths; for anything else
  (a `/flag`) set `MSYS_NO_PATHCONV=1` for that command.
- Smart App Control (Windows 11) can block the unsigned image library (sharp) that HyperFrames loads for snapshots
  (the cutout loads the same library); antivirus can make ffmpeg fail once with `spawn EBUSY`. Retry once, then
  tell the user what Windows blocked.
- Windows on ARM (Snapdragon): the transcription engine has no ARM build; setup.py asks for the x64 Python.
- Maé ends with "tchus": always spell it **tchus** in captions (no umlaut, one s), whatever Whisper writes ("Tchüss", "tchuss").
- Sound design (Maé): vary the sounds and make each one mean what is shown or said: a new follower = notification ding, a reply/DM = message bloop, money = till ka-ching, a toggle/save/send = click, things rising = soft whoosh. Cards and inserts come in silently; never chain two sounds less than ~0.6 s apart unless the picture does two things. Synth ones live in reels/formats-v2/assets/sfx (ding, bloop, kaching).
- Retouch: every reel of Maé goes through scripts/retouch.py after the look (her brightness + face light + light slimming, learned from "POLICE retouchée"). Never add skin smoothing: she keeps her skin texture.
- Maé: never put "ma girl" in on-screen titles/hooks (fine in her caption only).
- Maé: deliver the phone copy by default (format téléphone: scale=720:-2, crf 24, ~1-2 MB); 1080p only if she asks.
- Maé: her "tchus" at the very end is her signature: always keep it, even when it comes after the CTA and Whisper misses it (check the audio tail).
- Maé: no punch-in zooms on her face (23 Digital zoom) — she finds them unflattering. Retouch every visible frame of her, frozen/dimmed stills included.
- Maé: never darken her footage unless she asks (she does want it dark, almost black, for serious "femme forte" text reels), never grey. On the lilac-wall B-rolls the natural footage + retouch.py IS her usual lilac look (as in broll-variante): do not add lilac.py on top, it washes it out.
- Maé: her ending is a finger kiss then "tchus": keep both (look at the frames before the tchus, the kiss is silent). No rays / full-screen flash over her face.
- Maé hooks: speak to the pain of her target (women creators/entrepreneurs who post and get no views, no followers, no clients) in their own words, plainly: "Tu ne fais pas de vues ?" beats "Tes vues ont chuté ?" (that assumes they once had views).
- Maé posts as trial reels (« Reels d'essai »): Instagram's header bar covers the top ~300 px of the 1080x1920 frame. Keep every title / text below y 330.
- Maé « Lis la description » sound = her cling, cut from her viral reel audio (broll-variante/assets/ref_audio.m4a 1.97-2.97 s), saved as reels/5-habitudes/assets/sfx/cling.mp3. Not the library ding.
- DRIVE DELIVERY (her rule, 18 Nov): every finished video also goes to Google Drive « Pour Claude » (id 16laMR3nZ_M51DQ6LAf0ala5z_pgCpAVW)
  > <video title folder, UPPERCASE> > FINAL. If the title folder or its FINAL subfolder does not exist, create it. Upload the phone
  copy with Google_Drive create_file (base64Content = "sha256:<hex>:<abs path>", disableConversionToGoogleType true).
  Limit: ~3.1 MB per file from this session. Her choice (18 Nov): if bigger, make a lighter copy for Drive (720p, 2-pass
  libx264 at (2.8 MB*8/duration - 96k) video bitrate, aac 96k) and upload that. Upload ALL variants she validated.
  Known FINAL ids: 10 ANS DE MARKETING 1Egqo9VgHhBFZNGku8LqYfoJOWhPSGi5A · TU PERDS DES VENTES 1KXv9nPUhawURlsIfRn01f3f6Qn-L-D6r ·
  5 HABITUDES POUR FORCER INSTA 1JjVCV0SJeSi6-MwZtkRVXliY12N9QwV4 · FAÇON LA PLUS DÉBILE 16xY-ebnUWz3wBUut79XZ7SvwvRwmSLUF ·
  HOOKS DE LA SEMAINE 1eVRIBI0dtvGypJj-KYyT6G-9VYBn0sPQ · PAYANT / GRATUIT 1sZfKG7HecSz3hiS-ey81kId-Qn7QwxzC ·
  SONS VIRAUX 1qvtk_SogXevOTWftONvFqHbclBTtOrum · AU CAS OÙ TA MÈRE 1njv7vWJ6Ftnynu38AP_RJhOo0wKdOADs ·
  10 HOOKS QUI ARRÊTENT LE SCROLL 1LdI8T-ZE1Y2vk9egXaFNakdL4yhbdNzp · TOFU MOFU BOFU 13yHu4y3Z-M5ya8DYedm6tcOFnaX8A63C ·
  10 FORMATS VIRAUX 11AtsLoRxxvDr_fPCT0d4hRJUAgfyk83_ · CLONE 0/10K 16LZYxmpo1WZmI_6293XNpRNZRCztLpqQ ·
  EFFETS SONORES 1dJEYjE9FckWPlJ50EoWsGa_XJF5pjWG6 · TRANSITION 11qtv5zyc_5VzDhZL89D17-PStIWxuCcX ·
  PLANIFIER TON CONTENU EN 45MIN 1l8hyRl43GVA2mHoXf1Y8Zqk4y45yCaT- · VIDÉO PAR CLAUDE 1dPa4y5bgfSf8Q2UW9GxrhGize4SUBbvx ·
  3 FOIS PAR JOUR 1CcgKYHz3njRR0Mmq2bz1j92JHbi363wG · 100 VUES VS 10K VS 100K 1R-d64i_dnMjniQYsLHNvh4ORPzIu5WUH ·
  ZONE 1AANChH-rOKrHfSxpOKrK7qAmIVcimVAF · TEMPS QUI PASSE 1CDNdvHS_EdaZB0vLAmQKXMMH0F9cRSHa ·
  CARROUSEL REEL STORY 1rk72bgo4ntjsVT3gIvQmHgZCREeRwbRr · Comment forcer insta variants (BROLL subfolder, no FINAL) 1BTeg8gBxeSZTdxblWUJHtLi-xnVRjDXt
- RETOUCH STRENGTH (19 Nov): she found the original retouch invisible -> retouch.py now defaults to --strength=1.8 (face light/tint x1.8, jaw slim x1.4). Keep it.
- WEEKLY HOOKS (22 Nov): hooks must be GENERIC fill-in templates usable in any métier (coiffeuse, nutritionniste, photographe…), NOT about Instagram / views / followers / clients — she is the Instagram coach, her audience is not.
- HOOK LIBRARY (22 Nov): she now ALLOWS her Notion « Hook library » (FAM PLAYBOOK, database 3652c779-ea24-80ab-80b1-ca852ddbec9d, data source collection://3652c779-ea24-810d-a849-000b8e96dac0) as INSPIRATION for the weekly hooks: adapt, keep them generic (any métier), never copy one already in hooks_used.json.
- NO GOLD CARDS (23 Nov): she rejected gold cards/accents on « 3 fois » — use her brown + white only for cards/badges (gold only if she asks).
- FACE RETOUCH (23 Nov): on « 3 fois » she found strength 1.8 too much and asked for NO face retouch (cut.py uses --no-face). Strength 1.8 was asked on rcs-v3 (19 Nov); when unsure, ask or stay lighter.
- LILAC SHINE (23 Nov): lilac.py took the purple light on her forehead for wall (« blue above red ») and lifted it into an ugly bright patch. A face-protected version exists (reels/trois-fois/lilac_face.py) BUT she then preferred the original look (lilac.py, no face retouch) on « 3 fois » — keep the original lilac.py by default; offer lilac_face.py only if she complains about forehead shine again.
