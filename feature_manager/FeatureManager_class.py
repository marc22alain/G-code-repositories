from machines import SimpleMachine
from workpieces import SimpleWorkpiece
from ui import OptionQueryDialog
from utilities import Glib as G


class FeatureManager(object):
    def __init__(self, app):
        self.machine = SimpleMachine()
        self.work_piece = SimpleWorkpiece()
        self.features = []
        self.app = app

    def addFeature(self, feature_class):
        feature = feature_class(self)
        print feature
        self.features.append(feature)
        def addFunction():
            # would like a better binding with self.features
            self.app.feature_list.insertFeature(feature)
            print 'running OK function'
        def cancelFunction():
            self.features.pop()
            print 'running CANCEL function'
        OptionQueryDialog(self.app, feature.getOptionQueries(), feature.name, addFunction, cancelFunction)

    def deleteFeature(self, feature):
        self.app.feature_list.removeFeature(feature)
        self.features.remove(feature)

    def getGCode(self):
        # wrapping the features' gcode:
        feed_rate = self.machine.getParams()['feed_rate']
        self.g_code = G.F_rate(feed_rate)
        self.g_code += self.features[0].getGCode()
        self.g_code += G.set_ABS_mode() + G.end_program()
        return self.g_code
