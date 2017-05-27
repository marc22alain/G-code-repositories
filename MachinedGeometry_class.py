import abc


class MachinedGeometry:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getViewSpaceInit(self):
        pass

    @abc.abstractmethod
    def assertValid(self):
        pass

    @abc.abstractmethod
    def getDataQueries(self):
    	"""
    	Returns a list of instantiated Query objects.
        These are part of the data model, even if they get passed back and
        forth with the controller.
    	"""
        pass

    @abc.abstractmethod
    def getToolPasses(self):
        """
        Actually turns out to be optional.
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
