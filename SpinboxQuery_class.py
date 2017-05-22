from Query_class import Query
import MC_defaults as MC
from Tkinter import *


class SpinboxQuery(Query):
    def __init__(self, options):
        self.name = options["name"]
        self.type = options["type"]
        self.values = options["values"]
        self.assertValid()

    def assertValid(self):
        assert type(self.name) == type("label"), "'label' argument must be a string"
        assert self.type in [StringVar, DoubleVar, BooleanVar, IntVar], "'type_var' argument must be a TKinter variable class"
        assert type(self.values) == type(()), "'values' argument must be a tuple"

    def insertQuery(self, master, row_num):
        self.label = Label(master, text=self.name)
        self.label.grid(row=row_num, column=0)
        self.var = self.type()
        self.input = Spinbox(master, values=self.values, textvariable=self.var, width=13)
        self.input.grid(row=row_num, column=1)

    def getData(self):
        return self.var.get()

    def getName(self):
        return self.name
