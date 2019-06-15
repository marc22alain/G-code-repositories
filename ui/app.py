#!/usr/bin/env python
from Tkinter import *
from option_queries import GeometricFeatureQuery
from feature_manager import AbstractFeatureManager, FeatureManager

from OptionQueryDialog_class import OptionQueryDialog
from FeatureList_class import FeatureList
from ListItem_class import ListItem
from ViewSpace_class import ViewSpace
import os
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

        # create or inject machine and workpiece

    def createSubframes(self):
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, view_init)
        # TODO resolve who owns this
        self.feature_manager = FeatureManager(self.view_space)
        self.feature_manager.root = True

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
        self.makePrintButton(self.entry_frame, row_num)

        row_num += 1
        self.view_plane_var = StringVar()
        self.view_plane_button = Spinbox(self.entry_frame, values=["XY","YZ","XZ"], textvariable=self.view_plane_var, width=13, command=self.setViewPlane)
        self.view_plane_button.grid(row=row_num, column=0)


    def createFeature(self):
        choice = self.current_feature_choice
        choice.updateValue()
        feature_class = choice.getValue()
        self.feature_manager.addChild(feature_class)

    def genCode(self):
        return self.feature_manager.getGCode()

    def insertMachine(self, row_num):
        item = ListItem(self.entry_frame, self.feature_manager.machine)
        item.grid(row=row_num, column=0, columnspan=2, pady=5)

    def insertWorkpiece(self, row_num):
        item = ListItem(self.entry_frame, self.feature_manager.work_piece)
        item.grid(row=row_num, column=0, columnspan=2, pady=5)

    def setViewPlane(self):
        plane = self.view_plane_var.get()
        self.view_space.changeViewPlane(plane)
        self.feature_manager.changeViewPlane()

    def makePrintButton(self, master, row_num):
        # self.button_frame = Frame(master)
        # self.button_frame.grid(row=row, column=0, columnspan=2)

        # row_num = 0
        if IN_AXIS:
            self.printButton = Button(master, text='Write to AXIS and Quit',\
                command=self.writeToAxis)
        else:
            self.printButton = Button(master, text='Print', command=self.printToConsole)
        self.printButton.grid(row=row_num, column=0, columnspan=2)

    def printToConsole(self):
        log(self.genCode())
        # since self.quit() does not work on OSX
        os._exit(0)


    def writeToAxis(self):
        sys.stdout.write(self.genCode())
        # may want to keep this alive, for writing many similar holes
        # of course if AXIS does not delete the program, then maybe this
        # does work fine for UI
        self.quit()
