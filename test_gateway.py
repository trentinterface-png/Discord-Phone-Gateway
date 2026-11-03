import unittest
from gateway import DryRunBridge, CallState, self_test

class GatewayTests(unittest.TestCase):
    def test_happy_path(self):
        self.assertEqual(len(self_test()), 4)

    def test_unknown_route(self):
        with self.assertRaises(ValueError):
            DryRunBridge().incoming("not_configured")

    def test_reject_duplicate_active_call(self):
        bridge = DryRunBridge()
        bridge.incoming()
        with self.assertRaises(RuntimeError):
            bridge.incoming()

    def test_no_hangup_when_idle(self):
        with self.assertRaises(RuntimeError):
            DryRunBridge().hangup()

if __name__ == "__main__":
    unittest.main()
