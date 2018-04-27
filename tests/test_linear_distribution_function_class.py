import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from LinearDistributionFunction_class import LinearDistributionFunction


class Test_feature_distributor_class(unittest.TestCase):
    """
    LinearDistributionFunction(self, x_delta, y_delta)
    """

    def test_basic_distribution(self):
        distributing_function = LinearDistributionFunction(2.3, -1.8)
        self.assertEquals(distributing_function.generateCode(), 'G91 \nG0 X2.3 Y-1.8 \n')



def feature_distributor_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_feature_distributor_class("test_basic_distribution"))
    return suite


unittest.TextTestRunner().run(feature_distributor_suite())
