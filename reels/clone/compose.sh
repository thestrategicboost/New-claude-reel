#!/bin/sh
# Final a-roll: empty-wall plate + both cut-out Maé (0 followers 90px left and sharpened, 10K 40px right and
# re-centred with a hard cut at her jump cut, 36.0 s on the c2 track), brighter grade, 1.12x, lilac look, silences cut out.
set -e
ffmpeg -v error -y -loop 1 -framerate 30 -i work/plate.png -c:v libvpx-vp9 -i work/c1_cut.webm -c:v libvpx-vp9 -i work/c2_cut.webm -i work/c1.mp4 \
  -filter_complex "[0:v]format=yuv420p,trim=duration=39.6[bg];[1:v]format=yuva420p,unsharp=7:7:1.5:7:7:0,unsharp=3:3:0.6[a];[2:v]format=yuva420p[b];[bg][a]overlay=x=-90:y=0:enable='lt(t,37)'[m];[m][b]overlay=x='if(lt(t,35.995),40,-202)':y=0:eval=frame,format=yuv420p,curves=all='0/0 0.25/0.33 0.5/0.62 0.8/0.89 1/1',eq=saturation=1.06,setpts=PTS/1.12[v];[3:a]atempo=1.12[au]" \
  -map "[v]" -map "[au]" -r 30 -c:v libx264 -crf 14 -preset fast -c:a aac -b:a 256k work/aroll_bright.mp4
/root/.claude/skills/video-edit/.venv/bin/python lilac.py work/aroll_bright.mp4 work/aroll_lilac_full.mp4
python3 - <<'PY'
import json, subprocess
cuts = json.load(open('work/cuts.json'))
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'work/aroll_lilac_full.mp4'], capture_output=True, text=True).stdout)
keep, t = [], 0
for a, b in cuts:
    keep.append((t, a)); t = b
keep.append((t, dur))
e = '+'.join(f'between(t,{a:.4f},{b:.4f})' for a, b in keep)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/aroll_lilac_full.mp4', '-vf', f"select='{e}',setpts=N/FRAME_RATE/TB", '-af', f"aselect='{e}',asetpts=N/SR/TB",
                '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-c:a', 'aac', '-b:a', '256k', 'assets/aroll.mp4'], check=True)
PY
