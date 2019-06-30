from DepthSteppingFeature_class import DepthSteppingFeature
from ODRectangularGroove_class import ODRectangularGroove
from option_queries import *
from utilities import Glib as G
from drawn_features import RectangularPocketDrawing
import inspect
from utilities import log


class RectangularPocket(DepthSteppingFeature):
    name = 'Rectangular Pocket'
    user_selectable = True
    option_query_classes = [
        SideXQuery,
        SideYQuery,
    ]

    child_feature_classes = [
        ODRectangularGroove,
    ]

    def getGCode(self, sequence = None):
        self.validateParams()
        params = self.getParams()
        self.setUpODRectangularGroove(params['side_X'], params['side_Y'])
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        params = self.getParams()
        bit_diameter = params['bit_diameter']
        current_side_X = params['side_X']
        current_side_Y = params['side_Y']
        step_increment = bit_diameter - self.getOverlap()
        child = self.child_features[ODRectangularGroove]
        file_text = self.addDebug(inspect.currentframe())
        # do the full size outline first
        file_text += child.getGCode()
        while current_side_X >= (2 * bit_diameter) and current_side_Y >= (2 * bit_diameter):
            starting_side_X = current_side_X
            starting_side_Y = current_side_Y
            current_side_X = max(current_side_X - (2 * step_increment), 2 * step_increment)
            current_side_Y = max(current_side_Y - (2 * step_increment), 2 * step_increment)
            file_text += self.machine.setMode('INCR')
            file_text += G.G1_XY(((starting_side_X - current_side_X) / 2, (starting_side_Y - current_side_Y) / 2))
            self.setUpODRectangularGroove(current_side_X, current_side_Y)
            file_text += child.getGCode()
            file_text += self.addDebug(inspect.currentframe())
        if sequence not in ['last', 'only']:
            # returns to center of pocket, for
            file_text += self.returnToHome()
            file_text += self.moveToStart()
        return file_text

    def moveToStart(self):
        file_text = self.addDebug(inspect.currentframe())
        params = self.getParams()
        self.setUpODRectangularGroove(params['side_X'], params['side_Y'])
        file_text += self.child_features[ODRectangularGroove].moveToStart()
        return file_text

    def returnToHome(self):
        '''
        Called on the conclusion of each depth step, except for the last.
        '''
        file_text = self.addDebug(inspect.currentframe())
        file_text += self.child_features[ODRectangularGroove].returnToHome()
        return file_text

    def setUpODRectangularGroove(self, side_X, side_Y):
        child = self.child_features[ODRectangularGroove]
        child.option_queries[SideXQuery].setValue(side_X)
        child.option_queries[SideYQuery].setValue(side_Y)
        child.self_managed_depth = False
        # Leaky abstraction:
        child.setUpChild()

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'refX': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'side_X': self.option_queries[SideXQuery].getValue(),
            'side_Y': self.option_queries[SideYQuery].getValue(),
        })
        return basic_params

    def getOverlap(self):
        '''
        Returns a figure that determines the overlap between adjacent cuts that
        form the pocket.
        TBD, but probably based on a constant to begin with.
        Unit is mm of course.
        '''
        return 0.5

    def validateParams(self):
        params = self.getParams()
        bit_diameter = params['bit_diameter']
        if params['side_X'] < bit_diameter:
            raise ValueError('Side X is smaller than bit diameter')
        if params['side_Y'] < bit_diameter:
            raise ValueError('Side Y is smaller than bit diameter')

    def _makeDrawingClass(self):
        log('RectangularPocket makeDrawingClass: %s' % (self.__repr__()))
        class Anon(RectangularPocketDrawing):
            params = self.getParams()
            # options = self.getOptions()
            observable = self
            view_space = self.view_space
            reference_point = 'lower-left'
        return Anon
