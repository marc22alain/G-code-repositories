import unittest
import test_simple_generators as tsg


unittest.TextTestRunner().run(tsg.suiteAdd())

# TODO:
# unittest.TextTestRunner().run(tsg.bore_circle_OD_suite())

unittest.TextTestRunner().run(tsg.bore_tabbed_circle_suite())

unittest.TextTestRunner().run(tsg.polar_holes_suite())
