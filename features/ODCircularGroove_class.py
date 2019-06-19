from DepthSteppingFeature_class import DepthSteppingFeature
from CircularGroove_class import CircularGroove
from option_queries import *
from drawn_entities import Circle, Rectangle
import inspect


class ODCircularGroove(DepthSteppingFeature):
    name = 'OD Circular Groove'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery
    ]

    child_feature_classes = [
        CircularGroove
    ]

    def getGCode(self, sequence = None):
        self.setUpChild()
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    # def getParams(self):
    #     diameter = self.option_queries[PathDiameterQuery].getValue()
    #     return (diameter, self.getBasicParams())

    def getParams(self):
        basic_params = self.getBasicParams()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        diameter = self.option_queries[PathDiameterQuery].getValue()
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        return (basic_params, cut_depth, diameter, refX, refY)

    def _getInstructions(self, sequence):
        file_text = self.addDebug(inspect.currentframe())
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
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        center_diameter = diameter - basic_params['bit_diameter']

        child = self.child_features.values()[0]
        child.option_queries[PathDiameterQuery].setValue(center_diameter)
        child.self_managed_depth = False

    def _drawXYentities(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        radius = diameter / 2
        bit_diameter = basic_params['bit_diameter']
        if len(self.entities['XY']) == 0:
            self.entities['XY'].append(Circle(self.view_space).setAllByCenterRadius((refX, refY, radius), options).draw())
            self.entities['XY'].append(Circle(self.view_space).setAllByCenterRadius((refX, refY, radius - bit_diameter), options).draw())
        else:
            self.entities['XY'][0].setAllByCenterRadius((refX, refY, radius), options).draw()
            self.entities['XY'][1].setAllByCenterRadius((refX, refY, radius - bit_diameter), options).draw()

    def _drawYZentities(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        radius = diameter / 2
        bit_diameter = basic_params['bit_diameter']
        stock_height = basic_params['stock_height']
        if len(self.entities['YZ']) == 0:
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - radius, stock_height - cut_depth, refY + radius, stock_height),
                options
            ).draw())
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - radius + bit_diameter, stock_height - cut_depth, refY + radius - bit_diameter, stock_height),
                options
            ).draw())
        else:
            self.entities['YZ'][0].setAll(
                (refY - radius, stock_height - cut_depth, refY + radius, stock_height),
                options
            ).draw()
            self.entities['YZ'][1].setAll(
                (refY - radius + bit_diameter, stock_height - cut_depth, refY + radius - bit_diameter, stock_height),
                options
            ).draw()

    def _drawXZentities(self):
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        options = {"tag":"geometry","outline":"yellow","fill":None}
        radius = diameter / 2
        bit_diameter = basic_params['bit_diameter']
        stock_height = basic_params['stock_height']
        if len(self.entities['XZ']) == 0:
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - radius, stock_height - cut_depth, refX + radius, stock_height),
                options
            ).draw())
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - radius + bit_diameter, stock_height - cut_depth, refX + radius - bit_diameter, stock_height),
                options
            ).draw())
        else:
            self.entities['XZ'][0].setAll(
                (refX - radius, stock_height - cut_depth, refX + radius, stock_height),
                options
            ).draw()
            self.entities['XZ'][1].setAll(
                (refX - radius + bit_diameter, stock_height - cut_depth, refX + radius - bit_diameter, stock_height),
                options
            ).draw()

    def makeDrawingClass(self):
        pass

