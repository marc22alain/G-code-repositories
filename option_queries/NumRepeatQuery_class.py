from EntryQuery_class import *

class NumRepeatQuery(EntryQuery):
    name = 'NumRepeatQuery'
    options = {
        'name': 'Number of repeats',
        'type': IntVar,
        'hint': 'How many repeats'
    }

    def validate(self):
        return self.var.get() > 0
