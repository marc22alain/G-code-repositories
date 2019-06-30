from geometric_feature_class import GeometricFeature
from feature_manager import AbstractFeatureManager
import abc

class ComposedFeature(GeometricFeature, AbstractFeatureManager):

    is_composed = True

    def __init__(self, feature_manager, view_space):
        AbstractFeatureManager.__init__(self)
        GeometricFeature.__init__(self, feature_manager, view_space)

    def deleteChild(self, feature_instance):
        '''
        Delete the feature instance.
        TODO: maybe move this to DistributedFeature
        '''
        self.features.pop(feature_instance)

    def changeViewPlane(self):
        self.removeObservers('remove')
        for feature in self.features:
            feature.removeObservers('remove')
        self.drawGeometry()
