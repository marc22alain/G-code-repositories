#!/usr/bin/env python

from Tkinter import *
from math import *
import os
import simple_generators as G
import MC_defaults as MC
from Canvas_Geometry_classes import *


# what's this for ?
IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

"""
INPUT elements:
    all of the variables to select:
    -stock thickness
    -maximum depth of cut (set default at 3mm)
    -cutter diameter (choose from list with default of 1/4" bit)
    -Z-safe height
    -doughnut OD and ID
    -depth of cut
    -thickness of tabs
    -width of tabs (leave as default 1/4 inch for now)
"""

class DoughnutCutter(Frame):
    def __init__(self, master=None, setup=None):
        Frame.__init__(self, master)
        self.setup = setup
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        row_num = 0
        self.label = Label(self.EntryFrame, text='Make a tabbed doughnut')
        self.label.grid(row=row_num, column=0, columnspan=2)

        # row_num += 1
        # self.SubEntryFrame = Frame(self,bd=5)
        # self.SubEntryFrame.grid(row=row_num, column=1)

        row_num += 1
        self.setup.createWidgets(self.EntryFrame, row_num)



        row_num += 1
        self.tab_thickness_label = Label(self.EntryFrame, text='Tab thickness')
        self.tab_thickness_label.grid(row=row_num, column=0)
        self.tab_thickness_var = DoubleVar()
        self.tab_thickness_input = Entry(self.EntryFrame, textvariable=self.tab_thickness_var ,width=15)
        self.tab_thickness_input.grid(row=row_num, column=1)

        row_num += 1
        self.tab_width_label = Label(self.EntryFrame, text='Tab width')
        self.tab_width_label.grid(row=row_num, column=0)
        self.tab_width_var = StringVar()
        self.tab_width_input = Entry(self.EntryFrame, textvariable=self.tab_width_var ,width=15)
        self.tab_width_input.grid(row=row_num, column=1)
        self.tab_width_input.insert(0, MC.default_tab_width)

        row_num += 1
        self.doughnut_OD_label = Label(self.EntryFrame, text='Doughnut OD')
        self.doughnut_OD_label.grid(row=row_num, column=0)
        self.doughnut_OD_var = DoubleVar()
        self.doughnut_OD_input = Entry(self.EntryFrame, textvariable=self.doughnut_OD_var ,width=15)
        self.doughnut_OD_input.grid(row=row_num, column=1)

        row_num += 1
        self.doughnut_ID_input = Label(self.EntryFrame, text='Doughnut ID')
        self.doughnut_ID_input.grid(row=row_num, column=0)
        self.doughnut_ID_var = DoubleVar()
        self.doughnut_ID_input = Entry(self.EntryFrame, textvariable=self.doughnut_ID_var ,width=15)
        self.doughnut_ID_input.grid(row=row_num, column=1)


        row_num += 1
        self.setup.makePrintButton(self.EntryFrame, row_num, self)



    def generateCode(self):

        feed_rate, safe_Z, max_cut_per_pass, bit_diameter, stock_thickness = self.setup.getAllData()


        self.g_code = G.startProgram(int(feed_rate))
        self.g_code += G.bore_circle_ID(int(safe_Z),
                          stock_thickness,
                          max_cut_per_pass,
                          self.tab_thickness_var.get(),
                          bit_diameter,
                          self.doughnut_ID_var.get())
        self.g_code += G.bore_tabbed_ID(int(safe_Z),
                          stock_thickness,
                          max_cut_per_pass,
                          self.tab_thickness_var.get(),
                          bit_diameter,
                          self.doughnut_ID_var.get(),
                          float(self.tab_width_var.get()))
        self.g_code += G.bore_circle_OD(int(safe_Z),
                          stock_thickness,
                          max_cut_per_pass,
                          self.tab_thickness_var.get(),
                          bit_diameter,
                          self.doughnut_OD_var.get())
        self.g_code += G.bore_tabbed_OD(int(safe_Z),
                          self.tab_thickness_var.get(),
                          max_cut_per_pass,
                          self.tab_thickness_var.get(),
                          bit_diameter,
                          self.doughnut_OD_var.get(),
                          float(self.tab_width_var.get()))
        self.g_code += G.endProgram()

        return self.g_code

    def makeGeometricEntities(self):
        entities = []
        entities.append(Circle(65, (0,0), {"outline":"white"}))
        entities.append(Circle(97, (0,0), {"outline":"white"}))
        return entities
