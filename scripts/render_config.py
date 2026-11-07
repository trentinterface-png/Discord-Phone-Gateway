#!/usr/bin/env python3
"""Render Asterisk template locally: never write secrets to GitHub."""
import getpass, ipaddress, os, pathlib, re
root = pathlib.Path(__file__).resolve().parents[1]
out = root / ".private-asterisk"
out.mkdir(mode=0o700, exist_ok=True)
os.chmod(out, 0o700)
gateway = input("Trusted telephone gateway IPv4 address: ").strip()
try:
    if ipaddress.ip_address(gateway).version != 4:
        raise ValueError("Expected IPv4")
except ValueError as exc:
    raise SystemExit(f"Invalid gateway IPv4: {exc}")
username = input("SIPcord username [epic-dragon41]: ").strip() or "epic-dragon41"
if not re.fullmatch(r"[A-Za-z0-9_.-]+", username):
    raise SystemExit("Invalid SIP username")
password = getpass.getpass("SIPcord password (hidden): ")
if not password or "\n" in password or "\r" in password:
    raise SystemExit("Invalid password")
src = (root / "asterisk" / "pjsip.conf.template").read_text()
for key, value in {"GATEWAY_IP":gateway,"SIPCORD_USER":username,"SIPCORD_PASSWORD":password}.items():
    src = src.replace("{{" + key + "}}", value)
target = out / "pjsip.conf"
fd = os.open(str(target), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w") as f:
    f.write(src)
os.chmod(target, 0o600)
print("Created private configuration at", target)
print("Copy it securely to /etc/asterisk/pjsip.conf on your server.")
print("Never commit .private-asterisk or publish configuration with passwords.")
