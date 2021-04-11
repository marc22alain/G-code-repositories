from EntryQuery_class import *

class DeltaYQuery(EntryQuery):
    name = 'DeltaYQuery'
    options = {
        'name': 'Delta Y',
        'type': DoubleVar,
        'hint': 'What delta for Y'
    }

    def validate(self):
        return True
