from EntryQuery_class import *

class DeltaXQuery(EntryQuery):
    name = 'DeltaXQuery'
    options = {
        'name': 'Delta X',
        'type': DoubleVar,
        'hint': 'What delta for X'
    }

    def validate(self):
        return True
