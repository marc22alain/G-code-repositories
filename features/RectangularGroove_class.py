from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import Glib as G
from option_queries import *


class RectangularGroove(DepthSteppingFeature):
    '''
    Reference position is center.
    The queries determine the path of the center of the cutter.
    '''
    name = 'Rectangular Groove'
    user_selectable = True
    option_query_classes = [
        SideXQuery,
        SideYQuery,
    ]

    child_feature_classes = []

    def getGCode(self, sequence = None):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        '''
        Climb cutting ?
        '''
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G1_XY((0, side_y))
        file_text += G.G1_XY((side_x, 0))
        file_text += G.G1_XY((0, - side_y))
        file_text += G.G1_XY((- side_x, 0))
        return file_text

    def moveToStart(self):
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- side_x / 2, - side_y / 2))
        return file_text

    def returnToHome(self):
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((side_x / 2, side_y / 2))
        return file_text
