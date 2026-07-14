class RenderCommand:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
    def execute(self):
        self.function(*self.args, **self.kwargs)
class RenderBatch:
    def __init__(self):
        self._commands = []
    def add(self, function, *args, **kwargs):
        self._commands.append(RenderCommand(function,*args,**kwargs, ))
    def render(self):
        for command in self._commands:
            command.execute()
    def clear(self):
        self._commands.clear()
    def size(self):
        return len(self._commands)
    def empty(self):
        return len(self._commands) == 0