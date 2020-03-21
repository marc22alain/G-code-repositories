from feature_manager import FeatureManager
from joints import FingerJoint
from MockCanvas_class import MockCanvas
from MockViewSpace_class import MockViewSpace
from option_queries import *
from Tkinter import *
import unittest

Tk()

vs = MockViewSpace(MockCanvas())
fm = FeatureManager(vs)
designer = FingerJoint(fm)
designer.getOptionQueries()

class TestFingerJointDesigner(unittest.TestCase):
    def test_groove_distributions(self):
        """ Challenges getNumGrooves() method on its contract. """
        designer.option_queries[StockWidthQuery].setValue(50.0)
        designer.machine.option_queries[BitDiameterQuery].setValue(5.0)
        result = designer.getNumGrooves()
        self.assertEqual(result['num_a_grooves'], 5)
        self.assertEqual(result['num_b_grooves'], 4)
        self.assertEqual(result['tab_width'], 2.5)

        designer.option_queries[StockWidthQuery].setValue(50.1)
        result = designer.getNumGrooves()
        self.assertEqual(result['num_a_grooves'], 5)
        self.assertEqual(result['num_b_grooves'], 4)
        self.assertEqual(result['tab_width'], 2.55)

        designer.option_queries[StockWidthQuery].setValue(50.1)
        result = designer.getNumGrooves()
        self.assertEqual(result['num_a_grooves'], 5)
        self.assertEqual(result['num_b_grooves'], 4)
        self.assertEqual(result['tab_width'], 2.55)

        designer.option_queries[StockWidthQuery].setValue(54.9)
        result = designer.getNumGrooves()
        self.assertEqual(result['num_a_grooves'], 5)
        self.assertEqual(result['num_b_grooves'], 4)
        self.assertEqual(result['tab_width'], 4.95)

        designer.option_queries[StockWidthQuery].setValue(55.1)
        result = designer.getNumGrooves()
        self.assertEqual(result['num_a_grooves'], 5)
        self.assertEqual(result['num_b_grooves'], 4)
        self.assertEqual(result['tab_width'], 5.05)

        designer.option_queries[StockWidthQuery].setValue(59.9)
        result = designer.getNumGrooves()
        self.assertEqual(result['num_a_grooves'], 5)
        self.assertEqual(result['num_b_grooves'], 4)
        self.assertEqual(result['tab_width'], 7.45)

        designer.option_queries[StockWidthQuery].setValue(60.1)
        result = designer.getNumGrooves()
        self.assertEqual(result['num_a_grooves'], 6)
        self.assertEqual(result['num_b_grooves'], 5)
        self.assertEqual(result['tab_width'], 2.55)


suite = unittest.TestSuite()
suite.addTest(TestFingerJointDesigner("test_groove_distributions"))

unittest.TextTestRunner().run(suite)
