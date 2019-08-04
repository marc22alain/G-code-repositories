#!/usr/bin/env python
from Tkinter import *
from AxisPrintButton_class import AxisPrintButton
from feature_manager import AbstractFeatureManager
from jigs import MortiseAndTenonJig
from joints import MortiseAndTenonJoint
from ViewSpace_class import ViewSpace
from ui import OptionQueryDialog

view_init = { "view_plane": "XY", \
                  "extents": {"width": 50, "height": 50, "center": (25, 25)}}

class Application(Frame):
    def __init__(self, joint_designer=MortiseAndTenonJoint, master = None):
        self.view_space = None
        Frame.__init__(self, master)
        self.grid()
        self.createSubframes()
        self.feature_manager = MortiseAndTenonJig(self.view_space)
        self.feature_manager.getOptionQueries()
        self.joint_designer = joint_designer(self.feature_manager)
        stuff = self.joint_designer.getAllStuff()
        self.feature_manager.addEntities(stuff)
        self.addButtons()
        # UGH !
        AbstractFeatureManager.app = self

    def createSubframes(self):
        # drawing view
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, view_init)

        # entry panel
        row_num = 1
        self.entry_frame = Frame(self)
        self.entry_frame.grid(row=0, column=1)

    def addButtons(self):
        row_num = 1
        self.current_mode = "Design Mode"
        self.mode_label = Label(self.entry_frame, text=self.current_mode)
        self.mode_label.grid(row=row_num, column=0, pady=5)
        self.mode_switch = Button(self.entry_frame, text="Switch mode", command=self.switchMode)
        self.mode_switch.grid(row=row_num, column=1, pady=5)

        row_num += 1
        self.edit_design = Button(self.entry_frame,text=self.joint_designer.name,command=self.editDesign, width=30)
        self.edit_design.grid(row=row_num, column=0, columnspan=2, pady=5)

        row_num += 1
        self.print_button_object = AxisPrintButton(self.entry_frame, row_num, self.genCode)

    def switchMode(self):
        if self.current_mode == "Design Mode":
            self.current_mode = "Program review mode"
            # what next ?
        else:
            self.current_mode = "Design Mode"
            # what next ?
        self.mode_label.config(text=self.current_mode)

    def editDesign(self):
        OptionQueryDialog(
            self,
            self.joint_designer.getOptionQueries(),
            self.joint_designer.name,
            self.joint_designer.didUpdateQueries,
            None,
            self.joint_designer.__doc__
        )

    def genCode(self):
        return self.feature_manager.getGCode()
