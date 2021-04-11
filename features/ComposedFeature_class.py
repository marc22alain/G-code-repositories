from geometric_feature_class import GeometricFeature
from feature_manager import AbstractFeatureManager

class ComposedFeature(GeometricFeature, AbstractFeatureManager):
    """The ComposedFeature provides the functionality the composition of features,
    but offers no methods for locating/distributing those features.
    Each child feature must use their reference queries to locate
    themselves with respect to the ComposedFeatures reference point.
    Simple.
    Sub-classes may provide additional methods for locating/distributing features."""

    is_composed = True

    def __init__(self, feature_manager, view_space):
        AbstractFeatureManager.__init__(self)
        GeometricFeature.__init__(self, feature_manager, view_space)

    def deleteChild(self, feature_instance):
        """
        Delete the feature instance.
        """
        self.features.pop(feature_instance)

    def changeViewPlane(self):
        """Overrides GeometricFeature."""
        self.removeObservers('remove')
        for feature in self.features:
            feature.removeObservers('remove')
        self.drawGeometry()
