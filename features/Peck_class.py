import inspect
from geometric_feature_class import GeometricFeature
from drawn_features import HoleDrawing
from utilities import addDebugFrame, log, Glib as G
from option_queries import CutDepthQuery, ReferenceXQuery, ReferenceYQuery


class Peck(GeometricFeature):
    """The Peck is a straight drill down to specified depth.
    This feature does not require the features of the DepthSteppingFeature."""
    name = 'Peck'
    user_selectable = True
    option_query_classes = [
        CutDepthQuery
    ]

    child_feature_classes = []

    def getGCode(self):
        file_text = addDebugFrame(inspect.currentframe())
        params = self.getParams()
        file_text += self.machine.moveToSafeZ()
        file_text += self.moveToReference()
        file_text += addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(params['stock_height'])
        file_text += self.machine.setMode('INCR')
        file_text += G.G1_Z(- params['cut_depth'])
        file_text += G.set_dwell(0.5)
        file_text += self.machine.moveToSafeZ()
        file_text += self.returnFromReference()
        return file_text

    def moveToStart(self):
        """The reference point is the Peck operation's center, and requires no movement."""
        return ''

    def returnToHome(self):
        """The reference point is the Peck operation's center, and requires no movement."""
        return ''

    def getParams(self):
        basic_params = self.getBasicParams()
        diameter = basic_params['bit_diameter']
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'diameter': diameter
        })
        return basic_params

    def _makeDrawingClass(self):
        log('Peck makeDrawingClass')
        class Anon(HoleDrawing):
            params = self.getParams()
            observable = self
            view_space = self.view_space
        return Anon
