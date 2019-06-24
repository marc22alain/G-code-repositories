from features import test_scenarios
from machines import SimpleMachine
from workpieces import SimpleWorkpiece
from tests import testWithProgram, testDrawingGeometry
from feature_manager import FeatureManager
from Tkinter import *

Tk()

class MockCanvas(object):
    def __init__(self):
        self.entities = {}
        self.id_count = 0

    def create_line(self, *params):
        return self.create_item('line')

    def create_arc(self, *args, **kwds):
        return self.create_item('arc')

    def create_oval(self, *args, **kwds):
        return self.create_item('oval')

    def create_rectangle(self, *args, **kwds):
        return self.create_item('rectangle')

    def itemconfig(self, *args, **kwds):
        pass

    def coords(self, *args, **kwds):
        pass

    def delete(self, entity_id):
        del self.entities[entity_id]

    def create_item(self, entity_type):
        self.id_count += 1
        self.entities[self.id_count] = entity_type
        return self.id_count

    def find_all(self):
        return self.entities.values()

    def move(self, *args, **kwds):
        pass


class MockViewSpace(object):
    def __init__(self, canvas = None):
        self.view_plane = 'XY'
        self.canvas = canvas
        self.x_conv = lambda x: x
        self.y_conv = lambda x: x
        self.view_scale = 1

    def setExtents(self, *args, **kwds):
        pass


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
        self._runTests(feature_manager, output_program, scenario)

    def configureAll(self, feature, scenario):
        vs = MockViewSpace(MockCanvas())
        fm = FeatureManager(vs)
        feat = feature(fm, vs)
        fm.features.append(feat)
        self.configure(fm.machine, scenario['machine_config'])
        self.configure(fm.work_piece, scenario['work_piece_config'])
        self.configure(feat, scenario['config'])
        if hasattr(feat, 'is_composed'):
            feat.addChild()
            for child in feat.features:
                self.configure(child, scenario['child_features'][child.__class__])
        return fm

    def configure(self, thing, config):
        queries = thing.getOptionQueries()
        # print queries
        for item in config.keys():
            queries[item].setValue(config[item])

    def _runTests(self, feature_manager, output_program, scenario):
        program = feature_manager.getGCode()
        testWithProgram(program, scenario)
        if output_program:
            print program
        testDrawingGeometry(feature_manager, scenario)


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

