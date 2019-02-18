'''
1 5/16 between holes across the hinge
12mm gap between pieces

difference halved

10.66875

bit:
3.175 diameter
1.5875 radius

10.66875 + 1.5875 = 12.25625

hinge is 2" wide
holes are 1 3/8 apart 34.925mm
holes are 5/16" from edge

60mm
7.9375mm (5/16")
67.9375 + 1.5875 = 69.525
320.8
50.8 (2")
270

G0 X69.53 Y12.26
'''

from FeatureDistributor_class import FeatureDistributor
from LinearDistributionFunction_class import LinearDistributionFunction
from HoleFeature_class import HoleFeature
import Glib as G

# HoleFeature(safe_Z, stock_height, cut_depth, max_cut_per_pass, bit_diameter, circle_diameter)
hole = HoleFeature(80, 17.5, 5, 3, 3.175, 3.175)

# LinearDistributionFunction(x_delta, y_delta))
hinge_hole_set = LinearDistributionFunction(34.925, 0)
hinge_pair = LinearDistributionFunction(270 - 24.925, 0)

# feature, distribution function, number of cuts
feat_distributor_hinge = FeatureDistributor(hole, hinge_hole_set, 2)
feat_distributor_hinge_pair = FeatureDistributor(feat_distributor_hinge, hinge_pair, 2)


g_code = G.F_rate(500)
g_code += G.set_ABS_mode()
g_code += G.G0_Z(80)
g_code += G.set_INCR_mode()
g_code += G.G0_XY((69.525, 12.25625))
g_code += feat_distributor_hinge_pair.generateCode()
g_code += G.end_program()

print g_code
