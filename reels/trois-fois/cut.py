#!/usr/bin/env python3
"""src/raw.mov (Drive « 3 fois ») -> assets/aroll.mp4: keep 0-10.85 s minus the two dead pauses, play 12 % faster (as her
validated version), lilac look, face retouch. Audio kept inside aroll.mp4."""
import subprocess, sys
SEGS = [(0.0, 3.20), (3.66, 6.62), (7.25, 10.85)]
SPEED, PY = 1.12, sys.executable
fc = []
for i, (a, b) in enumerate(SEGS):
    fc += [f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]', f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.02,areverse[a{i}]']
fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(SEGS))) + f'concat=n={len(SEGS)}:v=1:a=1[vc][ac]')
fc += [f'[vc]setpts=PTS/{SPEED},fps=30[v]', f'[ac]atempo={SPEED}[a]']
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', 'src/raw.mov', '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', 'work/nat.mp4'], check=True)
subprocess.run([PY, 'lilac.py', 'work/nat.mp4', 'work/lil.mp4'], check=True)
subprocess.run([PY, '../../.claude/skills/video-edit/scripts/retouch.py', 'work/lil.mp4', 'assets/aroll.mp4', '--no-face'], check=True)   # no face retouch here (her ask, 23 Nov: too retouched)
