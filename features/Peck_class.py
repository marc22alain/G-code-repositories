from GeometricFeature_class import GeometricFeature
from utilities import Glib as G
from option_queries import *
import inspect
from drawn_entities import Circle


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
        basic_params, cut_depth = self.getParams()
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
        return (basic_params, cut_depth)

    def drawGeometry(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        radius = self.getBasicParams()['bit_diameter'] / 2
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        if len(self.entities) == 0:
            self.entities.append(Circle(self.view_space).setAllByCenterRadius((refX, refY, radius), options).draw())
        else:
            self.entities[0].setAllByCenterRadius((refX, refY, radius), options).draw()
