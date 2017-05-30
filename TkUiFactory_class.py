from Tkinter import *

from SpinboxQuery_class import SpinboxQuery
from EntryQuery_class import EntryQuery

data_types = {
    "string": StringVar,
    "double": DoubleVar,
    "boolean": BooleanVar,
    "integer": IntVar
}
query_types = {
    "spinbox": SpinboxQuery,
    "entry": EntryQuery
}

class TkUIFactory(object):
    def __init__(self):
        pass

    def makeMachinedGeometryEngine(self, machined_geometry_class):
        generator = machined_geometry_class()
        generator.makeQueries(data_types, query_types)
        return generator
