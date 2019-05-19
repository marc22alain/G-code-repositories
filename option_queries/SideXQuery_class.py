from EntryQuery_class import *

class SideXQuery(EntryQuery):
    name = 'SideXQuery'
    options = {
        'name': 'Side X',
        'type': DoubleVar,
        'hint': 'What dimension for side X'
    }

    def validate(self):
        return self.getValue() > 0
