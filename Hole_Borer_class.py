#!/usr/bin/env python

from Tkinter import *
from math import *
import os
import simple_generators as G
import MC_defaults as MC



# what's this for ?
IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

"""
INPUT elements:
    all of the variables to select:
    -stock thickness
    -maximum depth of cut (set default at 3mm)
    -cutter diameter (choose from list with default of 1/4" bit)
    -Z-safe height
    -hole diameter
    -depth of cut (default is full depth)
"""
class HoleBorer(Frame):
    def __init__(self, master=None, setup=None):
        Frame.__init__(self, master)
        self.setup = setup
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        row_num = 0
        self.st00 = Label(self.EntryFrame, text='Bore a hole (G2 is CW)')
        self.st00.grid(row=row_num, column=0, columnspan=2)

        row_num += 1
        self.setup.createWidgets(self.EntryFrame, row_num)

        row_num += 1
        self.hole_diameter_label = Label(self.EntryFrame, text='Hole diameter')
        self.hole_diameter_label.grid(row=row_num, column=0)
        self.hole_diameter_var = DoubleVar()
        self.hole_diameter_input = Entry(self.EntryFrame, textvariable=self.hole_diameter_var ,width=15)
        self.hole_diameter_input.grid(row=row_num, column=1)

        row_num += 1
        self.target_depth_label = Label(self.EntryFrame, text='Target depth')
        self.target_depth_label.grid(row=row_num, column=0)
        self.target_depth_var = DoubleVar()
        self.target_depth_input = Entry(self.EntryFrame, textvariable=self.target_depth_var ,width=15)
        self.target_depth_input.grid(row=row_num, column=1)

        row_num += 1
        self.setup.makePrintButton(self.EntryFrame, row_num, self)

    def generateCode(self):
        feed_rate, safe_Z, max_cut_per_pass, bit_diameter, stock_thickness = self.setup.getAllData()

        self.g_code = G.startProgram(feed_rate)
        self.g_code += G.bore_circle_ID(safe_Z,
                          stock_thickness,
                          max_cut_per_pass,
                          self.target_depth_var.get(),
                          bit_diameter,
                          self.hole_diameter_var.get())
        self.g_code += G.endProgram()

        return self.g_code


    # def printToConsole(self):
    #     self.generateCode()
    #     print self.g_code
    #     # since self.quit() does not work on OSX
    #     os._exit(0)


    # def writeToAxis(self):
    #     self.generateCode()
    #     sys.stdout.write(self.g_code)
    #     # may want to keep this alive, for writng many similar holes
    #     # of course if AXIS does not delete the program, then maybe this
    #     # does work fine for UI
    #     self.quit()
