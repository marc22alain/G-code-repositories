from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import Glib as G
from option_queries import PathDiameterQuery, CutDepthQuery, ReferenceXQuery, ReferenceYQuery,\
    PathReferenceQuery
from drawn_features import CircularGrooveDrawing


class CircularGroove(DepthSteppingFeature):
    """The CircularGroove is a single cut of a full circle. The feature's
    reference point is the center of the circle, and the path reference is the
    center of the bit."""
    name = 'Circular Groove'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery,
        PathReferenceQuery
    ]

    child_feature_classes = []

    def _getInstructions(self, sequence):
        diameter = self._getAdjustedDiameter()
        file_text = self.machine.setMode('INCR')
        file_text += G.G2XY((0, 0), (diameter / 2, 0))
        return file_text

    def moveToStart(self):
        """Assumes reference point at center."""
        diameter = self._getAdjustedDiameter()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- diameter / 2, 0))
        return file_text

    def returnToHome(self):
        """Assumes reference point at center."""
        diameter = self._getAdjustedDiameter()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((diameter / 2, 0))
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'path_reference': self.option_queries[PathReferenceQuery].getValue(),
            'diameter': self.option_queries[PathDiameterQuery].getValue()
        })
        return basic_params

    def _makeDrawingClass(self):
        class Anon(CircularGrooveDrawing):
            params = self.getParams()
            observable = self
            view_space = self.view_space
        return Anon

    def _getAdjustedDiameter(self):
        params = self.getParams()
        bit_diameter = params['bit_diameter']
        path_reference = params['path_reference']
        if path_reference is 'center':
            diameter = params['diameter']
        elif path_reference is 'od':
            diameter = params['diameter'] - bit_diameter
        elif path_reference is 'id':
            diameter = params['diameter'] + bit_diameter
        else:
            raise PathReferenceError(self, path_reference)
        return diameter
