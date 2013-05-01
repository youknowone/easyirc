
from ..const import *
from . import CommandManager, BaseCommand

manager = CommandManager()

@manager.command
def connect(client):
    client.connect()

@manager.command
def raw(client, line):
    client.sendraw(line)

@manager.command
def nick(client, nick):
    client.sends(NICK, nick)

@manager.command
def user(client, username, realname):
    client.sendl(USER, username, '*', '0', realname)

@manager.command
def ping(client, tag):
    client.sends(PING, tag)

@manager.command
def pong(client, tag):
    client.sends(PONG, tag)

@manager.command
def join(client, chan):
    client.sends(JOIN, chan)

@manager.command
def part(client, chan, reason=None):
    if reason:
        client.sendl(PART, chan, reason)
    else:
        client.sends(PART, chan)

@manager.command
def quit(client, reason=None):
    if reason:
        client.sendl(QUIT, reason)
    else:
        client.sends(QUIT)

@manager.command
def privmsg(client, target, msg):
    client.sendl(PRIVMSG, target, msg)

@manager.command
def notice(client, target, msg):
    client.sendl(PRIVMSG, target, msg)


for command in manager.values():
    command.category = 'protocol'
