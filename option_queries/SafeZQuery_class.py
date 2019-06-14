from EntryQuery_class import *

class SafeZQuery(EntryQuery):
    name = 'SafeZQuery'
    options = {
        'name': 'Safe Z',
        'type': DoubleVar,
        'hint': 'What height is safe',
        'default': 80
    }

    def validate(self):
        return self.var.get() > 0
