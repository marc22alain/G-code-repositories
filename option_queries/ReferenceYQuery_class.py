from EntryQuery_class import EntryQuery
from Tkinter import *

class ReferenceYQuery(EntryQuery):
    name = 'ReferenceYQuery'
    options = {
        'name': 'Reference Y',
        'type': DoubleVar,
        'hint': 'What reference for Y'
    }

    def validate(self):
        return True
