from Feature_class import Feature
import Glib as G


"""
This dado has no width.
"""

class Dado(Feature):
    def __init__(self, safe_Z, stock_height, cut_depth, max_cut_per_pass, x_delta, y_delta):
        self.safe_Z = safe_Z
        self.stock_height = stock_height
        self.cut_depth = cut_depth
        self.max_cut_per_pass = max_cut_per_pass
        self.x_delta = x_delta
        self.y_delta = y_delta
        self.reversed = False

    def generateCode(self):
        if not self.reversed:
            return self._genPrimaryPath()
        else:
            return self._genReversedPath()

    def _genPrimaryPath(self):
        # Assuming start at safe_Z and in (X,Y) position to start cutting.
        g_code = G.set_ABS_mode()
        g_code += G.G0_Z(self.stock_height)
        # TODO: elaborate for max_cut_per_pass
        g_code += G.G1_Z(self.stock_height - self.cut_depth)
        g_code += G.set_INCR_mode()
        g_code += G.G1_XY((self.x_delta, self.y_delta))
        self.reversed = not self.reversed
        g_code += G.set_ABS_mode()
        g_code += G.G0_Z(self.safe_Z)
        return g_code

    def _genReversedPath(self):
        # Assuming start at safe_Z and in (X,Y) position to start cutting.
        g_code = G.set_ABS_mode()
        g_code += G.G0_Z(self.stock_height)
        # TODO: elaborate for max_cut_per_pass
        g_code += G.G1_Z(self.stock_height - self.cut_depth)
        g_code += G.set_INCR_mode()
        g_code += G.G1_XY((- self.x_delta, - self.y_delta))
        self.reversed = not self.reversed
        g_code += G.set_ABS_mode()
        g_code += G.G0_Z(self.safe_Z)
        return g_code
