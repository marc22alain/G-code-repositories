#!/usr/bin/env python

from Tkinter import *
from math import *
import os
import simple_generators as G

# here we define the list of bits to choose from:
#   6.35mm = 1/4"
#   11.135mm = 7/16"
bits = (6.35, 11.135)
default_safe_Z = 100
default_feed_rate = 1000
default_tab_width = 6.35

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

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        # row = 0
        self.label = Label(self.EntryFrame, text='Make a tabbed doughnut')
        self.label.grid(row=0, column=0, columnspan=2)

        # row = 1
        self.feed_rate_label = Label(self.EntryFrame, text='Feed rate')
        self.feed_rate_label.grid(row=1, column=0)
        self.feed_rate_var = StringVar()
        self.feed_rate_input = Entry(self.EntryFrame, textvariable=self.feed_rate_var ,width=15)
        self.feed_rate_input.grid(row=1, column=1)
        self.feed_rate_input.insert(0, default_feed_rate)

        # row = 2
        self.Z_safe_label = Label(self.EntryFrame, text='Safe Z travel height')
        self.Z_safe_label.grid(row=2, column=0)
        self.Z_safe_var = StringVar()
        self.Z_safe_input = Entry(self.EntryFrame, textvariable=self.Z_safe_var ,width=15)
        self.Z_safe_input.grid(row=2, column=1)
        self.Z_safe_input.insert(0, default_safe_Z)

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
        self.bit_diameter_input = Spinbox(self.EntryFrame, values=bits, textvariable=self.bit_diameter_var, width=13)
        self.bit_diameter_input.grid(row=4, column=1)

        # row = 5
        self.stock_thickness_label = Label(self.EntryFrame, text='Stock thickness')
        self.stock_thickness_label.grid(row=5, column=0)
        self.stock_thickness_var = DoubleVar()
        self.stock_thickness_input = Entry(self.EntryFrame, textvariable=self.stock_thickness_var ,width=15)
        self.stock_thickness_input.grid(row=5, column=1)

        # row = 6
        self.tab_thickness_label = Label(self.EntryFrame, text='Tab thickness')
        self.tab_thickness_label.grid(row=6, column=0)
        self.tab_thickness_var = DoubleVar()
        self.tab_thickness_input = Entry(self.EntryFrame, textvariable=self.tab_thickness_var ,width=15)
        self.tab_thickness_input.grid(row=6, column=1)

        # row = 7
        self.tab_width_label = Label(self.EntryFrame, text='Tab width')
        self.tab_width_label.grid(row=7, column=0)
        self.tab_width_var = StringVar()
        self.tab_width_input = Entry(self.EntryFrame, textvariable=self.tab_width_var ,width=15)
        self.tab_width_input.grid(row=7, column=1)
        self.tab_width_input.insert(0, default_tab_width)

        # row = 8
        self.doughnut_OD_label = Label(self.EntryFrame, text='Doughnut OD')
        self.doughnut_OD_label.grid(row=8, column=0)
        self.doughnut_OD_var = DoubleVar()
        self.doughnut_OD_input = Entry(self.EntryFrame, textvariable=self.doughnut_OD_var ,width=15)
        self.doughnut_OD_input.grid(row=8, column=1)

        # row = 9
        self.doughnut_ID_input = Label(self.EntryFrame, text='Doughnut ID')
        self.doughnut_ID_input.grid(row=9, column=0)
        self.doughnut_ID_var = DoubleVar()
        self.doughnut_ID_input = Entry(self.EntryFrame, textvariable=self.doughnut_ID_var ,width=15)
        self.doughnut_ID_input.grid(row=9, column=1)

        # row = 10
        # not sure about this behaviour
        if IN_AXIS:
            self.printButton = Button(self, text='Write to AXIS and Quit',\
                command=self.WriteToAxis)
        else:
            self.printButton = Button(self, text='Print', command=self.Print)
        self.printButton.grid(row=10, column=1, sticky=S)
        
##        else:
##            self.quitButton = Button(self, text='Quit', command=self.quit)
##        self.quitButton.grid(row=13, column=1, sticky=S)
        """
        self.quitButton = Button(self.EntryFrame, text='Quit', command=self.quit)
        self.quitButton.grid(row=13, column=1, sticky=S)
        """


    def GenerateCode(self):
        self.g_code = G.startProgram(int(self.feed_rate_var.get()))
        self.g_code += G.bore_hole(int(self.Z_safe_var.get()),
                          self.stock_thickness_var.get(),
                          self.cut_per_pass_var.get(),
                          self.tab_thickness_var.get(),
                          self.bit_diameter_var.get(),
                          self.doughnut_ID_var.get())
        self.g_code += G.bore_tabbed_ID(int(self.Z_safe_var.get()),
                          self.tab_thickness_var.get(),
                          self.cut_per_pass_var.get(),
                          0,
                          self.bit_diameter_var.get(),
                          self.doughnut_ID_var.get(),
                          self.tab_width_var.get())
        self.g_code += G.bore_circle_OD(int(self.Z_safe_var.get()),
                          self.stock_thickness_var.get(),
                          self.cut_per_pass_var.get(),
                          self.tab_thickness_var.get(),
                          self.bit_diameter_var.get(),
                          self.doughnut_OD_var.get())
        self.g_code += G.bore_tabbed_OD(int(self.Z_safe_var.get()),
                          self.tab_thickness_var.get(),
                          self.cut_per_pass_var.get(),
                          0,
                          self.bit_diameter_var.get(),
                          self.doughnut_OD_var.get(),
                          self.tab_width_var.get())    
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
app.master.title("Doughnut Cutter 0.9")
app.mainloop()
