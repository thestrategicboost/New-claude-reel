#!/usr/bin/env python3
"""Keep the four "Utilise cette transition avec ce son" lines and the CTA of src/base.mp4, dead air removed, normal
speed -> work/aroll_nat.mp4; work/segs.json holds the kept (start, end) so build.py maps raw times to the edit."""
import json
import subprocess

SEGS = [(4.06, 6.50), (7.52, 10.06), (10.96, 13.48), (14.70, 16.90), (17.20, 19.40)]

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
