"""
GeometricEntity sets the pattern for wrapping TKinter canvas classes.
"""

import abc
from utilities import log

class GeometricEntity:
    """The abstract class for entities drawn to the Tkinter canvas."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, view_space):
        self.options = None
        self.view_space = view_space
        self.ids = []

    @abc.abstractmethod
    def assertValid(self):
        """ Check data when setting the entity's parameters,
        or immediately in the call to draw(). """
        pass

    @abc.abstractmethod
    def getParams(self):
        """Get the standard parameters."""
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

    def draw(self):
        """Draw the entities to the canvas."""
        if self.ids:
            self._update()
        else:
            self.ids = self._draw()
            self.applyOptions()
        return self

    @abc.abstractmethod
    def _draw(self):
        """Must return the result of a canvas.create_<entity> call."""
        pass

    @abc.abstractmethod
    def _update(self):
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
        for i_d in self.ids:
            if "fill" in keys:
                canvas.itemconfig(i_d, fill=self.options["fill"])
            if "outline" in keys:
                try:
                    canvas.itemconfig(i_d, outline=self.options["outline"])
                except:
                    # because create_line() can't be configured with outline option
                    canvas.itemconfig(i_d, fill=self.options["outline"])
            if "tag" in keys:
                canvas.itemconfig(i_d, tag=self.options["tag"])
            if "arrow" in keys:
                canvas.itemconfig(i_d, arrow=self.options["arrow"])
            if "dash" in keys:
                canvas.itemconfig(i_d, dash=self.options["dash"])
            if "width" in keys:
                canvas.itemconfig(i_d, width=self.options["width"])
            if "style" in keys:
                try:
                    canvas.itemconfig(i_d, style=self.options["style"])
                except:
                    pass
        return self

    def remove(self):
        """Remove drawn entities from the canvas,
        and delete them from own data structures."""
        for i_d in self.ids:
            self.view_space.canvas.delete(i_d)
        self.ids = []

    def move(self, params):
        """Move drawn entities in the canvas."""
        log('GeometricEntity move()')
        view_scale = self.view_space.view_scale
        if self.view_space.view_plane == 'XY':
            move_X = params['delta_X']
            move_Y = params['delta_Y']
        elif self.view_space.view_plane == 'YZ':
            move_X = params['delta_Y']
            move_Y = 0
        else:
            move_X = params['delta_X']
            move_Y = 0

        for i_d in self.ids:
            # TODO: leaky abstraction, also make this a lambda !
            self.view_space.canvas.move(i_d, view_scale * move_X, - view_scale * move_Y)
