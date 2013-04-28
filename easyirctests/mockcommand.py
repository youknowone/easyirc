
from easyirc.command import CommandManager

class MockCommandManager(CommandManager):
    def __init__(self, client, commands):
        self.cmdbuffer = []

        CommandManager.__init__(self, client, commands)

    def cmd(self, *args):
        self.cmdbuffer.append(u' '.join(args))

    def cmdl(self, *args):
        self.cmdbuffer.append(u' '.join(list(args[:-1]) + [u':' + args[-1]]))
