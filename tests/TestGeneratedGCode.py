import unittest
from post_processor import PostProcessor


def testWithProgram(program, scenario, machine_params):
    class TestGeneratedGCode(unittest.TestCase):

        @classmethod
        def setUpClass(TestGeneratedGCode):
            g = PostProcessor(machine_params)
            g.setProgram(program)
            g.parseProgram()
            TestGeneratedGCode.program_data = g.getProgramData()

        def test_program_ends_without_errors(self):
            self.assertEqual(len(self.program_data['program_errors'].keys()), 0, 'No errors were raised)')

        def test_program_ends_at_origin(self):
            ending_x_pos = round(self.program_data['ending_x_pos'], 5)
            ending_y_pos = round(self.program_data['ending_y_pos'], 5)
            ending_z_pos = round(self.program_data['ending_z_pos'], 5)
            self.assertEqual(ending_x_pos, 0, 'Program should end at X=0; ended at %f' % (ending_x_pos))
            self.assertEqual(ending_y_pos, 0, 'Program should end at Y=0; ended at %f' % (ending_y_pos))
            self.assertEqual(ending_z_pos, 80, 'Program should end at Z=80; ended at %f' % (ending_z_pos))

        def test_program_ends_in_ABS_mode(self):
            self.assertEqual(self.program_data['ending_mode'], 'abs', 'Program ends in ABS mode')

        def test_program_ends(self):
            self.assertTrue(self.program_data['program_ended'], 'Program ends with END command')

        def test_program_defines_feed_rate(self):
            self.assertTrue(self.program_data['feed_rate'] > 0, 'Program defines feed rate')

        def test_program_avoids_negative_Z(self):
            self.assertFalse(self.program_data['negative_Z'], 'Program avoids negative Z')

        def test_program_matches_benchmark_program(self):
            len1 = len(program)
            len2 = len(scenario['benchmark']['program'])
            # print '- - - - - - - '
            # print 'is this matching %s :: %s ?' % (str(len1), str(len2))
            # print '- - - - - - - '
            self.assertEqual(len1, len2, 'Program g-code matches benchmark length')
            self.assertEqual(program, scenario['benchmark']['program'], 'Program g-code matches benchmark')

        def test_optimized_program(self):
            print(self.program_data['processed_gcode'])


    suite = unittest.TestSuite()
    suite.addTest(TestGeneratedGCode("test_program_ends_without_errors"))
    suite.addTest(TestGeneratedGCode("test_program_ends_at_origin"))
    suite.addTest(TestGeneratedGCode("test_program_ends_in_ABS_mode"))
    suite.addTest(TestGeneratedGCode("test_program_ends"))
    suite.addTest(TestGeneratedGCode("test_program_defines_feed_rate"))
    suite.addTest(TestGeneratedGCode("test_program_avoids_negative_Z"))
    suite.addTest(TestGeneratedGCode("test_optimized_program"))

    if 'benchmark' in scenario.keys():
        if 'program' in scenario['benchmark'].keys():
            suite.addTest(TestGeneratedGCode("test_program_matches_benchmark_program"))

    unittest.TextTestRunner().run(suite)
