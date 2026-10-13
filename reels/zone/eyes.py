#!/usr/bin/env python3
"""Track her eye line (face box from OpenCV's Haar cascade, eyes ~0.42 down the face) every 2 frames over the eye-line
part of the reel, smoothed, -> work/eyes.json [[t, eye_y], ...] in 1080x1920 pixels.

PY eyes.py [t0 t1]
"""
import json
import sys

import cv2
import numpy as np

T0, T1 = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else (8.0, 14.2)
cap = cv2.VideoCapture('assets/aroll.mp4')
fps = cap.get(cv2.CAP_PROP_FPS) or 30
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_c = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cap.set(cv2.CAP_PROP_POS_FRAMES, int(T0 * fps))
pts, n = [], int(T0 * fps)
while n <= T1 * fps:
    ok, fr = cap.read()
    if not ok:
        break
    if n % 2 == 0:
        g = cv2.cvtColor(cv2.resize(fr, (540, 960)), cv2.COLOR_BGR2GRAY)
        faces = casc.detectMultiScale(g, 1.1, 5, minSize=(120, 120))
        if len(faces):
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            ey = y + .40 * h
            eyes = eye_c.detectMultiScale(g[y:y + int(h * .6), x:x + w], 1.1, 6, minSize=(20, 20))
            if len(eyes) >= 1:
                ey = y + float(np.median([e[1] + e[3] / 2 for e in eyes]))
            pts.append([n / fps, ey * 2])
    n += 1
t = np.array([p[0] for p in pts])
y = np.array([p[1] for p in pts])
# median then moving average: no jitter, still follows her head
ym = np.array([np.median(y[max(0, i - 3):i + 4]) for i in range(len(y))])
ys = np.convolve(np.pad(ym, 3, mode='edge'), np.ones(7) / 7, mode='valid')
json.dump([[round(a, 3), round(b, 1)] for a, b in zip(t, ys)], open('work/eyes.json', 'w'))
print(len(pts), 'points; eye y range', round(ys.min()), round(ys.max()))
