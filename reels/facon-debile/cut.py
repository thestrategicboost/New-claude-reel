#!/usr/bin/env python3
"""« La façon la plus débile » (her reel that worked, src/ref.mp4, 6.27 s) remade on other B-rolls: each variant = 6.27 s of one
B-roll (1080x1920, 30 fps), her retouch.   PY cut.py [n ...]  -> assets/v<n>.mp4"""
import subprocess
import sys

DUR = 6.27
B = '../broll-variante/src/broll/'
VARIANTS = {1: (B + 'b08.mov', 13.0), 2: (B + 'b08.mov', 20.5), 3: ('../temps-qui-passe/src/IMG_5497.mov', 1.2), 4: ('../temps-qui-passe/src/IMG_5532.mov', 1.8)}
if __name__ == '__main__':
    only = [int(a) for a in sys.argv[1:]] or list(VARIANTS)
    for n in only:
        src, t = VARIANTS[n]
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-t', str(DUR), '-i', src, '-an', '-vf',
                        'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30', '-c:v', 'libx264', '-crf', '15',
                        '-pix_fmt', 'yuv420p', f'work/raw{n}.mp4'], check=True)
        subprocess.run([sys.executable, '../../.claude/skills/video-edit/scripts/retouch.py', f'work/raw{n}.mp4', f'assets/v{n}.mp4'], check=True)
