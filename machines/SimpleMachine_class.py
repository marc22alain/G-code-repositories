from option_queries import BitDiameterQuery, FeedRateQuery, QueryManager, SafeZQuery
from utilities import Glib as G

class SimpleMachine(QueryManager):
    name = 'Simple Machine'
    option_query_classes = [
        BitDiameterQuery,
        SafeZQuery,
        FeedRateQuery
    ]

    def __init__(self, feature_manager=None):
        QueryManager.__init__(self)
        self.params = None
        self.feature_manager = feature_manager
        self.mode = None
        # to auto-initialize itself to default values
        # ... all of its option queries have defaults
        self.getOptionQueries()

    def getParams(self):
        params = {
            'bit_diameter': self.option_queries[BitDiameterQuery].getValue(),
            'safe_z': self.option_queries[SafeZQuery].getValue(),
            'feed_rate': self.option_queries[FeedRateQuery].getValue()
        }
        return params

    def setMode(self, mode):
        file_text = ''
        if mode.lower() == 'abs':
            if self.mode != 'abs':
                self.mode = 'abs'
                file_text = G.set_ABS_mode()
        elif mode.lower() == 'incr':
            if self.mode != 'incr':
                self.mode = 'incr'
                file_text = G.set_INCR_mode()
        else:
            raise ValueError('"%s" mode is not handled by SimpleMachine' % (mode))
        return file_text

    def setUpProgram(self):
        feed_rate = self.option_queries[FeedRateQuery].getValue()
        file_text = G.F_rate(feed_rate)
        return file_text

    def endProgram(self):
        file_text = self.setMode('ABS')
        file_text += G.end_program()
        return file_text

    def postQueryUpdateHook(self):
        if self.feature_manager:
            self.feature_manager.reDrawAll()
        self.params = self.getParams()

    def registerFeatureManager(self, feature_manager):
        """Add a feature manager as instance prop, and do other stuff as
        required."""
        self.feature_manager = feature_manager

    def getRepresentationForCollection(self):
        """Creates a dict representation of the FeatureManager's composition."""
        return self.getOptionQueryValues()

    def moveToSafeZ(self):
        if self.params is None:
            self.params = self.getParams()
        file_text = self.setMode('ABS')
        file_text += G.G0_Z(self.params['safe_z'])
        return file_text
