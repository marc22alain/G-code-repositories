from AbstractFeatureManager_class import AbstractFeatureManager
from machines import SimpleMachine
from workpieces import SimpleWorkpiece
from ui import OptionQueryDialog
from utilities import Glib as G
from features import *


class FeatureManager(AbstractFeatureManager):
    def __init__(self, view_space=None):
        self.machine = SimpleMachine(self)
        self.work_piece = SimpleWorkpiece(self, view_space)
        self.view_space = view_space
        AbstractFeatureManager.__init__(self)

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
