from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from drawn_entities import Rectangle, RoundedRectangle
from utilities import log
from errors import *

# used by LinearGroove
class RoundEndedRectangleDrawing(FeatureDrawing, AutoObserver):
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
        log('RoundEndedRectangleDrawing __init__')

    def _drawXYentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        refY = self.params['refY']
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        half_side_x = delta_X / 2
        half_side_y = delta_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        if (delta_X + delta_Y != 0) and (delta_Y * delta_X == 0):
            if len(self.entities['XY']) == 0:
                if self.reference_point == 'center':
                    self.entities['XY'].append(RoundedRectangle(self.view_space).setAll(
                        (refX - half_side_x - bit_radius, refY - half_side_y - bit_radius, refX + half_side_x + bit_radius, refY + half_side_y + bit_radius, bit_radius),
                        options
                    ).draw())
                elif self.reference_point == 'lower-left':
                    self.entities['XY'].append(RoundedRectangle(self.view_space).setAll(
                        (refX - bit_radius, refY - bit_radius, refX + delta_X + bit_radius, refY + delta_Y + bit_radius, bit_radius),
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
                elif self.reference_point == 'lower-left':
                    self.entities['XY'][0].setAll(
                        (refX - bit_radius, refY - bit_radius, refX + delta_x + bit_radius, refY + delta_y + bit_radius, bit_radius),
                        options
                    ).draw()
                else:
                    raise ReferencePointError(self, self.reference_point)
        else:
            raise TypeError('RoundEndedRectangleDrawing does not implement _drawXYentities')

    def _drawYZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refY = self.params['refY']
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        half_side_x = delta_X / 2
        half_side_y = delta_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if (delta_X + delta_Y != 0) and (delta_Y * delta_X == 0):
            if len(self.entities['YZ']) == 0:
                if self.reference_point == 'center':
                    self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                        (refY - half_side_y - bit_radius, stock_height - cut_depth, refY + half_side_y + bit_radius, stock_height),
                        options
                    ).draw())
                elif self.reference_point == 'lower-left':
                    self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                        (refY - bit_radius, stock_height - cut_depth, refY + delta_Y + bit_radius, stock_height),
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
                elif self.reference_point == 'lower-left':
                    self.entities['YZ'][0].setAll(
                        (refY - bit_radius, stock_height - cut_depth, refY + delta_Y + bit_radius, stock_height),
                        options
                    ).draw()
                else:
                    raise ReferencePointError(self, self.reference_point)
        else:
            raise TypeError('RoundEndedRectangleDrawing does not implement _drawYZentities')

    def _drawXZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        half_side_x = delta_X / 2
        half_side_y = delta_Y / 2
        bit_radius = self.params['bit_diameter'] / 2
        stock_height = self.params['stock_height']
        if (delta_X + delta_Y != 0) and (delta_Y * delta_X == 0):
            if len(self.entities['XZ']) == 0:
                if self.reference_point == 'center':
                    self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                        (refX - half_side_x - bit_radius, stock_height - cut_depth, refX + half_side_x + bit_radius, stock_height),
                        options
                    ).draw())
                elif self.reference_point == 'lower-left':
                    self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                        (refX - bit_radius, stock_height - cut_depth, refX + delta_X + bit_radius, stock_height),
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
                elif self.reference_point == 'lower-left':
                    self.entities['XZ'][0].setAll(
                        (refX - bit_radius, stock_height - cut_depth, refX + delta_X + bit_radius, stock_height),
                        options
                    ).draw()
                else:
                    raise ReferencePointError(self, self.reference_point)
        else:
            raise TypeError('RoundEndedRectangleDrawing does not implement _drawXZentities')
