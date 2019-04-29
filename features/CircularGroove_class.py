from GeometricFeature_class import GeometricFeature
from OptionQuery_class import OptionQuery
from DepthStepper_class import DepthStepper
from utilities import Glib
from option_queries import *


class CircularGroove(GeometricFeature):
    name = 'Circular Groove'
    user_selectable = True
    option_queries = [
        PathDiameterQuery,
        BitDiameterQuery,
        CutDepthQuery,
        BogusQuery
    ]

    child_feature_classes = []

    parent_feature_class = DepthStepper

    def getGCode(self):
        diameter = self.option_query_instances[PathDiameterQuery].getValue()
        # depth = self.option_query_instances[CutDepthQuery].getValue()
        # move to depth
        file_text = ''
        file_text += Glib.G2XY_to_INCR_FULL((0,0),(diameter / 2, 0))
        return file_text
