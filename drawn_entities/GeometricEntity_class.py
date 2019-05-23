"""
GeometricEntity sets the pattern for wrapping TKinter canvas classes.
"""

import abc

class GeometricEntity:
    __metaclass__ = abc.ABCMeta

    def __init__(self, view_space):
        self.view_space = view_space
        self.id = None

    @abc.abstractmethod
    def assertValid(self):
        """ Check data when setting the entity's parameters,
        or immediately in the call to draw(). """
        pass

    def setParams(self, params, options):
        """ *params is simply a series of parameters as would be expected by the wrapped class. """
        self._setParams(params)
        self.setOptions(options)
        return self

    @abc.abstractmethod
    def _setParams(self, *params):
        """ *params is simply a series of parameters as would be expected by the wrapped class. """
        pass

    def draw(self, view_plane = 'XY'):
        if self.id != None:
            self._update()
        else:
            self.id = self._draw()
            self.applyOptions()
        return self

    @abc.abstractmethod
    def _draw(self):
        '''
        Must return the result of a canvas.create_<entity> call.
        '''
        pass

    @abc.abstractmethod
    def _update():
        pass

    def setOptions(self, options):
        """ options is an object. """
        self.options = options
        return self

    def applyOptions(self):
        """ Used as the last step in the draw() method.
        TODO: expand to cover all possible options. """
        canvas = self.view_space.canvas
        keys = self.options.keys()
        if "fill" in keys:
            canvas.itemconfig(self.id, fill=self.options["fill"])
        if "outline" in keys:
            canvas.itemconfig(self.id, outline=self.options["outline"])
        if "tag" in keys:
            canvas.itemconfig(self.id, tag=self.options["tag"])
        if "arrow" in keys:
            canvas.itemconfig(self.id, arrow=self.options["arrow"])
        if "dash" in keys:
            canvas.itemconfig(self.id, dash=self.options["dash"])
        if "width" in keys:
            canvas.itemconfig(self.id, width=self.options["width"])
        # if "style" in keys:
        #     canvas.itemconfig(self.id, tag=self.options["style"])
        return self

    def remove(self):
        self.view_space.canvas.delete(self.id)
        self.id = None
