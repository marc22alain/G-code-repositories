from LinearGroove_scenarios import lg_scenarios
from CircularGroove_scenarios import cg_scenarios
from ODCircularGroove_scenarios import odcg_scenarios
from LinearDistribution_scenarios import ldist_scenarios
from features import *

scenarios = {
    LinearGroove: lg_scenarios,
    CircularGroove: cg_scenarios,
    ODCircularGroove: odcg_scenarios,
    LinearDistribution: ldist_scenarios
}
