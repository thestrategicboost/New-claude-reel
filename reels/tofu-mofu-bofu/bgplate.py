#!/usr/bin/env python3
"""Blurred background plate WITHOUT the speaker -> assets/bgplate.mp4 (270x480, scaled up by the page).

A plain CSS blur on the base video smears the speaker into the wall, which leaves a glowing halo around the
cutout. Here the speaker is masked out first (cutout alpha, dilated), then a normalised blur fills the gap from
the surrounding wall: bg = blur(frame * mask) / blur(mask).

Usage (from the project folder):  PY bgplate.py
"""
import subprocess

import numpy as np
from PIL import Image, ImageFilter

W, H, R = 270, 480, 8           # quarter resolution (it is blurred anyway); radius ~32px full-res
src = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', 'assets/aroll.mp4', '-vf', f'scale={W}:{H}', '-f', 'rawvideo',
                        '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
alp = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-c:v', 'libvpx-vp9', '-i', 'assets/subject.webm', '-vf',
                        f'alphaextract,scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
out = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30',
                        '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-g', '30',
                        'assets/bgplate.mp4'], stdin=subprocess.PIPE)


def box(a, r, axis):
    """running mean of width 2r+1 along an axis, edges clamped"""
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    c = np.moveaxis(np.cumsum(np.pad(a, pad, mode='edge'), axis=axis), axis, 0)
    n = a.shape[axis]
    return np.moveaxis((c[2 * r + 1:2 * r + 1 + n] - c[:n]) / (2 * r + 1), 0, axis)


def blur(a):
    """three box passes per axis ~ a gaussian of sigma ~R"""
    r = max(1, round(R * 0.85))
    for _ in range(3):
        a = box(box(a, r, 0), r, 1)
    return a


n = 0
while True:
    f = src.stdout.read(W * H * 3)
    a = alp.stdout.read(W * H)
    if len(f) < W * H * 3 or len(a) < W * H:
        break
    rgb = np.frombuffer(f, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    sub = Image.frombuffer('L', (W, H), a).filter(ImageFilter.MaxFilter(9))  # grow the subject
    m = 1 - np.asarray(sub, np.float32) / 255
    num, den = blur(rgb * m[..., None]), blur(m)
    bg = num / np.maximum(den, 1e-3)[..., None]
    # deep inside the subject no wall is near: fall back to a wide average (always hidden by the cutout)
    far = den < .04
    if far.any():
        wide = rgb[m > .5].mean(0) if (m > .5).any() else rgb.reshape(-1, 3).mean(0)
        bg[far] = wide
    out.stdin.write((np.clip(bg, 0, 1) * 255).astype(np.uint8).tobytes())
    n += 1
    if n % 300 == 0:
        print(f'{n} frames', flush=True)
out.stdin.close()
out.wait()
print(f'bgplate.mp4: {n} frames')
