from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import Glib as G
from option_queries import *
from drawn_features import RectangularGrooveDrawing


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
        side_X = self.option_queries[SideXQuery].getValue()
        side_Y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G1_XY((0, side_Y))
        file_text += G.G1_XY((side_X, 0))
        file_text += G.G1_XY((0, - side_Y))
        file_text += G.G1_XY((- side_X, 0))
        return file_text

    def moveToStart(self):
        side_X = self.option_queries[SideXQuery].getValue()
        side_Y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- side_X / 2, - side_Y / 2))
        return file_text

    def returnToHome(self):
        side_X = self.option_queries[SideXQuery].getValue()
        side_Y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((side_X / 2, side_Y / 2))
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'refX': self.option_queries[ReferenceXQuery].getValue(),
            'refY': self.option_queries[ReferenceYQuery].getValue(),
            'side_X': self.option_queries[SideXQuery].getValue(),
            'side_Y': self.option_queries[SideYQuery].getValue(),
        })
        return basic_params

    def _makeDrawingClass(self):
        class Anon(RectangularGrooveDrawing):
            params = self.getParams()
            # options = self.getOptions()
            observable = self
            view_space = self.view_space
            reference_point = 'lower-left'
        return Anon
