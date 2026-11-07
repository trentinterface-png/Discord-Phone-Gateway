import pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class AsteriskConfigTests(unittest.TestCase):
    def test_routes(self):
        d=(ROOT/"asterisk/extensions.conf").read_text()
        self.assertIn("Dial(PJSIP/1001@sipcord",d)
        self.assertIn("Dial(PJSIP/1002@sipcord",d)
        self.assertIn("Background(custom/choose-channel)",d)
    def test_secrets_placeholder_only(self):
        p=(ROOT/"asterisk/pjsip.conf.template").read_text()
        self.assertIn("{{SIPCORD_PASSWORD}}",p)
        self.assertIn("{{GATEWAY_IP}}",p)
    def test_rtp_range(self):
        r=(ROOT/"asterisk/rtp.conf").read_text()
        self.assertIn("rtpstart=10000",r)
        self.assertIn("rtpend=10019",r)
if __name__=="__main__": unittest.main()
