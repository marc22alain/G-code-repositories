from GeometricFeature_class import GeometricFeature
import abc

class ComposedFeature(GeometricFeature):

    @abc.abstractmethod
    def updateFeatures(self):
        pass

    @abc.abstractmethod
    def deleteFeature(self):
        pass
