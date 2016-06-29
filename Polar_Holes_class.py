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
    all of the variables to select (from Hole_Borer):
    default:
    -feed rate
    -Z-safe height
    -maximum depth of cut (set default at 3mm)
    -cutter diameter (choose from list with default of 1/4" bit)
    -stock thickness
    -depth of cut (default is full depth)
    specific:
    -hole diameter
    new:
    -number of holes
    -hole circle diameter
"""


class PolarHolesBorer(Frame):
    def __init__(self, master=None, setup=None):
        Frame.__init__(self, master)
        self.setup = setup
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        row_num = 0
        self.label = Label(self.EntryFrame, text='Make a polar arrangment of holes')
        self.label.grid(row=row_num, column=0, columnspan=2)

 
        row_num += 1
        self.setup.createWidgets(self.EntryFrame, row_num)


        row_num += 1
        self.hole_diameter_label = Label(self.EntryFrame, text='Hole Diameter')
        self.hole_diameter_label.grid(row=row_num, column=0)
        self.hole_diameter_var = DoubleVar()
        self.hole_diameter_input = Entry(self.EntryFrame, textvariable=self.hole_diameter_var ,width=15)
        self.hole_diameter_input.grid(row=row_num, column=1)

        row_num += 1
        self.num_holes_label = Label(self.EntryFrame, text='Number of Holes')
        self.num_holes_label.grid(row=row_num, column=0)
        self.num_holes_var = DoubleVar()
        self.num_holes_input = Entry(self.EntryFrame, textvariable=self.num_holes_var ,width=15)
        self.num_holes_input.grid(row=row_num, column=1)

        row_num += 1
        self.HCD_label = Label(self.EntryFrame, text='Hole Circle Diameter')
        self.HCD_label.grid(row=row_num, column=0)
        self.HCD_var = DoubleVar()
        self.HCD_input = Entry(self.EntryFrame, textvariable=self.HCD_var ,width=15)
        self.HCD_input.grid(row=row_num, column=1)


        row_num += 1
        self.setup.makePrintButton(self.EntryFrame, row_num, self)



    def generateCode(self):
        feed_rate, safe_Z, max_cut_per_pass, bit_diameter, stock_thickness = self.setup.getAllData()

        self.g_code = G.startProgram(feed_rate)

        self.g_code += G.polar_holes(safe_Z,
                          stock_thickness,
                          max_cut_per_pass,
                          0,
                          bit_diameter,
                          self.hole_diameter_var.get(),
                          self.num_holes_var.get(),
                          self.HCD_var.get())

        self.g_code += G.endProgram()


    def printToConsole(self):
        self.generateCode()
        print self.g_code
        # since self.quit() does not work on OSX
        os._exit(0)


    def writeToAxis(self):
        self.generateCode()
        sys.stdout.write(self.g_code)
        # may want to keep this alive, for writing many similar holes
        # of course if AXIS does not delete the program, then maybe this
        # does work fine for UI
        self.quit()
