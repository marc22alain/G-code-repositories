from GeometricFeature_class import GeometricFeature
from option_queries import *
from utilities import Glib

class DepthStepper(GeometricFeature):
    '''
    Conceived as a class that will automatically wrap <any> user-specified
    feature. Does this break the pattern by presenting a different
    initialization interface ?
    Alternatively, could satisfy the requirement by adding an OptionQuery.
    ---
    Consider the challenge of using the DepthStepper to cause the child feature
    to make a tabbed cut.
    '''
    # Consider if this might get over-written by the child feature's name
    # name = 'Depth Stepper'
    user_selectable = False
    option_query_classes = [
        CutPerPassQuery,
        CutDepthQuery
    ]

    child_feature_classes = []

    def __init__(self, machine, workpiece, feature_class):
        GeometricFeature.__init__(self, machine, workpiece)
        self.name = feature_class.name
        self.child_features[feature_class] = None
        self.makeChildren()

    def getGCode(self):
        return self.child_features.values()[0].getGCode()
