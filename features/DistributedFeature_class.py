import abc
from ComposedFeature_class import ComposedFeature
from utilities import log, Glib as G


class DistributedFeature(ComposedFeature):
    """Defines the interface for a feature that encapsulates a feature
    distribution function."""

    def getGCode(self):
        log('DistributedFeature getGCode: %s' % (self.__repr__()))
        params = self.getParams()
        file_text = self.machine.setMode('ABS')
        file_text += G.G0_Z(params['safe_z'])
        file_text += self.moveToReference()
        file_text += self.distributeChildFeature()
        file_text += self.returnFromReference()
        return file_text

    @abc.abstractmethod
    def distributeChildFeature(self):
        """Performs the operations to instantiate and distribute features, then
        gets them to produce their own gcode."""
        pass
