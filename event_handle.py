class EventHandle:
    def __init__(self):
        self.handles = {}

    def add_handle(self, event, handle):
        self.handles[event] = handle

    def process_events(self, event):
        if event in self.handles:
            return self.handles[event]
