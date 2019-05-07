from Tkinter import *
from Query_class import Query


class EntryQuery(Query):
    '''
    Instantiated with sub-class's options dict:
    {
        'name' - required
        'type' - required
        'default' - optional
    }
    '''
    def __init__(self):
        self.assertValidInit()
        self.var = self.options["type"]()
        if "default" in self.options:
            self.var.set(self.options["default"])

    def assertValidInit(self):
        assert type(self.options["name"]) == type("label"), "'label' argument must be a string"
        assert self.options["type"] in [StringVar, DoubleVar, BooleanVar, IntVar], "'type_var' argument must be a TKinter variable class"
        # TODO: work out some simple way to confirm 'self.options["default"]' is same as return type from 'self.options["type"]'

    def insertQuery(self, master, row_num):
        self.label = Label(master, text=self.options["name"])
        self.label.grid(row=row_num, column=0)
        self.input = Entry(master, textvariable=self.var, width=13)
        self.input.grid(row=row_num, column=1)

    def getValue(self):
        return self.var.get()

    def getName(self):
        return self.options["name"]

    def setValue(self, value):
        return self.var.set(value)
