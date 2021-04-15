from EntryQuery_class import *
from utilities import MC

class SafeZQuery(EntryQuery):
    name = 'SafeZQuery'
    options = {
        'name': 'Safe Z',
        'type': DoubleVar,
        'hint': 'What height is safe',
        'default': MC.default_safe_Z
    }

    def validate(self):
        return self.var.get() > 0
