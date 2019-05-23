#!/usr/bin/env python
from Tkinter import *
from option_queries import GeometricFeatureQuery
from feature_manager import FeatureManager

from OptionQueryDialog_class import OptionQueryDialog
from FeatureList_class import FeatureList
from ListItem_class import ListItem
from ViewSpace_class import ViewSpace


view_init = { "view_plane": "XY", \
                  "extents": {"width": 50, "height": 50, "center": (25, 25)}}

class Application(Frame):
    def __init__(self, master = None):
        self.features = []
        Frame.__init__(self, master)
        self.grid()
        self.createSubframes()

        # create or inject machine and workpiece

    def createSubframes(self):
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, view_init)
        # TODO resolve who owns this
        self.feature_manager = FeatureManager(self, self.view_space)

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
        self.output_button = Button(self.entry_frame,text="test gen gcode",command=self.genCode, width=30)
        self.output_button.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        self.view_plane_var = StringVar()
        self.view_plane_button = Spinbox(self.entry_frame, values=["XY","YZ","XZ"], textvariable=self.view_plane_var, width=13, command=self.setViewPlane)
        self.view_plane_button.grid(row=row_num, column=0)


    def createFeature(self):
        feature_class = self.current_feature_choice.getValue()
        self.feature_manager.addFeature(feature_class)

    def genCode(self):
        print self.feature_manager.getGCode()

    def insertMachine(self, row_num):
        item = ListItem(self.entry_frame, self.feature_manager.machine)
        item.grid(row=row_num, column=0, columnspan=2, pady=5)

    def insertWorkpiece(self, row_num):
        item = ListItem(self.entry_frame, self.feature_manager.work_piece)
        item.grid(row=row_num, column=0, columnspan=2, pady=5)

    def setViewPlane(self):
        plane = self.view_plane_var.get()
        print 'plane'
        print plane
        print self.view_space.view_plane
        self.view_space.view_plane = plane
        self.feature_manager.work_piece.drawGeometry()
        self.feature_manager.reDrawAll()
