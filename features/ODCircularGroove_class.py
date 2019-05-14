from DepthSteppingFeature_class import DepthSteppingFeature
from CircularGroove_class import CircularGroove
from option_queries import *


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
        diameter = self.option_queries[PathDiameterQuery].getValue()
        return (diameter, self.getBasicParams())

    def _getInstructions(self, sequence):
        return self.child_features.values()[0].getGCode(sequence)

    def moveToStart(self):
        # redundant ?
        self.setUpChild()
        return self.child_features.values()[0].moveToStart()

    def returnToHome(self):
        # redundant ?
        self.setUpChild()
        return self.child_features.values()[0].returnToHome()

    def setUpChild(self):
        diameter, basic_params = self.getParams()
        center_diameter = diameter - basic_params['bit_diameter']

        child = self.child_features.values()[0]
        child.option_queries[PathDiameterQuery].setValue(center_diameter)
        child.self_managed_depth = False
