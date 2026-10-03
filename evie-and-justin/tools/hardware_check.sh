#!/usr/bin/env bash
# Run on the machine you'll use for production. Paste the output back to the lead (Claude).
echo "== OS ==";  uname -a 2>/dev/null; sw_vers 2>/dev/null; ver 2>/dev/null
echo "== CPU ==";  (lscpu 2>/dev/null | grep -E 'Model name|^CPU\(s\)') || sysctl -n machdep.cpu.brand_string 2>/dev/null
echo "== RAM ==";  (free -h 2>/dev/null | sed -n 1,2p) || sysctl -n hw.memsize 2>/dev/null
echo "== GPU ==";  (nvidia-smi --query-gpu=name,memory.total --format=csv 2>/dev/null) || (system_profiler SPDisplaysDataType 2>/dev/null | grep -E 'Chipset|VRAM|Chip') || echo "no NVIDIA GPU found"
echo "== DISK ==";  df -h . | tail -1
echo "== TOOLS =="; for t in python3 ffmpeg git; do command -v $t >/dev/null && echo "$t: yes" || echo "$t: no"; done
