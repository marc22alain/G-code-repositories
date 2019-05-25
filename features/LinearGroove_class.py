from DepthSteppingFeature_class import DepthSteppingFeature
from DepthStepper_class import DepthStepper
from utilities import Glib as G
from option_queries import *


class LinearGroove(DepthSteppingFeature):
    name = 'Linear Groove'
    user_selectable = True
    option_query_classes = [
        DeltaXQuery,
        DeltaYQuery
    ]

    child_feature_classes = []

    def getGCode(self):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions()

    def _getInstructions(self, sequence):
        delta_x = self.option_queries[DeltaXQuery].getValue()
        delta_y = self.option_queries[DeltaYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        if self.at_start:
            file_text += G.G1_XY((delta_x, delta_y))
        else:
            file_text += G.G1_XY((- delta_x, - delta_y))
        self.at_start = not self.at_start
        return file_text

    def moveToStart(self):
        self.at_start = True
        # for starting point reference point
        file_text = ''
        return file_text

    def returnToHome(self):
        # for starting point reference point
        delta_x = self.option_queries[DeltaXQuery].getValue()
        delta_y = self.option_queries[DeltaYQuery].getValue()
        file_text = ''
        if not self.at_start:
            file_text = self.machine.setMode('INCR')
            file_text += G.G0_XY((- delta_x, - delta_y))
            self.at_start = True
        return file_text

    def _drawXYentities(self):
        raise TypeError('LinearGroove does not implement _drawXYentities')

    def _drawYZentities(self):
        raise TypeError('LinearGroove does not implement _drawYZentities')

    def _drawXZentities(self):
        raise TypeError('LinearGroove does not implement _drawXZentities')
