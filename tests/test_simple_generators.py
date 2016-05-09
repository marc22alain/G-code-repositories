import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
import simple_generators as sg


class Test_bore_circle(unittest.TestCase):

    def basic_match1(self):
        return "G90 \nG0 Z100 \nG91 \nG0 X-1.825 Y0 \nG90 \nG0 Z4 \nG90 \nG1 Z1 \nG91 G17 G2 X0 Y0 I1.825 J0 P1 \nG90 \nG1 Z0 \nG91 G17 G2 X0 Y0 I1.825 J0 P1 \nG4 P0.5 \nG90 \nG0 Z100 \nG91 \nG0 X1.825 Y0 \n"

    def basic_match2(self):
        return "G90 \nG0 Z100 \nG91 \nG0 X-4.5 Y0 \nG90 \nG0 Z1 \nG90 \nG1 Z0 \nG91 G17 G2 X0 Y0 I4.5 J0 P1 \nG4 P0.5 \nG90 \nG0 Z100 \nG91 \nG0 X4.5 Y0 \n"

    def basic_match3(self):
        return "G90 \nG0 Z100 \nG91 \nG0 X-4.5 Y0 \nG90 \nG0 Z5 \nG90 \nG1 Z4 \nG91 G17 G2 X0 Y0 I4.5 J0 P1 \nG90 \nG1 Z3 \nG91 G17 G2 X0 Y0 I4.5 J0 P1 \nG90 \nG1 Z2 \nG91 G17 G2 X0 Y0 I4.5 J0 P1 \nG90 \nG1 Z1 \nG91 G17 G2 X0 Y0 I4.5 J0 P1 \nG90 \nG1 Z0 \nG91 G17 G2 X0 Y0 I4.5 J0 P1 \nG4 P0.5 \nG90 \nG0 Z100 \nG91 \nG0 X4.5 Y0 \n"

    def basic_match4(self):
        return "G90 \nG0 Z100 \nG91 \nG0 X-4.2 Y0 \nG90 \nG0 Z3.5 \nG90 \nG1 Z2.3 \nG91 G17 G2 X0 Y0 I4.2 J0 P1 \nG90 \nG1 Z1.1 \nG91 G17 G2 X0 Y0 I4.2 J0 P1 \nG90 \nG1 Z0 \nG91 G17 G2 X0 Y0 I4.2 J0 P1 \nG4 P0.5 \nG90 \nG0 Z100 \nG91 \nG0 X4.2 Y0 \n"

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


# class Test_bore_tabbed_circle(unittest.TestCase):
#     """ arguments: (Z_safe, stock_thickness, cut_per_pass, target_depth,
#               cutter_diameter, circle_diameter)
#     """


#     def tabbed_bore_OD_equal_ID(self):
#         g_code_ID = sg.bore_tabbed_ID(100, 11.3, 3, 1.1, 2.5, 15)
#         g_code_OD = sg.bore_tabbed_OD(100, 11.3, 3, 1.1, 2.5, 10)
#         match = self.basic_match3()
#         self.assertEqual(g_code_ID, g_code_OD, "not a match")



# def bore_circle_OD_suite():
#     suite = unittest.TestSuite()
#     suite.addTest(Test_bore_circle_OD("basic_bore"))
#     suite.addTest(Test_bore_circle_OD("bore_OD_equal_ID"))
#     # suite.addTest(Test_bore_circle("basic_bore_FAIL"))
#     # suite.addTest(Test_bore_circle("max_cut_more_than_thickness"))
#     # suite.addTest(Test_bore_circle("max_cut_equal_to_thickness"))
#     # suite.addTest(Test_bore_circle("many_cuts"))
#     # suite.addTest(Test_bore_circle("all_floats"))
#     return suite


class Test_bore_tabbed_ID(unittest.TestCase):
    """ arguments: (Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, tab_width)
    """

    def tabbed_bore_OD_equal_ID(self):
        g_code_ID = sg.bore_tabbed_ID(100, 11.3, 3, 1.1, 2.5, 55, 6.35)
        g_code_OD = sg.bore_tabbed_OD(100, 11.3, 3, 1.1, 2.5, 50, 6.35)
        self.assertEqual(g_code_ID, g_code_OD, "not a match")


def bore_tabbed_ID_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_bore_tabbed_ID("tabbed_bore_OD_equal_ID"))
    # suite.addTest(Test_bore_circle("basic_bore_FAIL"))
    # suite.addTest(Test_bore_circle("max_cut_more_than_thickness"))
    # suite.addTest(Test_bore_circle("max_cut_equal_to_thickness"))
    # suite.addTest(Test_bore_circle("many_cuts"))
    # suite.addTest(Test_bore_circle("all_floats"))
    return suite