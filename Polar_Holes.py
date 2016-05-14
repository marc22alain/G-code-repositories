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


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.createMoreWidgets()

    def createWidgets(self):
        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        # row = 0
        self.label = Label(self.EntryFrame, text='Make a polar arrangment of holes')
        self.label.grid(row=0, column=0, columnspan=2)

        # row = 1
        self.feed_rate_label = Label(self.EntryFrame, text='Feed rate')
        self.feed_rate_label.grid(row=1, column=0)
        self.feed_rate_var = StringVar()
        self.feed_rate_input = Entry(self.EntryFrame, textvariable=self.feed_rate_var ,width=15)
        self.feed_rate_input.grid(row=1, column=1)
        self.feed_rate_input.insert(0, MC.default_feed_rate)

        # row = 2
        self.Z_safe_label = Label(self.EntryFrame, text='Safe Z travel height')
        self.Z_safe_label.grid(row=2, column=0)
        self.Z_safe_var = StringVar()
        self.Z_safe_input = Entry(self.EntryFrame, textvariable=self.Z_safe_var ,width=15)
        self.Z_safe_input.grid(row=2, column=1)
        self.Z_safe_input.insert(0, MC.default_safe_Z)

        # row = 3
        self.cut_per_pass_label = Label(self.EntryFrame, text='Maximum cut per pass')
        self.cut_per_pass_label.grid(row=3, column=0)
        self.cut_per_pass_var = DoubleVar()
        self.cut_per_pass_input = Entry(self.EntryFrame, textvariable=self.cut_per_pass_var ,width=15)
        self.cut_per_pass_input.grid(row=3, column=1)

        # row = 4
        self.bit_diameter_label = Label(self.EntryFrame, text='Cutter diameter')
        self.bit_diameter_label.grid(row=4, column=0)
        self.bit_diameter_var = DoubleVar()
        self.bit_diameter_input = Spinbox(self.EntryFrame, values=MC.bits, textvariable=self.bit_diameter_var, width=13)
        self.bit_diameter_input.grid(row=4, column=1)

        # row = 5
        self.stock_thickness_label = Label(self.EntryFrame, text='Stock thickness')
        self.stock_thickness_label.grid(row=5, column=0)
        self.stock_thickness_var = DoubleVar()
        self.stock_thickness_input = Entry(self.EntryFrame, textvariable=self.stock_thickness_var ,width=15)
        self.stock_thickness_input.grid(row=5, column=1)

        # row = 10
        # not sure about this behaviour
        if IN_AXIS:
            self.printButton = Button(self, text='Write to AXIS and Quit',\
                command=self.WriteToAxis)
        else:
            self.printButton = Button(self, text='Print', command=self.Print)
        self.printButton.grid(row=15, column=1, sticky=S)
        
##        else:
##            self.quitButton = Button(self, text='Quit', command=self.quit)
##        self.quitButton.grid(row=13, column=1, sticky=S)
        """
        self.quitButton = Button(self.EntryFrame, text='Quit', command=self.quit)
        self.quitButton.grid(row=13, column=1, sticky=S)
        """

    def createMoreWidgets(self):
        # row = 6
        self.hole_diameter_label = Label(self.EntryFrame, text='Hole Diameter')
        self.hole_diameter_label.grid(row=6, column=0)
        self.hole_diameter_var = DoubleVar()
        self.hole_diameter_input = Entry(self.EntryFrame, textvariable=self.hole_diameter_var ,width=15)
        self.hole_diameter_input.grid(row=6, column=1)
    

        # row = 7
        self.num_holes_label = Label(self.EntryFrame, text='Number of Holes')
        self.num_holes_label.grid(row=7, column=0)
        self.num_holes_var = DoubleVar()
        self.num_holes_input = Entry(self.EntryFrame, textvariable=self.num_holes_var ,width=15)
        self.num_holes_input.grid(row=7, column=1)

        # row = 8
        self.HCD_label = Label(self.EntryFrame, text='Hole Circle Diameter')
        self.HCD_label.grid(row=8, column=0)
        self.HCD_var = DoubleVar()
        self.HCD_input = Entry(self.EntryFrame, textvariable=self.HCD_var ,width=15)
        self.HCD_input.grid(row=8, column=1)




    def GenerateCode(self):
        self.g_code = G.startProgram(int(self.feed_rate_var.get()))

        self.g_code += G.polar_holes(int(self.Z_safe_var.get()),
                          self.stock_thickness_var.get(),
                          self.cut_per_pass_var.get(),
                          0,
                          self.bit_diameter_var.get(),
                          self.hole_diameter_var.get(),
                          self.num_holes_var.get(),
                          self.HCD_var.get())

        self.g_code += G.endProgram()


    def Print(self):
        self.GenerateCode()
        print self.g_code
        # since self.quit() does not work on OSX
        os._exit(0)


    def WriteToAxis(self):
        self.GenerateCode()
        sys.stdout.write(self.g_code)
        # may want to keep this alive, for writing many similar holes
        # of course if AXIS does not delete the program, then maybe this
        # does work fine for UI
        self.quit()


app = Application()
app.master.title("Polar Holes 0.9")
app.mainloop()
