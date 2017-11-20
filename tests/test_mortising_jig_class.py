import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from MortisingJig_class import MortisingJig

def fakeFeature1(position, also=False):
    if also:
        return 'bite me'
    return position

class Test_MortisingJig_class(unittest.TestCase):

    def test_test_case(self):
        jig = MortisingJig('test', fakeFeature1, fakeFeature1)
        iterator = jig.getFeaturesOffsets()
        offsets1, feature1 = iterator.next()
        self.assertEquals(False, feature1())
        offsets2, feature2 = iterator.next()
        self.assertEquals(True, feature2())
        offsets3, feature3 = iterator.next()
        self.assertEquals('bite me', feature3(True))
        offsets4, feature4 = iterator.next()
        self.assertEquals(True, feature4())
        self.assertRaises(StopIteration, iterator.next)

    def test_false_features(self):
        jig = MortisingJig('test', False, fakeFeature1)
        iterator = jig.getFeaturesOffsets()
        iterator.next()
        iterator.next()
        self.assertRaises(StopIteration, iterator.next)
        newjig = MortisingJig('test', fakeFeature1, False)
        iterator = newjig.getFeaturesOffsets()
        iterator.next()
        iterator.next()
        self.assertRaises(StopIteration, iterator.next)


def mortising_jig_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_MortisingJig_class("test_test_case"))
    suite.addTest(Test_MortisingJig_class("test_false_features"))
    return suite



unittest.TextTestRunner().run(mortising_jig_suite())
