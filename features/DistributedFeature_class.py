import abc
from ComposedFeature_class import ComposedFeature


class DistributedFeature(ComposedFeature):
    """Defines the interface for a feature that encapsulates a feature
    distribution function."""

    def getGCode(self):
        file_text = self.moveToReference()
        file_text += self.distributeChildFeature()
        file_text += self.returnFromReference()
        return file_text

    @abc.abstractmethod
    def distributeChildFeature(self):
        """Performs the operations to instantiate and distribute features, then
        gets them to produce their own gcode."""
        pass
