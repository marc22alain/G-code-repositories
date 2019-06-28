from FeatureDrawing_class import FeatureDrawing
from GrooveDrawing_class import GrooveDrawing
from observeder import AutoObserver
from drawn_entities import Rectangle, RoundedRectangle
from utilities import log
from errors import *

# used by RectangularGroove
class RectangularGrooveDrawing(FeatureDrawing, GrooveDrawing, AutoObserver):
    '''
    The drawing's reference point is one of ['center', 'lower-left']
    'center' is at the very center of the drawing.
    'lower-left' is at the centerpoint of the left-side radius.
    '''
    reference_point = None
    '''
    The drawing's path reference is one of ['center', 'od', 'id']
    'center' path reference is at the very center of bit's path.
    'od' path reference is the outer diameter of bit's path.
    'id' path reference is the inner diameter of bit's path.
    '''
    path_reference = None

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)
        log('RectangularGrooveDrawing __init__')

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        refY = self.params['refY']
        side_X = self.params['side_X']
        side_Y = self.params['side_Y']
        half_side_x = side_X / 2
        half_side_y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        inner_adj, outer_adj = self.getAdjustments()
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space)) # inner edge
            self.entities[plane].append(RoundedRectangle(self.view_space)) # outer edge
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (refX - half_side_x - inner_adj, refY - half_side_y - inner_adj, refX + half_side_x + inner_adj, refY + half_side_y + inner_adj),
                options
            ).draw()
            self.entities[plane][1].setAll(
                (refX - half_side_x - outer_adj, refY - half_side_y - outer_adj, refX + half_side_x + outer_adj, refY + half_side_y + outer_adj, bit_radius),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (refX - inner_adj, refY - inner_adj, refX + side_X + inner_adj, refY + side_Y + inner_adj),
                options
            ).draw()
            self.entities[plane][1].setAll(
                (refX - outer_adj, refY - outer_adj, refX + side_X + outer_adj, refY + side_Y + outer_adj, bit_radius),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refY = self.params['refY']
        side_X = self.params['side_X']
        side_Y = self.params['side_Y']
        half_side_x = side_X / 2
        half_side_y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        inner_adj, outer_adj = self.getAdjustments()
        stock_height = self.params['stock_height']
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space)) # inner edge
            self.entities[plane].append(Rectangle(self.view_space)) # outer edge
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (refY - half_side_y - inner_adj, stock_height - cut_depth, refY + half_side_y + inner_adj, stock_height),
                options
            ).draw()
            self.entities[plane][1].setAll(
                (refY - half_side_y - outer_adj, stock_height - cut_depth, refY + half_side_y + outer_adj, stock_height),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (refY - inner_adj, stock_height - cut_depth, refY + side_Y + inner_adj, stock_height),
                options
            ).draw()
            self.entities[plane][1].setAll(
                (refY - outer_adj, stock_height - cut_depth, refY + side_Y + outer_adj, stock_height),
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
        side_Y = self.params['side_Y']
        half_side_x = side_X / 2
        half_side_y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        inner_adj, outer_adj = self.getAdjustments()
        stock_height = self.params['stock_height']
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space)) # inner edge
            self.entities[plane].append(Rectangle(self.view_space)) # outer edge
        if self.reference_point == 'center':
            self.entities[plane][0].setAll(
                (refX - half_side_x - inner_adj, stock_height - cut_depth, refX + half_side_x + inner_adj, stock_height),
                options
            ).draw()
            self.entities[plane][1].setAll(
                (refX - half_side_x - outer_adj, stock_height - cut_depth, refX + half_side_x + outer_adj, stock_height),
                options
            ).draw()
        elif self.reference_point == 'lower-left':
            self.entities[plane][0].setAll(
                (refX - inner_adj, stock_height - cut_depth, refX + side_X + inner_adj, stock_height),
                options
            ).draw()
            self.entities[plane][1].setAll(
                (refX - outer_adj, stock_height - cut_depth, refX + side_X + outer_adj, stock_height),
                options
            ).draw()
        else:
            raise ReferencePointError(self, self.reference_point)
