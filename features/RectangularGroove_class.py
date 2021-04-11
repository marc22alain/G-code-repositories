import inspect
from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import addDebugFrame, Glib as G
from option_queries import SideXQuery, SideYQuery, CutDepthQuery, ReferenceXQuery, ReferenceYQuery,\
    PathReferenceQuery
from drawn_features import RectangularGrooveDrawing
from errors import PathReferenceError


class RectangularGroove(DepthSteppingFeature):
    """Reference position is the center. The path reference is the
    bit's center. The queries determine the path of the center of the cutter.
    As it is cut with straight moves only, the outer cut edge is radiused
    according to the bit's radius, while the inner cut edge has sharp corners."""
    name = 'Rectangular Groove'
    user_selectable = True
    option_query_classes = [
        SideXQuery,
        SideYQuery,
        PathReferenceQuery,
    ]

    child_feature_classes = []

    def _getInstructions(self, sequence):
        """Climb cutting ?"""
        side_X, side_Y = self.getGrooveAdjustments()
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('INCR')
        file_text += G.G1_XY((0, side_Y))
        file_text += G.G1_XY((side_X, 0))
        file_text += G.G1_XY((0, - side_Y))
        file_text += G.G1_XY((- side_X, 0))
        return file_text

    def moveToStart(self):
        """Reference position is the center, go to corner."""
        side_X, side_Y = self.getGrooveAdjustments()
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((- side_X / 2, - side_Y / 2))
        return file_text

    def returnToHome(self):
        """Reference position is the center, return from corner."""
        side_X, side_Y = self.getGrooveAdjustments()
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((side_X / 2, side_Y / 2))
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'side_X': self.option_queries[SideXQuery].getValue(),
            'side_Y': self.option_queries[SideYQuery].getValue(),
            'path_reference': self.option_queries[PathReferenceQuery].getValue()
        })
        return basic_params

    def _makeDrawingClass(self):
        class Anon(RectangularGrooveDrawing):
            params = self.getParams()
            observable = self
            view_space = self.view_space
            reference_point = 'center'
        return Anon

    def getGrooveAdjustments(self):
        params = self.getParams()
        bit_diameter = params['bit_diameter']
        path_reference = params['path_reference']
        side_X = params['side_X']
        side_Y = params['side_Y']
        if path_reference == 'center':
            pass
        elif path_reference == 'od':
            side_X = side_X - bit_diameter
            side_Y = side_Y - bit_diameter
        elif path_reference == 'id':
            side_X = side_X + bit_diameter
            side_Y = side_Y + bit_diameter
        else:
            raise PathReferenceError(self, path_reference)
        return (side_X, side_Y)
