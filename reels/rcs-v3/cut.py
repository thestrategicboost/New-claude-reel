#!/usr/bin/env python3
"""Last complete take of src/base.mp4 (same takes as her validated versions, « money money money » removed (her ask)), dead air
removed, normal speed -> lilac look -> face retouch -> assets/aroll.mp4 + assets/voice.m4a; work/segs.json for ct()."""
import json
import subprocess
import sys

SEGS = [(112.05, 125.78), (129.03, 134.74), (138.75, 144.45), (152.20, 158.72), (160.24, 163.66)]
PY = sys.executable

if __name__ == '__main__':
    fc, n = [], len(SEGS)
    for i, (a, b) in enumerate(SEGS):
        fc.append(f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps=30[v{i}]')
        fc.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.03,areverse[a{i}]')
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', 'src/base.mp4', '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', 'work/nat.mp4'], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', 'work/nat.mp4', '-vn', '-c:a', 'copy', 'assets/voice.m4a'], check=True)
    subprocess.run([PY, 'lilac.py', 'work/nat.mp4', 'work/lil.mp4'], check=True)
    subprocess.run([PY, '../../.claude/skills/video-edit/scripts/retouch.py', 'work/lil.mp4', 'assets/aroll.mp4'], check=True)
    json.dump(SEGS, open('work/segs.json', 'w'))
    print('edit', round(sum(b - a for a, b in SEGS), 2), 's')
