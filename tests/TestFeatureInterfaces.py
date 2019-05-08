from Tkinter import *
import unittest
from option_queries import *
from features import *

def testWithFeature(feature):
    class_name = feature.__class__.__name__

    class TestFeatureInterfaces(unittest.TestCase):

        @classmethod
        def setUpClass(TestFeatureInterfaces):
            print '%s --->' % (feature.__class__.__name__)

        def test_feature_returns_query_options(self):
            result = feature.getOptionQueries()
            self.assertGreater(len(result),0, 'No option queries were returned.')

        def test_composable_feature_updates_child(self):
            self.assertTrue(hasattr(feature, 'updateFeatures'), '%s does not support `updateFeatures`' % (class_name))
            feature.option_queries[GeometricFeatureQuery].setValue('LinearGroove')
            original_children = feature.child_features.copy()
            self.assertEqual(original_children, feature.child_features)
            feature.updateFeatures()
            self.assertNotEqual(original_children, feature.child_features)

        def test_composable_feature_deletes_features(self):
            self.assertTrue(hasattr(feature, 'deleteFeature'), '%s does not support `deleteFeature`' % (class_name))
            feature.option_queries[GeometricFeatureQuery].setValue('LinearGroove')
            feature.updateFeatures()
            original_children = feature.child_features.copy()
            feature.deleteFeature(original_children[LinearGroove])
            self.assertNotEqual(original_children, feature.child_features)

    suite = unittest.TestSuite()
    suite.addTest(TestFeatureInterfaces("test_feature_returns_query_options"))

    if hasattr(feature, 'is_composed'):
        suite.addTest(TestFeatureInterfaces("test_composable_feature_updates_child"))
        suite.addTest(TestFeatureInterfaces("test_composable_feature_deletes_features"))


    unittest.TextTestRunner().run(suite)
