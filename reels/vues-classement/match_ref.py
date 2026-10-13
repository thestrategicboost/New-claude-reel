#!/usr/bin/env python3
"""Whole-picture colour match to Maé's own lilac reel ("Ton rythme de publi"): an affine colour matrix fitted on matching
patches (wall, skin, white top, hair, darks) of her reference still and of this a-roll, applied to every frame alike.

PY match_ref.py in.mp4 out.mp4 [strength]      PY match_ref.py --frame in.png out.png [strength]
"""
import subprocess
import sys

import numpy as np
from PIL import Image

W, H = 1080, 1920
PAIRS = [   # this a-roll (graded)  ->  her reference reel
    ((114, 123, 133), (179, 161, 222)),   # wall, left
    ((141, 151, 158), (188, 157, 211)),   # wall, right
    ((225, 170, 143), (211, 151, 160)),   # skin, lit
    ((193, 158, 137), (212, 138, 162)),   # skin, mid
    ((226, 221, 214), (206, 201, 253)),   # white top
    ((110, 98, 85), (132, 78, 63)),       # hair
    ((45, 46, 52), (26, 27, 33)),         # darks
]
S = np.array([p[0] for p in PAIRS] + [(255, 255, 255)], np.float32)
T = np.array([p[1] for p in PAIRS] + [(250, 248, 255)], np.float32)
M, *_ = np.linalg.lstsq(np.c_[S, np.ones(len(S))], T, rcond=None)     # 4x3 affine


def grade(rgb, k=1.0):
    f = rgb.reshape(-1, 3).astype(np.float32)
    out = np.c_[f, np.ones(len(f), np.float32)] @ M
    out = f + k * (out - f)
    return np.clip(out, 0, 255).astype(np.uint8).reshape(rgb.shape)


if __name__ == '__main__':
    if sys.argv[1] == '--frame':
        k = float(sys.argv[4]) if len(sys.argv) > 4 else 1
        Image.fromarray(grade(np.asarray(Image.open(sys.argv[2]).convert('RGB')), k)).save(sys.argv[3])
        print(np.round(M, 3))
        sys.exit()
    src, dst = sys.argv[1], sys.argv[2]
    k = float(sys.argv[3]) if len(sys.argv) > 3 else 1
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                            '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
                            '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', dst], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        enc.stdin.write(grade(np.frombuffer(buf, np.uint8).reshape(H, W, 3), k).tobytes())
        n += 1
    enc.stdin.close()
    enc.wait()
    print(f'{dst}: {n} frames')
