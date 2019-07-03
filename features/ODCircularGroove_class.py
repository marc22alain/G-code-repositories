import inspect
from DepthSteppingFeature_class import DepthSteppingFeature
from CircularGroove_class import CircularGroove
from option_queries import PathDiameterQuery, CutDepthQuery, ReferenceXQuery, ReferenceYQuery
from drawn_features import CircularGrooveDrawing
from utilities import addDebug


class ODCircularGroove(DepthSteppingFeature):
    """The ODCircularGroove is a single cut of a full circle. The feature's
    reference point is the center of the circle, and the path reference is the
    OD of the cut."""
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
        return DepthSteppingFeature.getGCode(self, sequence)

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'diameter': self.option_queries[PathDiameterQuery].getValue()
        })
        return basic_params

    def _getInstructions(self, sequence):
        file_text = addDebug(inspect.currentframe())
        file_text += self.child_features.values()[0].getGCode(sequence)
        return file_text

    def moveToStart(self):
        file_text = addDebug(inspect.currentframe())
        file_text += self.child_features.values()[0].moveToStart()
        return file_text

    def returnToHome(self):
        file_text = addDebug(inspect.currentframe())
        file_text += self.child_features.values()[0].returnToHome()
        return file_text

    def setUpChild(self):
        """Set up to delegate to CircularGroove."""
        params = self.getParams()
        center_diameter = params['diameter'] - params['bit_diameter']

        child = self.child_features.values()[0]
        child.option_queries[PathDiameterQuery].setValue(center_diameter)
        child.self_managed_depth = False

    def _makeDrawingClass(self):
        class Anon(CircularGrooveDrawing):
            params = self.getParams()
            observable = self
            view_space = self.view_space
            path_reference = 'od'
        return Anon
