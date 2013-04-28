
#-*- coding: utf-8 -*-

import threading
from .const import *
from .socket import BaseSocket
from . import util
from .hook import BaseHook, ExceptionHook, MessageHook

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
        self.commands: command dictionary
    """

    def runloop_unit(self):
        raise NotImplementedError

    def dispatch(self):
        """Get a message from socket."""
        return self.socket.dispatch()

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

    def __getattr__(self, key):
        if key in self.commands:
            action = self.commands[key].run
            def call(*args):
                return action(self, *args)
            return call
        try:
            return self.__getattr__(key)
        except:
            return self.__getattribute__(key)


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
        self.socket.recv()


class CallbackClient(BaseClient):
    """Callback-driven IRC client"""

    def __init__(self, callback, commands, options=None):
        self.socket = none_socket
        self.callback = callback
        self.commands = commands

        BaseClient.__init__(self)

    def runloop_unit(self):
        """NOTE: blocking"""
        msg = self.dispatch()
        if msg is not None:
            self.callback(self, msg)
        else:
            self.socket.recv()


class EventHookClient(CallbackClient):
    def __init__(self, commands, options=None):
        def irc_event(client, message):
            # It is reversed to grant higher priority to new hook
            for hook in reversed(client.hooks):
                result = hook.run(client, message)
                if result:
                    break
        self.hooks = []
        CallbackClient.__init__(self, irc_event, commands, options)

    def hook(self, hook):
        if not isinstance(hook, BaseHook):
            hook = BaseHook(hook)
        self.hooks.append(hook)
        return hook

    def hookexc(self, exception):
        def decorator(job):
            hook = ExceptionHook(exception, job)
            self.hooks.append(hook)
            return hook
        return decorator

    def hookmsg(self, message):
        def decorator(job):
            hook = MessageHook(message, job)
            self.hooks.append(hook)
            return hook
        return decorator


