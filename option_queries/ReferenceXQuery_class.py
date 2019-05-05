from EntryQuery_class import EntryQuery
from Tkinter import *

class ReferenceXQuery(EntryQuery):
    name = 'ReferenceXQuery'
    options = {
        'name': 'Reference X',
        'type': DoubleVar,
        'hint': 'What reference for X'
    }

    def validate(self):
        return True
