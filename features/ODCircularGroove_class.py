from GeometricFeature_class import GeometricFeature
from CircularGroove_class import CircularGroove
from DepthStepper_class import DepthStepper
from option_queries import *

class ODCircularGroove(GeometricFeature):
    name = 'OD Circular Groove'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery,
        BitDiameterQuery,
        CutDepthQuery
    ]

    # child_features = {
    #     # works OK when there is only one instance of
    #     'CircularGroove': CircularGroove(1,2).getOptionQueries(),
    #     # alternatively
    #     CircularGroove: CircularGroove.option_queries
    # }
    child_feature_classes = [
        CircularGroove
    ]

    parent_feature_class = DepthStepper

    def getGCode(self):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        bit_diameter = self.option_queries[BitDiameterQuery].getValue()
        depth = self.option_queries[CutDepthQuery].getValue()
        center_diameter = diameter - (bit_diameter / 2.0)

        child = self.child_features.values()[0]
        child.option_queries[PathDiameterQuery].setValue(center_diameter)
        # this may be a relative cut per pass, or absolute cut depth,
        # quite up in the air !
        child.option_queries[CutDepthQuery].setValue(depth)
        return child.getGCode()
