
from ..const import *
from . import CommandManager, BaseCommand

manager = CommandManager()

@manager.command
def connect(connection):
    connection.connect()

@manager.command
def raw(connection, line):
    connection.sendraw(line)

@manager.command
def sendl(connection, *args):
    connection.sendl(*args)

@manager.command
def sends(connection, *args):
    connection.sends(*args)

@manager.command
def nick(connection, nick):
    connection.tried_nick = nick
    connection.sends(NICK, nick)

@manager.command
def user(connection, username, realname):
    connection.sendl(USER, username, '*', '0', realname)

@manager.command
def ping(connection, tag):
    connection.sends(PING, tag)

@manager.command
def pong(connection, tag):
    connection.sends(PONG, tag)

@manager.command
def join(connection, chan):
    connection.sends(JOIN, chan)

@manager.command
def part(connection, chan, reason=None):
    if reason:
        connection.sendl(PART, chan, reason)
    else:
        connection.sends(PART, chan)

@manager.command
def quit(connection, reason=None):
    connection.quitting = True
    if reason:
        connection.sendl(QUIT, reason)
    else:
        connection.sends(QUIT)

@manager.command
def privmsg(connection, target, msg):
    connection.sendl(PRIVMSG, target, msg)

@manager.command
def notice(connection, target, msg):
    connection.sendl(NOTICE, target, msg)


for command in manager.values():
    command.category = 'protocol'
