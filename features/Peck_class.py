from GeometricFeature_class import GeometricFeature
from drawn_features import HoleDrawing
from utilities import Glib as G
from option_queries import *
import inspect
from utilities import log


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
        params = self.getParams()
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(params['safe_z'])
        file_text += self.moveToReference()
        file_text += self.addDebug(inspect.currentframe())
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(params['stock_height'])
        file_text += self.machine.setMode('INCR')
        file_text += G.G1_Z(- params['cut_depth'])
        file_text += G.set_dwell(0.5)
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(params['safe_z'])
        file_text += self.returnFromReference()
        return file_text

    def moveToStart(self):
        return ''

    def returnToHome(self):
        return ''

    def getParams(self):
        basic_params = self.getBasicParams()
        diameter = basic_params['bit_diameter']
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'refX': self.option_queries[ReferenceXQuery].getValue(),
            'refY': self.option_queries[ReferenceYQuery].getValue(),
            'diameter': diameter
        })
        return basic_params

    def makeDrawingClass(self):
        log('Peck makeDrawingClass')
        class Anon(HoleDrawing):
            params = self.getParams()
            # options = self.getOptions()
            observable = self
            view_space = self.view_space
        self.drawing_class = Anon
        return Anon
