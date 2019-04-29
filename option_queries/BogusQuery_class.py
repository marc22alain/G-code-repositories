from EntryQuery_class import EntryQuery
from Tkinter import *

class BogusQuery(EntryQuery):
    name = 'BogusQuery'
    options = {
        'name': 'Bogus Q',
        'type': StringVar,
        'hint': 'What story to make up'
    }

    def validate(self):
        return len(self.getValue()) > 0
