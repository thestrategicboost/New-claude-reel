#!/usr/bin/env python3
"""Lilac wall (Maé's "Ton rythme de publi" look) without touching her skin: the blue-grey wall is found by colour
(blue above red), relit and re-tinted to her lilac (#B5A0DD, pinker on the right), everything warm stays as shot.

PY lilac.py in.mp4 out.mp4          (PY lilac.py --frame in.png out.png for a test still)
"""
import subprocess
import sys

import numpy as np
from PIL import Image

W, H = 1080, 1920
LIFT = 1.36                                    # wall luminance: ~125 in the raw grade -> ~170 like her reel
LEFT = np.array([0.99, 0.94, 1.30], np.float32)  # lilac chroma (rgb / luma), bluish-lilac on the left ...
RIGHT = np.array([1.12, 0.91, 1.17], np.float32)  # ... pinker on the right
X = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
TINT = LEFT * (1 - X) + RIGHT * X


def grade(rgb):
    f = rgb.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    m = np.clip((b - r - 4) / 22, 0, 1)[..., None]           # wall = blue above red; skin / hair / cream top are warm
    luma = (0.299 * r + 0.587 * g + 0.114 * b)[..., None]
    wall = np.clip(luma * LIFT, 0, 245) * TINT
    out = f * (1 - m) + wall * m
    return np.clip(out, 0, 255).astype(np.uint8)


if sys.argv[1] == '--frame':
    Image.fromarray(grade(np.asarray(Image.open(sys.argv[2]).convert('RGB')))).save(sys.argv[3])
    sys.exit()
src, dst = sys.argv[1], sys.argv[2]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                        '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                        '-c:a', 'copy', '-shortest', dst], stdin=subprocess.PIPE)
n = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    enc.stdin.write(grade(np.frombuffer(buf, np.uint8).reshape(H, W, 3)).tobytes())
    n += 1
enc.stdin.close()
enc.wait()
print(f'{dst}: {n} frames')
