#!/usr/bin/env python
from option_queries import GeometricFeatureQuery
from Tkinter import *
from BasicDialog_class import BasicDialog
from utilities import log

def doNothing():
    pass

class SelectFeatureDialog(BasicDialog):
    """Takes callbacks and returns a GeometricFeature class to the ok_callback."""
    def __init__(self, parent, ok_callback, cancel_callback=doNothing):
        self.callers_callback = ok_callback
        BasicDialog.__init__(self, parent, 'Add a Feature', self.selectFeature, cancel_callback)

    def body(self, master):
        row_num = 1
        self.label = Label(master, text='Choose from the list')
        self.label.grid(row=row_num, column=0, columnspan=2)

        row_num += 1
        self.current_feature_choice = GeometricFeatureQuery()
        self.current_feature_choice.insertQuery(master, row_num)

    def selectFeature(self):
        choice = self.current_feature_choice
        # need to prompt the OptionQuery to get actual value
        choice.updateValue()
        feature_class = choice.getValue()
        self.callers_callback(feature_class)

