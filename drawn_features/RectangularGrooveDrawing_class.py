from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from drawn_entities import Rectangle, RoundedRectangle
from utilities import log
from errors import *

# used by RectangularGroove
class RectangularGrooveDrawing(FeatureDrawing, AutoObserver):
    '''
    This is a sausage.
    The drawing's reference point is one of ['center', 'lower-left']
    'center' is at the very center of the drawing.
    'lower-left' is at the centerpoint of the left-side radius.
    '''
    reference_point = None

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)
        log('RectangularGrooveDrawing __init__')

    def _drawXYentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        refY = self.params['refY']
        side_X = self.params['side_X']
        side_Y = self.params['side_Y']
        half_side_x = side_X / 2
        half_side_y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        if len(self.entities['XY']) == 0:
            if self.reference_point == 'center':
                self.entities['XY'].append(RoundedRectangle(self.view_space).setAll(
                    (refX - half_side_x - bit_radius, refY - half_side_y - bit_radius, refX + half_side_x + bit_radius, refY + half_side_y + bit_radius, bit_radius),
                    options
                ).draw())
                self.entities['XY'].append(Rectangle(self.view_space).setAll(
                    (refX - half_side_x + bit_radius, refY - half_side_y + bit_radius, refX + half_side_x - bit_radius, refY + half_side_y - bit_radius),
                    options
                ).draw())
            elif self.reference_point == 'lower-left':
                self.entities['XY'].append(RoundedRectangle(self.view_space).setAll(
                    (refX - bit_radius, refY - bit_radius, refX + side_X + bit_radius, refY + side_Y + bit_radius, bit_radius),
                    options
                ).draw())
                self.entities['XY'].append(Rectangle(self.view_space).setAll(
                    (refX + bit_radius, refY + bit_radius, refX + side_X - bit_radius, refY + side_Y - bit_radius),
                    options
                ).draw())
            else:
                raise ReferencePointError(self, self.reference_point)
        else:
            if self.reference_point == 'center':
                self.entities['XY'][0].setAll(
                    (refX - half_side_x - bit_radius, refY - half_side_y - bit_radius, refX + half_side_x + bit_radius, refY + half_side_y + bit_radius, bit_radius),
                    options
                ).draw()
                self.entities['XY'][1].setAll(
                    (refX - half_side_x + bit_radius, refY - half_side_y + bit_radius, refX + half_side_x - bit_radius, refY + half_side_y - bit_radius),
                    options
                ).draw()
            elif self.reference_point == 'lower-left':
                self.entities['XY'][0].setAll(
                    (refX - bit_radius, refY - bit_radius, refX + side_X + bit_radius, refY + side_Y + bit_radius, bit_radius),
                    options
                ).draw()
                self.entities['XY'][1].setAll(
                    (refX + bit_radius, refY + bit_radius, refX + side_X - bit_radius, refY + side_Y - bit_radius),
                    options
                ).draw()
            else:
                raise ReferencePointError(self, self.reference_point)

    def _drawYZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refY = self.params['refY']
        side_X = self.params['side_X']
        side_Y = self.params['side_Y']
        half_side_x = side_X / 2
        half_side_y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if len(self.entities['YZ']) == 0:
            if self.reference_point == 'center':
                self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                    (refY - half_side_y - bit_radius, stock_height - cut_depth, refY + half_side_y + bit_radius, stock_height),
                    options
                ).draw())
                self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                    (refY - half_side_y + bit_radius, stock_height - cut_depth, refY + half_side_y - bit_radius, stock_height),
                    options
                ).draw())
            elif self.reference_point == 'lower-left':
                self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                    (refY - bit_radius, stock_height - cut_depth, refY + side_Y + bit_radius, stock_height),
                    options
                ).draw())
                self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                    (refY + bit_radius, stock_height - cut_depth, refY + side_Y - bit_radius, stock_height),
                    options
                ).draw())
            else:
                raise ReferencePointError(self, self.reference_point)
        else:
            if self.reference_point == 'center':
                self.entities['YZ'][0].setAll(
                    (refY - half_side_y - bit_radius, stock_height - cut_depth, refY + half_side_y + bit_radius, stock_height),
                    options
                ).draw()
                self.entities['YZ'][1].setAll(
                    (refY - half_side_y + bit_radius, stock_height - cut_depth, refY + half_side_y - bit_radius, stock_height),
                    options
                ).draw()
            elif self.reference_point == 'lower-left':
                self.entities['YZ'][0].setAll(
                    (refY - bit_radius, stock_height - cut_depth, refY + side_Y + bit_radius, stock_height),
                    options
                ).draw()
                self.entities['YZ'][1].setAll(
                    (refY + bit_radius, stock_height - cut_depth, refY + side_Y - bit_radius, stock_height),
                    options
                ).draw()
            else:
                raise ReferencePointError(self, self.reference_point)

    def _drawXZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        side_X = self.params['side_X']
        side_Y = self.params['side_Y']
        half_side_x = side_X / 2
        half_side_y = side_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if len(self.entities['XZ']) == 0:
            if self.reference_point == 'center':
                self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                    (refX - half_side_x - bit_radius, stock_height - cut_depth, refX + half_side_x + bit_radius, stock_height),
                    options
                ).draw())
                self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                    (refX - half_side_x + bit_radius, stock_height - cut_depth, refX + half_side_x - bit_radius, stock_height),
                    options
                ).draw())
            elif self.reference_point == 'lower-left':
                self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                    (refX - bit_radius, stock_height - cut_depth, refX + side_X + bit_radius, stock_height),
                    options
                ).draw())
                self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                    (refX + bit_radius, stock_height - cut_depth, refX + side_X - bit_radius, stock_height),
                    options
                ).draw())
            else:
                raise ReferencePointError(self, self.reference_point)
        else:
            if self.reference_point == 'center':
                self.entities['XZ'][0].setAll(
                    (refX - half_side_x - bit_radius, stock_height - cut_depth, refX + half_side_x + bit_radius, stock_height),
                    options
                ).draw()
                self.entities['XZ'][1].setAll(
                    (refX - half_side_x + bit_radius, stock_height - cut_depth, refX + half_side_x - bit_radius, stock_height),
                    options
                ).draw()
            elif self.reference_point == 'lower-left':
                self.entities['XZ'][0].setAll(
                    (refX - bit_radius, stock_height - cut_depth, refX + side_X + bit_radius, stock_height),
                    options
                ).draw()
                self.entities['XZ'][1].setAll(
                    (refX + bit_radius, stock_height - cut_depth, refX + side_X - bit_radius, stock_height),
                    options
                ).draw()
            else:
                raise ReferencePointError(self, self.reference_point)
