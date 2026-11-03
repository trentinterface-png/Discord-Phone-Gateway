"""Temporary Wispbyte startup placeholder; NOT a working voice gateway."""
import time
from datetime import datetime, timezone

print("Discord Phone Gateway POC: startup OK", flush=True)
print("Voice relay, TextNow answering, and SIPcord dialing are NOT implemented.", flush=True)
while True:
    print(f"[{datetime.now(timezone.utc).isoformat()}] POC idle; awaiting validated audio implementation", flush=True)
    time.sleep(300)
