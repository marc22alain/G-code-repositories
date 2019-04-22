import abc


class MachinedGeometry:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def makeQueries(self, data_types, query_types):
        """
        Permits abstraction of the UI library.
        """
        pass

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
    def getGeometry(self):
        """
        Returns a dict:
        {
            "entities": [],
            "extents": {"width": float, "height": float, "center": (float, float)}
        }
        """
        pass

    @abc.abstractmethod
    def generateGcode(self):
        pass
