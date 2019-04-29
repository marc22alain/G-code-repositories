from SpinboxQuery_class import SpinboxQuery
from Tkinter import *


class GeometricFeatureQuery(SpinboxQuery):
    name = 'GeometricFeatureQuery'


    def __init__(self):
        # delaying the import to avoid circular imports
        # ... which occurs since we want recursive structures of super-features and features
        from features import classes_dict
        self.classes_dict = classes_dict
        self.options = {
            'name': 'Feature',
            'type': StringVar,
            'values': tuple(classes_dict.keys()),
            'hint': 'What feature to make'
        }
        SpinboxQuery.__init__(self)

    def getValue(self):
        # translate from string to feature class
        return self.classes_dict[self.var.get()]
