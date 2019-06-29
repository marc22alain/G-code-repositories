from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from drawn_entities import Rectangle, RoundedRectangle
from utilities import log
from errors import *

# used by RectangularPocket
class RectangularPocketDrawing(FeatureDrawing, AutoObserver):
    '''
    The drawing's reference point is one of ['center', 'lower-left']
    'center' is at the very center of the drawing.
    'lower-left' is at the centerpoint of the left-side radius.
    '''
    reference_point = None

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)
        log('RectangularPocketDrawing __init__')

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        refX = self.params['refX']
        refY = self.params['refY']
        side_X = self.params['side_X']
        side_Y = self.params['side_Y']
        half_side_X = side_X / 2
        half_side_Y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(RoundedRectangle(self.view_space))
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (refX - half_side_X, refY - half_side_Y, refX + half_side_X, refY + half_side_Y, bit_radius),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (refX, refY, refX + side_X, refY + side_Y, bit_radius),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refY = self.params['refY']
        side_Y = self.params['side_Y']
        half_side_Y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space))
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (refY - half_side_Y, stock_height - cut_depth, refY + half_side_Y, stock_height),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (refY, stock_height - cut_depth, refY + side_Y, stock_height),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)

    def _drawXZentities(self):
        plane = 'XZ'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        side_X = self.params['side_X']
        half_side_X = side_X / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space))
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (refX - half_side_X, stock_height - cut_depth, refX + half_side_X, stock_height),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (refX, stock_height - cut_depth, refX + side_X, stock_height),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)
