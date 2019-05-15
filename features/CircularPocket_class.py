from DepthSteppingFeature_class import DepthSteppingFeature
from ODCircularGroove_class import ODCircularGroove
from option_queries import *
from utilities import Glib as G
import inspect


class CircularPocket(DepthSteppingFeature):
    name = 'Circular Pocket'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery
    ]

    child_feature_classes = [
        ODCircularGroove,
    ]

    def getGCode(self, sequence = None):
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        file_text = self.addDebug(inspect.currentframe())
        diameter, basic_params = self.getParams()
        current_od = basic_params['bit_diameter']
        od_feature = self.child_features[ODCircularGroove]
        while current_od < diameter:
            # increase current_od
            starting_od = current_od
            current_od = min(current_od + (2 * (basic_params['bit_diameter'] - self.getOverlap())), diameter)
            self.setUpODcircularGroove(current_od)
            file_text += G.set_INCR_mode()
            file_text += G.G1_XY((- (current_od - starting_od) / 2, 0))
            file_text += od_feature.getGCode()
            file_text += self.addDebug(inspect.currentframe())
        if sequence not in ['last', 'only']:
            file_text += od_feature.returnToHome()
        return file_text


    def moveToStart(self):
        return ''

    def returnToHome(self):
        od_feature = self.child_features[ODCircularGroove]
        file_text = self.addDebug(inspect.currentframe())
        file_text += od_feature.returnToHome()
        return file_text

    def setUpODcircularGroove(self, od):
        circ_groove_child = self.child_features[ODCircularGroove]
        circ_groove_child.option_queries[PathDiameterQuery].setValue(od)
        circ_groove_child.self_managed_depth = False

    def getParams(self):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        return (diameter, self.getBasicParams())

    def getOverlap(self):
        '''
        Returns a figure that determines the overlap between adjacent cuts that
        form the pocket.
        TBD, but probably based on a constant to begin with.
        Unit is mm of course.
        '''
        return 0.5
