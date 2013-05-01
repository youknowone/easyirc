
from . import CommandManager
from .protocol import manager as protocol_manager

manager = CommandManager()
manager.merge(protocol_manager)

@manager.command
def switch(client, chan):
    client.channel = chan

@manager.override
def join(client, super, chan):
    super.run(client, chan)
    switch.run(client, chan)

@manager.override
def part(client, super, chan, reason=None):
    switch(client, None)
    super.run(client, chan, reason)

@manager.override
def privmsg(client, super, msg):
    super.run(client, client.channel, msg)

@manager.override
def notice(client, super, msg):
    super.run(client, client.channel, msg)