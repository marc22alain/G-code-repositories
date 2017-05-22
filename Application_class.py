#!/usr/bin/env python
from Tkinter import *

from ViewSpace_class import ViewSpace
from Setup_class import Setup
from RoundBottomedDado_class import RoundBottomedDado
import MC_defaults as MC
from SpinboxQuery_class import SpinboxQuery
from EntryQuery_class import EntryQuery


# Determine the window size
# TODO: generalize to obtain the total view size
#       - is there an event triggered if the TK window is resized
canvas_options = {"width":500, "height":500, "bg":"black"}
# Note that scale is currently 1:1
grid_options = {"grid_spacing": 50, "canW": canvas_options["width"], "canH": canvas_options["height"], "margin": 0}


class Application(Frame):
    def __init__(self, master, machined_geometry_class):
        Frame.__init__(self, master)
        self.machined_geometry_engine = machined_geometry_class()
        self.setup = Setup()
        self.grid()
        self.createSubframes()
        self.createMoreWidgets()
        self.top=self.winfo_toplevel()
        self.top.bind("<Configure>", self.configure)
        self.master.title(self.machined_geometry_engine.name)

    def createSubframes(self):
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, canvas_options, grid_options)

        self.entry_frame = Frame(self)
        self.entry_frame.grid(row=0, column=1)

    def createMoreWidgets(self):
        # TODO: generalize this method to import a purpose-built class
        queries = [{"name":"Feed rate", "type":DoubleVar, "default":MC.default_feed_rate, "input_type": EntryQuery}, \
                        {"name":"Safe Z travel height", "type":DoubleVar, "default":MC.default_safe_Z, "input_type": EntryQuery}, \
                        {"name":"Maximum cut per pass", "type":DoubleVar, "input_type": EntryQuery}, \
                        {"name":"Cutter diameter", "type":DoubleVar, "input_type": SpinboxQuery, "values":MC.bits}]

        self.queries = []
        for query in queries:
            self.queries.append(query["input_type"](query))

        self.queries += self.machined_geometry_engine.getDataQueries()

        row_num = 1
        for query in self.queries:
            query.insertQuery(self.entry_frame, row_num)
            row_num += 1

        row_num += 1
        self.refresh_view = Button(self.entry_frame,text="Refresh_view",command=self.refreshView, width=30)
        self.refresh_view.grid(row=row_num, column=0, columnspan=2, pady=5)

    def refreshView(self):
        print self.extractRowData()

    def extractRowData(self):
        data = {}
        for query in self.queries:
            data[query.getName()] = query.getData()
        return data


    def configure(self, event):
        # print "Configure: %d, %d" % (event.width, event.height)
        # print dir(event)
        pass



def runApp(master, machined_geometry_class):
    app = Application(master, machined_geometry_class)
    # app.master.title("Blank App 0.9")
    app.mainloop()
