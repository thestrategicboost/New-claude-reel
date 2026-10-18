#!/usr/bin/env python3
"""Keep the good takes of work/raw.mp4 (dead air, hair-flip outtakes and the repeated lines removed) -> work/aroll_nat.mp4,
and write work/segs.json so build.py can map raw times to the edit with cut_time()."""
import json
import subprocess

SEGS = [(1.68, 4.08), (4.18, 6.32), (6.58, 7.50),     # tu vois cette vidéo... pas de CapCut, pas de logiciel... juste Claude
        (15.74, 21.20),                                # je lui ai envoyé mon prompt... un peu plus de rose, hop, il met du rose
        (21.38, 23.62), (25.42, 27.50),                # si je lui demande un mur de réel derrière moi | hop, il met un mur de réel derrière moi
        (38.46, 45.52),                                # et franchement j'y connais rien... il me fait ça tout seul
        (47.64, 51.36), (51.44, 57.20),                # texte derrière, ambiance... sous-titres, plan large, serré, cuts... deux secondes
        (65.30, 72.30)]                                # si toi aussi... commente montage... adios

if __name__ == '__main__':
    e = '+'.join(f'between(t,{a:.3f},{b:.3f})' for a, b in SEGS)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/raw.mp4', '-vf', f"select='{e}',setpts=N/FRAME_RATE/TB",
                    '-af', f"aselect='{e}',asetpts=N/SR/TB", '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', 'work/aroll_nat.mp4'], check=True)
    json.dump(SEGS, open('work/segs.json', 'w'))
    print('edit', round(sum(b - a for a, b in SEGS), 2), 's')
