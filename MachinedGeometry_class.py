import abc


class MachinedGeometry:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def assertValid(self):
        pass

    @abc.abstractmethod
    def getDataQueries(self):
    	"""
    	Returns a list of dicts characterizing the DataQueries.
    	It may be useful to also make them a class.
    	"""
        pass

    @abc.abstractmethod
    def getGeometry(self, data):
        pass

    @abc.abstractmethod
    def assertValid(self, data):
        pass

    @abc.abstractmethod
    def _makeEntryQueries():
        pass
