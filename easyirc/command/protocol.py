
from ..const import *
from . import BaseCommand

commands = {}

def _add(action):
    command = BaseCommand(action)
    commands[action.__name__] = command
    return command

@_add
def connect(client):
    client.connect()

@_add
def raw(client, line):
    client.sendraw(line)

@_add
def ping(client, tag):
    client.sends(PING, tag)

@_add
def join(client, chan):
    client.sends(JOIN, chan)

@_add
def part(client, chan, reason=None):
    if reason:
        client.sendl(PART, chan, reason)
    else:
        client.sends(PART, chan)

@_add
def quit(client, reason=None):
    if reason:
        client.sendl(QUIT, reason)
    else:
        client.sends(QUIT)

@_add
def privmsg(client, target, msg):
    client.sendl(PRIVMSG, target, msg)

@_add
def notice(client, target, msg):
    client.sendl(PRIVMSG, target, msg)

