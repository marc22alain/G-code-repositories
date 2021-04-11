from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from drawn_entities import Rectangle, RoundedRectangle
from utilities import log
from errors import ReferencePointError

# used by Tenon
class TenonDrawing(FeatureDrawing, AutoObserver):
    """
    The drawing's reference point is one of ['center', 'lower-left']
    'center' is at the very center of the drawing.
    'lower-left' is at the centerpoint of the left-side radius.
    """
    reference_point = None

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)
        log('TenonDrawing __init__')

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        ref_X = self.params['ref_X']
        ref_Y = self.params['ref_Y']
        stock_X = self.params['stock_length']
        stock_Y = self.params['stock_width']
        shoulder_offset = self.params['shoulder_offset']
        corner_radius = self.params['corner_radius']

        side_X = stock_X - (2 * shoulder_offset)
        side_Y = stock_Y - (2 * shoulder_offset)

        half_side_X = side_X / 2
        half_side_Y = side_Y / 2
        if not self.entities[plane]:
            self.entities[plane].append(RoundedRectangle(self.view_space))
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (
                    ref_X - half_side_X,
                    ref_Y - half_side_Y,
                    ref_X + half_side_X,
                    ref_Y + half_side_Y,
                    corner_radius
                ),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (ref_X, ref_Y, ref_X + side_X, ref_Y + side_Y, corner_radius),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_Y = self.params['ref_Y']
        stock_Y = self.params['stock_width']
        shoulder_offset = self.params['shoulder_offset']
        side_Y = stock_Y - (2 * shoulder_offset)
        half_side_Y = side_Y / 2
        stock_height = self.params['stock_height']
        if not self.entities[plane]:
            self.entities[plane].append(Rectangle(self.view_space))
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (ref_Y - half_side_Y, stock_height - cut_depth, ref_Y + half_side_Y, stock_height),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (ref_Y, stock_height - cut_depth, ref_Y + side_Y, stock_height),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)

    def _drawXZentities(self):
        plane = 'XZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_X = self.params['ref_X']
        stock_X = self.params['stock_length']
        shoulder_offset = self.params['shoulder_offset']
        side_X = stock_X - (2 * shoulder_offset)
        half_side_X = side_X / 2
        stock_height = self.params['stock_height']
        if not self.entities[plane]:
            self.entities[plane].append(Rectangle(self.view_space))
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (ref_X - half_side_X, stock_height - cut_depth, ref_X + half_side_X, stock_height),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (ref_X, stock_height - cut_depth, ref_X + side_X, stock_height),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)
