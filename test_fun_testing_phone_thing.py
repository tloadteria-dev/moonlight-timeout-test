import unittest
from fun_testing_phone_thing import CutePhoneLab, State

class CutePhoneTests(unittest.TestCase):
    def test_vulnerable_removes_simulated_passcode_and_unlocks(self):
        x=CutePhoneLab("vulnerable"); x.simulated_passcode_removal()
        self.assertFalse(x.passcode_enabled)
        self.assertEqual(x.state,State.UNLOCKED)
        self.assertIsNotNone(x.report()["synthetic_user_data_accessible"])
    def test_patched_blocks_simulated_passcode_removal(self):
        x=CutePhoneLab("patched"); x.simulated_passcode_removal()
        self.assertTrue(x.passcode_enabled)
        self.assertEqual(x.state,State.PASSCODE_REQUIRED)
        self.assertIsNone(x.report()["synthetic_user_data_accessible"])

if __name__=="__main__": unittest.main()
