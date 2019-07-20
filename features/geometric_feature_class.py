#!/usr/bin/env python

""" The GeometricFeature serves as the base Abstract class. """
import abc
import inspect
import pdb
from observeder import Observable
from option_queries import QueryManager, ReferenceXQuery, ReferenceYQuery
from utilities import log, addDebugFrame, Glib as G


class GeometricFeature(Observable, QueryManager):
    """Serve as the base Abstract class."""
    __metaclass__ = abc.ABCMeta

    common_query_classes = [
        ReferenceXQuery,
        ReferenceYQuery
    ]

    option_query_classes = None
    child_feature_classes = None

    def __init__(self, feature_manager, view_space):
        log('GeometricFeature ran __init__')
        Observable.__init__(self)
        self.feature_manager = feature_manager
        self.view_space = view_space
        self.machine = feature_manager.machine
        self.work_piece = feature_manager.work_piece
        QueryManager.__init__(self)
        self.option_queries.update({key: None for key in self.common_query_classes})
        self.child_features = {key: None for key in self.child_feature_classes}
        self.makeChildren()
        self.drawing_class = None

    @abc.abstractmethod
    def getGCode(self):
        """Get g-code ready to run on the machine."""
        pass

    @abc.abstractmethod
    def moveToStart(self):
        """Move to the starting position to cut the feature."""
        pass

    @abc.abstractmethod
    def returnToHome(self):
        """Return to the starting position after cutting the feature."""
        pass

    @abc.abstractmethod
    def getParams(self):
        """Get all own and inherited parameters."""
        pass

    @abc.abstractmethod
    def _makeDrawingClass(self):
        """Generate the instance's own class for its drawn instances."""
        pass

    def drawGeometry(self):
        """Add a missing drawn instance, then call `draw` on all its drawn instances."""
        log('GeometricFeature drawGeometry')
        if not self.observers:
            self.drawing_class()
        self.notifyObservers('draw')

    def validateParams(self):
        """Validate its own parameters."""
        pass

    def getOptionQueriesObject(self):
        """ Override of QueryManager.
        Return the feature's own (and any children's) option queries."""
        # To prevent overwriting instantiated queries
        if None in self.option_queries.values():
            # https://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/
            child_query_instances = self._getChildOptionQueries()
            child_query_instances.update(self._getOwnOptionQueries())
            self.option_queries.update(child_query_instances)
        return self.option_queries

    def _getOwnOptionQueries(self):
        """Core interface."""
        return {key: key() for key in self.option_queries}

    def _getChildOptionQueries(self):
        """May be spun out to other interface."""
        try:
            child_query_instances = {}
            for child in self.child_features.values():
                child_query_instances.update(child.getOptionQueriesObject().copy())
        except IndexError:
            child_query_instances = {}
        return child_query_instances

    def setChildFeatures(self, feature_class):
        """Used for composed features, where user creates the composition.
        May spin out to other interface
        TODO: determine whether to keep or turf, as it isn't yet used.
        """
        # here, self.child_feature_classes is an instance property
        # ... oooh so dynamic !
        # to be really clever, would confirm that super_class is GeometricFeature
        assert isinstance(feature_class, GeometricFeature), 'Must be a class'
        self.child_features[feature_class] = feature_class

    def makeChildren(self):
        """May be spun out to other interface."""
        children = {key: key(self.feature_manager, self.view_space) for key in self.child_features}
        self.child_features.update(children)

    def getBasicParams(self):
        """Core interface."""
        params = {}
        params.update(self.machine.getParams().copy())
        params.update(self.work_piece.getParams().copy())
        return params

    def delete(self):
        """Core interface."""
        self.removeObservers('remove')
        self.feature_manager.deleteChild(self)

    def moveToReference(self):
        """Core interface."""
        file_text = addDebugFrame(inspect.currentframe())
        ref_X = self.option_queries[ReferenceXQuery].getValue()
        ref_Y = self.option_queries[ReferenceYQuery].getValue()
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((ref_X, ref_Y))
        file_text += self.moveToStart()
        return file_text

    def returnFromReference(self):
        """Core interface."""
        file_text = addDebugFrame(inspect.currentframe())
        ref_X = self.option_queries[ReferenceXQuery].getValue()
        ref_Y = self.option_queries[ReferenceYQuery].getValue()
        file_text += self.returnToHome()
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((- ref_X, - ref_Y))
        return file_text

    def postQueryUpdateHook(self):
        """A callback to call when the feature's parameters are changed, to
        trigger other changes."""
        log('GeometricFeature postQueryUpdateHook')
        if self.drawing_class is None:
            self.makeDrawingClass()
        else:
            # pdb.set_trace()
            if hasattr(self, 'getDrawingParams'):
                drawing_params = self.getDrawingParams()
            else:
                drawing_params = self.getParams()
            self.drawing_class.params = drawing_params
            self.notifyObservers('draw')

    def changeViewPlane(self):
        """Perform tasks required to reflect change in viewspace plane."""
        self.removeObservers('remove')
        self.drawGeometry()

    def makeDrawingClass(self):
        """Trigger the feature-specific method for creating the feature instance's
        drawing class."""
        anon = self._makeDrawingClass()
        self.drawing_class = anon
        return anon
