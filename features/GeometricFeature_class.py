#!/usr/bin/env python
import abc
from option_queries import *
from utilities import Glib as G


class GeometricFeature:
    __metaclass__ = abc.ABCMeta

    common_query_classes = [
        ReferenceXQuery,
        ReferenceYQuery
    ]

    def __init__(self, feature_manager, manages_depth=True):
        self.feature_manager = feature_manager
        self.machine = feature_manager.machine
        self.work_piece = feature_manager.work_piece
        try:
            self.self_managed_depth = manages_depth and self.can_manage_depth
        except AttributeError:
            self.self_managed_depth = False
        # may move this into child_feature_classes, when better handling of children is produced
        if self.self_managed_depth:
            from DepthStepper_class import DepthStepper
            self.option_query_classes = self.option_query_classes + DepthStepper.option_query_classes
            self.depth_stepper = DepthStepper(feature_manager)
        self.option_queries = { key: None for key in self.option_query_classes }
        self.option_queries.update({ key: None for key in self.common_query_classes })
        self.child_features = { key: None for key in self.child_feature_classes }
        self.makeChildren()

    @abc.abstractmethod
    def getGCode(self):
        pass

    @abc.abstractmethod
    def moveToStart(self):
        pass

    @abc.abstractmethod
    def returnToHome(self):
        pass

    @abc.abstractmethod
    def getInstructions(self):
        pass

    def getManagedDepthInstructions(self):
        self.depth_stepper.option_queries[CutPerPassQuery] = self.option_queries[CutPerPassQuery]
        self.depth_stepper.option_queries[CutDepthQuery] = self.option_queries[CutDepthQuery]
        return self.depth_stepper.getGCode(self.getInstructions, self.moveToReference, self.returnFromReference)

    def getOptionQueries(self):
        # To prevent overwriting instantiated queries
        if None in self.option_queries.values():
            # https://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/
            child_query_instances = self._getChildOptionQueries()
            child_query_instances.update(self._getOwnOptionQueries())
            self.option_queries.update(child_query_instances)
        return self.option_queries

    def _getOwnOptionQueries(self):
        return { key: key() for key in self.option_queries }

    def _getChildOptionQueries(self):
        try:
            # TODO: resolve for multiple children, for composed features
            child_query_instances = self.child_features.values()[0].getOptionQueries().copy()
        except IndexError:
            child_query_instances = {}
        return child_query_instances

    def setChildFeatures(self, feature_class):
        '''
        Used for composed features, where user creates the composition.
        '''
        # here, self.child_feature_classes is an instance property
        # ... oooh so dynamic !
        # to be really clever, would confirm that super_class is GeometricFeature
        assert type(feature_class) == type(GeometricFeature), 'Must be a class'
        self.child_features[feature_class] = feature_class

    def makeChildren(self):
        children = { key: key(self.feature_manager) for key in self.child_features}
        self.child_features.update(children)

    def getBasicParams(self):
        params = self.machine.getParams().copy()
        params.update(self.work_piece.getParams().copy())
        return params

    def delete(self):
        self.feature_manager.deleteFeature(self)

    def moveToReference(self):
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        file_text = G.set_INCR_mode()
        file_text += G.G0_XY((refX, refY))
        file_text += self.moveToStart()
        return file_text

    def returnFromReference(self):
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        file_text = self.returnToHome()
        file_text += G.set_INCR_mode()
        file_text += G.G0_XY((- refX, - refY))
        return file_text
