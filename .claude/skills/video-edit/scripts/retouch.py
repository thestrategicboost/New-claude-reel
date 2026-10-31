#!/usr/bin/env python3
"""Maé's retouch, learned from her own CapCut edit ("POLICE retouchée", Drive folder "Les polices"), applied to the
A-roll after the look and before the overlays:
  1. brightness: her tone curve (mids +15 to +18 on 0-255, shadows +5, highlights kept), which also lowers the
     saturation a little (about -10 %); the per-channel curve is in retouch_curve.json next to this script
  2. face: a soft face light (about +7 on 0-255 over the face, a touch more under the eyes), skin a hair less red and
     a hair warmer, and a very light slimming of the lower face (each jaw side pulled ~0.6 % of the face width toward
     the centre), following her face frame by frame.
No skin smoothing: her edit keeps the skin texture (measured: same fine detail before and after).

PY retouch.py in.mp4 out.mp4 [--no-face]
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np

SLIM = .0065          # jaw pull, as a share of the face width (her edit: ~2 px on a 330 px face)
FACE_L, EYES_L, FACE_A, FACE_B = 7.0, 1.5, -1.0, 2.3     # face light and skin tint, in Lab units (her edit)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    face = '--no-face' not in sys.argv
    cur = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'retouch_curve.json')))['bgr']
    lut = np.stack([np.clip(np.array(c), 0, 255).astype(np.uint8) for c in cur], -1).reshape(256, 1, 3)
    W, H = [int(v) for v in subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                            '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split(',')[:2]]
    fps = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', src],
                         capture_output=True, text=True).stdout.strip()
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', fps, '-i', '-',
                            '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p',
                            '-c:a', 'copy', dst], stdin=subprocess.PIPE)
    fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    box, k = None, 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        f = cv2.LUT(f, lut)
        if face:
            if k % 3 == 0:
                small = cv2.cvtColor(cv2.resize(f, (W // 3, H // 3)), cv2.COLOR_BGR2GRAY)
                d = fc.detectMultiScale(small, 1.1, 5, minSize=(40, 40))
                if len(d):
                    x, y, w, h = [v * 3 for v in max(d, key=lambda r: r[2] * r[3])]
                    nb = np.array([x + w / 2, y + h / 2, w], np.float32)
                    box = nb if box is None else box * .6 + nb * .4
            if box is not None:
                cx, cy, w = box
                # slimming: sample a little further out on the jaw sides (pulls them inward), fading out from the centre
                u = (gx - cx) / (w * .55)
                v = (gy - (cy + w * .28)) / (w * .45)
                fall = np.exp(-(v ** 2)) * np.clip(1.6 - np.abs(u), 0, 1)
                mapx = gx + SLIM * w * np.clip(u, -1.2, 1.2) * fall
                f = cv2.remap(f, mapx, gy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                # face light + skin tint, inside a soft ellipse over the face (worked in Lab, on the face crop only)
                x0, x1 = int(max(0, cx - w * .75)), int(min(W, cx + w * .75))
                y0, y1 = int(max(0, cy - w * .75)), int(min(H, cy + w * 1.0))
                crop = cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2LAB).astype(np.float32)
                ux = (gx[y0:y1, x0:x1] - cx) / (w * .52)
                uy = (gy[y0:y1, x0:x1] - (cy + w * .08)) / (w * .72)
                m = np.exp(-(ux ** 2 + uy ** 2) ** 2 * 1.6)
                e = sum(np.exp(-(((gx[y0:y1, x0:x1] - (cx + sd * w * .2)) / (w * .1)) ** 2 + ((gy[y0:y1, x0:x1] - (cy + w * .08)) / (w * .06)) ** 2))
                        for sd in (-1, 1))
                crop[..., 0] += (FACE_L * m + EYES_L * e)
                crop[..., 1] += FACE_A * m
                crop[..., 2] += FACE_B * m
                f = f.copy()
                f[y0:y1, x0:x1] = cv2.cvtColor(np.clip(crop, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
        enc.stdin.write(f.tobytes())
        k += 1
    enc.stdin.close()
    enc.wait()
    print(dst, k, 'frames')


if __name__ == '__main__':
    main()
