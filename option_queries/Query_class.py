import abc

class Query:
    __metaclass__ = abc.ABCMeta

    '''
    Instantiated with sub-class's options dict:
    {
        'name' - required
        'type' - required
        'default' - optional
    }
    '''
    def __init__(self):
        self.assertValidInit()
        self.var = self.options["type"]()
        if "default" in self.options:
            self.value = self.options["default"]
        else:
            self.value = 0

    def getValue(self):
        return self.value

    def setValue(self, value):
        print '* * *** * * ** * ** **     ran setValue !     * * *** * * ** * *'
        self.value = value
        return self.var.set(value)

    def updateValue(self):
        print 'will update value'
        self.value = self.var.get()

    def getName(self):
        return self.options["name"]

    @abc.abstractmethod
    def assertValidInit(self):
        pass

    @abc.abstractmethod
    def insertQuery(self, master, row_num):
        pass

    @abc.abstractmethod
    def validate(self):
        '''
        Intended to validate user input.
        '''
        pass
