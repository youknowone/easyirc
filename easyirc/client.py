
#-*- coding: utf-8 -*-

import threading
from .const import *
from .socket import BaseSocket
from . import util

class NoneSocket(BaseSocket):
    def __init__(self, addr, charset='utf-8'):
        self.connected = None

        BaseSocket.__init__(self, addr, charset)

    def dispatch(self):
        return CREATED
none_socket = NoneSocket(None)

class BaseClient(object):
    """Command IRC client interface.
    Any client should support:
        self.socket: any ircsocket
        self.cmdmanager: command dictionary
    """

    def __init__(self, eventmanager, cmdmanager, options=None):
        self.eventmanager = eventmanager
        self.cmdmanager = cmdmanager
        self.options = options
        self.socket = none_socket

    def runloop_unit(self):
        raise NotImplementedError

    def dispatch(self):
        """Get a message from socket."""
        return self.socket.dispatch()

    def handle_message(self):
        message = self.socket.dispatch()
        if message is None:
            return None
        self.eventmanager.putln(self, message)
        return True

    def run(self):
        """Thread loop."""
        while self.socket.connected is not False:
            self.runloop_unit()

    def start(self):
        self.thread = threading.Thread()
        self.thread.run = self.run
        self.thread.start()

    #command interface
    def connect(self):
        self.socket.connect()

    def disconnect(self):
        self.socket.disconnect()

    def cmdln(self, command):
        items = util.cmdsplit(command)
        self.cmd(*items)

    def cmd(self, *items):
        self.cmdmanager.run(self, *items)

    def sendraw(self, line, *args, **kwargs):
        self.socket.sendln(line, *args, **kwargs)

    def sendl(self, *args):
        self.socket.cmdl(*args)

    def sends(self, *args):
        self.socket.cmds(*args)

    def send(self, *args):
        self.socket.cmd(*args)

    def __getattr__(self, key):
        """Borrow commands from command manager."""
        if key in self.cmdmanager:
            action = self.cmdmanager[key].run
            def call(*args):
                return action(self, *args)
            return call
        try:
            return self.__getattr__(key)
        except:
            return self.__getattribute__(key)


class DispatchClient(BaseClient):
    """Client implementation based on manual dispatching."""

    def runloop_unit(self):
        """NOTE: blocking"""
        self.socket.recv()


class EventHookClient(BaseClient):
    def runloop_unit(self):
        """NOTE: blocking"""
        msg = self.handle_message()
        if msg is None:
            self.socket.recv()


class CallbackClient(BaseClient):
    """Callback-driven IRC client"""

    def __init__(self, callback, cmdmanager, options=None):
        self.callback = callback

        BaseClient.__init__(self, None, cmdmanager, options=None)

    def runloop_unit(self):
        """NOTE: blocking"""
        msg = self.dispatch()
        if msg is not None:
            self.callback(self, msg)
        else:
            self.socket.recv()

