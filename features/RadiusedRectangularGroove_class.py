import inspect
from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import addDebugFrame, Glib as G
from option_queries import SideXQuery, SideYQuery, CutDepthQuery, ReferenceXQuery, ReferenceYQuery,\
    PathReferenceQuery, CornerRadiusQuery
from drawn_features import RadiusedRectangularGrooveDrawing
from errors import PathReferenceError


class RadiusedRectangularGroove(DepthSteppingFeature):
    """Reference position is the center. The queries determine the path of the
    center of the cutter.
    Queries define a square to which the radius is later applied."""
    name = 'Radiused Rectangular Groove'
    user_selectable = True
    option_query_classes = [
        SideXQuery,
        SideYQuery,
        PathReferenceQuery,
        CornerRadiusQuery,
    ]

    child_feature_classes = []

    def _getInstructions(self, sequence):
        """CW direction ATM"""
        side_X, side_Y, corner_radius = self.getGrooveAdjustments()
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('INCR')
        file_text += G.G1_XY((0, side_Y - (2* corner_radius)))
        file_text += G.G2XY((corner_radius, corner_radius), (corner_radius, 0))
        file_text += G.G1_XY((side_X - (2* corner_radius), 0))
        file_text += G.G2XY((corner_radius, - corner_radius), (0, - corner_radius))
        file_text += G.G1_XY((0, - side_Y + (2* corner_radius)))
        file_text += G.G2XY((- corner_radius, - corner_radius), (- corner_radius, 0))
        file_text += G.G1_XY((- side_X + (2* corner_radius), 0))
        file_text += G.G2XY((- corner_radius, corner_radius), (0, corner_radius))
        return file_text

    def moveToStart(self):
        """Where does it start ?"""
        side_X, side_Y, corner_radius = self.getGrooveAdjustments()
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((- side_X / 2, corner_radius - (side_Y / 2)))
        return file_text

    def returnToHome(self):
        """Where does it finish ?"""
        side_X, side_Y, corner_radius = self.getGrooveAdjustments()
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((side_X / 2, - corner_radius + (side_Y / 2)))
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'side_X': self.option_queries[SideXQuery].getValue(),
            'side_Y': self.option_queries[SideYQuery].getValue(),
            'path_reference': self.option_queries[PathReferenceQuery].getValue(),
            'corner_radius': self.option_queries[CornerRadiusQuery].getValue()
        })
        return basic_params

    def validateParams(self):
        """Validate consistency of corner radius and other params."""
        params = self.getParams()
        path_reference = params['path_reference']
        corner_radius = params['corner_radius']
        bit_radius = params['bit_diameter'] / 2
        # TODO: define some formula involving corner_radius, bit_diameter, path_reference
        if path_reference is 'od':
            if corner_radius <= bit_radius:
                raise ValueError('Side Y is smaller than bit diameter')
        if path_reference is 'center':
            if corner_radius <= bit_radius / 2:
                raise ValueError('Side Y is smaller than bit diameter')


    def _makeDrawingClass(self):
        class Anon(RadiusedRectangularGrooveDrawing):
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
        corner_radius = params['corner_radius']
        if path_reference == 'center':
            pass
        elif path_reference == 'od':
            side_X -= bit_diameter
            side_Y -= bit_diameter
            corner_radius -= (bit_diameter / 2)
        elif path_reference == 'id':
            side_X += bit_diameter
            side_Y += bit_diameter
            corner_radius += (bit_diameter / 2)
        else:
            raise PathReferenceError(self, path_reference)
        return (side_X, side_Y, corner_radius)
