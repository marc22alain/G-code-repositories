class QueryManager(object):
    """Provides the interface for instantiating, retrieving, setting and
    changing values stored by option queries."""
    option_query_classes = []

    def __init__(self):
        self.option_queries = {key: None for key in self.option_query_classes}

    def getOptionQueries(self):
        """Retrieves option queries; instantiates them if not already created."""
        if None in self.option_queries.values():
            self.option_queries = { key: key() for key in self.option_query_classes }
        return self.option_queries.values()

    def didUpdateQueries(self):
        """A callback to call when the owner's parameters are changed, to
        trigger other changes."""
        if hasattr(self, 'preQueryUpdateHook'):
            self.preQueryUpdateHook()

        for query in self.option_queries.values():
            query.updateValue()

        if hasattr(self, 'postQueryUpdateHook'):
            self.postQueryUpdateHook()
