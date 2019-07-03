class PathReferenceError(TypeError):
    """Particular to path reference specificiers."""
    def __init__(self, drawing_entity, path_reference):
        TypeError.__init__(
            self,
            '%s does not implement "%s"' % (drawing_entity.__class__, path_reference)
        )
