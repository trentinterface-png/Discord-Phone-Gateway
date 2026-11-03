#!/usr/bin/env bash
set -euo pipefail
for program in baresip pactl pavucontrol; do
  if command -v "$program" >/dev/null; then echo "OK: $program"; else echo "MISSING: $program"; fi
done
printf '\nAudio server: '
pactl info 2>/dev/null | grep 'Server Name:' || true
printf '\nVirtual sinks and mic:\n'
pactl list short sinks 2>/dev/null | grep -E 'TN_TO_SIP|SIP_TO_TN' || true
pactl list short sources 2>/dev/null | grep -E 'TN_TO_SIP.monitor|DiscordBridgeMic' || true
