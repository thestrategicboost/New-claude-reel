#!/usr/bin/env python3
"""Clone reel: Maé who flops (Clone 1, standing left) and Maé who succeeds (Clone 2, standing right) talk to
each other. Each line is the best take; while one speaks, the other track runs the moments right around her own
reply (listening before, reacting after), so both are alive in every frame. Writes work/c1.mp4 (flop track, with
the speaker's audio of the whole dialogue) and work/c2.mp4 (success track, video only, to be cut out) + work/plan.json.

PY assemble.py
"""
import json
import subprocess

# (speaker, [(start, end), ...] in her own clip): flop = clone1, success = clone2
LINES = [
    ('f', [(10.80, 13.75)]),                       # j'ai pas une super caméra pour filmer
    ('s', [(26.10, 29.85)]),                       # moi non plus... mon téléphone fera l'affaire
    ('f', [(24.45, 27.25)]),                       # regarde ma vidéo elle a fait que 500 vues
    ('s', [(55.05, 61.35)]),                       # mais 500 vues ! t'imagines... c'est dingue quand même
    ('f', [(45.25, 47.10)]),                       # en fait moi je n'ai pas le temps de créer du contenu
    ('s', [(77.20, 80.80)]),                       # moi aussi je suis super occupée... j'ai des priorités
    ('f', [(55.05, 57.75), (64.95, 65.98)]),       # je trouve ça super gênant de poster, en plus on va me juger
    ('s', [(107.20, 113.15)]),                     # moi non plus je suis pas super à l'aise...
    ('f', [(75.95, 79.50)]),                       # je sais pas quoi poster, ça me saoule alors j'abandonne
    ('s', [(134.30, 135.72), (140.80, 144.40)]),   # mais non tu vois moi je reste focus ... Strategic Boost
]


def run(*a):
    subprocess.run(a, check=True)


# listening windows of the success Maé that replace the default (the camera hunted focus there): line index -> start
LISTEN_FIX = {0: 21.90, 6: 115.50}

plan, t = [], 0.0
segs1, segs2 = [], []          # (src_start, dur, audio?) per track
for k, (who, parts) in enumerate(LINES):
    dur = sum(b - a for a, b in parts)
    if who == 'f':
        for a, b in parts:
            segs1.append((a, b - a, True))
        nxt = LINES[k + 1][1][0][0] if k + 1 < len(LINES) else None
        s_from = (nxt - dur) if nxt else LINES[k - 1][1][-1][1]       # success listens just before her reply
        s_from = LISTEN_FIX.get(k, s_from)
        segs2.append((s_from, dur, False))
    else:
        for a, b in parts:
            segs2.append((a, b - a, True))
        prev_end = LINES[k - 1][1][-1][1]                              # flop reacts just after her own line
        segs1.append((prev_end, dur, False))
    plan.append({'who': who, 'start': round(t, 3), 'end': round(t + dur, 3), 'parts': parts})
    t += dur


def track(src, segs, out, with_audio):
    fc, n = [], len(segs)
    for i, (a, d, spk) in enumerate(segs):
        fc.append(f'[0:v]trim=start={a:.3f}:duration={d:.3f},setpts=PTS-STARTPTS[v{i}]')
        if with_audio:
            fc.append(f'[0:a]atrim=start={a:.3f}:duration={d:.3f},asetpts=PTS-STARTPTS,volume={1 if spk else 0}[a{i}]')
    ins = ''.join(f'[v{i}]' + (f'[a{i}]' if with_audio else '') for i in range(n))
    fc.append(f'{ins}concat=n={n}:v=1:a={1 if with_audio else 0}[v]' + ('[a]' if with_audio else ''))
    maps = ['-map', '[v]'] + (['-map', '[a]'] if with_audio else [])
    run('ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', ';'.join(fc), *maps, '-c:v', 'libx264', '-crf', '14',
        '-preset', 'fast', '-pix_fmt', 'yuv420p', *(['-c:a', 'aac', '-b:a', '256k'] if with_audio else []), out)


# success track also needs its own voice: build its audio separately and mix in assemble of c1's audio
track('work/clone1.mov', segs1, 'work/c1_v.mp4', True)
track('work/clone2.mov', segs2, 'work/c2.mp4', True)
run('ffmpeg', '-v', 'error', '-y', '-i', 'work/c1_v.mp4', '-i', 'work/c2.mp4', '-filter_complex',
    '[0:a][1:a]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]', '-map', '0:v', '-map', '[a]',
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', 'work/c1.mp4')
json.dump(plan, open('work/plan.json', 'w'), indent=1)
print(f'dialogue {t:.2f}s', [(p['who'], p['start'], p['end']) for p in plan])
