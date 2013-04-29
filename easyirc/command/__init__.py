
from .. import util

class CommandManager(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs) # useful? useless?

        self['run'] = self # trick!

    def runln(self, client, command):
        items = util.cmdsplit(command)
        self.run(client, *items)

    def run(self, client, *items):
        if not isinstance(items, util.Line):
            items = util.Line(items)
        command = self[items.cmd]
        command.run(client, *items[1:])

    def inherit(self, name, command, strict=True):
        """Works like 'push', but parent is accessible."""
        if name not in self:
            if strict:
                raise KeyError(name)
            parent = None
        else:
            parent = self[name]
        command.parent = parent
        self[name] = command

    def disinherit(self, name, strict=True):
        """Works like 'pop'."""
        parent = self[name].parent
        if parent:
            self[name] = self[name].parent
        else:
            if strict:
                raise KeyError(name)
            else:
                del(self[name])

    # decorators
    def command(self, command):
        if isinstance(command, BaseCommand):
            self.inherit(command.__name__, command, strict=False)
        elif callable(command):
            name = command.__name__
            command = SoleFunctionCommand(command)
            self[name] = command
        else:
            raise TypeError
        return command

    def inherit(self, command):
        if isinstance(command, BaseCommand):
            self.inherit(command.__name__, command, strict=True)
        elif callable(command):
            name = command.__name__
            command = FunctionCommand(command)
            self.inherit(name, command)
        else:
            raise TypeError
        return command


class BaseCommand(object):
    def __init__(self):
        self.super = None

    def run(self, manager, *items):
        """Implement to define a command."""
        raise NotImplementedError


class FunctionCommand(BaseCommand):
    def __init__(self, action, super=None):
        BaseCommand.__init__(self)
        self.super = super
        self.action = action

    def run(self, manager, *items):
        return self.action(manager, self.super, *items)


class SoleFunctionCommand(FunctionCommand):
    def run(self, manager, *items):
        return self.action(manager, *items)

