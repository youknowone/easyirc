
#-*- coding: utf-8 -*-
from __future__ import absolute_import
import socket

from . import util, exception
from .const import *

try:
    from settings import RAW_LOG
except ImportError:
    RAW_LOG = False

class BaseSocket(object):
    def __init__(self, addr, charset='utf-8'):
        """addr is a tuple represents (host, port)"""
        self.addr = addr
        self.charset = charset
        self.msgqueue = []
        self.recvbuffer = ''
        self.connected = None
        self.create_socket()

    def create_socket(self):
        """Override to change internal socket."""
        self.socket = socket.socket()

    def send(self, line):
        raise NotImplementedError

    def connect(self):
        self.msgqueue.append(CONNECTED) # EVERYTHING-IS-RESPONSE!
        self.connected = True
        raise NotImplementedError

    def disconnect(self):
        self.msgqueue.append(DISCONNECTED) # EVERYTHING-IS-RESPONSE!
        raise NotImplementedError

    def _recv(self):
        raise NotImplementedError

    def sendln(self, line, *arg, **kwargs):
        if len(arg) or len(kwargs):
            line = line.format(*arg, **kwargs)
        #print '--> SEND', line
        self.send(line + '\r\n')

    def cmds(self, cmd, *args):
        self.sendln(u' '.join(map(unicode, [cmd] + list(args))))

    def cmdl(self, cmd, *args): # destructive!
        nargs = list(args[:-1]) + [':' + args[-1]]
        self.cmds(cmd, *nargs)

    def cmd(self, cmd, *args):
        if ' ' in args[-1]:
            self.cmdl(cmd, *args)
        else:
            self.cmds(cmd, *args)

    def dispatch(self):
        """Dispatch an item from msgqueue."""
        if len(self.msgqueue) == 0:
           return None
        msg = self.msgqueue[0]
        del(self.msgqueue[0])
        if RAW_LOG:
            print '>', msg
        return msg

    def dispatch_all(self):
        msg = True
        while msg:
            msg = self.dispatch()
            if msg:
                yield msg
        raise StopIteration

    def _split_buffer(self):
        """Catch 'ValueError' to check unsplitable"""
        newline, self.recvbuffer = self.recvbuffer.split('\r\n', 1)
        try:
            return newline.decode(self.charset)
        except:
            print 'Supposed charset is', self.charset, ', but undecodable string found:', newline
            return newline

    def _enqueue(self, line):
        self.msgqueue.append(line)

    def _enqueue_buffer(self):
        try:
            while True:
                newline = self._split_buffer()
                self._enqueue(newline)
        except ValueError:
            pass

    def recv(self, wait_enqueue=False):
        """NOTE: blocking"""
        while True:
            try:
                recv = self._recv()
                self.recvbuffer += recv
                self._enqueue_buffer()
            except Exception as e:
                if isinstance(e, socket.error):
                    self.msgqueue.append(DISCONNECTED)
                    self.connected = False
                    #raise exception.Disconnected
                else:
                    import traceback
                    print '--- Error caught ---'
                    traceback.print_exc()
                    raise e # debug
                self._enqueue(e)
            if not wait_enqueue or len(self.msgqueue) > 0:
                break


class Socket(BaseSocket):
    def send(self, line):
        if RAW_LOG:
            print '<', line,
        self.socket.send(line.encode(self.charset))

    def connect(self):
        self.socket.connect(self.addr)
        self.msgqueue.append(CONNECTED) # EVERYTHING-IS-RESPONSE!
        self.connected = True

    def disconnect(self):
        #self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def _recv(self):
        """NOTE: blocking"""
        return self.socket.recv(1024) # 1kb is enough for irc

