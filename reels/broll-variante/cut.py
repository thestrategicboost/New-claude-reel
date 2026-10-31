#!/usr/bin/env python3
"""Variants of her "comment forcer Insta à montrer tes réels à des non abonnés" reel (src/ref.mp4, 5.3 s): same
format, other B-roll from her Drive folder BROLL, other hook angles. Each variant: 5.3 s of one B-roll, muted, with
her retouch (brightness + face) -> assets/v<n>.mp4.   PY cut.py"""
import subprocess
import sys

VARIANTS = {1: ('b06', 0.3), 2: ('b08', 3.0), 3: ('b10', 3.0), 4: ('b01', 1.0)}
DUR = 5.3

if __name__ == '__main__':
    for n, (b, t) in VARIANTS.items():
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-t', str(DUR), '-i', f'src/broll/{b}.mov', '-an', '-vf',
                        'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30', '-c:v', 'libx264', '-crf', '15',
                        '-pix_fmt', 'yuv420p', f'work/raw{n}.mp4'], check=True)
        subprocess.run([sys.executable, '/root/.claude/skills/video-edit/scripts/retouch.py', f'work/raw{n}.mp4', f'assets/v{n}.mp4'], check=True)
