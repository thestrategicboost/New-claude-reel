#!/usr/bin/env python3
"""Keep the last clean take of each line of src/base.mp4 (landscape footage), dead air removed, normal speed, lilac-ish
grade -> assets/aroll.mp4 (1920x1080) + assets/voice.m4a + three shifted muted copies for the dimmed bands
(assets/idleS*.mp4). Every kept piece starts and ends while she faces the camera (the reading glances to her computer,
found with work/face.json, are cut out). work/segs.json holds the kept (start, end)."""
import json
import subprocess

SEGS = [(4.88, 8.78), (14.32, 17.92), (23.53, 25.68), (33.03, 36.08), (41.32, 43.66), (44.68, 49.42), (55.0, 56.40),
        (56.62, 60.38), (64.25, 68.48), (74.44, 77.85), (89.83, 91.02), (106.40, 108.65), (109.80, 112.40),
        (120.73, 124.20), (124.48, 127.76), (131.99, 140.72), (146.60, 154.08), (160.62, 163.62)]
GRADE = 'colorbalance=rs=.05:bs=.07:rm=.05:bm=.06,eq=brightness=.03:saturation=1.06'

if __name__ == '__main__':
    # one piece at a time (a single 19-trim filtergraph on this HEVC source runs out of memory), then concat
    parts = []
    for i, (a, b) in enumerate(SEGS):
        p = f'work/part{i:02d}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', 'src/base.mp4', '-vf', f'fps=30,{GRADE}',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                        '-ar', '48000', '-ac', '2', p], check=True)
        parts.append(p)
    with open('work/parts.txt', 'w') as f:
        f.write(''.join(f"file '{p.split('/')[1]}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'work/parts.txt', '-c', 'copy', 'assets/aroll.mp4'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'assets/aroll.mp4', '-vn', '-c:a', 'copy', 'assets/voice.m4a'], check=True)
    # the dimmed bands play muted, shifted copies of the edit (she faces the camera there, never the reading pauses)
    for k in range(3):
        sh = (k * 18 + 22) % 60
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sh), '-i', 'assets/aroll.mp4', '-i', 'assets/aroll.mp4', '-filter_complex',
                        f'[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=end={sh},setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0', '-an',
                        '-c:v', 'libx264', '-crf', '22', '-pix_fmt', 'yuv420p', f'assets/idleS{k}.mp4'], check=True)
    json.dump(SEGS, open('work/segs.json', 'w'))
    print('edit', round(sum(b - a for a, b in SEGS), 2), 's')
