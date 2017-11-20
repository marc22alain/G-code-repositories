import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
import simple_generators as sg


class Test_bore_circle(unittest.TestCase):

    def basic_match1(self):
        return "G90 \nG0 Z100.0 \nG91 \nG0 X-1.825 Y0.0 \nG90 \nG0 Z4.0 \nG90 \nG1 Z1.0 \nG91 G17 G2 X0.0 Y0.0 I1.825 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I1.825 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X1.825 Y0.0 \n"

    def basic_match2(self):
        return "G90 \nG0 Z100.0 \nG91 \nG0 X-4.5 Y0.0 \nG90 \nG0 Z1.0 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X4.5 Y0.0 \n"

    def basic_match3(self):
        return "G90 \nG0 Z100.0 \nG91 \nG0 X-4.5 Y0.0 \nG90 \nG0 Z5.0 \nG90 \nG1 Z4.0 \nG91 G17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG90 \nG1 Z3.0 \nG91 G17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG90 \nG1 Z2.0 \nG91 G17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG90 \nG1 Z1.0 \nG91 G17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X4.5 Y0.0 \n"

    def basic_match4(self):
        return "G90 \nG0 Z100.0 \nG91 \nG0 X-4.2 Y0.0 \nG90 \nG0 Z3.5 \nG90 \nG1 Z2.3 \nG91 G17 G2 X0.0 Y0.0 I4.2 J0.0 P1 \nG90 \nG1 Z1.1 \nG91 G17 G2 X0.0 Y0.0 I4.2 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I4.2 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X4.2 Y0.0 \n"

    def basic_bore(self):
        g_code = sg.bore_circle_ID(100, 4, 3, 0, 6.35, 10)
        match = self.basic_match1()
        self.assertEqual(g_code, match, "not a match")

    def basic_bore_FAIL(self):
        g_code = sg.bore_circle_ID(100, 4, 3, 0, 6.35, 11)
        match = self.basic_match1()
        self.assertNotEqual(g_code, match, "not a match")

    def max_cut_more_than_thickness(self):
        g_code = sg.bore_circle_ID(100, 1, 10, 0, 1, 10)
        match = self.basic_match2()
        self.assertEqual(g_code, match, "not a match")

    def max_cut_equal_to_thickness(self):
        g_code = sg.bore_circle_ID(100, 1, 1, 0, 1, 10)
        match = self.basic_match2()
        self.assertEqual(g_code, match, "not a match")

    def many_cuts(self):
        g_code = sg.bore_circle_ID(100, 5, 1, 0, 1, 10)
        match = self.basic_match3()
        self.assertEqual(g_code, match, "not a match")

    def all_floats(self):
        g_code = sg.bore_circle_ID(100, 3.5, 1.2, 0, 1.9, 10.3)
        match = self.basic_match4()
        self.assertEqual(g_code, match, "not a match")

    def bore_OD_equal_ID(self):
        g_code_ID = sg.bore_circle_ID(100, 11.3, 3, 1.1, 2.5, 15)
        g_code_OD = sg.bore_circle_OD(100, 11.3, 3, 1.1, 2.5, 10)
        self.assertEqual(g_code_ID, g_code_OD, "not a match")


def suiteAdd():
    suite = unittest.TestSuite()
    suite.addTest(Test_bore_circle("basic_bore"))
    suite.addTest(Test_bore_circle("basic_bore_FAIL"))
    suite.addTest(Test_bore_circle("max_cut_more_than_thickness"))
    suite.addTest(Test_bore_circle("max_cut_equal_to_thickness"))
    suite.addTest(Test_bore_circle("many_cuts"))
    suite.addTest(Test_bore_circle("all_floats"))
    suite.addTest(Test_bore_circle("bore_OD_equal_ID"))
    return suite



class Test_bore_tabbed_circle(unittest.TestCase):
    """ arguments: (Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, tab_width)
    """

    def proven_doughnut(self):
        # example run with machine on 16-05-13
        return 'F1000.0 \nG90 \nG0 Z40.0 \nG91 \nG0 X-56.6185 Y0.0 \nG90 \nG0 Z4.5 \nG90 \nG1 Z1.5 \nG91 G17 G2 X0.0 Y0.0 I56.6185 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z40.0 \nG91 \nG0 X56.6185 Y0.0 \nG90 \nG0 Z40.0 \nG91 \nG0 X-55.53137 Y11.04178 \nG90 \nG1 Z0.0 \nG91 G17 G2 X83.84062 Y37.99128 I55.53137 J-11.04178 P1 \nG0 Z1.5 \nG91 G17 G2 X9.0189 Y-6.46237 I-28.30925 J-49.03306 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y-85.14138 I-37.32815 J-42.57069 P1 \nG0 Z1.5 \nG91 G17 G2 X-9.0189 Y-6.46237 I-37.32815 J42.57069 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X-84.92775 Y49.03306 I-28.30925 J49.03306 P1 \nG90 \nG0 Z40.0 \nG91 \nG0 X56.6185 Y0.0 \nG90 \nG0 Z40.0 \nG91 \nG0 X-77.3815 Y0.0 \nG90 \nG0 Z4.5 \nG90 \nG1 Z1.5 \nG91 G17 G2 X0.0 Y0.0 I77.3815 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z40.0 \nG91 \nG0 X77.3815 Y0.0 \nG90 \nG0 Z40.0 \nG91 \nG0 X-76.58488 Y11.07484 \nG90 \nG1 Z0.0 \nG91 G17 G2 X115.27563 Y55.93951 I76.58488 J-11.07484 P1 \nG0 Z1.5 \nG91 G17 G2 X9.19278 Y-6.22731 I-38.69075 J-67.01434 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y-121.57407 I-47.88353 J-60.78704 P1 \nG0 Z1.5 \nG91 G17 G2 X-9.19278 Y-6.22731 I-47.88353 J60.78704 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X-116.07225 Y67.01434 I-38.69075 J67.01434 P1 \nG90 \nG0 Z40.0 \nG91 \nG0 X77.3815 Y0.0 \nG90 \nM2 \n'

    def tabbed_bore_OD_equal_ID(self):
        g_code_ID = sg.bore_tabbed_ID(100, 11.3, 3, 1.1, 2.5, 55, 6.35)
        g_code_OD = sg.bore_tabbed_OD(100, 11.3, 3, 1.1, 2.5, 50, 6.35)
        self.assertEqual(g_code_ID, g_code_OD, "not a match")

    def full_doughnut(self):
        g_code = sg.startProgram(1000)
        g_code += sg.bore_circle_ID(40, 4.5, 3, 1.5, 4.763, 118)
        g_code += sg.bore_tabbed_ID(40, 1.5, 3, 1.5, 4.763, 118, 6.35)
        g_code += sg.bore_circle_OD(40, 4.5, 3, 1.5, 4.763, 150)
        g_code += sg.bore_tabbed_OD(40, 1.5, 3, 1.5, 4.763, 150, 6.35)
        g_code += sg.endProgram()
        match = self.proven_doughnut()
        self.assertEqual(g_code, match, "not a match")

def bore_tabbed_circle_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_bore_tabbed_circle("tabbed_bore_OD_equal_ID"))
    suite.addTest(Test_bore_tabbed_circle("full_doughnut"))
    return suite



class Test_polar_holes(unittest.TestCase):
    """ arguments: (Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, num_holes, hole_circle_diameter)
    """

    def basic_match1(self):
        return "G90 \nG0 Z100.0 \nG91 \nG0 X5.0 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-2.0 Y0.0 \nG90 \nG0 Z3.0 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I2.0 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X2.0 Y0.0 \nG91 \nG0 X-10.0 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-2.0 Y0.0 \nG90 \nG0 Z3.0 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I2.0 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X2.0 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X5.0 Y-0.0 \n"

    def proven_drill(self):
        # example run with machine on 16-05-13
        return "G90 \nG0 Z40.0 \nG91 \nG0 X65.75 Y0.0 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z40.0 \nG91 \nG0 X-32.875 Y56.94117 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z40.0 \nG91 \nG0 X-65.75 Y0.0 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z40.0 \nG91 \nG0 X-32.875 Y-56.94117 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z40.0 \nG91 \nG0 X32.875 Y-56.94117 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z40.0 \nG91 \nG0 X65.75 Y-0.0 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z40.0 \nG90 \nG0 Z40.0 \nG91 \nG0 X-32.875 Y56.94117 \n"

    def tabbed_two_polar_holes(self):
        g_code = sg.polar_holes(100, 3.0, 3.0, 0, 1, 5, 2, 10)
        match = self.basic_match1()
        self.assertEqual(g_code, match, "not a match")

    def proven_straight_drill1(self):
        g_code = sg.polar_holes(40, 4.5, 3, 0, 2, 2, 6, 131.5)
        match = self.proven_drill()
        self.assertEqual(g_code, match, "not a match")

    def proven_straight_drill2(self):
        # challenging that different bit sizes do not change the program
        g_code = sg.polar_holes(40, 4.5, 3, 0, 4.763, 4.763, 6, 131.5)
        match = self.proven_drill()
        self.assertEqual(g_code, match, "not a match")


def polar_holes_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_polar_holes("tabbed_two_polar_holes"))
    suite.addTest(Test_polar_holes("proven_straight_drill1"))
    suite.addTest(Test_polar_holes("proven_straight_drill2"))
    return suite



class Test_rectangular_area(unittest.TestCase):
    """ arguments: (area, bit_diameter), with
    area as (length, width)
    """

    def bit_too_large(self):
        return sg.rectArea((1,1), 20)

    def test_bit_too_large(self):
        self.assertRaises(ValueError, self.bit_too_large)

    def test_single_pass(self):
        g_code = sg.rectArea((10,20), 10)
        match = "G91 \nG1 Y10.0 \nG1 X0.0 Y-10.0 \nG90 \n"
        self.assertEqual(g_code, match, "not a match, got \n%s" % g_code)

    def test_two_passes(self):
        g_code = sg.rectArea((15,20), 10)
        match = "G91 \nG1 Y10.0 \nG1 X5.0 \nG1 Y-10.0 \nG1 X-5.0 Y0.0 \nG90 \n"
        self.assertEqual(g_code, match, "not a match, got \n%s" % g_code)

    def test_three_passes(self):
        g_code = sg.rectArea((25,20), 10)
        match = "G91 \nG1 Y10.0 \nG1 X9.5 \nG1 Y-10.0 \nG1 X5.5 \nG1 Y10.0 \nG1 X-15.0 Y-10.0 \nG90 \n"
        self.assertEqual(g_code, match, "not a match, got \n%s" % g_code)

    def test_odd_multi_pass(self):
        g_code = sg.rectArea((200,220),19.05)
        match = "G91 \nG1 Y200.95 \nG1 X18.55 \nG1 Y-200.95 \nG1 X18.55 \nG1 Y200.95 \nG1 X18.55 \nG1 Y-200.95 \nG1 X18.55 \nG1 Y200.95 \nG1 X18.55 \nG1 Y-200.95 \nG1 X18.55 \nG1 Y200.95 \nG1 X18.55 \nG1 Y-200.95 \nG1 X18.55 \nG1 Y200.95 \nG1 X18.55 \nG1 Y-200.95 \nG1 X14.0 \nG1 Y200.95 \nG1 X-180.95 Y-200.95 \nG90 \n"
        self.assertEqual(g_code, match)

    def test_even_multi_pass(self):
        """ Tested on the machine. """
        g_code = sg.rectArea((100,220),19.05)
        match = "G91 \nG1 Y200.95 \nG1 X18.55 \nG1 Y-200.95 \nG1 X18.55 \nG1 Y200.95 \nG1 X18.55 \nG1 Y-200.95 \nG1 X18.55 \nG1 Y200.95 \nG1 X6.75 \nG1 Y-200.95 \nG1 X-80.95 Y0.0 \nG90 \n"
        self.assertEqual(g_code, match)


def rect_area_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_rectangular_area("test_bit_too_large"))
    suite.addTest(Test_rectangular_area("test_single_pass"))
    suite.addTest(Test_rectangular_area("test_two_passes"))
    suite.addTest(Test_rectangular_area("test_three_passes"))
    suite.addTest(Test_rectangular_area("test_odd_multi_pass"))
    suite.addTest(Test_rectangular_area("test_even_multi_pass"))
    return suite


class Test_rounded_rectangle(unittest.TestCase):
    """
    Tests roundedRectangle(length, width, corner_radius, bit_diameter, path_ref='outside')
    """

    def test_invalid_corner_radius(self):
        """ Checks assertions for valid corner_radius. """
        def no_radius():
            return sg.roundedRectangle(50, 50, 0, 5, 'center')
        self.assertRaises(ValueError, no_radius)
        def small_radius():
            return sg.roundedRectangle(50, 50, 2, 5, 'outside')
        self.assertRaises(ValueError, small_radius)

    def test_equivalent_args(self):
        """ Checks that path_ref-equivalent function calls produce the same G-code. """
        def center_ref():
            return sg.roundedRectangle(46, 46, 10, 4, 'center')
        def outside_ref():
            return sg.roundedRectangle(50, 50, 12, 4, 'outside')
        def inside_ref():
            return sg.roundedRectangle(42, 42, 8, 4, 'inside')
        self.assertEqual(center_ref(), outside_ref())
        self.assertEqual(inside_ref(), outside_ref())


def rounded_rect_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_rounded_rectangle("test_invalid_corner_radius"))
    suite.addTest(Test_rounded_rectangle("test_equivalent_args"))
    return suite
