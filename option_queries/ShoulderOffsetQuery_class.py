from EntryQuery_class import *

class ShoulderOffsetQuery(EntryQuery):
    name = 'ShoulderOffsetQuery'
    options = {
        'name': 'Shoulder offset',
        'type': DoubleVar,
        'hint': 'What dimension for the shoulder offset'
    }

    def validate(self):
        return self.var.get() > 0
