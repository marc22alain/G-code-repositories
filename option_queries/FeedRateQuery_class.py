from EntryQuery_class import *
from utilities import MC

class FeedRateQuery(EntryQuery):
    name = 'FeedRateQuery'
    options = {
        'name': 'Feed rate',
        'type': IntVar,
        'hint': 'What feed rate',
        'default': MC.default_feed_rate
    }

    def validate(self):
        return self.var.get() > 0
