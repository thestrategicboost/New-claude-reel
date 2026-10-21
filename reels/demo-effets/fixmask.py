#!/usr/bin/env python3
"""The background remover drops her gold microphone. Re-alpha each cut-out: union of its alpha and a "warm pixels" key
taken from the natural-grade frames (her wall is cool blue-grey, the mic / skin / hair are warm), colours from the
grade asked for. PY fixmask.py <cut.webm> <colour src.mp4> <start s> <out.webm>"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

cut, src, start, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
W, H = 1080, 1920
n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames',
                        '-of', 'csv=p=0', '-c:v', 'libvpx-vp9', cut], capture_output=True, text=True).stdout.strip() or 0)
dec_a = subprocess.Popen(['ffmpeg', '-v', 'error', '-c:v', 'libvpx-vp9', '-i', cut, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
dec_n = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{start}', '-i', 'work/aroll_nat.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
dec_c = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{start}', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                        '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '6M', '-auto-alt-ref', '0', out], stdin=subprocess.PIPE)
k = 0
while True:
    a = dec_a.stdout.read(W * H * 4)
    nb = dec_n.stdout.read(W * H * 3)
    cb = dec_c.stdout.read(W * H * 3)
    if len(a) < W * H * 4 or len(nb) < W * H * 3 or len(cb) < W * H * 3:
        break
    al = np.frombuffer(a, np.uint8).reshape(H, W, 4)[..., 3].astype(np.float32)
    nat = np.frombuffer(nb, np.uint8).reshape(H, W, 3).astype(np.float32)
    warm = np.clip((nat[..., 0] - nat[..., 2] - 12) / 18, 0, 1) * 255
    warm[:int(H * .45)] = 0                       # only the lower half (the mic); hair is already in the cut-out
    wm = Image.fromarray(warm.astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(3))
    alpha = np.maximum(al, np.asarray(wm, np.float32)).astype(np.uint8)
    rgba = np.dstack([np.frombuffer(cb, np.uint8).reshape(H, W, 3), alpha])
    enc.stdin.write(rgba.tobytes())
    k += 1
enc.stdin.close()
enc.wait()
print(out, k, 'frames')
