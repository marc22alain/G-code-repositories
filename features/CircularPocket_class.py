from DepthSteppingFeature_class import DepthSteppingFeature
from ODCircularGroove_class import ODCircularGroove
from option_queries import *
from drawn_entities import Circle, Rectangle
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
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        current_od = basic_params['bit_diameter']
        od_feature = self.child_features[ODCircularGroove]
        while current_od < diameter:
            # increase current_od
            starting_od = current_od
            current_od = min(current_od + (2 * (basic_params['bit_diameter'] - self.getOverlap())), diameter)
            file_text += self.machine.setMode('INCR')
            file_text += G.G1_XY((- (current_od - starting_od) / 2, 0))
            self.setUpODcircularGroove(current_od)
            file_text += od_feature.getGCode()
            file_text += self.addDebug(inspect.currentframe())
        if sequence not in ['last', 'only']:
            # returns to center of pocket
            file_text += od_feature.returnToHome()
        return file_text


    def moveToStart(self):
        return ''

    def returnToHome(self):
        '''
        Called after the last depth step in the pocket has been cut.
        '''
        od_feature = self.child_features[ODCircularGroove]
        file_text = self.addDebug(inspect.currentframe())
        file_text += od_feature.returnToHome()
        return file_text

    def setUpODcircularGroove(self, od):
        circ_groove_child = self.child_features[ODCircularGroove]
        circ_groove_child.option_queries[PathDiameterQuery].setValue(od)
        circ_groove_child.self_managed_depth = False


    def getParams(self):
        basic_params = self.getBasicParams()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        diameter = self.option_queries[PathDiameterQuery].getValue()
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        return (basic_params, cut_depth, diameter, refX, refY)

    def getOverlap(self):
        '''
        Returns a figure that determines the overlap between adjacent cuts that
        form the pocket.
        TBD, but probably based on a constant to begin with.
        Unit is mm of course.
        '''
        return 0.5

    def _drawXYentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        radius = diameter / 2
        if len(self.entities['XY']) == 0:
            self.entities['XY'].append(Circle(self.view_space).setAllByCenterRadius((refX, refY, radius), options).draw())
        else:
            self.entities['XY'][0].setAllByCenterRadius((refX, refY, radius), options).draw()

    def _drawYZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        radius = diameter / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['YZ']) == 0:
            self.entities['YZ'].append(Rectangle(self.view_space).setAll(
                (refY - radius, stock_height - cut_depth, refY + radius, stock_height),
                options
            ).draw())
        else:
            self.entities['YZ'][0].setAll(
                (refY - radius, stock_height - cut_depth, refY + radius, stock_height),
                options
            ).draw()

    def _drawXZentities(self):
        options = {"tag":"geometry","outline":"yellow","fill":None}
        basic_params, cut_depth, diameter, refX, refY = self.getParams()
        radius = diameter / 2
        stock_height = basic_params['stock_height']
        if len(self.entities['XZ']) == 0:
            self.entities['XZ'].append(Rectangle(self.view_space).setAll(
                (refX - radius, stock_height - cut_depth, refX + radius, stock_height),
                options
            ).draw())
        else:
            self.entities['XZ'][0].setAll(
                (refX - radius, stock_height - cut_depth, refX + radius, stock_height),
                options
            ).draw()
