"""Safe, non-invasive Wispbyte host capability scan. No secrets printed."""
import os
import platform
import shutil
import sys
import time
from datetime import datetime, timezone

def say(key, value):
    print(f"[HOST CHECK] {key}: {value}", flush=True)

def read_limit(path):
    try:
        with open(path, encoding="utf-8") as f:
            value = f.read().strip()
        if value == "max":
            return "unlimited by this cgroup setting"
        n = int(value)
        if n > 1 << 60:
            return "not explicitly limited by cgroup"
        return f"{n / (1024**2):.0f} MiB"
    except (OSError, ValueError):
        return "unavailable"

def scan():
    print("=== DISCORD PHONE GATEWAY HOST COMPATIBILITY CHECK ===", flush=True)
    say("mode", "diagnostic only; no phone calls or SIP registration")
    say("Python", sys.version.split()[0])
    say("OS", platform.system() + " " + platform.release())
    say("Architecture", platform.machine())
    for name in ("chromium", "chromium-browser", "google-chrome", "firefox",
                 "baresip", "pactl", "pipewire", "wireplumber",
                 "Xvfb", "ffmpeg", "git", "apt-get", "apk"):
        say(name, shutil.which(name) or "NOT FOUND")
    say("DISPLAY configured", bool(os.environ.get("DISPLAY")))
    say("WAYLAND_DISPLAY configured", bool(os.environ.get("WAYLAND_DISPLAY")))
    say("XDG_RUNTIME_DIR configured", bool(os.environ.get("XDG_RUNTIME_DIR")))
    say("PulseAudio socket available", os.path.exists("/run/user/%d/pulse/native" % os.getuid()))
    say("/dev/snd exists", os.path.exists("/dev/snd"))
    say("Memory cgroup v2", read_limit("/sys/fs/cgroup/memory.max"))
    say("Memory cgroup v1", read_limit("/sys/fs/cgroup/memory/memory.limit_in_bytes"))
    try:
        mem = [x for x in open("/proc/meminfo", encoding="utf-8") if x.startswith(("MemTotal:", "MemAvailable:"))]
        for line in mem:
            key, value = line.strip().split(":", 1)
            say(key + " (host-level; not quota)", value.strip())
    except OSError:
        say("Host memory", "unavailable")
    try:
        usage = shutil.disk_usage(".")
        say("Working directory free disk", f"{usage.free / (1024**2):.0f} MiB")
    except OSError:
        say("Working directory free disk", "unavailable")
    say("TextNow browser calling", "NOT TESTED")
    say("SIPcord registration on this host", "NOT TESTED")
    say("Two-way virtual audio bridge", "NOT TESTED")
    print("=== END HOST CHECK ===", flush=True)

scan()
while True:
    print(f"[{datetime.now(timezone.utc).isoformat()}] Diagnostic placeholder running; phone gateway NOT implemented.", flush=True)
    time.sleep(300)
