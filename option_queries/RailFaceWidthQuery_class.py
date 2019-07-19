from EntryQuery_class import *

class RailFaceWidthQuery(EntryQuery):
    name = 'RailFaceWidthQuery'
    options = {
        'name': 'Rail face width',
        'type': DoubleVar,
        'hint': 'What dimension for rail face width'
    }

    def validate(self):
        return self.var.get() > 0
