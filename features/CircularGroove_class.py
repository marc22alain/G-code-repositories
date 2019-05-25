from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import Glib as G
from option_queries import *
from drawn_entities import Circle, Rectangle


class CircularGroove(DepthSteppingFeature):
    name = 'Circular Groove'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery
    ]

    child_feature_classes = []

    def getGCode(self, sequence = None):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        file_text = self.machine.setMode('INCR')
        file_text += G.G2XY((0,0),(diameter / 2, 0))
        return file_text

    def moveToStart(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- diameter / 2, 0))
        return file_text

    def returnToHome(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((diameter / 2, 0))
        return file_text

    def _drawXYentities(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        radius = diameter / 2
        bit_radius = basic_params['bit_diameter'] / 2
        if len(self.entities['XY']) == 0:
            self.entities['XY'].append(Circle(self.view_space).setAllByCenterRadius((refX, refY, radius - bit_radius), options).draw())
            self.entities['XY'].append(Circle(self.view_space).setAllByCenterRadius((refX, refY, radius + bit_radius), options).draw())
        else:
            self.entities['XY'][0].setAllByCenterRadius((refX, refY, radius - bit_radius), options).draw()
            self.entities['XY'][1].setAllByCenterRadius((refX, refY, radius + bit_radius), options).draw()


    def _drawYZentities(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        radius = diameter / 2
        bit_radius = basic_params['bit_diameter'] / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['YZ']) == 0:
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - radius - bit_radius, stock_height - cut_depth, refY + radius + bit_radius, stock_height),
                options
            ).draw())
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - radius + bit_radius, stock_height - cut_depth, refY + radius - bit_radius, stock_height),
                options
            ).draw())
        else:
            self.entities['YZ'][0].setAll(
                (refY - radius - bit_radius, stock_height - cut_depth, refY + radius + bit_radius, stock_height),
                options
            ).draw()
            self.entities['YZ'][1].setAll(
                (refY - radius + bit_radius, stock_height - cut_depth, refY + radius - bit_radius, stock_height),
                options
            ).draw()

    def _drawXZentities(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        radius = diameter / 2
        bit_radius = basic_params['bit_diameter'] / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['XZ']) == 0:
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - radius - bit_radius, stock_height - cut_depth, refX + radius + bit_radius, stock_height),
                options
            ).draw())
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - radius + bit_radius, stock_height - cut_depth, refX + radius - bit_radius, stock_height),
                options
            ).draw())
        else:
            self.entities['XZ'][0].setAll(
                (refX - radius - bit_radius, stock_height - cut_depth, refX + radius + bit_radius, stock_height),
                options
            ).draw()
            self.entities['XZ'][1].setAll(
                (refX - radius + bit_radius, stock_height - cut_depth, refX + radius - bit_radius, stock_height),
                options
            ).draw()

    def getParams(self):
        basic_params = self.getBasicParams()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        diameter = self.option_queries[PathDiameterQuery].getValue()
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        return (basic_params, cut_depth, diameter, refX, refY)
