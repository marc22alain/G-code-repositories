#!/usr/bin/env python

from Tkinter import *
from math import *
import os
import simple_generators as G
import MC_defaults as MC


# what's this for ?
IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")



class Setup(object):
    """ 
    Provides UI to obtain commonly required variables:
     - feed rate
     - safe Z travel height
     - maximum cut per pass
     - cutter diameter
     - stock thickness
    """
    def __init__(self):
        pass

    def createWidgets(self, master, row):
        self.EntryFrame = Frame(master,bd=5)
        self.EntryFrame.grid(row=row, column=0, columnspan=2)

        row_num = 0
        self.feed_rate_label = Label(self.EntryFrame, text='Feed rate')
        self.feed_rate_label.grid(row=row_num, column=0)
        self.feed_rate_var = StringVar()
        self.feed_rate_input = Entry(self.EntryFrame, textvariable=self.feed_rate_var ,width=15)
        self.feed_rate_input.grid(row=row_num, column=1)
        self.feed_rate_input.insert(0, MC.default_feed_rate)

        row_num += 1
        self.Z_safe_label = Label(self.EntryFrame, text='Safe Z travel height')
        self.Z_safe_label.grid(row=row_num, column=0)
        self.Z_safe_var = StringVar()
        self.Z_safe_input = Entry(self.EntryFrame, textvariable=self.Z_safe_var ,width=15)
        self.Z_safe_input.grid(row=row_num, column=1)
        self.Z_safe_input.insert(0, MC.default_safe_Z)

        row_num += 1
        self.cut_per_pass_label = Label(self.EntryFrame, text='Maximum cut per pass')
        self.cut_per_pass_label.grid(row=row_num, column=0)
        self.cut_per_pass_var = DoubleVar()
        self.cut_per_pass_input = Entry(self.EntryFrame, textvariable=self.cut_per_pass_var ,width=15)
        self.cut_per_pass_input.grid(row=row_num, column=1)

        row_num += 1
        self.bit_diameter_label = Label(self.EntryFrame, text='Cutter diameter')
        self.bit_diameter_label.grid(row=row_num, column=0)
        self.bit_diameter_var = DoubleVar()
        self.bit_diameter_input = Spinbox(self.EntryFrame, values=MC.bits, textvariable=self.bit_diameter_var, width=13)
        self.bit_diameter_input.grid(row=row_num, column=1)

        row_num += 1
        self.stock_thickness_label = Label(self.EntryFrame, text='Stock thickness')
        self.stock_thickness_label.grid(row=row_num, column=0)
        self.stock_thickness_var = DoubleVar()
        self.stock_thickness_input = Entry(self.EntryFrame, textvariable=self.stock_thickness_var ,width=15)
        self.stock_thickness_input.grid(row=row_num, column=1)

        return self.EntryFrame


    def makePrintButton(self, master, row, parent):
    	self.parent = parent
        self.button_frame = Frame(master)
        self.button_frame.grid(row=row, column=0, columnspan=2)

        row_num = 0
        if IN_AXIS:
            self.printButton = Button(self.button_frame, text='Write to AXIS and Quit',\
                command=self.writeToAxis)
        else:
            self.printButton = Button(self.button_frame, text='Print', command=self.printToConsole)
        self.printButton.grid(row=row_num, column=1, sticky=S)

        return self.button_frame

    def getFeed(self):
        return self.feed_rate_var.get()

    def getSafeZ(self):
    	return self.Z_safe_var.get()

    def getMaxCut(self):
    	return self.cut_per_pass_var.get()

    def getCutter(self):
    	return self.bit_diameter_var.get()

    def getStock(self):
    	return self.stock_thickness_var.get()

    def getAllData(self):
        return int(self.feed_rate_var.get()), int(self.Z_safe_var.get()), self.cut_per_pass_var.get(),\
                   self.bit_diameter_var.get(), self.stock_thickness_var.get()


    def printToConsole(self):
        self.g_code = self.parent.generateCode()
        print self.g_code
        # since self.quit() does not work on OSX
        os._exit(0)


    def writeToAxis(self):
        self.g_code = self.parent.generateCode()
        sys.stdout.write(self.g_code)
        # may want to keep this alive, for writing many similar holes
        # of course if AXIS does not delete the program, then maybe this
        # does work fine for UI
        self.quit()