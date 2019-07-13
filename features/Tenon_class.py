import inspect
import math
from DepthSteppingFeature_class import DepthSteppingFeature
from drawn_features import TenonDrawing
from option_queries import CornerRadiusQuery, CutDepthQuery, PathReferenceQuery,\
    ReferenceXQuery, ReferenceYQuery, ShoulderOffsetQuery, SideXQuery, SideYQuery
from RadiusedRectangularGroove_class import RadiusedRectangularGroove
from RectangularGroove_class import RectangularGroove
from utilities import addDebugFrame, log, Glib as G


class Tenon(DepthSteppingFeature):
    """The Tenon is co-centric with the work-piece, but the machining reference
    starting point is the 'lower-left' (0,0) point.
    The shoulder offset determines the distance from the tenon to
    the rail faces. The cut depth is the tenon's length."""
    name = 'Tenon'
    user_selectable = True
    option_query_classes = [
        ShoulderOffsetQuery,
        CornerRadiusQuery,
    ]

    child_feature_classes = [
        RectangularGroove,
        RadiusedRectangularGroove
    ]

    def _getInstructions(self, sequence):
        params = self.getParams()
        stock_X = params['stock_length']
        stock_Y = params['stock_width']
        shoulder_offset = params['shoulder_offset']
        max_offset = self._getMaxStartingOffset()
        current_offset = max_offset
        # accounting for the setup in moveToStart
        stock_X -= (2 * max_offset)
        stock_Y -= (2 * max_offset)
        rect_groove = self.child_features[RectangularGroove]
        rad_rect_groove = self.child_features[RadiusedRectangularGroove]
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('INCR')
        # get the base case first cut of rectangular groove
        file_text += rect_groove.getGCode()
        while current_offset < shoulder_offset:
            if current_offset + max_offset >= shoulder_offset:
                # calculates the last offset increment
                max_offset = shoulder_offset - current_offset
                # sets the guard to end the loop
                current_offset = shoulder_offset
            else:
                current_offset += max_offset
            stock_X -= (2 * max_offset)
            stock_Y -= (2 * max_offset)
            self.setUpRectangularGroove(stock_X, stock_Y)
            # set up and make another RectangularGroove cut
            file_text += self.machine.setMode('INCR')
            file_text += G.G1_XY((max_offset, max_offset))
            file_text += rect_groove.getGCode()
        # finish up with a single RadiusedRectangularGroove cut
        side_X, side_Y, corner_radius = rad_rect_groove.getGrooveAdjustments()
        file_text += self.machine.setMode('INCR')
        file_text += G.G1_XY((0, corner_radius))
        file_text += rad_rect_groove.getGCode()
        if sequence not in ['last', 'only']:
            file_text += G.comment(' *** watch for machining across the tenon *** ')
            max_offset = self._getMaxStartingOffset()
            # is the difference between the definitions of the starting
            # RectangularGroove and the finishing RadiusedRectangularGroove
            shift = - shoulder_offset + max_offset
            file_text += G.G1_XY((shift, shift - corner_radius))
        return file_text

    def setUpRectangularGroove(self, side_X, side_Y):
        """Set up and delegate to RectangularGroove."""
        # !!! must ensure bit is at tenon's center
        params = self.getParams()
        rect_groove = self.child_features[RectangularGroove]
        rect_groove.option_queries[SideXQuery].setValue(side_X),
        rect_groove.option_queries[SideYQuery].setValue(side_Y),
        rect_groove.option_queries[PathReferenceQuery].setValue('id')
        rect_groove.self_managed_depth = False

    def setUpRadiusedRectangularGroove(self):
        params = self.getParams()
        stock_X = params['stock_length']
        stock_Y = params['stock_width']
        shoulder_offset = params['shoulder_offset']
        corner_radius = params['corner_radius']
        rad_rect_groove = self.child_features[RadiusedRectangularGroove]
        rad_rect_groove.option_queries[SideXQuery].setValue(stock_X - (2 * shoulder_offset)),
        rad_rect_groove.option_queries[SideYQuery].setValue(stock_Y - (2 * shoulder_offset)),
        rad_rect_groove.option_queries[CornerRadiusQuery].setValue(corner_radius),
        rad_rect_groove.option_queries[PathReferenceQuery].setValue('id')
        rad_rect_groove.self_managed_depth = False

    def _getMaxStartingOffset(self):
        params = self.getParams()
        bit_diameter = params['bit_diameter']
        shoulder_offset = params['shoulder_offset']
        # this only works for uniform shoulder offset, i.e. all sides of the rail
        return min(round(bit_diameter / math.sqrt(2), 5), shoulder_offset)

    def moveToStart(self):
        file_text = addDebugFrame(inspect.currentframe())
        params = self.getParams()
        stock_X = params['stock_length']
        stock_Y = params['stock_width']
        max_offset = self._getMaxStartingOffset()
        self.setUpRadiusedRectangularGroove()
        self.setUpRectangularGroove(stock_X - (2 * max_offset), stock_Y - (2 * max_offset))
        file_text += self.child_features[RectangularGroove].moveToStart()
        return file_text

    def returnToHome(self):
        file_text = addDebugFrame(inspect.currentframe())
        file_text += self.child_features[RadiusedRectangularGroove].returnToHome()
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'corner_radius': self.option_queries[CornerRadiusQuery].getValue(),
            'shoulder_offset': self.option_queries[ShoulderOffsetQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue()
        })
        return basic_params

    def getOverlap(self):
        """Returns a figure that determines the overlap between adjacent cuts that
        form the tenon.
        TBD, but probably based on a constant to begin with.
        Unit is mm of course."""
        return 0.5

    def _makeDrawingClass(self):
        class Anon(TenonDrawing):
            params = self.getParams()
            observable = self
            view_space = self.view_space
            reference_point = 'center'
        return Anon
