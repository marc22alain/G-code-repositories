import abc
from GeometricFeature_class import GeometricFeature
from DepthStepper_class import DepthStepper
from option_queries import *

class DepthSteppingFeature(GeometricFeature):
    def __init__(self, feature_manager, manages_depth=True):
        self.self_managed_depth = manages_depth
        if self.self_managed_depth:
            self.option_query_classes = self.option_query_classes + DepthStepper.option_query_classes
        GeometricFeature.__init__(self, feature_manager)
        if self.self_managed_depth:
            self.depth_stepper = DepthStepper(feature_manager)

    def getManagedDepthInstructions(self):
        self.depth_stepper.option_queries[CutPerPassQuery] = self.option_queries[CutPerPassQuery]
        self.depth_stepper.option_queries[CutDepthQuery] = self.option_queries[CutDepthQuery]
        return self.depth_stepper.getGCode(self.getInstructions, self.moveToReference, self.returnFromReference)

    @abc.abstractmethod
    def getInstructions(self):
        pass
