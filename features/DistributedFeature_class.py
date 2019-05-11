from ComposedFeature_class import ComposedFeature
import abc

class DistributedFeature(ComposedFeature):

    def getGCode(self):
        file_text = self.moveToReference()
        file_text += self.distributeChildFeature()
        file_text += self.returnFromReference()
        return file_text

    @abc.abstractmethod
    def distributeChildFeature(self):
        pass
