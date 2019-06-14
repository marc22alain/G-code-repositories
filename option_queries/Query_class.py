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
        # Is used to set/get query dialog data.
        self.var = self.options["type"]()
        # Is the Query's stored data.
        if "default" in self.options:
            self.value = self.options["default"]
        else:
            # May get bugs here:
            self.value = 0

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def updateValue(self):
        '''
        Update from query dialog.
        '''
        self.value = self.var.get()

    def getName(self):
        return self.options["name"]

    @abc.abstractmethod
    def assertValidInit(self):
        pass

    @abc.abstractmethod
    def insertQuery(self, master, row_num):
        '''
        Insert into query dialogs.
        '''
        pass

    @abc.abstractmethod
    def validate(self):
        '''
        Intended to validate user input.
        '''
        pass
