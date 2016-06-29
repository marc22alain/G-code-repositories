import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from Polar_Holes_class import PolarHolesBorer
from Setup_class import Setup

setup = Setup()

Polar_Holes = PolarHolesBorer(None,  setup)

class Test_polar_holes_wizard(unittest.TestCase):

    def polar_match1(self):
        """ This is a hypothetical example. """
        return "F1000.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X37.5 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-0.825 Y0.0 \nG90 \nG0 Z11.0 \nG90 \nG1 Z8.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z5.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z2.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X0.825 Y0.0 \nG91 \nG0 X-25.91186 Y35.66462 \nG90 \nG0 Z100.0 \nG91 \nG0 X-0.825 Y0.0 \nG90 \nG0 Z11.0 \nG90 \nG1 Z8.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z5.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z2.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X0.825 Y0.0 \nG91 \nG0 X-41.92627 Y-13.62267 \nG90 \nG0 Z100.0 \nG91 \nG0 X-0.825 Y0.0 \nG90 \nG0 Z11.0 \nG90 \nG1 Z8.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z5.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z2.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X0.825 Y0.0 \nG91 \nG0 X-0.0 Y-44.08389 \nG90 \nG0 Z100.0 \nG91 \nG0 X-0.825 Y0.0 \nG90 \nG0 Z11.0 \nG90 \nG1 Z8.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z5.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z2.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X0.825 Y0.0 \nG91 \nG0 X41.92627 Y-13.62267 \nG90 \nG0 Z100.0 \nG91 \nG0 X-0.825 Y0.0 \nG90 \nG0 Z11.0 \nG90 \nG1 Z8.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z5.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z2.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I0.825 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X0.825 Y0.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-11.58814 Y35.66462 \nG90 \nM2 \n"


    def polar_match2(self):
        """ This example from successful work for the Contender. 
        Inspection port hole backing plate. """
        return "F500.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X65.75 Y0.0 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z80.0 \nG91 \nG0 X-32.875 Y56.94117 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z80.0 \nG91 \nG0 X-65.75 Y0.0 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z80.0 \nG91 \nG0 X-32.875 Y-56.94117 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z80.0 \nG91 \nG0 X32.875 Y-56.94117 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z80.0 \nG91 \nG0 X65.75 Y-0.0 \nG90 \nG0 Z4.5 \nG1 Z0.0 \nG4 P0.5 \nG0 Z80.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X-32.875 Y56.94117 \nG90 \nM2 \n"

    def test_polar_match1(self):
        Polar_Holes.setup.feed_rate_var.set("1000")
        Polar_Holes.setup.Z_safe_var.set("100")
        Polar_Holes.setup.stock_thickness_var.set(11)
        Polar_Holes.setup.cut_per_pass_var.set(3)
        Polar_Holes.setup.bit_diameter_var.set(6.35)

        Polar_Holes.hole_diameter_var.set(8)
        Polar_Holes.num_holes_var.set(5)
        Polar_Holes.HCD_var.set(75)
        Polar_Holes.generateCode()
        g_code = Polar_Holes.g_code
        self.assertEquals(self.polar_match1(), g_code)

    def test_polar_match2(self):
        """ This example from successful work for the Contender. 
        Inspection port hole backing plate. """
        Polar_Holes.setup.feed_rate_var.set("500")
        Polar_Holes.setup.Z_safe_var.set("80")
        Polar_Holes.setup.stock_thickness_var.set(4.5)
        Polar_Holes.setup.cut_per_pass_var.set(3)
        Polar_Holes.setup.bit_diameter_var.set(3.175)
        
        Polar_Holes.hole_diameter_var.set(3.175)
        Polar_Holes.num_holes_var.set(6)
        Polar_Holes.HCD_var.set(131.5)
        Polar_Holes.generateCode()
        g_code = Polar_Holes.g_code
        self.assertEquals(self.polar_match2(), g_code)



def polar_holes_wizard_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_polar_holes_wizard("test_polar_match1"))
    suite.addTest(Test_polar_holes_wizard("test_polar_match2"))
    return suite
