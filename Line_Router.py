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
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        self.st00 = Label(self.EntryFrame, text='Route a slot')
        self.st00.grid(row=0, column=0, columnspan=2)

        # not sure about this behaviour
        if IN_AXIS:
            self.printButton = Button(self, text='Write to AXIS and Quit',\
                command=self.WriteToAxis)
        else:
            self.printButton = Button(self, text='Print', command=self.Print)
        self.printButton.grid(row=13, column=1, sticky=S)

        self.alignButton = Button(self, text='Present options', command=self.AlignOptions)
        self.alignButton.grid(row=12, column=1, sticky=S)
        

        self.st01 = Label(self.EntryFrame, text='Safe Z travel height')
        self.st01.grid(row=1, column=0)
        self.Z_safe_var = StringVar()
        self.Z_safe = Entry(self.EntryFrame, textvariable=self.Z_safe_var ,width=15)
        self.Z_safe.grid(row=1, column=1)
        self.Z_safe.insert(0, default_safe_Z)

        self.st02 = Label(self.EntryFrame, text='Stock thickness')
        self.st02.grid(row=2, column=0)
        self.stock_thickness_var = IntVar()
        self.stock_thickness = Entry(self.EntryFrame, textvariable=self.stock_thickness_var ,width=15)
        self.stock_thickness.grid(row=2, column=1)

        self.st03 = Label(self.EntryFrame, text='Maximum cut per pass')
        self.st03.grid(row=3, column=0)
        self.cut_depth_var = IntVar()
        self.cut_depth = Entry(self.EntryFrame, textvariable=self.cut_depth_var ,width=15)
        self.cut_depth.grid(row=3, column=1)

        self.st04 = Label(self.EntryFrame, text='Cutter diameter')
        self.st04.grid(row=4, column=0)
        self.bit_diameter_var = DoubleVar()
        self.bit_diameter = Spinbox(self.EntryFrame, values=bits, textvariable=self.bit_diameter_var, width=13)
        self.bit_diameter.grid(row=4, column=1)

        self.st05 = Label(self.EntryFrame, text='Slot width')
        self.st05.grid(row=5, column=0)
        self.slot_width_var = IntVar()
        self.slot_width = Entry(self.EntryFrame, textvariable=self.slot_width_var ,width=15)
        self.slot_width.grid(row=5, column=1)
        self.slot_width.insert(0, self.bit_diameter_var.get())

        self.st06 = Label(self.EntryFrame, text='Slot depth')
        self.st06.grid(row=6, column=0)
        self.slot_depth_var = IntVar()
        self.slot_depth = Entry(self.EntryFrame, textvariable=self.slot_depth_var ,width=15)
        self.slot_depth.grid(row=6, column=1)

        self.st07 = Label(self.EntryFrame, text='Starting coordinates')
        self.st07.grid(row=7, column=0)
        self.start_coords_as_string = StringVar()
        self.start_coords = Entry(self.EntryFrame, textvariable=self.start_coords_as_string ,width=15)
        self.start_coords.grid(row=7, column=1)

        self.st08 = Label(self.EntryFrame, text='Ending coordinates')
        self.st08.grid(row=8, column=0)
        self.end_coords_as_string = StringVar()
        self.end_coords = Entry(self.EntryFrame, textvariable=self.end_coords_as_string ,width=15)
        self.end_coords.grid(row=8, column=1)

        self.st09 = Label(self.EntryFrame, text='Feed rate')
        self.st09.grid(row=9, column=0)
        self.feed_rate_var = StringVar()
        self.feed_rate = Entry(self.EntryFrame, textvariable=self.feed_rate_var ,width=15)
        self.feed_rate.grid(row=9, column=1)
        self.feed_rate.insert(0, default_feed_rate)

        print self.bit_diameter_var.get()


    def GenerateCode(self):
        start_coords_as_list_string = self.start_coords_as_string.get().split(',')
        end_coords_as_list_string = self.end_coords_as_string.get().split(',')
        start_coords = (float(start_coords_as_list_string[0]), float(start_coords_as_list_string[1]))
        end_coords = (float(end_coords_as_list_string[0]), float(end_coords_as_list_string[1]))
        self.g_code = G.route_line(int(self.Z_safe_var.get()),
                          self.stock_thickness_var.get(),
                          self.cut_depth_var.get(),
                          self.bit_diameter_var.get(),
                          start_coords,
                          end_coords,
                          int(self.feed_rate_var.get()))


    def Print(self):
        self.GenerateCode()
        print self.g_code
        # since self.quit() does not work on OSX
        os._exit(0)


    def AlignOptions(self):
        start_coords_as_list_string = self.start_coords_as_string.get().split(',')
        end_coords_as_list_string = self.end_coords_as_string.get().split(',')
        start_coords = (float(start_coords_as_list_string[0]), float(start_coords_as_list_string[1]))
        end_coords = (float(end_coords_as_list_string[0]), float(end_coords_as_list_string[1]))
        if abs(end_coords[0] - start_coords[0]) > abs(end_coords[1] - start_coords[1]):
            radio_options = ['-Y','=Y','+Y']
        else:
            radio_options = ['-X','=X','+X']
        self.st11 = Label(self.EntryFrame, text='Side of line to cut')
        self.st11.grid(row=11, column=0)        
        self.DirectionVar = IntVar()
        Radiobutton(self.EntryFrame, text=radio_options[0], value=0, variable=self.DirectionVar)\
            .grid(row=11, column=1, sticky = W)
        Radiobutton(self.EntryFrame, text=radio_options[0], value=1, variable=self.DirectionVar)\
            .grid(row=11, column=1)
        Radiobutton(self.EntryFrame, text=radio_options[0], value=2, variable=self.DirectionVar)\
            .grid(row=11, column=1, sticky = E)
        print self.bit_diameter_var.get()


    def WriteToAxis(self):
        self.GenerateCode()
        sys.stdout.write(self.g_code)
        # may want to keep this alive, for writng many similar holes
        # of course if AXIS does not delete the program, then maybe this
        # does work fine for UI
        self.quit()


app = Application()
app.master.title("Line Router 0.1")
app.mainloop() 
