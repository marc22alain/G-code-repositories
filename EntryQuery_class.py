from Query_class import Query
import MC_defaults as MC
from Tkinter import *


class EntryQuery(Query):
    def __init__(self, options):
        self.name = options["name"]
        self.type = options["type"]
        try:
            self.default = options["default"]
        except:
            self.default = None
        self.assertValid()

    def assertValid(self):
        assert type(self.name) == type("label"), "'label' argument must be a string"
        assert self.type in [StringVar, DoubleVar, BooleanVar, IntVar], "'type_var' argument must be a TKinter variable class"
        # TODO: work out some simple way to confirm 'self.default' is same as return type from 'self.type'

    def insertQuery(self, master, row_num):
        self.label = Label(master, text=self.name)
        self.label.grid(row=row_num, column=0)
        self.var = self.type()
        self.input = Entry(master, textvariable=self.var, width=13)
        self.input.grid(row=row_num, column=1)
        if self.default is not None:
            self.var.set(self.default)

    def getValue(self):
        return self.var.get()

    def getName(self):
        return self.name
