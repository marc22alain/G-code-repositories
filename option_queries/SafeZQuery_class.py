from EntryQuery_class import EntryQuery
from Tkinter import *

class SafeZQuery(EntryQuery):
    name = 'SafeZQuery'
    options = {
        'name': 'Safe Z',
        'type': DoubleVar,
        'hint': 'What height is safe',
        'default': 80
    }

    def validate(self):
        return self.getValue() > 0
