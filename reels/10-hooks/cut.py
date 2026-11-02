#!/usr/bin/env python3
"""10 hooks qui arrêtent le scroll: two raw takes, two reels (v1 = raw1, finger counting, CTA "commente 20";
v2 = raw2, with the mic, CTA "abonne-toi"). One piece per line, pauses cut (audio envelope), normal speed,
her lilac look then her retouch.
PY cut.py v1|v2   -> work/<v>/aroll.mp4 + voice.m4a + segs.json"""
import json
import os
import subprocess
import sys

# (start, end, kind, pill text)   kind: intro / hook / cta / bye
PIECES = {
    'v1': ('raw1', [
        (2.28, 4.10, 'intro', 'qui arrêtent le scroll'),
        (4.44, 6.12, 'hook', "tu vas sûrement pas être d'accord mais"),
        (6.70, 7.86, 'hook', 'personne ne parle de ça'),
        (8.42, 9.82, 'hook', "j'aurais aimé savoir ça plus tôt"),
        (10.38, 12.18, 'hook', 'arrête de scroller, écoute ça'),
        (12.72, 14.32, 'hook', "est-ce que t'as déjà remarqué que"),
        (14.80, 16.74, 'hook', 'la vérité dérangeante à propos de…'),
        (17.36, 19.22, 'hook', 'laisse-moi te faire gagner du temps sur…'),
        (20.00, 21.54, 'hook', 'ça va te surprendre mais'),
        (22.30, 23.64, 'hook', "t'as besoin d'entendre ça aujourd'hui"),
        (24.38, 26.30, 'hook', 'je viens juste de réaliser que…'),
        (26.70, 30.40, 'cta', '20'),
        (30.86, 31.60, 'bye', ''),
    ]),
    'v2': ('raw2', [
        (1.28, 2.92, 'intro', 'qui arrêtent le scroll'),
        (3.32, 4.86, 'hook', "tu vas sûrement pas être d'accord mais"),
        (5.08, 6.28, 'hook', 'personne ne parle de ça'),
        (6.54, 7.80, 'hook', "j'aurais aimé savoir ça plus tôt"),
        (8.20, 9.90, 'hook', 'arrête de scroller et écoute ça'),
        (10.40, 11.70, 'hook', "est-ce que t'as déjà remarqué que"),
        (12.00, 14.02, 'hook', 'la vérité dérangeante à propos de…'),
        (14.46, 16.04, 'hook', 'laisse-moi te faire gagner du temps sur…'),
        (16.44, 17.88, 'hook', 'ça va te surprendre mais'),
        (18.38, 19.62, 'hook', "t'as besoin d'entendre ça aujourd'hui"),
        (20.16, 21.96, 'hook', 'je viens juste de réaliser quelque chose'),
        (22.30, 23.50, 'cta', 'pour plus de conseils'),
    ]),
}
PY = sys.executable

if __name__ == '__main__':
    v = sys.argv[1]
    src, pieces = PIECES[v]
    d = f'work/{v}'
    os.makedirs(d, exist_ok=True)
    parts = []
    for i, (a, b, *_r) in enumerate(pieces):
        p = f'{d}/p{i:02d}.mp4'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', f'src/{src}.mp4', '-vf', 'fps=30',
                        '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
                        '-ac', '2', '-af', 'afade=t=in:d=0.02,areverse,afade=t=in:d=0.03,areverse', p], check=True)
        parts.append(p)
    with open(f'{d}/parts.txt', 'w') as f:
        f.write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{d}/parts.txt', '-c', 'copy', f'{d}/nat.mp4'], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{d}/nat.mp4', '-vn', '-c:a', 'copy', f'{d}/voice.m4a'], check=True)
    subprocess.run([PY, 'lilac.py', f'{d}/nat.mp4', f'{d}/lilac.mp4'], check=True)
    subprocess.run([PY, '/root/.claude/skills/video-edit/scripts/retouch.py', f'{d}/lilac.mp4', f'{d}/aroll.mp4'], check=True)
    durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                 capture_output=True, text=True).stdout) for p in parts]
    json.dump({'src': src, 'pieces': pieces, 'durs': durs}, open(f'{d}/segs.json', 'w'), ensure_ascii=False)
    print(v, round(sum(durs), 2), 's')
