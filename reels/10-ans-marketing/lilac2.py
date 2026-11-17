#!/usr/bin/env python3
"""Her lilac look for a WARM greige wall (lilac.py keys on a blue-grey wall and blotches this one): every low-saturation,
light pixel (wall, white shirt) gets her lilac chroma at its own brightness, soft mask so skin, hair and gold stay as shot.
PY lilac2.py in.mp4 out.mp4  |  --frame in.png out.png"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
W, H = 1080, 1920
LEFT = np.array([0.99, 0.94, 1.30], np.float32); RIGHT = np.array([1.12, 0.91, 1.17], np.float32)
X = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]; TINT = LEFT * (1 - X) + RIGHT * X
def grade(rgb):
    f = rgb.astype(np.float32); mx = f.max(2); mn = f.min(2)
    sat = (mx - mn) / (mx + 1); luma = 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]
    m = np.clip((0.22 - sat) / 0.10, 0, 1) * np.clip((luma - 95) / 40, 0, 1)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5)), np.float32)[..., None] / 255
    lum = np.asarray(Image.fromarray(np.clip(luma, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), np.float32)[..., None]
    wall = np.clip(lum * 1.08, 0, 240) * TINT
    return np.clip(f * (1 - m) + wall * m, 0, 255).astype(np.uint8)
if sys.argv[1] == '--frame':
    Image.fromarray(grade(np.asarray(Image.open(sys.argv[2]).convert('RGB')))).save(sys.argv[3]); sys.exit()
src, dst = sys.argv[1], sys.argv[2]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-i', src,
                        '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', dst], stdin=subprocess.PIPE)
n = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    enc.stdin.write(grade(np.frombuffer(buf, np.uint8).reshape(H, W, 3)).tobytes()); n += 1
enc.stdin.close(); enc.wait(); print(dst, n, 'frames')
