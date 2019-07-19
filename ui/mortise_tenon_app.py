#!/usr/bin/env python
from Tkinter import *
from ViewSpace_class import ViewSpace
from joints import MortiseAndTenonJoint
from ui import OptionQueryDialog

view_init = { "view_plane": "XY", \
                  "extents": {"width": 50, "height": 50, "center": (25, 25)}}

class Application(Frame):
    def __init__(self, joint_designer=MortiseAndTenonJoint, master = None):
        self.joint_designer = joint_designer()
        self.view_space = None
        Frame.__init__(self, master)
        self.grid()
        self.createSubframes()
        # UGH !
        # AbstractFeatureManager.app = self

    def createSubframes(self):
        # drawing view
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, view_init)

        # entry panel
        row_num = 1
        self.entry_frame = Frame(self)
        self.entry_frame.grid(row=0, column=1)

        self.current_mode = "Design Mode"
        self.mode_switch = Button(self.entry_frame,text=self.current_mode,command=self.switchMode, width=30)
        self.mode_switch.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        self.edit_design = Button(self.entry_frame,text=self.joint_designer.name,command=self.editDesign, width=30)
        self.edit_design.grid(row=row_num, column=0, columnspan=2, pady=5)

    def switchMode(self):
        if self.current_mode == "Design Mode":
            self.current_mode = "Program review mode"
        else:
            self.current_mode = "Design Mode"
        self.mode_switch.config(text=self.current_mode)

    def editDesign(self):
        OptionQueryDialog(
            self,
            self.joint_designer.getOptionQueries(),
            self.joint_designer.name,
            self.joint_designer.didUpdateQueries,
            None,
            self.joint_designer.__doc__
        )


