from DepthSteppingFeature_class import DepthSteppingFeature
from CircularGroove_class import CircularGroove
from option_queries import *
from drawn_features import ODCircularGrooveDrawing
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

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'refX': self.option_queries[ReferenceXQuery].getValue(),
            'refY': self.option_queries[ReferenceYQuery].getValue(),
            'diameter': self.option_queries[PathDiameterQuery].getValue()
        })
        return basic_params

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
        params = self.getParams()
        center_diameter = params['diameter'] - params['bit_diameter']

        child = self.child_features.values()[0]
        child.option_queries[PathDiameterQuery].setValue(center_diameter)
        child.self_managed_depth = False

    def makeDrawingClass(self):
        class Anon(ODCircularGrooveDrawing):
            params = self.getParams()
            observable = self
            view_space = self.view_space
        return Anon
