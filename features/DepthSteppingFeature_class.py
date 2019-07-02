import abc
from geometric_feature_class import GeometricFeature
from DepthStepper_class import DepthStepper
from option_queries import *

class DepthSteppingFeature(GeometricFeature):
    def __init__(self, feature_manager, view_space, manages_depth=True):
        self.self_managed_depth = manages_depth
        if self.self_managed_depth:
            self.option_query_classes = self.option_query_classes + DepthStepper.option_query_classes
        GeometricFeature.__init__(self, feature_manager, view_space)
        if self.self_managed_depth:
            self.depth_stepper = DepthStepper(feature_manager, view_space)

    def getGCode(self, sequence = None):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        return self._getInstructions(sequence)

    def getManagedDepthInstructions(self):
        self.depth_stepper.option_queries[CutPerPassQuery] = self.option_queries[CutPerPassQuery]
        self.depth_stepper.option_queries[CutDepthQuery] = self.option_queries[CutDepthQuery]
        return self.depth_stepper.getGCode(self._getInstructions, self.moveToReference, self.returnFromReference)

    @abc.abstractmethod
    def _getInstructions(self, sequence):
        '''
        Use of sequence is to enable the implementing class to provide different
        procedures depending on the current sequence for the requested cutting
        instructions.
        '''
        pass
