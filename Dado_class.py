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
        # Assuming start at safe_Z and in (X,Y) position to start cutting.
        g_code = G.set_ABS_mode()
        g_code += G.G0_Z(self.stock_height)
        g_code += self._depthOfCut()
        g_code += G.set_ABS_mode()
        g_code += G.G0_Z(self.safe_Z)
        return g_code

    def _depthOfCut(self):
        g_code = ''
        height = self.stock_height
        end_height = self.stock_height - self.cut_depth
        while height > end_height:
            height -= self.max_cut_per_pass
            if height < end_height:
                height = end_height
            g_code += G.set_ABS_mode()
            g_code += G.G1_Z(height)
            g_code += self._genPath()
        return g_code

    def _genPath(self):
        g_code = G.set_INCR_mode()
        if not self.reversed:
            # The primary path
            g_code += G.G1_XY((self.x_delta, self.y_delta))
        else:
            # The reversed path
            g_code += G.G1_XY((- self.x_delta, - self.y_delta))
        self.reversed = not self.reversed
        return g_code