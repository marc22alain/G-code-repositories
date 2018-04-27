import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from FeatureDistributor_class import FeatureDistributor

class Mock(object):
    def __init__(self, mock_code):
        self.mock_code = mock_code

    def generateCode(self):
        return self.mock_code

feature = Mock('feature; ')
dist_funct = Mock('dist_funct; ')

class Test_feature_distributor_class(unittest.TestCase):
    """
    FeatureDistributor(self, feature, distribution_function, num_steps)
    """

    def test_basic_distribution(self):
        feature_distributor = FeatureDistributor(feature, dist_funct, 4)
        self.assertEquals(feature_distributor.generateCode(), 'feature; dist_funct; feature; dist_funct; feature; dist_funct; feature; ')



def feature_distributor_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_feature_distributor_class("test_basic_distribution"))
    return suite


unittest.TextTestRunner().run(feature_distributor_suite())
