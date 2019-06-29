from DepthSteppingFeature_class import DepthSteppingFeature
from RectangularGroove_class import RectangularGroove
from utilities import Glib as G
from option_queries import *
from drawn_features import RectangularGrooveDrawing
import inspect


class ODRectangularGroove(DepthSteppingFeature):
    '''
    Reference position is lower-left, and path reference is outer diameter.
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
        self.validateParams()
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
        params = self.getParams()
        bit_diameter = params['bit_diameter']

        # RectangularGroove
        child = self.child_features.values()[0]
        child.option_queries[SideXQuery].setValue(params['side_X'] - bit_diameter)
        child.option_queries[SideYQuery].setValue(params['side_Y'] - bit_diameter)
        child.self_managed_depth = False

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'refX': self.option_queries[ReferenceXQuery].getValue(),
            'refY': self.option_queries[ReferenceYQuery].getValue(),
            'side_X': self.option_queries[SideXQuery].getValue(),
            'side_Y': self.option_queries[SideYQuery].getValue(),
        })
        return basic_params

    def validateParams(self):
        params = self.getParams()
        bit_diameter = params['bit_diameter']
        if params['side_X'] < bit_diameter:
            raise ValueError('Side X is smaller than bit diameter')
        if params['side_Y'] < bit_diameter:
            raise ValueError('Side Y is smaller than bit diameter')

    def _makeDrawingClass(self):
        class Anon(RectangularGrooveDrawing):
            params = self.getParams()
            # options = self.getOptions()
            observable = self
            view_space = self.view_space
            reference_point = 'lower-left'
            path_reference = 'od'
        return Anon
