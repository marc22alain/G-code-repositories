from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import Glib as G
from option_queries import *
from drawn_entities import Circle


class CircularGroove(DepthSteppingFeature):
    name = 'Circular Groove'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery
    ]

    child_feature_classes = []

    def getGCode(self, sequence = None):
        # manage height - optionally -
        if self.self_managed_depth:
            return self.getManagedDepthInstructions()
        else:
            return self._getInstructions(sequence)

    def _getInstructions(self, sequence):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G2XY((0,0),(diameter / 2, 0))
        return file_text

    def moveToStart(self):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- diameter / 2, 0))
        return file_text

    def returnToHome(self):
        diameter = self.option_queries[PathDiameterQuery].getValue()
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((diameter / 2, 0))
        return file_text

    def getDrawnGeometry(self):
        entities = []
        options = {"tag":"geometry","outline":"yellow","fill":None}
        diameter = self.option_queries[PathDiameterQuery].getValue()
        bit_radius = self.getBasicParams()['bit_diameter'] / 2
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()

        entities.append(Circle().setAllByCenterRadius((refX, refY, diameter - bit_radius), options))
        entities.append(Circle().setAllByCenterRadius((refX, refY, diameter + bit_radius), options))

        return {"entities":entities,
                "extents": {"width": refX * 2, "height": refY * 2, "center": (refX, refY)}}
