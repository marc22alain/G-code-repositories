#!/usr/bin/env python
from Tkinter import *

from ViewSpace_class import ViewSpace
from RoundBottomedDado_class import RoundBottomedDado
import os
import sys
import time

IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

# Determine the window size
# TODO: generalize to obtain the total view size
#       - is there an event triggered if the TK window is resized


class Application(Frame):
    def __init__(self, master, machined_geometry_class):
        Frame.__init__(self, master)
        self.machined_geometry_engine = machined_geometry_class()
        self.grid()
        self.createSubframes()
        self.createMoreWidgets()
        self.master.title(self.machined_geometry_engine.name)
        # Possible to enable window re-sizing with this
        self.top=self.winfo_toplevel()
        self.top.bind("<Configure>", self.configure)

    def createSubframes(self):
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, self.machined_geometry_engine.getViewSpaceInit())

        self.entry_frame = Frame(self)
        self.entry_frame.grid(row=0, column=1)

    def createMoreWidgets(self):
        self.queries = self.machined_geometry_engine.getDataQueries()

        row_num = 1
        for query in self.queries:
            query.insertQuery(self.entry_frame, row_num)
            row_num += 1

        row_num += 1
        self.refresh_view = Button(self.entry_frame,text="Refresh view",command=self.refreshView, width=30)
        self.refresh_view.grid(row=row_num, column=0, columnspan=2, pady=5)

        if self.machined_geometry_engine.implements_toolpass_view:
            row_num += 1
            self.toolpass_view = Button(self.entry_frame,text="Show tool passes",command=self.showToolPasses, width=30)
            self.toolpass_view.grid(row=row_num, column=0, columnspan=2, pady=5)

        if IN_AXIS:
            output_button_text="Write g-code to AXIS"
            output_button_function = self.writeToAXIS
        else:
            output_button_text="Save g-code to file"
            output_button_function = self.writeToFile
            row_num += 1
            self.file_name_label = Label(self.entry_frame, text='File name')
            self.file_name_label.grid(row=row_num, column=0)
            self.file_name_var = StringVar()
            self.file_name_input = Entry(self.entry_frame, textvariable=self.file_name_var ,width=15)
            self.file_name_input.grid(row=row_num, column=1)

        row_num += 1
        self.output_button = Button(self.entry_frame,text=output_button_text,command=output_button_function, width=30)
        self.output_button.grid(row=row_num, column=0, columnspan=2, pady=5)


    def refreshView(self):
        geometry = self.machined_geometry_engine.getGeometry()
        # example:
        # {'arc': [(20.0, 20.0, 80.0, 80.0, 180, 180)],
        #  'extents': {'width': 100.0, 'center': (50.0, 25.0), 'height': 50.0},
        #  'rectangle': [(0, 0, 100.0, 50.0)]}
        print geometry
        self.view_space.drawGeometry(geometry)


    def showToolPasses(self):
        tool_passes = self.machined_geometry_engine.getToolPasses()
        geometry = self.machined_geometry_engine.getGeometry()
        self.view_space.drawGeometry(tool_passes, geometry)

    def generateGcode(self):
        """
        Delegates the generation of a G-code file.
        """
        return self.machined_geometry_engine.generateGcode()

    def writeToAXIS(self):
        self.g_code = self.generateGcode()
        sys.stdout.write(self.g_code)

    def writeToFile(self):
        self.g_code = self.generateGcode()
        print self.g_code

        file_name = self.file_name_var.get() + ".ngc"
        # If user forgets, or wants the default name:
        if file_name == ".ngc":
            file_name = type(self.machined_geometry_engine).__name__ + "-" + time.ctime() + ".ngc"
        with open(file_name, 'w') as myFile:
            myFile.write(self.g_code)
        # TODO: consider returning it for testing.

    def configure(self, event):
        # print "Configure: %d, %d" % (event.width, event.height)
        # print dir(event)
        pass



def runApp(master, machined_geometry_class):
    app = Application(master, machined_geometry_class)
    # app.master.title("Blank App 0.9")
    app.mainloop()
