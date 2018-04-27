from DistributionFunction_class import DistributionFunction
import Glib as G


class LinearDistributionFunction(DistributionFunction):
    def __init__(self, x_delta, y_delta):
        self.x_delta = x_delta
        self.y_delta = y_delta
        # self.z_delta = z_delta

    def generateCode(self):
        g_code = G.set_INCR_mode()
        g_code += G.G0_XY((self.x_delta, self.y_delta))
        return g_code
