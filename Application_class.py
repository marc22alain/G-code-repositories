#!/usr/bin/env python
from Tkinter import *

from ViewSpace_class import ViewSpace
from RoundBottomedDado_class import RoundBottomedDado


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
        self.grid()
        self.createSubframes()
        self.createMoreWidgets()
        self.top=self.winfo_toplevel()
        self.top.bind("<Configure>", self.configure)
        self.master.title(self.machined_geometry_engine.name)

    def createSubframes(self):
        self.geo_frame = Frame(self)
        self.geo_frame.grid(row=0, column=0)
        self.view_space = ViewSpace(self.geo_frame, self.machined_geometry_engine.getViewSpaceInit())

        self.entry_frame = Frame(self)
        self.entry_frame.grid(row=0, column=1)

    def createMoreWidgets(self):
        self.queries = []
        self.queries += self.machined_geometry_engine.getDataQueries()

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

        row_num += 1
        self.gen_code = Button(self.entry_frame,text="Refresh view",command=self.generateGcode, width=30)
        self.gen_code.grid(row=row_num, column=0, columnspan=2, pady=5)


    def refreshView(self):
        data = self.extractRowData()
        # example:
        # {'Bottom Radius': 30.0, 'Stock Width - Y': 100.0, 'Maximum cut per pass': 3.0,
        #  'Stock Height - Z': 50.0, 'Cutter diameter': 3.175, 'Stock Length - X': 200.0,
        #  'Safe Z travel height': 100.0, 'Feed rate': 1000.0}
        print data
        geometry = self.machined_geometry_engine.getGeometry(data)
        # example:
        # {'arc': [(20.0, 20.0, 80.0, 80.0, 180, 180)],
        #  'extents': {'width': 100.0, 'center': (50.0, 25.0), 'height': 50.0},
        #  'rectangle': [(0, 0, 100.0, 50.0)]}
        print geometry
        self.view_space.drawGeometry(geometry)


    def showToolPasses(self):
        data = self.extractRowData()
        tool_passes = self.machined_geometry_engine.getToolPasses(data)
        geometry = self.machined_geometry_engine.getGeometry(data)
        self.view_space.drawGeometry(tool_passes, geometry)

    def generateGcode(self):
        pass

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
