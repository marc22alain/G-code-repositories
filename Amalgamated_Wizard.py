#!/usr/bin/env python

from Tkinter import *
import os
from Canvas_Geometry_classes import *
from Doughnut_Cutter_class import DoughnutCutter
from Setup_class import Setup


IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")


class AmalgamWizard(Frame):
    def __init__(self, master=None):
        self.canvasOptions = {"width":500, "height":500, "bg":"black"}
        Frame.__init__(self, master)
        self.grid()		# TKinter call to arrange the elements
        self.wizards = []   # to hold wizards as the user selects them
        self.createWidgets()
        self.drawGrid()

    def createWidgets(self):
        self.CanvasFrame = Frame(self,bd=5)
        self.CanvasFrame.grid(row=0, column=0)

        self.canvas = Canvas(self.CanvasFrame, self.canvasOptions)
        self.canvas.grid(row=0, column=0)
        # self.drawCanvasGrid()

        self.plotButton = Button(self, text='Plot all geometry', command=self.plotGeometry)
        self.plotButton.grid(row=1, column=0, sticky=S, pady=10)

        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        self.setup_wizard = Setup()
        self.doughnut_wizard = DoughnutCutter(self.EntryFrame, self.setup_wizard)
        self.wizards.append(self.doughnut_wizard)

    def plotGeometry(self):
        c = Circle(57, (0, 0), {"outline":"white"})
        
        canvas_items = [c.draw(self.canvas)]
        for wiz in self.wizards:
        	geo_entities = wiz.makeGeometricEntities()
        	for element in geo_entities:
        		canvas_items.append(element.draw(self.canvas))
        print canvas_items
        print self.canvas.bbox(1)
        # self.canvas.yview_moveto(-250)
        # self.canvas.yview("moveto", 10000.5)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        # self.canvas.move(1, 250, 250)

    def drawGrid(self):
        x_range = self.canvasOptions["width"] / 2
        y_range = self.canvasOptions["height"] / 2
        self.canvas.create_line( - x_range, 0, x_range, 0, tag="grid")
        self.canvas.create_line( 0, - y_range, 0, y_range, tag="grid")
        self.canvas.itemconfig("grid", fill="#555")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))




app = AmalgamWizard()
app.master.title("Amalgamated Wizard 0.9")
app.mainloop()
