import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from Dado_class import Dado


class Test_dado_class(unittest.TestCase):
    """
    Dado(safe_Z, stock_height, cut_depth, max_cut_per_pass, x_delta, y_delta)
    """

    def test_basic_groove(self):
        dado = Dado(80, 20, 3, 3, 1, 0)
        self.assertEquals(dado.generateCode(), 'G90 \nG0 Z20.0 \nG1 Z17.0 \nG91 \nG1 X1.0 Y0.0 \nG90 \nG0 Z80.0 \n')
        # The cut should be reversed now.
        self.assertEquals(dado.generateCode(), 'G90 \nG0 Z20.0 \nG1 Z17.0 \nG91 \nG1 X-1.0 Y0.0 \nG90 \nG0 Z80.0 \n')



def dado_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_dado_class("test_basic_groove"))
    return suite


unittest.TextTestRunner().run(dado_suite())
