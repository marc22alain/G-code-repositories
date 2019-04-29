import abc

class Query:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def assertValidInit(self):
        pass

    @abc.abstractmethod
    def insertQuery(self, master, row_num):
        pass

    @abc.abstractmethod
    def getValue(self):
        pass

    @abc.abstractmethod
    def getName(self):
        pass

    @abc.abstractmethod
    def validate(self):
        '''
        Intended to validate user input.
        '''
        pass
