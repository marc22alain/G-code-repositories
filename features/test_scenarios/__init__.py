from LinearGroove_scenarios import lg_scenarios
from CircularGroove_scenarios import cg_scenarios
from ODCircularGroove_scenarios import odcg_scenarios
from LinearDistribution_scenarios import ldist_scenarios
from Peck_scenarios import peck_scenarios
from CircularPocket_scenarios import circ_pock_scenarios
from RectangularGroove_scenarios import rect_scenarios
from ODRectangularGroove_scenarios import odrect_scenarios
from RectangularPocket_scenarios import rect_pocket_scenarios
from features import *

scenarios = {
    LinearGroove: lg_scenarios,
    CircularGroove: cg_scenarios,
    ODCircularGroove: odcg_scenarios,
    LinearDistribution: ldist_scenarios,
    Peck: peck_scenarios,
    CircularPocket: circ_pock_scenarios,
    RectangularGroove: rect_scenarios,
    ODRectangularGroove: odrect_scenarios,
    RectangularPocket: rect_pocket_scenarios,
}
