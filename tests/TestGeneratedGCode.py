import unittest
from gcode_parser import *


def testWithProgram(program):
    class TestGeneratedGCode(unittest.TestCase):

        @classmethod
        def setUpClass(TestGeneratedGCode):
            g = GCodeParser()
            g.resetProgram(program.split('\n'))
            g.parseProgram()
            TestGeneratedGCode.program_data = g.getProgramData()

        def test_program_ends_without_errors(self):
            self.assertEqual(len(self.program_data['program_errors'].keys()), 0, 'No errors were raised)')

        def test_program_ends_at_origin(self):
            self.assertEqual(self.program_data['ending_x_pos'], 0, 'Program ends at X=0')
            self.assertEqual(self.program_data['ending_y_pos'], 0, 'Program ends at Y=0')
            self.assertEqual(self.program_data['ending_z_pos'], 80, 'Program ends at Z=80')

        def test_program_ends_in_ABS_mode(self):
            self.assertEqual(self.program_data['ending_mode'], 'abs', 'Program ends in ABS mode')

        def test_program_ends(self):
            self.assertTrue(self.program_data['program_ended'], 'Program ends with END command')

        def test_program_defines_feed_rate(self):
            self.assertTrue(self.program_data['feed_rate'] > 0, 'Program defines feed rate')


    suite = unittest.TestSuite()
    suite.addTest(TestGeneratedGCode("test_program_ends_without_errors"))
    suite.addTest(TestGeneratedGCode("test_program_ends_at_origin"))
    suite.addTest(TestGeneratedGCode("test_program_ends_in_ABS_mode"))
    suite.addTest(TestGeneratedGCode("test_program_ends"))
    suite.addTest(TestGeneratedGCode("test_program_defines_feed_rate"))

    unittest.TextTestRunner().run(suite)
