#!/usr/bin/env python3
"""Keep the good takes of work/raw.mp4 (dead air, hair-flip outtakes, repeated lines and the silence before the snap
removed), each take sped up (the opening faster) -> work/aroll_nat.mp4; work/segs.json holds (start, end, speed) so
build.py maps raw times to the edit with ct()."""
import json
import subprocess

SEGS = [(1.68, 4.08, 1.2), (4.18, 6.32, 1.2), (6.58, 7.50, 1.2),   # tu vois cette vidéo... pas de CapCut... juste Claude
        (15.74, 21.20, 1.1),                                         # je lui ai envoyé mon prompt... plus de rose, hop
        (21.38, 23.62, 1.1), (25.80, 27.50, 1.1),                    # mur de réel derrière moi | (snap) hop, il met un mur de réel
        (38.46, 45.52, 1.1),                                         # et franchement j'y connais rien... tout seul
        (47.64, 51.36, 1.1), (51.44, 57.20, 1.1),                    # texte derrière, ambiance | sous-titres, plan large, serré, cuts
        (65.30, 72.30, 1.1)]                                         # si toi aussi... commente montage... tchus

if __name__ == '__main__':
    fc, n = [], len(SEGS)
    for i, (a, b, sp) in enumerate(SEGS):
        fc.append(f'[0:v]trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{sp}[v{i}]')
        fc.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,atempo={sp}[a{i}]')
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/raw.mp4', '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
                    '-r', '30', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                    'work/aroll_nat.mp4'], check=True)
    json.dump(SEGS, open('work/segs.json', 'w'))
    print('edit', round(sum((b - a) / sp for a, b, sp in SEGS), 2), 's')
