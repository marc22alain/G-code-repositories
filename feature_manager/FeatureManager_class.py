from AbstractFeatureManager_class import AbstractFeatureManager
from machines import SimpleMachine
from workpieces import SimpleWorkpiece
from ui import OptionQueryDialog
from utilities import Glib as G
from features import *


class FeatureManager(AbstractFeatureManager):
    def __init__(self, app=None, view_space=None):
        self.machine = SimpleMachine(self)
        self.work_piece = SimpleWorkpiece(self, view_space)
        self.features = []
        self.app = app
        self.view_space = view_space

    def addChild(self, feature_class):
        feature = feature_class(self, self.view_space)
        print feature
        self.features.append(feature)
        def addFunction():
            print 'running OK function'
            if hasattr(feature, 'is_composed'):
                feature.updateFeatures()
            # would like a better binding with self.features
            feature.didUpdateQueries()
            self.app.feature_list.insertFeature(feature)
            feature.drawGeometry()
        def cancelFunction():
            self.features.pop()
            print 'running CANCEL function'
        OptionQueryDialog(self.app, feature.getOptionQueries(), feature.name, addFunction, cancelFunction)

    def deleteChild(self, feature):
        self.app.feature_list.removeFeature(feature)
        self.features.remove(feature)

    def getGCode(self):
        # wrapping the features' gcode:
        self.g_code = self.machine.setUpProgram()
        for feature in self.features:
            self.g_code += feature.getGCode()
        self.g_code += self.machine.endProgram()
        return self.g_code

    def changeViewPlane(self):
        self.work_piece.drawGeometry()
        for feature in self.features:
            feature.changeViewPlane()

    def reDrawAll(self):
        for feature in self.features:
            feature.drawGeometry()

    def childDidUpdate(self):
        pass
