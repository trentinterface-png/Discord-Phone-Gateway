# Asterisk IVR: phone -> SIPcord -> Discord

**Status: prepared config, not yet deployed or verified with real telephone calls.**
This is ONLY the telephone routing layer. The existing hosted SIPcord service remains the Discord bridge.

## Routes
- Dial 1 -> SIPcord extension 1001 -> Gaming channel 1565811189395755136
- Dial 2 -> SIPcord extension 1002 -> Lobby channel 1565811189395755135

## Requirements
- Debian/Ubuntu Linux host with permission to install Asterisk and keep it online.
- Inbound publicly reachable **UDP 5060 and UDP 10000-10019** (or corresponding mapped ports).
- A legitimate PSTN/SIP gateway capable of routing an incoming regular-phone call to YOUR Asterisk host.
- Gateway's stable source IP for the IP allowlist; SIPcord credentials entered privately.
- SIPcord must permit outbound calls using challenge authentication from Asterisk. This is **not yet verified**.

## Setup (do not run on Android, GitHub Actions, or Serv00 FreeBSD)
1. In the repository root: `sudo bash scripts/install_debian.sh`.
2. Run `python3 scripts/render_config.py`. Enter the gateway IP and SIPcord password **locally**.
3. `sudo cp .private-asterisk/pjsip.conf /etc/asterisk/pjsip.conf`
4. `sudo cp asterisk/extensions.conf asterisk/rtp.conf /etc/asterisk/`
5. `sudo mkdir -p /var/lib/asterisk/sounds/custom`
6. `espeak-ng -v en-us -s 135 -w /tmp/menu.wav "Press 1 for Gaming. Press 2 for Lobby."`
7. `sudo ffmpeg -y -i /tmp/menu.wav -ar 8000 -ac 1 -c:a pcm_s16le /var/lib/asterisk/sounds/custom/choose-channel.wav`
8. `sudo systemctl restart asterisk`; inspect `sudo asterisk -rx 'pjsip show endpoints'`.
9. Limit ingress to the known gateway IP with a firewall; permit RTP only from known providers where possible. Make a test call and review Asterisk verbose output.

## Known limitations / must test
- Without a working PSTN gateway, a flip phone cannot reach this.
- Some SIPcord deployments REQUIRE registration or a SIP outbound proxy; the simple outbound-auth template may not suffice.
- SIP Broker and SIPcord are NOT interchangeable SIP services. Call path and DTMF must be tested.
- Incoming endpoint identification is by trusted source IP, not a password. Restrict at firewall.
- VPS free plan must allow all UDP RTP ports; 3-5 NAT-forwarded ports generally won't cover this config.
- If host uses IPv6-only networking, verify the PSTN provider and SIPcord support it before deploying.
- Caller DTMF must arrive as RFC4733 or SIP INFO depending on the gateway; test menu keypresses.
- Change the SIPcord password if it was ever exposed.
- This repository's old TextNow/virtual-audio prototype remains unchanged.
