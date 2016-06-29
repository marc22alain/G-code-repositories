import unittest
import test_simple_generators as tsg

import test_hole_borer_wizard as thbw
import test_polar_holes_wizard as tphw
import test_doughnut_cutter_wizard as tdcw


# SIMPLE GENERATORS
unittest.TextTestRunner().run(tsg.suiteAdd())

# TODO:
# unittest.TextTestRunner().run(tsg.bore_circle_OD_suite())

unittest.TextTestRunner().run(tsg.bore_tabbed_circle_suite())

unittest.TextTestRunner().run(tsg.polar_holes_suite())


unittest.TextTestRunner().run(tsg.rect_area_suite())



# WIZARDS
unittest.TextTestRunner().run(thbw.hole_borer_wizard_suite())

unittest.TextTestRunner().run(tphw.polar_holes_wizard_suite())

unittest.TextTestRunner().run(tdcw.doughnuts_wizard_suite())
