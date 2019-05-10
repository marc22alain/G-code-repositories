from features import test_scenarios
from machines import SimpleMachine
from workpieces import SimpleWorkpiece
from tests import testWithProgram
from feature_manager import FeatureManager

class ScenarioRunner(object):
    def __init__(self):
        self.scenarios = test_scenarios.scenarios

    def runAllScenarios(self):
        for feature in self.scenarios.keys():
            self.announceScenarioSet(feature)
            for scenario_key in self.scenarios[feature]:
                scenario = self.scenarios[feature][scenario_key]
                self.runScenario(feature, scenario)
                # for scenarios in scenario_set.values():
                    # print scenario['description']

    def runScenario(self, feature, scenario):
        feature_manager = self.configureAll(feature, scenario)
        self.announceScenarioTest(scenario['description'])
        self.runTests(feature_manager)

    def configureAll(self, feature, scenario):
        fm = FeatureManager()
        feat = feature(fm)
        fm.features.append(feat)
        self.configure(fm.machine, scenario['machine_config'])
        self.configure(fm.work_piece, scenario['work_piece_config'])
        self.configure(feat, scenario['config'])
        return fm

    def configure(self, thing, config):
        queries = thing.getOptionQueries()
        # print queries
        for item in config.keys():
            queries[item].setValue(config[item])

    def runTests(self, feature_manager):
        program = feature_manager.getGCode()
        testWithProgram(program)


    def announceScenarioSet(self, feature):
        print
        print '* * * * * *'
        print '* * * * * *   starting %s scenarios   * * * * * *' % (feature.name)
        print '* * * * * *'
        print

    def announceScenarioTest(self, description):
        print '- - - >  %s' % (description)
