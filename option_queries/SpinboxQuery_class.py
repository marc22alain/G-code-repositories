from Tkinter import *
from Query_class import Query
# import MC_defaults as MC


class SpinboxQuery(Query):

    def assertValidInit(self):
        assert type(self.options["name"]) == type("label"), "'label' argument must be a string"
        assert self.options["type"] in [StringVar, DoubleVar, BooleanVar, IntVar], "'type_var' argument must be a TKinter variable class"
        assert type(self.options["values"]) == type(()), "'values' argument must be a tuple"

    def insertQuery(self, master, row_num):
        self.label = Label(master, text=self.options["name"])
        self.label.grid(row=row_num, column=0)
        # this resets the associated variable, so must elsewhere store the previously chosen value,
        # then restore after defining
        self.input = Spinbox(master, values=self.options["values"], textvariable=self.var, width=13)
        self.input.grid(row=row_num, column=1)
        self.var.set(self.value)

    def validate(self):
        # Can only select from pre-approved choices
        return True
