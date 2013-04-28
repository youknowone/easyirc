
#-*- coding: utf-8 -*-

import threading
from .socket import Socket
from . import util

class BaseClient(threading.Thread):
    """Command IRC client interface.
    Any client should support:
        self.socket: any ircsocket
        self.commands: command dictionary
    """

    def runloop_unit(self):
        raise NotImplementedError

    def dispatch(self):
        """Get a message from socket."""
        self.socket.dispatch()

    def run(self):
        """Thread loop."""
        while True:
            self.runloop_unit()

    #command interface
    def cmdln(self, command):
        items = util.cmdsplit(command)
        self.cmd(*items)

    def cmd(self, *items):
        if not isinstance(items, util.Line):
            items = util.Line(items)
        command = self.commands[items.cmd]
        command.run(self, *items[1:])

    def sendraw(self, line, *args, **kwargs):
        self.socket.sendln(line, *args, **kwargs)

    def sendl(self, *args):
        self.socket.cmdl(*args)
    
    def sends(self, *args):
        self.socket.cmds(*args)
    
    def send(self, *args):
        self.socket.cmd(*args)


class DispatchClient(BaseClient):
    """Common IRC Client interface."""

    def __init__(self, sock_or_addr, commands, options=None):
        if isinstance(sock_or_addr, tuple):
            self.socket = Socket(sock_or_addr)
        else:
            self.socket = sock_or_addr
        self.commands = commands
        self.options = options

        BaseClient.__init__(self)

    def runloop_unit(self):
        """NOTE: blocking"""
        self.socket.recv_enqueue()


class CallbackClient(BaseClient):
    """Callback-driven IRC client"""

    def __init__(self, callback, commands, options=None):
        if isinstance(sock_or_addr, tuple):
            self.socket = Socket(sock_or_addr)
        else:
            self.socket = sock_or_addr
        self.socket = None
        self.callback = callback
        self.commands = commands

        BaseClient.__init__(self)

    def runloop_unit(self):
        """NOTE: blocking"""
        msg = self.dispatch()
        if msg is not None:
            self.callback(self, msg)
        else:
            """NOTE: blocking HERE"""
            super(EventClient, self).runloop_unit()


class EventHookClient(CallbackClient):
    def __init__(self, commands, options=None):
        def irc_event(client, message):
            # It is reversed to grant higher priority to new hook
            for hook in reversed(client.hooks):
                result = hook.run(message)
                if result:
                    break
            else:
                self.unhandled(message)
        def unhandled(client, message):
            print 'Unhandled message event:', message
        self.hooks = []
        self.unhandled = unhandled
        CallbackClient.__init__(self, irc_events, commands, options)

