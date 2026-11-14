#!/usr/bin/env python3
"""Variants of her "comment forcer Insta à montrer tes réels à des non abonnés" reel (src/ref.mp4, 5.3 s): same
format, other B-roll from her Drive folder BROLL, other hook angles. Each variant: 5.3 s of one B-roll, muted, with
her retouch (brightness + face) -> assets/v<n>.mp4.   PY cut.py [n ...]"""
import subprocess
import sys

VARIANTS = {
            # round 3: « COMMENT FORCER INSTA » on B-rolls / moments not used for it yet
            16: ('bvoit', 0.5), 17: ('b09', 8.0), 18: ('b06', 2.8), 19: ('b05', 14.0), 20: ('b11', 20.0), 21: ('b08', 22.0),
            
            # round 2, after variante 2 worked (4 025 views, 75 saves): same hook, other moments / other lilac B-rolls
            10: ('b08', 13.0), 11: ('b06', 5.0), 12: ('b01', 5.5), 13: ('b05', 6.0), 14: ('b08', 18.0), 15: ('b08', 8.0),
            1: ('b06', 0.3), 2: ('b08', 3.0), 3: ('b10', 3.0), 4: ('b01', 1.0),
            # same hook as the original, other places: chateau, Marrakech x2, purple wall, computer
            5: ('b02', 0.3), 6: ('b03', 1.5), 7: ('b04', 1.0), 8: ('b05', 2.0), 9: ('b11', 8.0)}
DUR = 5.3

if __name__ == '__main__':
    only = [int(a) for a in sys.argv[1:]] or list(VARIANTS)
    for n, (b, t) in VARIANTS.items():
        if n not in only:
            continue
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-t', str(DUR), '-i', f'src/broll/{b}.mov', '-an', '-vf',
                        'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30', '-c:v', 'libx264', '-crf', '15',
                        '-pix_fmt', 'yuv420p', f'work/raw{n}.mp4'], check=True)
        subprocess.run([sys.executable, '../../.claude/skills/video-edit/scripts/retouch.py', f'work/raw{n}.mp4', f'assets/v{n}.mp4'], check=True)
