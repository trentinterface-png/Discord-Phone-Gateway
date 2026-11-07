#!/usr/bin/env bash
set -euo pipefail
if [[ "${EUID}" -ne 0 ]]; then echo "Run as root with sudo" >&2; exit 1; fi
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y asterisk espeak-ng ffmpeg
echo "Dependencies installed. Run python3 scripts/render_config.py as your normal user."
echo "After copying generated configuration to /etc/asterisk, create the menu prompt:"
echo 'espeak-ng -v en-us -s 135 -w /tmp/menu.wav "Press 1 for Gaming. Press 2 for Lobby."'
echo 'ffmpeg -y -i /tmp/menu.wav -ar 8000 -ac 1 -c:a pcm_s16le /var/lib/asterisk/sounds/custom/choose-channel.wav'
echo 'Then: sudo systemctl restart asterisk'
