import unittest
from fun_testing_phone_thing import Lab, State

class RecoveryTests(unittest.TestCase):
    def test_vulnerable_transition(self):
        x=Lab("vulnerable"); x.face_scan_attempt()
        self.assertEqual(x.state, State.FACE_ID_ELIGIBLE)
    def test_patched_blocks_transition(self):
        x=Lab("patched"); x.face_scan_attempt()
        self.assertEqual(x.state, State.PASSCODE_REQUIRED)

if __name__=="__main__": unittest.main()
