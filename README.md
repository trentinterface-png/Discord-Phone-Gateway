# Discord Phone Gateway

**Status: experimental proof of concept — NOT a working PSTN-to-Discord gateway yet.**

## Goal
Friend calls an ordinary phone number on a flip phone -> internet calling service receives call -> gateway answers and dials SIPcord extension **1002** -> two-way Discord voice -> hangs up with caller.

## Confirmed working (on Motorola)
- Dedicated Discord identity: triotrombot
- SIPcord server: `bridge-usw1.sipcord.net`
- SIPcord SIP username: `epic-dragon41`
- SIPcord extension: **1002**
- Linphone registers and successfully calls 1002 with two-way audio.

## Not yet implemented or verified
- Automatic incoming TextNow browser call detection / answering
- Virtual audio routing between TextNow web calling and Baresip
- Baresip registration against SIPcord
- Automatic call setup, teardown, reconnection
- Free, always-on graphical Linux host

**Security:** A SIPcord password was exposed in chat. Rotate it before deployment. Never commit SIP passwords, browser profiles/cookies, phone numbers, or API tokens. Use private local configuration and environment secrets.

## Planned architecture (not proven)
TextNow **browser** <-> PipeWire virtual audio devices <-> Baresip SIP client <-> SIPcord extension 1002 <-> Discord voice channel.

TextNow does not provide an official public API for automatic inbound-call control. Browser automation may be fragile or unavailable. A GitHub repo alone is not a continuously running voice gateway, and ordinary free web hosting usually cannot run Chromium + PipeWire + SIP media persistently.

## Local POC on Debian/Ubuntu graphical Linux
1. Install `baresip`, `pipewire`, `pipewire-pulse`, `wireplumber`, `pulseaudio-utils`, and `pavucontrol` via your distribution package manager.
2. Run `bash check.sh` to inspect tools and audio session.
3. Run `bash setup_audio.sh` to create virtual audio sinks (reversible).
4. Configure Baresip locally in `~/.baresip/accounts` with **newly rotated** SIPcord password. Do NOT place credentials in this repository.
5. Independently test Baresip registering and dialing 1002 before trying browser-audio integration.
6. Sign into TextNow in a graphical browser and manually check an inbound call.
7. Use `pavucontrol` to manually route TextNow audio into Baresip and vice versa; verify both directions. This is a test hypothesis, not a preconfigured end-to-end bridge.

## Next milestone
**One manually answered TextNow call with intelligible audio both directions through Baresip to Discord**. Only after proving that should we automate answering/dialing and pick a reliable host.

## Scope
Completely separate from the already-working `discord-sms-bridge` repository, Worker, MacroDroid and TextNow SMS macros.
