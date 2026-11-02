#!/usr/bin/env python3
"""Mirror + speed variant: work/<v>/ -> work/<v>m/ (image flipped left-right, 1.1x speed, voice pitch kept),
timings of segs.json and words.json divided by the speed.   PY mirror.py v1|v2 [speed]"""
import json
import os
import subprocess
import sys

v = sys.argv[1]
sp = float(sys.argv[2]) if len(sys.argv) > 2 else 1.1
a, b = f'work/{v}', f'work/{v}m'
os.makedirs(b, exist_ok=True)
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{a}/aroll.mp4', '-an', '-vf', f'hflip,setpts=PTS/{sp},fps=30',
                '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', f'{b}/aroll.mp4'], check=True)
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{a}/voice.m4a', '-af', f'atempo={sp}', '-c:a', 'aac', '-b:a', '256k',
                f'{b}/voice.m4a'], check=True)
seg = json.load(open(f'{a}/segs.json'))
seg['durs'] = [d / sp for d in seg['durs']]
json.dump(seg, open(f'{b}/segs.json', 'w'), ensure_ascii=False)
json.dump([dict(w, s=w['s'] / sp, e=w['e'] / sp) for w in json.load(open(f'{a}/words.json'))], open(f'{b}/words.json', 'w'), ensure_ascii=False)
print(b, round(sum(seg['durs']), 2), 's')
