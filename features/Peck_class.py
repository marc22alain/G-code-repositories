from GeometricFeature_class import GeometricFeature
from utilities import Glib as G
from option_queries import *
import inspect
from drawn_entities import Circle, Rectangle


class Peck(GeometricFeature):
    '''
    This feature does not require composition with DepthSteppingFeature.
    '''
    name = 'Peck'
    user_selectable = True
    option_query_classes = [
        CutDepthQuery
    ]

    child_feature_classes = []

    def getGCode(self):
        file_text = self.addDebug(inspect.currentframe())
        basic_params, cut_depth, refX, refY = self.getParams()
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(basic_params['safe_z'])
        file_text += self.moveToReference()
        file_text += self.addDebug(inspect.currentframe())
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(basic_params['stock_height'])
        file_text += self.machine.setMode('INCR')
        file_text += G.G1_Z(- cut_depth)
        file_text += G.set_dwell(0.5)
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(basic_params['safe_z'])
        file_text += self.returnFromReference()
        return file_text

    def moveToStart(self):
        return ''

    def returnToHome(self):
        return ''

    def getParams(self):
        basic_params = self.getBasicParams()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        return (basic_params, cut_depth, refX, refY)

    def _drawXYentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        basic_params, cut_depth, refX, refY = self.getParams()
        radius = basic_params['bit_diameter'] / 2
        if len(self.entities['XY']) == 0:
            self.entities['XY'].append(Circle(self.view_space).setAllByCenterRadius((refX, refY, radius), options).draw())
        else:
            self.entities['XY'][0].setAllByCenterRadius((refX, refY, radius), options).draw()

    def _drawYZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        basic_params, cut_depth, refX, refY = self.getParams()
        radius = basic_params['bit_diameter'] / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['YZ']) == 0:
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - radius, stock_height - cut_depth, refY + radius, stock_height),
                options
            ).draw())
        else:
            self.entities['YZ'][0].setAll(
                (refY - radius, stock_height - cut_depth, refY + radius, stock_height),
                options
            ).draw()

    def _drawXZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        basic_params, cut_depth, refX, refY = self.getParams()
        radius = basic_params['bit_diameter'] / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['XZ']) == 0:
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - radius, stock_height - cut_depth, refX + radius, stock_height),
                options
            ).draw())
        else:
            self.entities['XZ'][0].setAll(
                (refX - radius, stock_height - cut_depth, refX + radius, stock_height),
                options
            ).draw()
