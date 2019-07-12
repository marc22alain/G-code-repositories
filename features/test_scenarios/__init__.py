from LinearGroove_scenarios import lg_scenarios
from CircularGroove_scenarios import cg_scenarios
from LinearDistribution_scenarios import ldist_scenarios
from Peck_scenarios import peck_scenarios
from CircularPocket_scenarios import circ_pock_scenarios
from RectangularGroove_scenarios import rect_scenarios
from RectangularPocket_scenarios import rect_pocket_scenarios
from Tenon_scenarios import tenon_scenarios
from RadiusedRectangularGroove_scenarios import rad_rect_scenarios
from features import *

scenarios = {
    LinearGroove: lg_scenarios,
    CircularGroove: cg_scenarios,
    LinearDistribution: ldist_scenarios,
    Peck: peck_scenarios,
    CircularPocket: circ_pock_scenarios,
    RectangularGroove: rect_scenarios,
    RectangularPocket: rect_pocket_scenarios,
    Tenon: tenon_scenarios,
    RadiusedRectangularGroove: rad_rect_scenarios,
}
