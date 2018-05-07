from FeatureDistributor_class import FeatureDistributor
from LinearDistributionFunction_class import LinearDistributionFunction
from Dado_class import Dado
import Glib as G

# Dado(safe_Z, stock_height, cut_depth, max_cut_per_pass, x_delta, y_delta)
groove = Dado(100, 95, 5, 5, 52, 0)

# LinearDistributionFunction(x_delta, y_delta))
groove_set = LinearDistributionFunction(0, 12.7)

# feature, distribution function, number of cuts
feat_distributor = FeatureDistributor(groove, groove_set, 27)


g_code = G.F_rate(500)
g_code += G.set_ABS_mode()
g_code += G.G0_Z(100)
g_code += feat_distributor.generateCode()
g_code += G.end_program()

print g_code
