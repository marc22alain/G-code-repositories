from GeometricFeature_class import GeometricFeature
from OptionQuery_class import OptionQuery
from DepthStepper_class import DepthStepper
from utilities import Glib as G
from option_queries import *


class CircularGroove(GeometricFeature):
    name = 'Circular Groove'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery,
        CutDepthQuery
    ]

    child_feature_classes = []

    parent_feature_class = DepthStepper

    def getGCode(self, ref_point='center'):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        cut_instruction = G.G2XY_to_INCR_FULL((0,0),(diameter / 2, 0))
        if ref_point == 'center':
            return self.wrapCenterRef(cut_instruction)
        elif ref_point == 'start':
            return cut_instruction
        raise ValueError('"%s" is not a valid reference point for CircularGroove' % (ref_point))
        # depth = self.option_query_instances[CutDepthQuery].getValue()
        # move to depth

    def wrapCenterRef(self, cut_instruction):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        file_text = G.set_INCR_mode()
        file_text += G.G0_XY((- diameter / 2, 0))
        file_text += cut_instruction
        file_text += G.G0_XY((diameter / 2, 0))
        return file_text
