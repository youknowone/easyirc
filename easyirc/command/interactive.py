
from . import CommandManager
from .protocol import manager as protocol_manager

manager = CommandManager()
manager.merge(protocol_manager)

@manager.command
def switch(connection, chan):
    connection.channel = chan

@manager.override
def join(connection, super, chan):
    super.run(connection, chan)
    switch.run(connection, chan)

@manager.override
def part(connection, super, chan, reason=None):
    switch(connection, None)
    super.run(connection, chan, reason)

@manager.override
def privmsg(connection, super, chan, msg=None):
    if msg is None:
        chan, msg = connection.channel, chan
    super.run(connection, chan, msg)

@manager.override
def notice(connection, super, msg):
    if msg is None:
        chan, msg = connection.channel, chan
    super.run(connection, chan, msg)