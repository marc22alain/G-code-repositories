from Tkinter import *
import unittest

def testWithQuery(query):

    class TestQueryInterfaces(unittest.TestCase):

        @classmethod
        def setUpClass(TestFeatureInterfaces):
            print '- %s --->' % (query.__class__.__name__)

        def test_query_sets_entry_value(self):
            print 'EntryQuery'

        def test_query_sets_spinbox_value(self):
            print 'SpinBoxQuery'

        def test_query_returns_query_value(self):
            result = query.getValue()
            # print result
            self.assertGreater(len(result),0, 'No option queries were returned.')


    suite = unittest.TestSuite()
    suite.addTest(TestQueryInterfaces("test_query_returns_query_value"))

    if query.__class__.__base__.__name__ == 'EntryQuery':
        suite.addTest(TestQueryInterfaces("test_query_sets_entry_value"))
    else:
        suite.addTest(TestQueryInterfaces("test_query_sets_spinbox_value"))

    unittest.TextTestRunner().run(suite)
