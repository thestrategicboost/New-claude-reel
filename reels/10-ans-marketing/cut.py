#!/usr/bin/env python3
"""10 ans de marketing: one take, dead air cut (audio envelope), normal speed, her lilac (lilac2.py, warm wall) + retouch.
PY cut.py -> assets/aroll.mp4, assets/voice.m4a, work/segs.json"""
import json, subprocess, sys
SEGS = [(0.62, 24.18), (24.36, 27.60), (27.72, 36.46), (36.62, 44.40)]
parts = []
for i, (a, b) in enumerate(SEGS):
    p = f'work/p{i}.mp4'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', 'src/brut.mov', '-vf', 'fps=30', '-af',
                    'afade=t=in:d=0.02,areverse,afade=t=in:d=0.03,areverse', '-c:v', 'libx264', '-crf', '15', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                    '-b:a', '256k', '-ar', '48000', p], check=True)
    parts.append(p)
open('work/parts.txt', 'w').write(''.join(f"file '{p.split('/')[1]}'\n" for p in parts))
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'work/parts.txt', '-c', 'copy', 'work/nat.mp4'], check=True)
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', 'work/nat.mp4', '-vn', '-c:a', 'copy', 'assets/voice.m4a'], check=True)
subprocess.run([sys.executable, 'lilac2.py', 'work/nat.mp4', 'work/lil.mp4'], check=True)
subprocess.run([sys.executable, '../../.claude/skills/video-edit/scripts/retouch.py', 'work/lil.mp4', 'assets/aroll.mp4'], check=True)
durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout) for p in parts]
json.dump({'segs': SEGS, 'durs': durs}, open('work/segs.json', 'w'))
print(round(sum(durs), 2))
