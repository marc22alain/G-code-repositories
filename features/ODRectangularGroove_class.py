from DepthSteppingFeature_class import DepthSteppingFeature
from RectangularGroove_class import RectangularGroove
from utilities import Glib as G
from option_queries import *
from drawn_entities import Rectangle, RoundedRectangle
import inspect


class ODRectangularGroove(DepthSteppingFeature):
    '''
    Reference position is center.
    The queries determine the path of the center of the cutter.
    '''
    name = 'ODRectangular Groove'
    user_selectable = True
    option_query_classes = [
        SideXQuery,
        SideYQuery,
    ]

    child_feature_classes = [
        RectangularGroove
    ]

    def getGCode(self, sequence = None):
        self.validateParams()
        self.setUpChild()
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        '''
        Climb cutting ?
        '''
        file_text = self.addDebug(inspect.currentframe())
        self.setUpChild()
        file_text += self.child_features.values()[0].getGCode(sequence)
        return file_text

    def moveToStart(self):
        file_text = self.addDebug(inspect.currentframe())
        file_text += self.child_features.values()[0].moveToStart()
        return file_text

    def returnToHome(self):
        file_text = self.addDebug(inspect.currentframe())
        file_text += self.child_features.values()[0].returnToHome()
        return file_text

    def setUpChild(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        bit_diameter = basic_params['bit_diameter']

        # RectangularGroove
        child = self.child_features.values()[0]
        child.option_queries[SideXQuery].setValue(side_x - bit_diameter)
        child.option_queries[SideYQuery].setValue(side_y - bit_diameter)
        child.self_managed_depth = False

    def getParams(self):
        basic_params = self.getBasicParams()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        return (basic_params, cut_depth, side_x, side_y, refX, refY)

    def validateParams(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        bit_diameter = basic_params['bit_diameter']
        if side_x < bit_diameter:
            raise ValueError('Side X is smaller than 2x bit diameter')
        if side_y < bit_diameter:
            raise ValueError('Side Y is smaller than 2x bit diameter')

    def _drawXYentities(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_x = side_x / 2
        half_side_y = side_y / 2
        bit_diameter = basic_params['bit_diameter']
        if len(self.entities['XY']) == 0:
            self.entities['XY'].append(RoundedRectangle(self.view_space).setAll(
                (refX - half_side_x, refY - half_side_y, refX + half_side_x, refY + half_side_y, bit_diameter),
                options
            ).draw())
            self.entities['XY'].append(Rectangle(self.view_space).setAll(
                (refX - half_side_x + bit_diameter, refY - half_side_y + bit_diameter, refX + half_side_x - bit_diameter, refY + half_side_y - bit_diameter),
                options
            ).draw())
        else:
            self.entities['XY'][0].setAll(
                (refX - half_side_x, refY - half_side_y, refX + half_side_x, refY + half_side_y, bit_diameter),
                options
            ).draw()
            self.entities['XY'][1].setAll(
                (refX - half_side_x + bit_diameter, refY - half_side_y + bit_diameter, refX + half_side_x - bit_diameter, refY + half_side_y - bit_diameter),
                options
            ).draw()

    def _drawYZentities(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_y = side_y / 2
        stock_height = basic_params['stock_height']
        bit_diameter = basic_params['bit_diameter']
        if len(self.entities['YZ']) == 0:
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - half_side_y, stock_height - cut_depth, refY + half_side_y, stock_height),
                options
            ).draw())
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - half_side_y + bit_diameter, stock_height - cut_depth, refY + half_side_y - bit_diameter, stock_height),
                options
            ).draw())
        else:
            self.entities['YZ'][0].setAll(
                (refY - half_side_y, stock_height - cut_depth, refY + half_side_y, stock_height),
                options
            ).draw()
            self.entities['YZ'][1].setAll(
                (refY - half_side_y + bit_diameter, stock_height - cut_depth, refY + half_side_y - bit_diameter, stock_height),
                options
            ).draw()

    def _drawXZentities(self):
        basic_params, cut_depth, side_x, side_y, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        half_side_x = side_x / 2
        stock_height = basic_params['stock_height']
        bit_diameter = basic_params['bit_diameter']
        if len(self.entities['XZ']) == 0:
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - half_side_x, stock_height - cut_depth, refX + half_side_x, stock_height),
                options
            ).draw())
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - half_side_x + bit_diameter, stock_height - cut_depth, refX + half_side_x - bit_diameter, stock_height),
                options
            ).draw())
        else:
            self.entities['XZ'][0].setAll(
                (refX - half_side_x, stock_height - cut_depth, refX + half_side_x, stock_height),
                options
            ).draw()
            self.entities['XZ'][1].setAll(
                (refX - half_side_x + bit_diameter, stock_height - cut_depth, refX + half_side_x - bit_diameter, stock_height),
                options
            ).draw()
