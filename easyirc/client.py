
# -*- coding: utf-8 -*-
import traceback
from . import util
from .const import *
from .model import DataDict
from .connection import EventHookConnection
from .socket import Socket
from .event import EventManager
from .command import CommandManager
from .command.client import manager as client_commands
from .command.interactive import manager as commands
from .event.protocol import manager as protocol_events

from . import settings

events = EventManager()
events.extends(protocol_events)

if settings.RAW_LOG:
    @events.hookglobal
    def log(connection, message):
        print '<', message

@events.hookmsg(CREATED)
def on_create(connection, sender):
    connopt = settings.connections[connection.name]
    connection.socket = Socket(connopt.addr)
    connection.connect()

@events.hookmsg(CONNECTED)
def on_connected(connection, sender):
    connopt = settings.connections[connection.name]
    connection.nick(connopt.nick)
    connection.user(connopt.username, connopt.realname)

@events.hookmsg(LOADED)
def on_loaded(connection, *args):
    connopt = settings.connections[connection.name]
    for autojoin in connopt.autojoins:
        connection.join(autojoin)


class BasicClient(DataDict):
    def __init__(self, cmdmanager=commands, client_cmdmanager=client_commands):
        DataDict.__init__(self)

        self.cmdmanager = client_cmdmanager
        self.connection_cmdmanager = cmdmanager
        for connopt in settings.connections.values():
            if not connopt.enabled:
                continue
            connection = EventHookConnection(events, commands)
            connection.name = connopt.name
            connection.client = self
            self.add(connection)

    @property
    def settings(self):
        return settings

    @property
    def connections(self):
        return self.values()

    def cmdln(self, command):
        items = util.cmdsplit(command)
        self.cmd(*items)

    def cmd(self, *items):
        if items[0] in self.cmdmanager:
            self.cmdmanager.run(self, *items)
        elif self.connection is not None:
            connection = self.connection
            connection.cmdmanager.run(connection, *items)
        else:
            raise KeyError(items[0])

    def __getattr__(self, key):
        """Borrow commands from command manager."""
        cmdmanager = self.__getattribute__('cmdmanager')
        if key in cmdmanager:
            action = cmdmanager[key].run
            def call(*args):
                return action(self, *args)
            return call
        connection = self.__getattribute__('connection')
        if connection is not None and key in connection.cmdmanager:
            action = connection.cmdmanager[key].run
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