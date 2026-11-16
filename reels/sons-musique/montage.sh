#!/bin/bash
# PY montage.sh <out> <src:start:dur:zoom> ... -> cut each piece (top-anchored static punch so her face sits under the bar), concat, retouch
out=$1; shift; i=0; : > work/m.txt
for p in "$@"; do IFS=: read f t d z <<< "$p"; W=$(python3 -c "print(round(1080*$z/2)*2)"); H=$(python3 -c "print(round(1920*$z/2)*2)")
  ffmpeg -nostdin -v error -y -ss $t -t $d -i $f -an -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=$W:$H:flags=lanczos,crop=1080:1920:(iw-1080)/2:0,fps=30" -c:v libx264 -crf 15 -pix_fmt yuv420p work/mp$i.mp4
  echo "file 'mp$i.mp4'" >> work/m.txt; i=$((i+1)); done
ffmpeg -nostdin -v error -y -f concat -safe 0 -i work/m.txt -c copy work/mcat.mp4
$PY ../../.claude/skills/video-edit/scripts/retouch.py work/mcat.mp4 $out
