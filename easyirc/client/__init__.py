
# -*- coding: utf-8 -*-
import traceback
from .. import util
from ..const import *
from ..model import DataDict
from ..connection import EventHookConnection
from ..socket import Socket
from ..event import EventManager
from ..command import CommandManager
from ..command.client import manager as client_commands
from ..command.interactive import manager as commands
from ..event.protocol import manager as protocol_events

from .. import settings


class BasicClient(DataDict):
    """Basic client implementation, heavily depends on settings."""
    def __init__(self, events=None, cmdmanager=commands, client_cmdmanager=client_commands):
        DataDict.__init__(self)

        self.cmdmanager = client_cmdmanager
        self.connection_cmdmanager = cmdmanager
        self.events = events if events else self._events
        for connopt in settings.connections.values():
            if not connopt.enabled:
                continue
            connection = EventHookConnection(self.events, self.connection_cmdmanager)
            connection.name = connopt.name
            connection.client = self
            self.add(connection)
            self.connection = connection

    @property
    def settings(self):
        """Alias of settings just to avoid import. Good or bad idea?"""
        return settings

    @property
    def connections(self):
        return self.values()

    def cmdln(self, command):
        items = util.cmdsplit(command)
        self.cmd(*items)

    def cmd(self, *items):
        self.cmdmanager(self, *items)

    def __getattr__(self, key):
        """Borrow commands from command manager."""
        cmdmanager = self.__getattribute__('cmdmanager')
        if key in cmdmanager:
            action = cmdmanager[key]
            def call(*args):
                return action(self, *args)
            return call
        try:
            return super.__getattr__(key)
        except AttributeError:
            pass
        try:
            return self.__getattribute__(key)
        except AttributeError:
            pass

    def interactive(self):
        while True:
            try:
                line = raw_input().decode('utf-8')
                if line[0] == '/':
                    cmdln = line[1:]
                    self.cmdln(cmdln)
                elif line[0] == '\\':
                    cmdln = line[1:]
                    self.raw(cmdln)
                else:
                    self.privmsg(line)
            except KeyboardInterrupt:
                break
            except Exception as e:
                traceback.print_exc()


BasicClient._events = _e = EventManager()
BasicClient._events.extends(protocol_events)

@_e.hookmsg(CREATED)
def on_create(connection, sender):
    connopt = settings.connections[connection.name]
    connection.socket = Socket(connopt.addr)
    connection.connect()

@_e.hookmsg(CONNECTED)
def on_connected(connection, sender):
    connopt = settings.connections[connection.name]
    connection.nick(connopt.nick)
    connection.user(connopt.username, connopt.realname)

@_e.hookmsg(ERR_NICKNAMEINUSE, ERR_NICKCOLLISION)
def on_nickerror(connection, *args):
    if not connection.identifier:
        # initial failure
        connopt = settings.connections[connection.name]
        connection.nick(connection.tried_nick + '_')
        connection.user(connopt.username, connopt.realname)

@_e.hookmsg(LOADED)
def on_loaded(connection, *args):
    connopt = settings.connections[connection.name]
    for autojoin in connopt.autojoins:
        connection.join(autojoin)

