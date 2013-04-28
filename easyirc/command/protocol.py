
from ..const import *
from . import BaseCommand

commands = {}

def _add(action):
    command = BaseCommand(action)
    commands[action.__name__] = command
    return command

@_add
def connect(manager):
    manager.connect()

@_add
def raw(manager, line):
    manager.socket.sendln(line)

@_add
def ping(manager, tag):
    manager.cmd(PING, tag)

@_add
def join(manager, chan):
    manager.cmd(JOIN, chan)

@_add
def part(manager, chan, reason=None):
    if reason:
        manager.cmdl(PART, chan, reason)
    else:
        manager.cmd(PART, chan)

@_add
def quit(manager, reason=None):
    if reason:
        manager.cmdl(QUIT, reason)
    else:
        manager.cmd(QUIT)

@_add
def privmsg(manager, target, msg):
    manager.cmdl(PRIVMSG, target, msg)

@_add
def notice(manager, target, msg):
    manager.cmdl(PRIVMSG, target, msg)
