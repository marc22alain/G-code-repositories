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
            if len(self.scenarios[feature].keys()) == 0:
                self.announceNoScenarioExist(feature)
            else:
                self.announceScenarioSet(feature)
                for scenario_key in self.scenarios[feature]:
                    scenario = self.scenarios[feature][scenario_key]
                    self.runScenario(feature, scenario)

    def runScenario(self, feature, scenario, output_program=False):
        feature_manager = self.configureAll(feature, scenario)
        self.announceScenarioTest(scenario['description'])
        self._runTests(feature_manager, output_program)

    def configureAll(self, feature, scenario):
        fm = FeatureManager()
        feat = feature(fm)
        fm.features.append(feat)
        self.configure(fm.machine, scenario['machine_config'])
        self.configure(fm.work_piece, scenario['work_piece_config'])
        self.configure(feat, scenario['config'])
        if hasattr(feat, 'is_composed'):
            feat.updateFeatures()
            for child_key in feat.child_features.keys():
                self.configure(feat.child_features[child_key], scenario['child_features'][child_key])
        return fm

    def configure(self, thing, config):
        queries = thing.getOptionQueries()
        # print queries
        for item in config.keys():
            queries[item].setValue(config[item])

    def _runTests(self, feature_manager, output_program):
        program = feature_manager.getGCode()
        testWithProgram(program)
        if output_program:
            print program


    def announceScenarioSet(self, feature):
        print
        print '* * * * * *'
        print '* * * * * *   starting %s scenarios   * * * * * *' % (feature.name)
        print '* * * * * *'

    def announceScenarioTest(self, description):
        print
        print '- - - >  %s' % (description)

    def announceNoScenarioExist(self, feature):
        print
        print '  !  !  !   no scenarios defined for %s   !  !  !' % (feature.name)

