from drawn_features import ComposedFeatureDrawing
from geometric_feature_class import GeometricFeature
from feature_manager import AbstractFeatureManager
from option_queries import GeometricFeatureQuery, ReferenceXQuery, ReferenceYQuery
from utilities import log, Glib as G

class ComposedFeature(GeometricFeature, AbstractFeatureManager):
    """The ComposedFeature provides the functionality the composition of features,
    but offers no methods for locating/distributing those features.
    Each child feature must use their reference queries to locate
    themselves with respect to the ComposedFeatures reference point.
    Simple.
    Sub-classes may provide additional methods for locating/distributing features."""

    name = 'Composed Feature'
    option_query_classes = [
        GeometricFeatureQuery
    ]
    child_feature_classes = []
    is_composed = True

    def __init__(self, feature_manager, view_space):
        AbstractFeatureManager.__init__(self)
        GeometricFeature.__init__(self, feature_manager, view_space)

    def deleteChild(self, feature_instance):
        """
        Delete the feature instance.
        """
        self.features.remove(feature_instance)

    def changeViewPlane(self):
        """Overrides GeometricFeature."""
        self.removeObservers('remove')
        for feature in self.features:
            feature.removeObservers('remove')
        self.drawGeometry()

    def moveToStart(self):
        log('ComposedFeature moveToStart: %s' % (self.__repr__()))
        return ''

    def returnToHome(self):
        log('ComposedFeature moveToStart: %s' % (self.__repr__()))
        return ''

    def getGCode(self):
        log('ComposedFeature getGCode: %s' % (self.__repr__()))
        file_text = self.moveToReference()
        for feature in self.features:
            file_text += feature.getGCode()
        file_text += self.returnFromReference()
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue()
        })
        return basic_params

    def _makeDrawingClass(self):
        log('ComposedFeature makeDrawingClass: %s' % (self.__repr__()))
        drawing_classes = []
        for feature in self.features:
            drawing_classes.append(feature.makeDrawingClass())
        class Anon(ComposedFeatureDrawing):
            params = self.getParams()
            observable = self
            child_object_functions = drawing_classes
            view_space = self.view_space
        return Anon

    def getChildren(self):
        return self.features
