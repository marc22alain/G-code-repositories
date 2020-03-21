class MockCanvas(object):
    """
    Mocks the Tkinter Canvas Widget.
    Private methods (prefixed with `_`) are not part of the Canvas interface.
    """
    def __init__(self):
        self.entities = {}
        self.id_count = 0

    def create_line(self, *params):
        return self._create_item('line')

    def create_arc(self, *args, **kwds):
        return self._create_item('arc')

    def create_oval(self, *args, **kwds):
        return self._create_item('oval')

    def create_rectangle(self, *args, **kwds):
        return self._create_item('rectangle')

    def itemconfig(self, *args, **kwds):
        pass

    def coords(self, *args, **kwds):
        # args is a tuple, and does not include `self`
        self._count_entity_call(args[0], 'coords', args)

    def delete(self, entity_id):
        del self.entities[entity_id]

    def _create_item(self, entity_type):
        self.id_count += 1
        self.entities[self.id_count] = {
            'entity_type': entity_type,
            'calls': {}
        }
        return self.id_count

    def _count_entity_call(self, entity_id, call, args):
        if call not in self.entities[entity_id]['calls'].keys():
            self.entities[entity_id]['calls'][call] = []
        # end up with a list of tuples
        self.entities[entity_id]['calls'][call].append(args)

    def _get_calls_of_call(self, entity_id, call):
        if call not in self.entities[entity_id]['calls'].keys():
            return []
        return self.entities[entity_id]['calls'][call]

    def find_all(self):
        entities = self.entities.values()
        return [entity['entity_type'] for entity in entities]

    def move(self, *args, **kwds):
        pass
