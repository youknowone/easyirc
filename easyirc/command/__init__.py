
from .. import util

class CommandManager(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs) # useful? useless?

        def run(sender, *items):
            items = util.CommandLine(items)
            command = self[items.cmd]
            command(sender, *items[1:])
        self['run'] = run # trick!

    def runln(self, connection, command):
        items = util.cmdsplit(command)
        self.run(connection, *items)

    def __call__(self, sender, *items):
        return self['run'](sender, *items)

    def merge(self, manager, override=False):
        for cmd, action in manager.iteritems():
            if not override and cmd in self:
                continue
            self[cmd] = action

    def inherit(self, name, command, strict=True):
        """Works like 'push', but parent is accessible."""
        if name not in self:
            if strict:
                raise KeyError(name)
            parent = None
        else:
            parent = self[name]
        command.super = parent
        self[name] = command

    def disinherit(self, name, strict=True):
        """Works like 'pop'."""
        parent = self[name].super
        if parent:
            self[name] = parent
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

    def override(self, command):
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
    def __init__(self, super=None, category=None):
        self.super = super
        self.category = category

    def __call__(self, manager, *items):
        """Implement to define a command."""
        raise NotImplementedError


class FunctionCommand(BaseCommand):
    def __init__(self, action, super=None, category=None):
        BaseCommand.__init__(self, super, category)
        self.action = action

    def __call__(self, manager, *items):
        return self.action(manager, self.super, *items)


class SoleFunctionCommand(FunctionCommand):
    def __call__(self, manager, *items):
        return self.action(manager, *items)

