import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from Doughnut_Cutter_class import DoughnutCutter
from Setup_class import Setup

setup = Setup()

Doughnut_Cutter = DoughnutCutter(None,  setup)

class Test_doughnut_cutter_wizard(unittest.TestCase):


    def doughnut_match1(self):
        """ This example from successful work for the Contender. 
        Inspection port hole backing plate. """
        return "F500.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X-57.4125 Y0.0 \nG90 \nG0 Z4.5 \nG90 \nG1 Z1.5 \nG91 G17 G2 X0.0 Y0.0 I57.4125 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z80.0 \nG91 \nG0 X57.4125 Y0.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X-56.62419 Y9.48137 \nG90 \nG1 Z0.0 \nG91 G17 G2 X85.33044 Y40.23932 I56.62419 J-9.48137 P1 \nG0 Z1.5 \nG91 G17 G2 X7.81695 Y-5.42338 I-28.70625 J-49.72068 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y-88.59461 I-36.5232 J-44.2973 P1 \nG0 Z1.5 \nG91 G17 G2 X-7.81695 Y-5.42338 I-36.5232 J44.2973 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X-86.11875 Y49.72068 I-28.70625 J49.72068 P1 \nG90 \nG0 Z80.0 \nG91 \nG0 X57.4125 Y0.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X-76.5875 Y0.0 \nG90 \nG0 Z4.5 \nG90 \nG1 Z1.5 \nG91 G17 G2 X0.0 Y0.0 I76.5875 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z80.0 \nG91 \nG0 X76.5875 Y0.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X-75.99596 Y9.50046 \nG90 \nG1 Z0.0 \nG91 G17 G2 X114.28971 Y56.82626 I75.99596 J-9.50046 P1 \nG0 Z1.5 \nG91 G17 G2 X7.93188 Y-5.26252 I-38.29375 J-66.32672 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y-122.1284 I-46.22563 J-61.0642 P1 \nG0 Z1.5 \nG91 G17 G2 X-7.93188 Y-5.26252 I-46.22563 J61.0642 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X-114.88125 Y66.32672 I-38.29375 J66.32672 P1 \nG90 \nG0 Z80.0 \nG91 \nG0 X76.5875 Y0.0 \nG90 \nM2 \n"

    def doughnut_match2(self):
        return "F1000.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-34.375 Y0.0 \nG90 \nG0 Z7.0 \nG90 \nG1 Z4.0 \nG91 G17 G2 X0.0 Y0.0 I34.375 J0.0 P1 \nG90 \nG1 Z1.5 \nG91 G17 G2 X0.0 Y0.0 I34.375 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X34.375 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-32.05553 Y12.41305 \nG90 \nG1 Z0.0 \nG91 G17 G2 X49.24303 Y17.35658 I32.05553 J-12.41305 P1 \nG0 Z1.5 \nG91 G17 G2 X9.59028 Y-8.21525 I-17.1875 J-29.76962 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y-43.10876 I-26.77778 J-21.55438 P1 \nG0 Z1.5 \nG91 G17 G2 X-9.59028 Y-8.21525 I-26.77778 J21.55438 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X-51.5625 Y29.76962 I-17.1875 J29.76962 P1 \nG90 \nG0 Z100.0 \nG91 \nG0 X34.375 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-63.325 Y0.0 \nG90 \nG0 Z7.0 \nG90 \nG1 Z4.0 \nG91 G17 G2 X0.0 Y0.0 I63.325 J0.0 P1 \nG90 \nG1 Z1.5 \nG91 G17 G2 X0.0 Y0.0 I63.325 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X63.325 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-62.05575 Y12.61504 \nG90 \nG1 Z0.0 \nG91 G17 G2 X93.71825 Y42.22602 I62.05575 J-12.61504 P1 \nG0 Z1.5 \nG91 G17 G2 X10.29032 Y-7.40672 I-31.6625 J-54.84106 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y-94.86868 I-41.95282 J-47.43434 P1 \nG0 Z1.5 \nG91 G17 G2 X-10.29032 Y-7.40672 I-41.95282 J47.43434 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X-94.9875 Y54.84106 I-31.6625 J54.84106 P1 \nG90 \nG0 Z100.0 \nG91 \nG0 X63.325 Y0.0 \nG90 \nM2 \n"

    def test_doughnut_match1(self):
        """ This example from successful work for the Contender. 
        Inspection port hole backing plate. """

        Doughnut_Cutter.setup.feed_rate_var.set("500")
        Doughnut_Cutter.setup.Z_safe_var.set("80")
        Doughnut_Cutter.setup.cut_per_pass_var.set(3)
        Doughnut_Cutter.setup.bit_diameter_var.set(3.175)
        Doughnut_Cutter.setup.stock_thickness_var.set(4.5)

        Doughnut_Cutter.tab_thickness_var.set(1.5)
        Doughnut_Cutter.tab_width_var.set("6.35")
        Doughnut_Cutter.doughnut_OD_var.set(150)
        Doughnut_Cutter.doughnut_ID_var.set(118)

        Doughnut_Cutter.generateCode()
        g_code = Doughnut_Cutter.g_code

        self.assertEquals(self.doughnut_match1(), g_code)


    def test_doughnut_match2(self):
        """ This example is actually unknown. """

        Doughnut_Cutter.setup.feed_rate_var.set("1000")
        Doughnut_Cutter.setup.Z_safe_var.set("100")
        Doughnut_Cutter.setup.cut_per_pass_var.set(3)
        Doughnut_Cutter.setup.bit_diameter_var.set(6.35)
        Doughnut_Cutter.setup.stock_thickness_var.set(7)

        Doughnut_Cutter.tab_thickness_var.set(1.5)
        Doughnut_Cutter.tab_width_var.set("6.35")
        Doughnut_Cutter.doughnut_OD_var.set(120.3)
        Doughnut_Cutter.doughnut_ID_var.set(75.1)

        Doughnut_Cutter.generateCode()
        g_code = Doughnut_Cutter.g_code

        self.assertEquals(self.doughnut_match2(), g_code)



def doughnuts_wizard_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_doughnut_cutter_wizard("test_doughnut_match1"))
    suite.addTest(Test_doughnut_cutter_wizard("test_doughnut_match2"))
    return suite
