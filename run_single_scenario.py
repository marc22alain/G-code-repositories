from features import classes_dict
from tests import ScenarioRunner

# scenario = ScenarioRunner.test_scenarios.cg_scenarios['cg_config_1']
# feature = classes_dict['CircularGroove']

scenario = ScenarioRunner.test_scenarios.ldist_scenarios['ldist_config_1']
feature = classes_dict['LinearDistribution']

ScenarioRunner.ScenarioRunner().runScenario(feature, scenario, True)
