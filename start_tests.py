from Tkinter import *
from tests import *
import features
import option_queries
from utilities import parseModuleClasses
# from feature_manager import FeatureManager

Tk()

class MockFeatureManager(object):
    machine = None
    work_piece = None

# -----------------------------------------------------------------------------
# ----------------------------- GeometricFeature ------------------------------
# -----------------------------------------------------------------------------

def feature_suite():
    fm = MockFeatureManager()
    feature_classes = parseModuleClasses(features, ['GeometricFeature', 'ComposedFeature', 'DistributedFeature'])
    num_feature_class_tests = 0
    for feature in feature_classes.values():
        testWithFeature(feature(fm))
        num_feature_class_tests += 1
    assert num_feature_class_tests == len(feature_classes), 'Must run one test for each query_class'

feature_suite()

# -----------------------------------------------------------------------------
# ---------------------------------- Query ------------------------------------
# -----------------------------------------------------------------------------

def query_suite():
    query_classes = parseModuleClasses(option_queries, ['EntryQuery', 'SpinboxQuery'])
    num_query_class_tests = 0
    for query in query_classes.values():
        testWithQuery(query())
        num_query_class_tests += 1
    assert num_query_class_tests == len(query_classes), 'Must run one test for each query_class'

# query_suite()
