from features import classes_dict
from tests import ScenarioRunner

# scenario = ScenarioRunner.test_scenarios.cg_scenarios['cg_config_1']
# feature = classes_dict['CircularGroove']

# scenario = ScenarioRunner.test_scenarios.odcg_scenarios['odcg_config_2']
# feature = classes_dict['ODCircularGroove']

# scenario = ScenarioRunner.test_scenarios.ldist_scenarios['ldist_config_2']
# feature = classes_dict['LinearDistribution']


# scenario = ScenarioRunner.test_scenarios.peck_scenarios['peck_config_1']
# feature = classes_dict['Peck']


# scenario = ScenarioRunner.test_scenarios.circ_pock_scenarios['circ_pock_config_2']
# feature = classes_dict['CircularPocket']

# scenario = ScenarioRunner.test_scenarios.odrect_scenarios['odrect_config_2']
# feature = classes_dict['ODRectangularGroove']

# scenario = ScenarioRunner.test_scenarios.rect_pocket_scenarios['rect_pocket_config_2']
# feature = classes_dict['RectangularPocket']

# scenario = ScenarioRunner.test_scenarios.lg_scenarios['lg_config_1']
# feature = classes_dict['LinearGroove']

# ScenarioRunner.ScenarioRunner().runScenario(feature, scenario, True)

# # # BUG FIXES
# # # BUG FIXES
# # # BUG FIXES
# scenario = ScenarioRunner.test_scenarios.ldist_scenarios['ldist_bug_fix_1']
# feature = classes_dict['LinearDistribution']

scenario = ScenarioRunner.test_scenarios.ldist_scenarios['ldist_bug_fix_2']
feature = classes_dict['LinearDistribution']

# ScenarioRunner.ScenarioRunner().runScenario(feature, scenario, False)

# scenario = ScenarioRunner.test_scenarios.peck_scenarios['peck_bug_fix_1']
# feature = classes_dict['Peck']

ScenarioRunner.ScenarioRunner().runScenario(feature, scenario, False)
