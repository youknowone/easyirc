
from . import CommandManager
from .protocol import manager as protocol_manager

manager = CommandManager()
manager.merge(protocol_manager)

@manager.command
def println(connection, *args):
    print ' '.join(map(str, args))

@manager.command
def switch(connection, chan):
    connection.channel = chan
    connection.println('Switch channel:', chan)

@manager.command
def list(connection):
    connection.println('Opened channels:', *connection.channels.keys())

@manager.override
def join(connection, super, chan):
    super(connection, chan)
    switch(connection, chan)

@manager.override
def part(connection, super, chan, reason=None):
    switch(connection, None)
    super(connection, chan, reason)

@manager.override
def privmsg(connection, super, chan, msg=None):
    if msg is None:
        chan, msg = connection.channel, chan
    super(connection, chan, msg)

@manager.override
def notice(connection, super, chan, msg=None):
    if msg is None:
        chan, msg = connection.channel, chan
    super(connection, chan, msg)