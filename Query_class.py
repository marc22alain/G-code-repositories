import abc

class Query:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def assertValid(self):
        pass

    @abc.abstractmethod
    def insertQuery(self, master, row_num):
        pass

    @abc.abstractmethod
    def getData(self):
        pass

    @abc.abstractmethod
    def getName(self):
        pass
