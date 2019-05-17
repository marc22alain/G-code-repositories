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

scenario = ScenarioRunner.test_scenarios.circ_pock_scenarios['circ_pock_config_2']
feature = classes_dict['CircularPocket']

ScenarioRunner.ScenarioRunner().runScenario(feature, scenario, True)
