# Deployment feasibility (Wispbyte free Python plan)

Measured from actual host startup diagnostic on Nov 3, 2026:
- 589 MiB memory cgroup; Python 3.11 and ffmpeg available.
- Chromium/Chrome/Firefox, Baresip, PipeWire, pactl, Xvfb missing.
- No audio server, /dev/snd, or DISPLAY configured.

**Conclusion:** This is suitable for a lightweight controller/simulator, NOT a proven live media gateway. The reported absence of audio hardware does not by itself rule out virtual audio; current dependencies/resources are insufficient and running them hasn't been validated.

## What is actually working
On the user's Motorola, Linphone registers with SIPcord and joins Discord with two-way audio when dialing 1002.

## Missing integration
1. A *legal and supported* way to receive internet-based PSTN calls as an audio stream (TextNow has no publicly supported inbound call automation/audio API).
2. A host capable of running the telephone media endpoint and authenticated SIP client simultaneously.
3. Bidirectional real-time audio and lifecycle coordination.
4. Sustainable 24/7 hosting with a genuinely free phone number and no quotas: **not verified**.

Do not add SIP passwords or TextNow cookies to GitHub or paste them into issue reports. Rotate previously exposed SIP credentials.

## GitHub -> Wispbyte
The server downloads the repo on **one restart/pull**. This version uses only Python standard library. Startup prints a dry-run self-test and reports that real calls are disabled. No third-party install necessary.

## Future adapters
Replace simulated DryRunBridge with independent interfaces implementing:
- inbound_call: answer, hang_up, media read/write
- outbound_sip: register/authenticate SIPcord, dial 1002, media read/write
- session: propagate disconnects, enforce concurrency and timeouts

**Do not automatically answer or initiate calls before both actual media adapters pass end-to-end tests.**
