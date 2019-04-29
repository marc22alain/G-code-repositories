from Query_class import Query
# import MC_defaults as MC
from Tkinter import *


class SpinboxQuery(Query):
    '''
    Instantiated with sub-class's options dict:
    {
        'name' - required
        'type' - required
        'values' - required
        'default' - optional
    }
    '''
    def __init__(self):
        self.assertValidInit()

    def assertValidInit(self):
        assert type(self.options["name"]) == type("label"), "'label' argument must be a string"
        assert self.options["type"] in [StringVar, DoubleVar, BooleanVar, IntVar], "'type_var' argument must be a TKinter variable class"
        assert type(self.options["values"]) == type(()), "'values' argument must be a tuple"

    def insertQuery(self, master, row_num):
        self.label = Label(master, text=self.options["name"])
        self.label.grid(row=row_num, column=0)
        self.var = self.options["type"]()
        self.input = Spinbox(master, values=self.options["values"], textvariable=self.var, width=13)
        self.input.grid(row=row_num, column=1)

    def getValue(self):
        return self.var.get()

    def getName(self):
        return self.options["name"]

    def validate(self):
        # Can only select from pre-approved choices
        return True

