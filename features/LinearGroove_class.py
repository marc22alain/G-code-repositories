from DepthSteppingFeature_class import DepthSteppingFeature
from DepthStepper_class import DepthStepper
from utilities import Glib as G
from option_queries import *
from drawn_features import RoundedRectangleDrawing


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
        params = self.getParams()
        delta_X = params['delta_X']
        delta_Y = params['delta_Y']
        file_text = self.machine.setMode('INCR')
        if self.at_start:
            file_text += G.G1_XY((delta_X, delta_Y))
        else:
            file_text += G.G1_XY((- delta_X, - delta_Y))
        self.at_start = not self.at_start
        return file_text

    def moveToStart(self):
        self.at_start = True
        # for starting point reference point
        file_text = ''
        return file_text

    def returnToHome(self):
        # for starting point reference point
        params = self.getParams()
        delta_X = params['delta_X']
        delta_Y = params['delta_Y']
        file_text = ''
        if not self.at_start:
            file_text = self.machine.setMode('INCR')
            file_text += G.G0_XY((- delta_X, - delta_Y))
            self.at_start = True
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'refX': self.option_queries[ReferenceXQuery].getValue(),
            'refY': self.option_queries[ReferenceYQuery].getValue(),
            'delta_X': self.option_queries[DeltaXQuery].getValue(),
            'delta_Y': self.option_queries[DeltaYQuery].getValue()
        })
        return basic_params

    def makeDrawingClass(self):
        print 'LinearGroove makeDrawingClass: %s' % (self.__repr__())
        class Anon(RoundedRectangleDrawing):
            params = self.getParams()
            # options = self.getOptions()
            observable = self
            view_space = self.view_space
        return Anon
