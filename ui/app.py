#!/usr/bin/env python
from Tkinter import *
from option_queries import GeometricFeatureQuery
from feature_manager import AbstractFeatureManager, FeatureManager

from FeatureList_class import FeatureList
from ListItem_class import ListItem
from AxisPrintButton_class import AxisPrintButton
from ViewSpace_class import ViewSpace
import os
import time
from utilities import log

IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

view_init = { "view_plane": "XY", \
                  "extents": {"width": 50, "height": 50, "center": (25, 25)}}

class Application(Frame):
    def __init__(self, master = None):
        self.features = []
        Frame.__init__(self, master)
        self.grid()
        self.createSubframes()
        AbstractFeatureManager.app = self

    def createSubframes(self):
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, view_init)
        # TODO resolve who owns this
        self.feature_manager = FeatureManager(self.view_space)
        self.feature_manager.root = True

        # entry panel
        row_num = 1
        self.entry_frame = Frame(self)
        self.entry_frame.grid(row=0, column=1)

        row_num += 1
        self.insertMachine(row_num)
        row_num += 1
        self.insertWorkpiece(row_num)

        row_num += 1
        self.refresh_view = Button(self.entry_frame,text="Add Class",command=self.createFeature, width=30)
        self.refresh_view.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        self.current_feature_choice = GeometricFeatureQuery()
        self.current_feature_choice.insertQuery(self.entry_frame, row_num)

        row_num += 1
        self.feature_list = FeatureList(self.entry_frame)
        self.feature_list.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        self.print_button_object = AxisPrintButton(self.entry_frame, row_num, self.genCode, save_config=self.saveConfig)

        row_num += 1
        button_options = {
            'row_num': row_num,
            'column': 0,
            'width': 13
        }
        self.view_space.insertViewPlaneSelector(self.entry_frame, button_options, self.setViewPlane)

    def createFeature(self):
        choice = self.current_feature_choice
        choice.updateValue()
        feature_class = choice.getValue()
        self.feature_manager.addChildByClass(feature_class)

    def genCode(self):
        return self.feature_manager.getGCode()

    def insertMachine(self, row_num):
        item = ListItem(self.entry_frame, self.feature_manager.machine)
        item.grid(row=row_num, column=0, columnspan=2, pady=5)

    def insertWorkpiece(self, row_num):
        item = ListItem(self.entry_frame, self.feature_manager.work_piece)
        item.grid(row=row_num, column=0, columnspan=2, pady=5)

    def setViewPlane(self):
        self.feature_manager.changeViewPlane()

    def saveConfig(self):
        # generate a unique filename
        file_name = self.getFeatureConfigsFileName()
        self.feature_manager.saveFeatureConfigs(file_name)

    def getFeatureConfigsFileName(self):
        # TODO: pop up a dialog to name the file
        return 'json/features_%d' % (int(time.time()))
