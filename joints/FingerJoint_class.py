from features import LinearGroove, LinearDistribution
import math
from option_queries import *
from workpieces import SimpleWorkpiece

class FingerJoint(QueryManager):
    """ The designer will assume that the desired result is a rectangular frame.
    Two pieces will hold a pair of A parts,
    other two pieces will hold the pair of B parts.
    The A part has the lesser number of cuts, so has fingers on the workpiece
    edge. These fingers will be >= half the bit width.

    Stock dimensions, when normally lying on spoil-board:
    - height = Z
    - width = Y
    - length = X
    Therefore:
    - height is the board thickness, relating to the length of the grooves
    - width is the board width, along which the grooves are distributed

    A future feature might be to provide a user option to define the edge finger
    width. """

    name = 'Finger Joint Designer'
    option_query_classes = [
        StockHeightQuery,
        StockWidthQuery
    ]

    def __init__(self, feature_manager):
        QueryManager.__init__(self)
        self.machine = feature_manager.machine

        self.a_workpiece = SimpleWorkpiece(None, None)
        self.a_workpiece.getOptionQueries()
        self.b_workpiece = SimpleWorkpiece(None, None)
        self.b_workpiece.getOptionQueries()

        self.a_cuts = LinearDistribution(None, None)
        self.a_cuts.setWorkpiece(self.a_workpiece)
        self.a_cuts.setMachine(self.machine)
        self.a_cuts.getOptionQueries()

        self.b_cuts = LinearDistribution(None, None)
        self.b_cuts.setWorkpiece(self.b_workpiece)
        self.b_cuts.setMachine(self.machine)
        self.b_cuts.getOptionQueries()

    def getFeatures(self):
        """ Hoping that I don't have to use this ..."""
        if self.b_cuts is None or self.a_cuts is None:
            raise ValueError('leaf features are not yet defined')
        return {
            LinearDistribution: [ self.a_cuts, self.b_cuts ]
        }

    def getAllStuff(self):
        return {
            'a_workpiece': self.a_workpiece,
            'b_workpiece': self.b_workpiece,
            'a_cuts': self.a_cuts,
            'b_cuts': self.b_cuts,
        }

    def cancelFunction(self):
        print 'cancelFunction passed'

    def postQueryUpdateHook(self):
        """ Clearly something to define in a parent/abstract class. """
        self.designJoint()

    def designJoint(self):
        """
        . negative space is the groove cut at bit's width
        . the spacing creates the tenons that fill the negative space
        . there is a spacing adjustment factor that mutates the tenons to fit the spaces
        . there is also an algorithm to center the grooves in A part, that takes into account the narrowest tenons of B part
            .. this will pick either an odd or even number of spaces, since the spacing will be independently determined by the bit width
        """
        num_a_grooves = self.getNumGrooves()

    def getNumGrooves(self):
        """ For the A piece to always have tabs on both sides, when A piece has
        n grooves, B piece has n-1 grooves and 2 tab cuts.
        """
        workpiece_width = self.option_queries[StockWidthQuery].getValue()
        bit_diameter = self.machine.option_queries[BitDiameterQuery].getValue()

        # tabs will each be: 1/2 groove width <= tab width < 1 1/2 groove width
        ratio = workpiece_width / bit_diameter
        floored = math.floor(ratio)
        num_grooves = (floored - 2) if (floored % 2 > 0) else (floored - 1)
        # num_grooves is always odd
        num_b_grooves = (num_grooves - 1) / 2

        # float math goes wonky
        tab_width = round((workpiece_width - (num_grooves * bit_diameter)) / 2, 5)

        return {
            'num_grooves': num_grooves,
            'num_a_grooves': num_b_grooves + 1,
            'num_b_grooves': num_b_grooves,
            'tab_width': tab_width
        }
