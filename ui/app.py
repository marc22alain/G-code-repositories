#!/usr/bin/env python
from Tkinter import *
from machines import SimpleMachine
from workpieces import SimpleWorkpiece
from option_queries import GeometricFeatureQuery

from OptionQueryDialog_class import OptionQueryDialog
from FeatureList_class import FeatureList

class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid()
        self.createSubframes()
        self.machine = SimpleMachine()
        self.workpiece = SimpleWorkpiece()
        self.features = []

        # create or inject machine and workpiece

    def createSubframes(self):
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=1)
        # self.view_space = ViewSpace(self.geo_frame, self.machined_geometry_engine.getViewSpaceInit())

        row_num = 1
        self.entry_frame = Frame(self)
        self.entry_frame.grid(row=0, column=1)
        self.refresh_view = Button(self.entry_frame,text="Add Class",command=self.createFeature, width=30)
        self.refresh_view.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        self.current_feature_choice = GeometricFeatureQuery()
        self.current_feature_choice.insertQuery(self.entry_frame, row_num)

        row_num += 1
        self.feature_list = FeatureList(self)
        self.feature_list.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        self.output_button = Button(self.entry_frame,text="test gen gcode",command=self.genCode, width=30)
        self.output_button.grid(row=row_num, column=0, columnspan=2, pady=5)

    def createFeature(self):
        feature_class = self.current_feature_choice.getValue()
        # so far, for DepthStepper
        if hasattr(feature_class, 'parent_feature_class'):
            feature = feature_class.parent_feature_class(self.machine, self.workpiece, feature_class)
        else:
            feature = feature_class(self.machine, self.workpiece)

        print feature
        self.features.append(feature)
        def addFunction():
            self.feature_list.insertFeature(feature)
            print 'running OK function'
        def cancelFunction():
            self.features.pop()
            print 'running CANCEL function'
        # will run if user chooses to CANCEL
        self.okFunction = addFunction
        self.cancelFunction = cancelFunction
        # now get the feature's OptionQueries and get some answers for it,
        # or allow the user to cancel and delete the new feature
        OptionQueryDialog(self, feature.getOptionQueries(), feature.name )
        # take away this dangerous option !
        self.okFunction = None
        self.cancelFunction = None

    def genCode(self):
        print self.features[0].getGCode()
