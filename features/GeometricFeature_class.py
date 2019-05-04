#!/usr/bin/env python
import abc
from option_queries import *


class GeometricFeature:
    __metaclass__ = abc.ABCMeta

    def __init__(self, machine, work_piece, manages_depth=True):
        try:
            self.self_managed_depth = manages_depth and self.can_manage_depth
        except AttributeError:
            self.self_managed_depth = False
        # may move this into child_feature_classes, when better handling of children is produced
        if self.self_managed_depth:
            from DepthStepper_class import DepthStepper
            self.option_query_classes = self.option_query_classes + DepthStepper.option_query_classes
            self.depth_stepper = DepthStepper(machine, work_piece)
        self.machine = machine
        self.work_piece = work_piece
        self.option_queries = { key: None for key in self.option_query_classes }
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
        return self.depth_stepper.getGCode(self.getInstructions, self.moveToStart, self.returnToHome)

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
        children = { key: key(self.machine, self.work_piece) for key in self.child_features}
        self.child_features.update(children)

    def getBasicParams(self):
        params = self.machine.getParams().copy()
        params.update(self.work_piece.getParams().copy())
        return params
