#!/usr/bin/env python

import abc

class OptionQuery:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def getHint(self):
        return self.hint

    def getValue(self):
        return self.value

    def setValue(self, value):
        assert type(value) == self.variable_type, 'Query value must match specified type.'
        self.value = value

    def getVariableType(self):
        return self.variable_type
