#!/usr/bin/env python3
"""Les polices: keep the last clean take of each line of src/base.mp4 (dead air out, normal speed, her lilac look).
Three versions share the body:  v1 = body alone,  v2 = hook 2 + body,  v3 = hook 3 + body (when hook 3 is supplied).
PY cut.py v1|v2|v3   -> work/<v>/aroll.mp4 (lilac) + voice.m4a + segs.json [(source, start, end), ...]"""
import json
import os
import subprocess
import sys

BODY = [('base', 8.50, 10.46),                                 # facecam
        ('base', 12.90, 13.38), ('base', 13.60, 15.57),         # storytelling (pause after "utilise" cut)
        ('base', 17.76, 18.24), ('base', 18.54, 20.44),         # éducatives (pause after "utilise" cut)
        ('base', 30.86, 33.10),                                 # b-roll
        ('base', 35.60, 38.11),                                 # sous-titres
        ('base', 38.86, 41.00)]                                 # abonne-toi + tchus
# left out: first facecam take 4.34-6.44, first b-roll take 25.9-29.2 (both redone right after), the pauses
HOOKS = {'v1': [], 'v2': [('hook2', 1.80, 5.42)], 'v3': [('hook3', 1.34, 4.42)]}

if __name__ == '__main__':
    v = sys.argv[1]
    segs = HOOKS[v] + BODY
    os.makedirs(f'work/{v}', exist_ok=True)
    parts = []
    for i, (src, a, b) in enumerate(segs):
        p = f'work/{v}/p{i:02d}.mp4'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', f'src/{src}.mp4', '-vf', 'fps=30',
                        '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
                        '-ac', '2', p], check=True)
        parts.append(p)
    with open(f'work/{v}/parts.txt', 'w') as f:
        f.write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'work/{v}/parts.txt', '-c', 'copy',
                    f'work/{v}/nat.mp4'], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'work/{v}/nat.mp4', '-vn', '-c:a', 'copy', f'work/{v}/voice.m4a'], check=True)
    subprocess.run([sys.executable, 'lilac.py', f'work/{v}/nat.mp4', f'work/{v}/aroll.mp4'], check=True)
    durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                 capture_output=True, text=True).stdout) for p in parts]
    json.dump({'segs': segs, 'durs': durs}, open(f'work/{v}/segs.json', 'w'))
    print(v, round(sum(durs), 2), 's')
