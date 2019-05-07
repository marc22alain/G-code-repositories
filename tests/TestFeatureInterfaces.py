from Tkinter import *
import unittest

def testWithFeature(feature):

    class TestFeatureInterfaces(unittest.TestCase):

        @classmethod
        def setUpClass(TestFeatureInterfaces):
            print '%s --->' % (feature.__class__.__name__)

        def test_feature_returns_query_options(self):
            result = feature.getOptionQueries()
            self.assertGreater(len(result),0, 'No option queries were returned.')


    suite = unittest.TestSuite()
    suite.addTest(TestFeatureInterfaces("test_feature_returns_query_options"))

    unittest.TextTestRunner().run(suite)
