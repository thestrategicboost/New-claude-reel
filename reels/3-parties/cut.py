#!/usr/bin/env python3
"""Keep the last clean take of each line of src/base.mp4 (landscape footage), dead air removed, normal speed, her lilac
look -> assets/aroll.mp4 (1920x1080) + assets/voice.m4a. Every kept piece starts and ends while she faces the camera (the reading glances to her computer,
found with work/face.json, are cut out). work/segs.json holds the kept (start, end)."""
import json
import subprocess
import sys

SEGS = [(4.88, 8.78), (14.32, 17.92), (23.53, 25.68), (33.03, 36.08), (44.68, 49.42), (55.0, 56.40), (56.62, 60.38),
        (64.25, 68.48), (74.44, 77.85), (89.83, 90.98), (109.80, 112.40), (120.73, 124.20), (124.48, 127.76),
        (131.99, 140.72), (146.60, 154.08), (160.62, 163.62)]
# left out on purpose: 41.32-43.66 (false start of "les types de contenus tofu..."), 106.40-108.65 (first try of the
# storytelling line, redone right after), 116.34-116.84 (head turned to her notes), 91.0-91.1 ("des vidéos..." cut off)
GRADE = 'null'

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
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'work/parts.txt', '-c', 'copy', 'work/aroll_nat.mp4'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/aroll_nat.mp4', '-vn', '-c:a', 'copy', 'assets/voice.m4a'], check=True)
    subprocess.run([sys.executable, 'lilac.py', 'work/aroll_nat.mp4', 'assets/aroll.mp4'], check=True)   # her lilac look
    json.dump(SEGS, open('work/segs.json', 'w'))
    print('edit', round(sum(b - a for a, b in SEGS), 2), 's')
