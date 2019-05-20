from machines import SimpleMachine
from workpieces import SimpleWorkpiece
from ui import OptionQueryDialog
from utilities import Glib as G
from features import *


class FeatureManager(object):
    def __init__(self, app=None, view_space=None):
        self.machine = SimpleMachine()
        self.work_piece = SimpleWorkpiece()
        self.features = []
        self.app = app
        self.view_space = view_space

    def addFeature(self, feature_class):
        feature = feature_class(self)
        print feature
        self.features.append(feature)
        def addFunction():
            print 'running OK function'
            if hasattr(feature, 'is_composed'):
                feature.updateFeatures()
            # would like a better binding with self.features
            self.app.feature_list.insertFeature(feature)
            self.view_space.drawGeometry(feature.getDrawnGeometry())
        def cancelFunction():
            self.features.pop()
            print 'running CANCEL function'
        OptionQueryDialog(self.app, feature.getOptionQueries(), feature.name, addFunction, cancelFunction)

    def deleteFeature(self, feature):
        self.app.feature_list.removeFeature(feature)
        self.features.remove(feature)

    def getGCode(self):
        # wrapping the features' gcode:
        self.g_code = self.machine.setUpProgram()
        for feature in self.features:
            self.g_code += feature.getGCode()
        self.g_code += self.machine.endProgram()
        return self.g_code
