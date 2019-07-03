import abc

class AutoObserver:
    __metaclass__ = abc.ABCMeta

    observable = None

    def __init__(self):
        self.observable.registerObserver(self)

    def notify(self, message, *args):
        """
        Receives notifications with optional messages and additional arguments.
        """
        getattr(self, message)(*args)
