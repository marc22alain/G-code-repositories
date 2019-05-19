from DepthSteppingFeature_class import DepthSteppingFeature
from RectangularGroove_class import RectangularGroove
from utilities import Glib as G
from option_queries import *
import inspect


class ODRectangularGroove(DepthSteppingFeature):
    '''
    Reference position is center.
    The queries determine the path of the center of the cutter.
    '''
    name = 'ODRectangular Groove'
    user_selectable = True
    option_query_classes = [
        SideXQuery,
        SideYQuery,
    ]

    child_feature_classes = [
        RectangularGroove
    ]

    def getGCode(self, sequence = None):
        self.setUpChild()
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        '''
        Climb cutting ?
        '''
        file_text = self.addDebug(inspect.currentframe())
        self.setUpChild()
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
        side_x, side_y, basic_params = self.getParams()
        bit_diameter = basic_params['bit_diameter']

        # RectangularGroove
        child = self.child_features.values()[0]
        child.option_queries[SideXQuery].setValue(side_x - bit_diameter)
        child.option_queries[SideYQuery].setValue(side_y - bit_diameter)
        child.self_managed_depth = False

    def getParams(self):
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        return (side_x, side_y, self.getBasicParams())

