from ComposedFeature_class import ComposedFeature
import abc

class DistributedFeature(ComposedFeature):

    @abc.abstractmethod
    def distributeChildFeature(self):
        pass
