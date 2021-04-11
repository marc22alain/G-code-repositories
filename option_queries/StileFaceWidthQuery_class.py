from EntryQuery_class import *

class StileFaceWidthQuery(EntryQuery):
    name = 'StileFaceWidthQuery'
    options = {
        'name': 'Stile face width',
        'type': DoubleVar,
        'hint': 'What dimension for stile face width'
    }

    def validate(self):
        return self.var.get() > 0
