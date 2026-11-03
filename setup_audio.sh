#!/usr/bin/env bash
set -euo pipefail
command -v pactl >/dev/null || { echo 'Install pulseaudio-utils and pipewire-pulse first.'; exit 1; }
for name in TN_TO_SIP SIP_TO_TN; do
  if ! pactl list short sinks | awk '{print $2}' | grep -qx "$name"; then
    pactl load-module module-null-sink sink_name="$name" sink_properties="device.description=$name" >/dev/null
  fi
done
if ! pactl list short sources | awk '{print $2}' | grep -qx 'DiscordBridgeMic'; then
  pactl load-module module-remap-source master=SIP_TO_TN.monitor source_name=DiscordBridgeMic source_properties='device.description=DiscordBridgeMic' >/dev/null || echo 'Could not create virtual microphone. Choose SIP_TO_TN.monitor if available.'
fi
printf '\nVirtual paths created; routing is NOT automatically configured.\n'
printf 'TextNow browser playback -> TN_TO_SIP; browser microphone -> DiscordBridgeMic\n'
printf 'Baresip playback -> SIP_TO_TN; Baresip microphone -> TN_TO_SIP.monitor\n'
