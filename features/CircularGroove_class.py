from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import Glib as G
from option_queries import *


class CircularGroove(DepthSteppingFeature):
    name = 'Circular Groove'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery
    ]

    child_feature_classes = []

    def getGCode(self):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self.getInstructions(None)

    def getInstructions(self, sequence):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        return G.G2XY_to_INCR_FULL((0,0),(diameter / 2, 0))

    def moveToStart(self):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        file_text = G.set_INCR_mode()
        file_text += G.G0_XY((- diameter / 2, 0))
        return file_text

    def returnToHome(self):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        file_text = G.set_INCR_mode()
        file_text += G.G0_XY((diameter / 2, 0))
        return file_text
