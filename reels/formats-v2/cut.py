#!/usr/bin/env python3
"""Keep the last complete take of src/base.mp4 (1:52-2:43), dead air removed, normal speed -> work/aroll_nat.mp4;
work/segs.json holds the kept (start, end) so build.py maps raw times to the edit with ct()."""
import json
import subprocess

SEGS = [(112.05, 125.78), (129.03, 134.74), (138.75, 144.27), (152.29, 158.72), (160.24, 163.66)]

if __name__ == '__main__':
    fc, n = [], len(SEGS)
    for i, (a, b) in enumerate(SEGS):
        fc.append(f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps=30[v{i}]')
        fc.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]')
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'src/base.mp4', '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                    'work/aroll_nat.mp4'], check=True)
    json.dump(SEGS, open('work/segs.json', 'w'))
    print('edit', round(sum(b - a for a, b in SEGS), 2), 's')
