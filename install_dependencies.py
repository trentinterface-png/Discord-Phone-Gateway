"""One-time best-effort installation of Linux gateway dependencies.
Only runs apt as root. Does not alter Python dependency files or reveal secrets.
If blocked by container restrictions, logs the blocker and exits successfully.
"""
import os, shutil, subprocess, time

PACKAGES = ["baresip", "pipewire", "pipewire-pulse", "wireplumber",
            "pulseaudio-utils", "xvfb", "chromium"]

def emit(line):
    print("[INSTALL] " + line, flush=True)

def installed():
    return {name: bool(shutil.which(name)) for name in
            ("baresip", "pipewire", "pactl", "Xvfb", "chromium", "chromium-browser", "google-chrome")}

def run_command(args, timeout):
    try:
        p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, timeout=timeout, check=False)
        last = (p.stdout or "").splitlines()[-12:]
        for line in last: emit(line[:350])
        return p.returncode
    except (OSError, subprocess.TimeoutExpired) as ex:
        emit(f"could not finish {args[0]}: {type(ex).__name__}")
        return 1

def install_once():
    before = installed()
    emit("Available before: " + ", ".join(k for k,v in before.items() if v))
    if all((before["baresip"], before["pactl"], before["Xvfb"],
            any(before[k] for k in ("chromium","chromium-browser","google-chrome")))):
        emit("Required commands already available; skipping installation")
        return
    if os.geteuid() != 0:
        emit("BLOCKED: server user is not root. Cannot apt-install Linux packages in this container.")
        emit("Changing pip requirements cannot install these operating-system programs.")
        return
    if not shutil.which("apt-get"):
        emit("BLOCKED: apt-get not available. Provider must permit a custom image.")
        return
    emit("Attempting apt-get installation with 180-second overall process timeout per step.")
    if run_command(["apt-get","update","-qq"], 120) != 0:
        emit("apt repository refresh failed; leaving existing files intact")
        return
    command=["apt-get", "install", "-y", "-qq", "--no-install-recommends"]+PACKAGES
    if run_command(command, 180) != 0:
        emit("Package installation failed or exceeded time limit; check disk/memory/permissions")
    after=installed()
    emit("Available after: " + ", ".join(k for k,v in after.items() if v))
    emit("Warning: successful install does NOT prove browser, audio, or TextNow integration.")

if __name__ == "__main__":
    install_once()
