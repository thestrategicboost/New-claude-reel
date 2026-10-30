#!/usr/bin/env python3
"""Keep the spoken parts of src/base.mp4 ("les 10 formats viraux..."), dead air between the formats removed, normal
speed -> work/aroll_nat.mp4; work/segs.json holds the kept (start, end) so build.py maps raw times to the edit."""
import json
import subprocess

SEGS = [(3.40, 6.72), (7.10, 7.82), (8.11, 8.73), (9.01, 9.99), (10.45, 11.24), (11.60, 12.47), (12.87, 13.74),
        (14.08, 14.74), (15.22, 15.96), (16.38, 17.23), (17.59, 18.44), (18.77, 20.74)]

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
