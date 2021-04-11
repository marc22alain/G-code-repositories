from EntryQuery_class import *

class FeedRateQuery(EntryQuery):
    name = 'FeedRateQuery'
    options = {
        'name': 'Feed rate',
        'type': IntVar,
        'hint': 'What feed rate',
        'default': 1000
    }

    def validate(self):
        return self.var.get() > 0
