from GeometricFeature_class import GeometricFeature
from feature_manager import AbstractFeatureManager
import abc

class ComposedFeature(GeometricFeature, AbstractFeatureManager):

    def deleteChild(self, feature_instance):
        '''
        Delete the feature instance.
        TODO: maybe move this to DistributedFeature
        '''
        self.child_features = { k:v for k,v in self.child_features.iteritems() if v != feature_instance }
