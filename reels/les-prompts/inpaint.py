#!/usr/bin/env python3
"""Remove her burned-in white text (region x 90-630, y 315-585 at 720p) frame by frame: mask = bright pixels in the
region (dilated), filled with OpenCV inpainting. PY inpaint.py in.mp4 out.mp4 [t_end]"""
import subprocess, sys
import cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]
t_end = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
W, H, FPS = 720, 1280, 30
X0, X1, Y0, Y1 = 90, 630, 315, 585
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', src,
                        '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', dst],
                       stdin=subprocess.PIPE)
k = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3:
        break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()
    if k / FPS < t_end:
        roi = f[Y0:Y1, X0:X1]
        g = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        bg = cv2.medianBlur(g, 31)
        m = ((g.astype(int) - bg.astype(int)) > 25).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((7, 7), np.uint8))
        f[Y0:Y1, X0:X1] = cv2.inpaint(roi, m, 6, cv2.INPAINT_TELEA)
    enc.stdin.write(f.tobytes())
    k += 1
enc.stdin.close(); enc.wait(); print(dst, k)
