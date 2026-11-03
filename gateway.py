"""Call-routing state machine with explicitly simulated adapters.
NO PSTN/TextNow integration or SIP audio bridge is implemented.
"""
from dataclasses import dataclass
from enum import Enum
from time import monotonic

class CallState(str, Enum):
    IDLE = "idle"
    RINGING = "ringing"
    BRIDGING = "bridging"
    CONNECTED = "connected"
    ENDED = "ended"
    FAILED = "failed"

@dataclass(frozen=True)
class Destination:
    label: str
    extension: str

DESTINATIONS = {"eaglercraft": Destination("Eaglercraft VC", "1002")}

class DryRunBridge:
    """Simulates routing only, never initiates a real telephone or SIP call."""
    def __init__(self):
        self.state = CallState.IDLE
        self.destination = None
        self.started = None
        self.events = []

    def incoming(self, route="eaglercraft"):
        if self.state not in (CallState.IDLE, CallState.ENDED, CallState.FAILED):
            raise RuntimeError("call already in progress")
        if route not in DESTINATIONS:
            raise ValueError("unknown destination")
        self.destination = DESTINATIONS[route]
        self.started = monotonic()
        self.state = CallState.RINGING
        self.events.append(f"SIMULATED inbound call for {self.destination.label}")
        return self.state

    def answer(self):
        if self.state != CallState.RINGING:
            raise RuntimeError("no ringing call")
        self.state = CallState.BRIDGING
        self.events.append(f"SIMULATED SIP dialing extension {self.destination.extension}")
        return self.state

    def media_connected(self):
        if self.state != CallState.BRIDGING:
            raise RuntimeError("not bridging")
        self.state = CallState.CONNECTED
        self.events.append("SIMULATED two-way media connected (NO REAL AUDIO)")
        return self.state

    def hangup(self):
        if self.state not in (CallState.RINGING, CallState.BRIDGING, CallState.CONNECTED):
            raise RuntimeError("no active call")
        self.state = CallState.ENDED
        self.events.append("SIMULATED both legs disconnected")
        return self.state

def self_test():
    call = DryRunBridge()
    assert call.incoming() == CallState.RINGING
    assert call.answer() == CallState.BRIDGING
    assert call.media_connected() == CallState.CONNECTED
    assert call.hangup() == CallState.ENDED
    assert call.destination.extension == "1002"
    return call.events
