from DepthSteppingFeature_class import DepthSteppingFeature
from ODRectangularGroove_class import ODRectangularGroove
from option_queries import *
from utilities import Glib as G
import inspect


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
        side_x, side_y, basic_params = self.getParams()
        self.setUpODRectangularGroove(side_x, side_y)
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        current_side_x, current_side_y, basic_params = self.getParams()
        bit_diameter = basic_params['bit_diameter']
        step_increment = bit_diameter - self.getOverlap()
        child = self.child_features[ODRectangularGroove]
        file_text = self.addDebug(inspect.currentframe())
        # do the full size outline first
        file_text += child.getGCode()
        while current_side_x >= (2 * bit_diameter) and current_side_y >= (2 * bit_diameter):
            starting_side_x = current_side_x
            starting_side_y = current_side_y
            current_side_x = max(current_side_x - (2 * step_increment), 2 * step_increment)
            current_side_y = max(current_side_y - (2 * step_increment), 2 * step_increment)
            file_text += self.machine.setMode('INCR')
            file_text += G.G1_XY(((starting_side_x - current_side_x) / 2, (starting_side_y - current_side_y) / 2))
            self.setUpODRectangularGroove(current_side_x, current_side_y)
            file_text += child.getGCode()
            file_text += self.addDebug(inspect.currentframe())
        if sequence not in ['last', 'only']:
            # returns to center of pocket, for
            file_text += self.returnToHome()
            file_text += self.moveToStart()
        return file_text


    def moveToStart(self):
        file_text = self.addDebug(inspect.currentframe())
        side_x, side_y, basic_params = self.getParams()
        self.setUpODRectangularGroove(side_x, side_y)
        file_text += self.child_features[ODRectangularGroove].moveToStart()
        return file_text

    def returnToHome(self):
        '''
        Called on the conclusion of each depth step, except for the last.
        '''
        file_text = self.addDebug(inspect.currentframe())
        file_text += self.child_features[ODRectangularGroove].returnToHome()
        return file_text

    def setUpODRectangularGroove(self, side_x, side_y):
        child = self.child_features[ODRectangularGroove]
        child.option_queries[SideXQuery].setValue(side_x)
        child.option_queries[SideYQuery].setValue(side_y)
        child.self_managed_depth = False
        # Leaky abstraction:
        child.setUpChild()

    def getParams(self):
        side_x = self.option_queries[SideXQuery].getValue()
        side_y = self.option_queries[SideYQuery].getValue()
        return (side_x, side_y, self.getBasicParams())

    def getOverlap(self):
        '''
        Returns a figure that determines the overlap between adjacent cuts that
        form the pocket.
        TBD, but probably based on a constant to begin with.
        Unit is mm of course.
        '''
        return 0.5

    def validateParams(self):
        side_x, side_y, basic_params = self.getParams()
        bit_diameter = basic_params['bit_diameter']
        if side_x < bit_diameter:
            raise ValueError('Side X is smaller than 2x bit diameter')
        if side_y < bit_diameter:
            raise ValueError('Side Y is smaller than 2x bit diameter')
