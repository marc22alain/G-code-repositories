import abc

class Observable:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.observers = []

    def registerObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer, message=None):
        o = self.observers.pop(observer)
        if message != None:
            o.notify(message)

    def removeObservers(self, message=None):
        while len(self.observers) > 0:
            o = self.observers.pop()
            if message != None:
                o.notify(message)

    def notifyObservers(self, message):
        for o in self.observers:
            o.notify(message)
