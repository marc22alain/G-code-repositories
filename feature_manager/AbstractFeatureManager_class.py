import abc
from ui import OptionQueryDialog
from option_queries import GeometricFeatureQuery
from utilities import log

class AbstractFeatureManager:
    """The meta class for all feature managers."""
    __metaclass__ = abc.ABCMeta

    app = None

    def __init__(self):
        log('AbstractFeatureManager ran __init__')
        self.features = []
        self.root = False   # default value; set to True for root by app


    def addChild(self, feature_class = None):
        """Add child, by argument or inferred from option_query."""
        # for ComposedFeature
        if feature_class is None:
            query = self.option_queries[GeometricFeatureQuery]
            query.updateValue()
            feature_class = query.getValue()
        feature = feature_class(self, self.view_space)
        log(feature)
        self.features.append(feature)
        # passed in as callback
        def addFunction():
            log('running FeatureManager OK function: %s' % (self.__repr__()))
            if hasattr(feature, 'is_composed'):
                feature.addChild()
            # makes the initial call to makeDrawingClass()
            feature.didUpdateQueries()
            # root FeatureManager has special responsibilities
            if self.root:
                feature.drawGeometry()
                self.app.feature_list.insertFeature(feature)
        # passed in as callback
        def cancelFunction():
            self.features.pop()
            log('running CANCEL function')
        if self.app:
            OptionQueryDialog(
                self.app,
                feature.getOptionQueries(),
                feature.name,
                addFunction,
                cancelFunction
            )

    @abc.abstractmethod
    def deleteChild(self, feature_instance):
        """Delete the feature instance."""
        pass
