from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import Glib as G
from option_queries import *
from drawn_entities import Rectangle, RoundedRectangle


class RectangularGroove(DepthSteppingFeature):
    '''
    Reference position is center.
    The queries determine the path of the center of the cutter.
    '''
    name = 'Rectangular Groove'
    user_selectable = True
    option_query_classes = [
        SideXQuery,
        SideYQuery,
    ]

    child_feature_classes = []

    def getGCode(self, sequence = None):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        '''
        Climb cutting ?
        '''
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G1_XY((0, side_y))
        file_text += G.G1_XY((side_x, 0))
        file_text += G.G1_XY((0, - side_y))
        file_text += G.G1_XY((- side_x, 0))
        return file_text

    def moveToStart(self):
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- side_x / 2, - side_y / 2))
        return file_text

    def returnToHome(self):
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((side_x / 2, side_y / 2))
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        return (basic_params, cut_depth, side_x, side_y, refX, refY)

    def _drawXYentities(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_x = side_x / 2
        half_side_y = side_y / 2
        bit_diameter = basic_params['bit_diameter']
        bit_radius = bit_diameter / 2
        if len(self.entities['XY']) == 0:
            self.entities['XY'].append(RoundedRectangle(self.view_space).setAll(
                (refX - half_side_x - bit_radius, refY - half_side_y - bit_radius, refX + half_side_x + bit_radius, refY + half_side_y + bit_radius, bit_diameter),
                options
            ).draw())
            self.entities['XY'].append(Rectangle(self.view_space).setAll(
                (refX - half_side_x + bit_radius, refY - half_side_y + bit_radius, refX + half_side_x - bit_radius, refY + half_side_y - bit_radius),
                options
            ).draw())
        else:
            self.entities['XY'][0].setAll(
                (refX - half_side_x - bit_radius, refY - half_side_y - bit_radius, refX + half_side_x + bit_radius, refY + half_side_y + bit_radius, bit_diameter),
                options
            ).draw()
            self.entities['XY'][1].setAll(
                (refX - half_side_x + bit_radius, refY - half_side_y + bit_radius, refX + half_side_x - bit_radius, refY + half_side_y - bit_radius),
                options
            ).draw()

    def _drawYZentities(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_y = side_y / 2
        bit_radius = basic_params['bit_diameter'] / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['YZ']) == 0:
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - half_side_y - bit_radius, stock_height - cut_depth, refY + half_side_y + bit_radius, stock_height),
                options
            ).draw())
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - half_side_y + bit_radius, stock_height - cut_depth, refY + half_side_y - bit_radius, stock_height),
                options
            ).draw())
        else:
            self.entities['YZ'][0].setAll(
                (refY - half_side_y - bit_radius, stock_height - cut_depth, refY + half_side_y + bit_radius, stock_height),
                options
            ).draw()
            self.entities['YZ'][1].setAll(
                (refY - half_side_y + bit_radius, stock_height - cut_depth, refY + half_side_y - bit_radius, stock_height),
                options
            ).draw()

    def _drawXZentities(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_x = side_x / 2
        bit_radius = basic_params['bit_diameter'] / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['XZ']) == 0:
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - half_side_x - bit_radius, stock_height - cut_depth, refX + half_side_x + bit_radius, stock_height),
                options
            ).draw())
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - half_side_x + bit_radius, stock_height - cut_depth, refX + half_side_x - bit_radius, stock_height),
                options
            ).draw())
        else:
            self.entities['XZ'][0].setAll(
                (refX - half_side_x - bit_radius, stock_height - cut_depth, refX + half_side_x + bit_radius, stock_height),
                options
            ).draw()
            self.entities['XZ'][1].setAll(
                (refX - half_side_x + bit_radius, stock_height - cut_depth, refX + half_side_x - bit_radius, stock_height),
                options
            ).draw()
