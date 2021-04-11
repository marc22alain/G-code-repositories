from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from drawn_entities import Rectangle, RoundedRectangle
from utilities import log
from errors import ReferencePointError

# used by LinearGroove
class RoundEndedRectangleDrawing(FeatureDrawing, AutoObserver):
    """This is a sausage.
    The drawing's reference point is one of ['center', 'lower-left']
    'center' is at the very center of the drawing.
    'lower-left' is at the centerpoint of the left-side radius."""
    reference_point = None

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)
        log('RoundEndedRectangleDrawing __init__')

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        ref_X = self.params['ref_X']
        ref_Y = self.params['ref_Y']
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        half_side_x = delta_X / 2
        half_side_y = delta_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        if (delta_X + delta_Y != 0) and (delta_Y * delta_X == 0):
            if not self.entities[plane]:
                self.entities[plane].append(RoundedRectangle(self.view_space))
            if self.reference_point == 'center':
                self.entities[plane][0].setAll(
                    (
                        ref_X - half_side_x - bit_radius,
                        ref_Y - half_side_y - bit_radius,
                        ref_X + half_side_x + bit_radius,
                        ref_Y + half_side_y + bit_radius,
                        bit_radius
                    ),
                    options
                ).draw()
            elif self.reference_point == 'lower-left':
                self.entities[plane][0].setAll(
                    (
                        ref_X - bit_radius,
                        ref_Y - bit_radius,
                        ref_X + delta_X + bit_radius,
                        ref_Y + delta_Y + bit_radius,
                        bit_radius
                    ),
                    options
                ).draw()
            else:
                raise ReferencePointError(self, self.reference_point)
        else:
            raise TypeError('RoundEndedRectangleDrawing does not implement _drawXYentities')

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_Y = self.params['ref_Y']
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        half_side_y = delta_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if (delta_X + delta_Y != 0) and (delta_Y * delta_X == 0):
            if not self.entities[plane]:
                self.entities[plane].append(Rectangle(self.view_space))
            if self.reference_point == 'center':
                self.entities[plane][0].setAll(
                    (
                        ref_Y - half_side_y - bit_radius,
                        stock_height - cut_depth,
                        ref_Y + half_side_y + bit_radius,
                        stock_height
                    ),
                    options
                ).draw()
            elif self.reference_point == 'lower-left':
                self.entities[plane][0].setAll(
                    (
                        ref_Y - bit_radius,
                        stock_height - cut_depth,
                        ref_Y + delta_Y + bit_radius,
                        stock_height
                    ),
                    options
                ).draw()
            else:
                raise ReferencePointError(self, self.reference_point)
        else:
            raise TypeError('RoundEndedRectangleDrawing does not implement _drawYZentities')

    def _drawXZentities(self):
        plane = 'XZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_X = self.params['ref_X']
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        half_side_x = delta_X / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if (delta_X + delta_Y != 0) and (delta_Y * delta_X == 0):
            if not self.entities[plane]:
                self.entities[plane].append(Rectangle(self.view_space))
            if self.reference_point == 'center':
                self.entities[plane][0].setAll(
                    (
                        ref_X - half_side_x - bit_radius,
                        stock_height - cut_depth,
                        ref_X + half_side_x + bit_radius,
                        stock_height
                    ),
                    options
                ).draw()
            elif self.reference_point == 'lower-left':
                self.entities[plane][0].setAll(
                    (
                        ref_X - bit_radius,
                        stock_height - cut_depth,
                        ref_X + delta_X + bit_radius,
                        stock_height
                    ),
                    options
                ).draw()
            else:
                raise ReferencePointError(self, self.reference_point)
        else:
            raise TypeError('RoundEndedRectangleDrawing does not implement _drawXZentities')
