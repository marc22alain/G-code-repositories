from EntryQuery_class import *

class SideYQuery(EntryQuery):
    name = 'SideYQuery'
    options = {
        'name': 'Side Y',
        'type': DoubleVar,
        'hint': 'What dimension for side Y'
    }

    def validate(self):
        return self.getValue() > 0
