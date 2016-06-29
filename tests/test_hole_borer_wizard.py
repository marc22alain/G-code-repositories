import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from Hole_Borer_class import HoleBorer


HB = HoleBorer()

class Test_hole_borer_wizard(unittest.TestCase):


	def hole_match1(self):
		return "F1000.0 \nG90 \nG0 Z100.0 \nG91 \nG0 X-4.325 Y0.0 \nG90 \nG0 Z10.0 \nG90 \nG1 Z7.0 \nG91 G17 G2 X0.0 Y0.0 I4.325 J0.0 P1 \nG90 \nG1 Z4.0 \nG91 G17 G2 X0.0 Y0.0 I4.325 J0.0 P1 \nG90 \nG1 Z1.0 \nG91 G17 G2 X0.0 Y0.0 I4.325 J0.0 P1 \nG90 \nG1 Z0.0 \nG91 G17 G2 X0.0 Y0.0 I4.325 J0.0 P1 \nG4 P0.5 \nG90 \nG0 Z100.0 \nG91 \nG0 X4.325 Y0.0 \nG90 \nM2 \n"


	def hole_match2(self):
		return "F1000.0 \nG90 \nG0 Z12.0 \nG1 Z0.0 \nG4 P0.5 \nG0 Z100.0 \nG90 \nM2 \n"

	def test_hole_match1(self):
		HB.feed_rate_var.set("1000")
		HB.Z_safe_var.set("100")
		HB.cut_depth_var.set(3)
		HB.bit_diameter_var.set(6.35)
		HB.stock_thickness_var.set(10)

		HB.hole_diameter_var.set(15)
		HB.generateCode()
		g_code = HB.g_code

		self.assertEquals(self.hole_match1(), g_code)


	def test_hole_match2(self):
		HB.feed_rate_var.set("1000")
		HB.Z_safe_var.set("100")
		HB.cut_depth_var.set(4)
		HB.bit_diameter_var.set(3.175)
		HB.stock_thickness_var.set(12)

		HB.hole_diameter_var.set(3.175)
		HB.generateCode()
		g_code = HB.g_code

		self.assertEquals(self.hole_match2(), g_code)


def hole_borer_wizard_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_hole_borer_wizard("test_hole_match1"))
    suite.addTest(Test_hole_borer_wizard("test_hole_match2"))
    return suite
