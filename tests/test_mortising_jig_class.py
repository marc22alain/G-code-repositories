import os
import sys
import unittest

cwd = os.getcwd()
assert cwd[-6:] == "/tests", "directory locations don't match"

sys.path.append(cwd[0:-6])
from MortisingJig_class import MortisingJig, mortisingJig

def fakeFeature1(position, also=False):
    if also:
        return 'bite me'
    return position


class Test_MortisingJig_class(unittest.TestCase):

    moveAsideTest1 = 'G90 \nG0 Z40.0 \nG0 X0.0 Y200.0 \n'
    moveToStartTest1 = 'G90 \nG0 Z80.0 \nG0 X200.0 Y0.0 \n'
    moveToStartTest2 = 'G90 \nG0 Z80.0 \nG0 X1040.0 Y270.0 \n'

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

    def test_moveAside(self):
        jig = MortisingJig('test', False, fakeFeature1)
        move = jig.moveAside()
        result1 = move(mortisingJig['minimumSafeZ'])
        self.assertEquals(result1, self.moveAsideTest1)
        def result2():
            return move(mortisingJig['minimumSafeZ'] - 1)
        self.assertRaises(ValueError, result2)


    def test__findStart(self):
        jig1 = MortisingJig('test', False, fakeFeature1)
        result1 = jig1._findStart()
        self.assertEquals(result1, (200, 0))
        jig2 = MortisingJig(270, False, fakeFeature1)
        result2 = jig2._findStart()
        self.assertEquals(result2, (1040, 270))


    def test_moveToStart(self):
        jig1 = MortisingJig('test', False, fakeFeature1)
        result1 = jig1.moveToStart()
        self.assertEquals(result1(80), self.moveToStartTest1)
        jig2 = MortisingJig(270, False, fakeFeature1)
        result2 = jig2.moveToStart()
        self.assertEquals(result2(80), self.moveToStartTest2)



def mortising_jig_suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_MortisingJig_class("test_test_case"))
    suite.addTest(Test_MortisingJig_class("test_false_features"))
    suite.addTest(Test_MortisingJig_class("test_moveAside"))
    suite.addTest(Test_MortisingJig_class("test__findStart"))
    suite.addTest(Test_MortisingJig_class("test_moveToStart"))
    return suite



unittest.TextTestRunner().run(mortising_jig_suite())
