from DepthSteppingFeature_class import DepthSteppingFeature
from DepthStepper_class import DepthStepper
from utilities import Glib as G
from option_queries import *
from drawn_entities import RoundedRectangle, Rectangle


class LinearGroove(DepthSteppingFeature):
    name = 'Linear Groove'
    user_selectable = True
    option_query_classes = [
        DeltaXQuery,
        DeltaYQuery
    ]

    child_feature_classes = []

    def getGCode(self):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions()

    def _getInstructions(self, sequence):
        basic_params, cut_depth, delta_x, delta_y, refX, refY = self.getParams()
        file_text = self.machine.setMode('INCR')
        if self.at_start:
            file_text += G.G1_XY((delta_x, delta_y))
        else:
            file_text += G.G1_XY((- delta_x, - delta_y))
        self.at_start = not self.at_start
        return file_text

    def moveToStart(self):
        self.at_start = True
        # for starting point reference point
        file_text = ''
        return file_text

    def returnToHome(self):
        # for starting point reference point
        basic_params, cut_depth, delta_x, delta_y, refX, refY = self.getParams()
        file_text = ''
        if not self.at_start:
            file_text = self.machine.setMode('INCR')
            file_text += G.G0_XY((- delta_x, - delta_y))
            self.at_start = True
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        delta_x = self.option_queries[DeltaXQuery].getValue()
        delta_y = self.option_queries[DeltaYQuery].getValue()
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        return (basic_params, cut_depth, delta_x, delta_y, refX, refY)

    def _drawXYentities(self):
        basic_params, cut_depth, delta_x, delta_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_x = delta_x / 2
        half_side_y = delta_y / 2
        bit_radius = basic_params['bit_diameter'] / 2
        if (delta_x + delta_y != 0) and (delta_y * delta_x == 0):
            if len(self.entities['XY']) == 0:
                self.entities['XY'].append(RoundedRectangle(self.view_space).setAll(
                    (refX - half_side_x - bit_radius, refY - half_side_y - bit_radius, refX + half_side_x + bit_radius, refY + half_side_y + bit_radius, bit_radius),
                    options
                ).draw())
            else:
                self.entities['XY'][0].setAll(
                    (refX - half_side_x - bit_radius, refY - half_side_y - bit_radius, refX + half_side_x + bit_radius, refY + half_side_y + bit_radius, bit_radius),
                    options
                ).draw()
        else:
            raise TypeError('LinearGroove does not implement _drawXYentities')

    def _drawYZentities(self):
        basic_params, cut_depth, delta_x, delta_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_y = delta_y / 2
        bit_radius = basic_params['bit_diameter']
        stock_height = basic_params['stock_height']
        if (delta_x + delta_y != 0) and (delta_y * delta_x == 0):
            if len(self.entities['YZ']) == 0:
                self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                    (refY - half_side_y - bit_radius, stock_height - cut_depth, refY + half_side_y + bit_radius, stock_height),
                    options
                ).draw())
            else:
                self.entities['YZ'][0].setAll(
                    (refY - half_side_y - bit_radius, stock_height - cut_depth, refY + half_side_y + bit_radius, stock_height),
                    options
                ).draw()
        else:
            raise TypeError('LinearGroove does not implement _drawYZentities')

    def _drawXZentities(self):
        basic_params, cut_depth, delta_x, delta_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_x = delta_x / 2
        bit_radius = basic_params['bit_diameter']
        stock_height = basic_params['stock_height']
        if (delta_x + delta_y != 0) and (delta_y * delta_x == 0):
            if len(self.entities['XZ']) == 0:
                self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                    (refX - half_side_x - bit_radius, stock_height - cut_depth, refX + half_side_x + bit_radius, stock_height),
                    options
                ).draw())
            else:
                self.entities['XZ'][0].setAll(
                    (refX - half_side_x - bit_radius, stock_height - cut_depth, refX + half_side_x + bit_radius, stock_height),
                    options
                ).draw()
        else:
            raise TypeError('LinearGroove does not implement _drawXZentities')
