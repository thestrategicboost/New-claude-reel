#!/usr/bin/env python3
"""« La façon la plus débile » (her reel that worked, src/ref.mp4, 6.27 s) remade on other B-rolls: each variant = 6.27 s of one
B-roll (1080x1920, 30 fps), her retouch.   PY cut.py [n ...]  -> assets/v<n>.mp4"""
import subprocess
import sys

DUR = 6.27
B = '../broll-variante/src/broll/'
T = '../temps-qui-passe/src/'
# round 2 (all of round 1 is published): her other B-rolls, framed a bit tighter from the TOP (static, not a zoom move) so her
# face lands under the view-count screenshots, as in her reel (face top ~950 px)
VARIANTS = {5: (B + 'b05.mov', 6.0, 1.33), 6: (B + 'b06.mov', 4.0, 1.33), 7: (T + 'c3.mov', 9.0, 1.12), 8: (T + 'c1.mov', 8.0, 1.3),
            9: (T + 'voiture.mov', 0.3, 1.38),
            1: (B + 'b08.mov', 13.0), 2: (B + 'b08.mov', 20.5), 3: ('../temps-qui-passe/src/IMG_5497.mov', 1.2), 4: ('../temps-qui-passe/src/IMG_5532.mov', 1.8)}
if __name__ == '__main__':
    only = [int(a) for a in sys.argv[1:]] or list(VARIANTS)
    for n in only:
        src, t, *z = VARIANTS[n] + (1.0,) if len(VARIANTS[n]) == 2 else VARIANTS[n]
        z = z[0]
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-t', str(DUR), '-i', src, '-an', '-vf',
                        f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale={round(1080*z/2)*2}:{round(1920*z/2)*2}:flags=lanczos,crop=1080:1920:(iw-1080)/2:0,fps=30', '-c:v', 'libx264', '-crf', '15',
                        '-pix_fmt', 'yuv420p', f'work/raw{n}.mp4'], check=True)
        subprocess.run([sys.executable, '../../.claude/skills/video-edit/scripts/retouch.py', f'work/raw{n}.mp4', f'assets/v{n}.mp4'], check=True)
