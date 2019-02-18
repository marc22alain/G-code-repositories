from Feature_class import Feature
import Glib as G
import simple_generators as G


"""
A hole.
"""

class HoleFeature(Feature):
    def __init__(self, safe_Z, stock_height, cut_depth, max_cut_per_pass, bit_diameter, circle_diameter):
        self.safe_Z = safe_Z
        self.stock_height = stock_height
        self.cut_depth = cut_depth
        self.max_cut_per_pass = max_cut_per_pass
        self.bit_diameter = bit_diameter
        self.circle_diameter = circle_diameter

    def generateCode(self):
        target_depth = self.stock_height - self.cut_depth
        return G.bore_circle_ID(self.safe_Z, self.stock_height, self.max_cut_per_pass, target_depth,
              self.bit_diameter, self.circle_diameter)
